import argparse
from lib2to3.pgen2 import driver
import pandas as pd
import numpy as np
from pathlib import Path
from connection import Cursor, Connection
from helpers import read_sql_insert_template, ROOT_PATH

### USAGE ###
# python3 upsert_races.py -c ICST -l Superstars -s 2 -e 20220109
parser = argparse.ArgumentParser(description='Upsert races for a specific championship, league, season and event')
parser.add_argument('-c', '--championship', help='Championship', type=str, required=True)
parser.add_argument('-l', '--league', help='League', type=str, required=True)
parser.add_argument('-s', '--season', help='Season', type=str, required=True)
parser.add_argument('-e', '--event', help='Event', type=str, required=True)

args = parser.parse_args()

championship, league, season, event = args.championship, args.league, args.season, args.event

# check if folder exists
event_path = ROOT_PATH / Path(championship, league) / Path("Season"+season) / Path(event)
assert event_path.is_dir(), f"This folder does not exist: {event_path}"

# now there are two options:
# either a event consists of one race and the race details and results are in the event path
# or there are multiple RaceX folders for that event with the files

# first check if results.csv file exists
results_file_path = event_path / Path("results.csv")

result_files_to_process = []

if results_file_path.is_file():
    result_files_to_process.append(results_file_path)
else:
    for el in event_path.iterdir():
        assert not el.is_file(), "As there was not results.csv file, no file is expected to be found here!"

        results_file_path = event_path / el / "results.csv"

        assert results_file_path.is_file(), f"results.csv not found here: {race_file_path}"

        result_files_to_process.append(results_file_path)


sql_quali = read_sql_insert_template("35_insert_quali_results.sql")
sql_race = read_sql_insert_template("40_insert_race_results.sql")

with Connection() as conn:  
    for results_file in result_files_to_process:
        results = pd.read_csv(results_file)
        results["driver"] = results["driver"].str.strip()

        # replace NaN with None (this makes it possible for postgresql to handle missing values)
        results = results.replace({np.nan: None})
        print(results)
        if results_file.parent.name.startswith("Race"):
            order = results_file.parent.name[4:]
        else:
            order = 1

        ###
        # In order to add the results to the db, we need the race id (r_r_id)
        # 1. get s_id from seasons table
        # 2. get event id based on s_s_id and event name (=date)
        # 3. get race id based on e_e_id and order

        # get season id 
        season = pd.read_sql("select s_id "
            "from base.seasons s "
            f"left join base.leagues l on l_name = '{league}' "
            f"left join base.championships c on c_name = '{championship}' "
            f"where s.s_desc = '{season}' and s.l_l_id = l.l_id and l.c_c_id = c.c_id", 
        con=conn)

        assert len(season) == 1, "Found no or more than one s_id, exciting.."

        sid = season["s_id"].values[0]

        # get event id
        event = pd.read_sql(f"select e_id from base.events where s_s_id = {sid} and e_date=to_date('{event}', 'YYYYMMDD')", con=conn)

        assert len(event) == 1, "Found no or more than one e_id, exciting.."
        e_id = event["e_id"].values[0]

        # get race id
        race = pd.read_sql(f"select r_id from base.races where e_e_id = {e_id} and r_order={order}", con=conn)

        assert len(race) == 1, "Found no or more than one e_id, exciting.."
        r_id = race["r_id"].values[0]

        results["r_r_id"] = r_id

        ###
        # Now, we need the d_d_id
        # get driver id
        drivers = pd.read_sql("select d_id, d_name from base.drivers", con=conn)

        results = results.set_index("driver").join(drivers.set_index("d_name"))

        results.rename(columns={
            "d_id" : "d_d_id"
            }, 
            inplace=True
        )

        ###
        # Add Quali Position, if not in the data
        # In the beginning, this column was not included, but it is needed, if two people have the exact same time
        # or someone attended the Quali, but did not finish a lap
        if not "quali_position" in results.columns:
            results["quali_position"] = results["quali_lap_time_seconds"].rank(method="min")

            # Check if, any times occur twice
            assert results["quali_position"].loc[~results["quali_position"].isnull()].rank(method="min").duplicated().sum() == 0, \
                "This file needs the quali position column as two drivers seem to have driven the same time."

            results["quali_position"] = results["quali_position"].replace({np.nan: None})

        # add penalty and penalty_description column, if not given
        if not "penalty" in results.columns:
            results["penalty"] = None
        if not "penalty_description" in results.columns:
            results["penalty_description"] = None


        # Now, we need split the data into quali and race

        results_quali = results[["r_r_id", "d_d_id", "quali_lap_time_seconds", "quali_position"]].copy()
        results_race = results[["r_r_id", "d_d_id", "race_time_seconds", "position", "lappings", "fastest_lap_seconds", "penalty", "penalty_description"]].copy()

        results_quali.rename(columns={
            "quali_position" : "position"
            }, 
            inplace=True
        )
        
        print("Inserting race result data")
        for _, row in results_quali.iterrows():
            print(f"Upserting data for quali results:")
            print(row)

            list_insert = list(row)
            
            conn.cursor().execute(sql_quali, dict(zip(results_quali.columns, list_insert)))
        
        
        print("Inserting quali result data")
        for _, row in results_race.iterrows():
            print(f"Upserting data for race results:")
            print(row)

            list_insert = list(row)

            conn.cursor().execute(sql_race, dict(zip(results_race.columns, list_insert)))
