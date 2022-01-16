import argparse
from operator import le
import pandas as pd
from pathlib import Path
from connection import Cursor, Connection
from helpers import read_sql_insert_template, ROOT_PATH

### USAGE ###
# Insert all seasons
# python3 upsert_seasons.py -c ICST -l Superstars 
# Insert one season (season 2)
# python3 upsert_seasons.py -c ICST -l Superstars -s 2
parser = argparse.ArgumentParser(description='Upsert season info for a specific championship and League')
parser.add_argument('-c', '--championship', help='Championship', type=str, required=True)
parser.add_argument('-l', '--league', help='League', type=str, required=True)
parser.add_argument('-s', '--season', help='Season', type=str, required=False)

args = parser.parse_args()

championship, league, season = args.championship, args.league, args.season

# check if folder exists
league_path = ROOT_PATH / Path(championship, league)

if season is None:
    # specific season has not been provided
    assert league_path.is_dir(), f"This folder does not exist: {league_path}"
else:
    # season has been provided
    season_path = league_path / Path("Season"+season)
    assert season_path.is_dir(), f"This folder does not exist: {season_path}"

with Connection() as conn:
    df = pd.read_sql("select c_name, l_name, l_id from base.leagues l left join base.championships c on l.c_c_id=c.c_id", con=conn)

    # check if championship and league exists in the database
    assert championship in list(df["c_name"]), "Championship has to be added to the database first!"
    assert league in list(df.loc[df["c_name"]==championship, "l_name"]), "League has to be added to the database first!"


    sql = read_sql_insert_template("20_insert_seasons.sql")

    if season is None:
        # go through the folder an read desc of seasons
        # folder are named like this: "Season{desc_of_season}"
        for season_path in league_path.iterdir():
            if not season_path.is_dir():
                continue
            
            assert season_path.name.startswith("Season"), "Found folder that does not start with 'Season'! Aborting."

            season_desc = season_path.name[6:]
            assert len(season_desc) > 0, "Season description needs to consist of at least one character!"

            print(f"Inserting data from season {season_desc}")

            l_l_id = int(df.loc[(df.c_name == championship) & (df.l_name == league), "l_id"].values[0])
            
            conn.cursor().execute(sql, {"l_l_id": l_l_id, "s_desc": season_desc})
    else:
        # only insert that one season
        assert not season.startswith("Season"), "Only provide the name after the word 'Season'"
        assert len(season) > 0, "Season description needs to consist of at least one character!"

        print(f"Inserting data from season {season}")

        l_l_id = int(df.loc[(df.c_name == championship) & (df.l_name == league), "l_id"].values[0])
        
        conn.cursor().execute(sql, {"l_l_id": l_l_id, "s_desc": season})


