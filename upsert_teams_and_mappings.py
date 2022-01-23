import argparse
from lib2to3.pgen2 import driver
import pandas as pd
from pathlib import Path
from connection import Cursor, Connection
from helpers import read_sql_insert_template, ROOT_PATH

### USAGE ###
# python3 upsert_teams_and_mappings.py -c ICST -l Superstars -s 2
parser = argparse.ArgumentParser(description='Upsert team mappings for a specific championship, league and season')
parser.add_argument('-c', '--championship', help='Championship', type=str, required=True)
parser.add_argument('-l', '--league', help='League', type=str, required=True)
parser.add_argument('-s', '--season', help='Season', type=str, required=True)

args = parser.parse_args()

championship, league, season = args.championship, args.league, args.season

# check if folder exists
season_path = ROOT_PATH / Path(championship, league) / Path("Season"+season)
assert season_path.is_dir(), f"This folder does not exist: {season_path}"

# now check if events.csv file exists
team_mapping_file_path = season_path / Path("team_membership.csv")

assert team_mapping_file_path.is_file(), f"team membership/mapping file not found: {team_mapping_file_path}"

team_mapping = pd.read_csv(team_mapping_file_path)

team_mapping["driver"] = team_mapping["driver"].str.strip()
team_mapping["team"] = team_mapping["team"].str.strip()
print(team_mapping)

with Connection() as conn:    
    # get season id 
    season = pd.read_sql("select s_id "
        "from base.seasons s "
        f"left join base.leagues l on l_name = '{league}' "
        f"left join base.championships c on c_name = '{championship}' "
        f"where s.s_desc = '{season}' and s.l_l_id = l.l_id and l.c_c_id = c.c_id", 
    con=conn)

    print("season", season)

    assert len(season) == 1, "Found no or more that one s_id, exciting.."

    sid = season["s_id"].values[0]

    print(sid)

    team_mapping["s_s_id"] = sid

    # get driver id
    drivers = pd.read_sql("select d_id,d_name from base.drivers", con=conn)

    team_mapping = team_mapping.set_index("driver").join(drivers.set_index("d_name"))

    assert sum(team_mapping["d_id"].isnull()) == 0, "At least one of the given drivers is not in the drivers table."

    # get team id
    teams = pd.read_sql("select t_id, t_name from base.teams", con=conn)

    team_mapping = team_mapping.set_index("team").join(teams.set_index("t_name"))

    assert sum(team_mapping["d_id"].isnull()) == 0, "At least one of the given drivers is not in the drivers table."


    team_mapping.rename(columns={
            "t_id" : "t_t_id",
            "d_id" : "d_d_id"
        }, 
        inplace=True
    )

    print(team_mapping)

    sql = read_sql_insert_template("80_insert_team_mappings.sql")

    for _, row in team_mapping.iterrows():
        print(f"Upserting data for team mapping:")
        print(row)

        row_insert = row[["d_d_id", "t_t_id", "s_s_id"]]
        list_insert = list(row_insert)

        conn.cursor().execute(sql, dict(zip(["d_d_id", "t_t_id", "s_s_id"], list_insert)))
