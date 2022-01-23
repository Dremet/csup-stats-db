import argparse
from lib2to3.pgen2 import driver
import pandas as pd
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

# first check if events.csv file exists
race_file_path = event_path / Path("race.csv")

race_files_to_process = []

if race_file_path.is_file():
    race_files_to_process.append(race_file_path)
else:
    for el in event_path.iterdir():
        assert not el.is_file(), "As there was not race.csv file, no file is expected to be found here!"

        race_file_path = event_path / el / "race.csv"

        assert race_file_path.is_file(), f"race.csv not found here: {race_file_path}"

        race_files_to_process.append(race_file_path)


sql = read_sql_insert_template("30_insert_races.sql")

with Connection() as conn:  
    for race_file in race_files_to_process:
        race = pd.read_csv(race_file)

        if race_file.parent.name.startswith("Race"):
            race["order"] = race_file.parent.name[4:]
        else:
            race["order"] = 1

        # correct typo
        race.rename(columns={
            "detailes_were_announced" : "details_were_announced"
            }, 
            inplace=True
        )

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

        race["e_e_id"] = e_id

        for _, row in race.iterrows():
            print(f"Upserting data for race:")
            print(row)

            list_insert = list(row)

            conn.cursor().execute(sql, dict(zip(race.columns, list_insert)))
