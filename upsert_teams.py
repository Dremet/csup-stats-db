import pandas as pd
import math
from connection import Cursor
from helpers import read_sql_insert_template, ROOT_PATH


with Cursor() as cur:
    path = ROOT_PATH / "teams.csv"

    teams = pd.read_csv(path)
    teams["name"] = teams["name"].str.strip()
    teams["tag"] = teams["tag"].str.strip()
    
    sql_upsert = read_sql_insert_template("70_upsert_teams.sql")
    
    for _, row in teams.iterrows():
        input_data = list(row)
        
        print("Upserting data for team:", input_data[1])
        print(row)
        
        cur.execute(sql_upsert, dict(zip(teams.columns, input_data)))
