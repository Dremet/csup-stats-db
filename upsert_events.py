import argparse
import pandas as pd
from pathlib import Path
from connection import Cursor, Connection
from helpers import read_sql_insert_template, ROOT_PATH

### USAGE ###
# python3 upsert_events.py -c ICST -l Superstars -s 2
parser = argparse.ArgumentParser(description='Upsert events for a specific championship, league and season')
parser.add_argument('-c', '--championship', help='Championship', type=str, required=True)
parser.add_argument('-l', '--league', help='League', type=str, required=True)
parser.add_argument('-s', '--season', help='Season', type=str, required=True)

args = parser.parse_args()

championship, league, season = args.championship, args.league, args.season

# check if folder exists
season_path = ROOT_PATH / Path(championship, league) / Path("Season"+season)
assert season_path.is_dir(), f"This folder does not exist: {season_path}"

# now check if events.csv file exists
events_file_path = season_path / Path("events.csv")
assert events_file_path.is_file(), f"events file not found: {events_file_path}"

events = pd.read_csv(events_file_path)
events["date"] = events["date"].astype(str).apply(lambda x: pd.Timestamp(x))

print(events)

with Connection() as conn:
    season = pd.read_sql("select s_id "
        "from base.seasons s "
        f"left join base.leagues l on l_name = '{league}' "
        f"left join base.championships c on c_name = '{championship}' "
        f"where s.s_desc = '{season}' and s.l_l_id = l.l_id and l.c_c_id = c.c_id", 
    con=conn)

    assert len(season) == 1, "Found no or more that one s_id, exciting.."

    sid = season["s_id"].values[0]

    events["s_s_id"] = sid

    sql = read_sql_insert_template("25_insert_events.sql")

    for _, row in events.iterrows():
        input_data = list(row)
        
        print(f"Upserting data for this event: championship {championship}, league {league}, season {season}, event date {input_data[1]}")
        print(row)

        conn.cursor().execute(sql, dict(zip(events.columns, input_data)))
