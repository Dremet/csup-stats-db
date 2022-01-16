import pandas as pd
from pathlib import Path
from connection import Cursor
from helpers import ROOT_PATH, read_sql_insert_template

with Cursor() as cur:
    path = ROOT_PATH / "championships.csv"

    # na_filter would transform "NA" (North America) to NaN, which we do not want
    cs_leagues = pd.read_csv(path, na_filter=False)

    ### CHAMPIONSHIPS ###
    cs = cs_leagues[["name","has_teams","region"]]

    # as we have no na filter, we have to do this for the row that allows None values
    cs.loc[cs["region"] == "", "region"] = None

    # as league infos are also in the table, we have duplicates after removing the league name column
    cs.drop_duplicates(inplace=True)

    cs.rename(columns={
            "name" : "c_name",
            "has_teams" : "c_has_teams",
            "region" : "c_region"
        }, 
        inplace=True
    )

    sql_upsert_cs = read_sql_insert_template("10_insert_championships.sql")

    # as we need the c_id to fill the league table later, we save them to a list
    c_ids_by_name = {}

    for _, row in cs.iterrows():
        input_data = list(row)
        print(f"Upserting data from championship {input_data[0]}")
        cur.execute(sql_upsert_cs, dict(zip(cs.columns, input_data)))

        c_id, c_name = cur.fetchone()

        c_ids_by_name[c_name] = c_id
    
    ### LEAGUES ###
    leagues = cs_leagues[["name", "league_name"]]
    leagues["c_c_id"] = leagues["name"].apply(lambda x: c_ids_by_name[x])

    del cs_leagues["name"]

    leagues.rename(columns={
            "league_name" : "l_name"
        }, 
        inplace=True
    )

    sql_upsert_league = read_sql_insert_template("15_insert_leagues.sql")

    for _, row in leagues.iterrows():
        input_data = list(row)
        print(f"Upserting data from league {input_data[0]}")
        cur.execute(sql_upsert_league, dict(zip(leagues.columns, input_data)))