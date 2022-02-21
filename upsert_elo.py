import argparse
from os import sep
import pandas as pd
from connection import Connection
from helpers import read_sql_insert_template, ROOT_PATH

### USAGE ###
# python3 upsert_elo.py -d 20220213
parser = argparse.ArgumentParser(description='Upsert ELO rankings for a specific date')
parser.add_argument('-d', '--date', help='Date', type=str, required=True)

args = parser.parse_args()

date = args.date

with Connection() as conn:  
    path = ROOT_PATH / "ELO" / f"{date}.csv"

    assert path.is_file(), f"This ELO file does not exist: {path}"

    elo = pd.read_csv(path, sep=";")

    elo.rename(columns={
            "number tournaments" : "number_tournaments",
            "Pos." : "position",
            "Piloto/Driver" : "driver",
            "Pts." : "elo_ranking"
        }, 
        inplace=True
    )

    elo["elo_date"] = date
    elo["elo_date"] = elo["elo_date"].astype(str).apply(lambda x: pd.Timestamp(x))
    elo["driver"] = elo["driver"].str.strip()


    ###
    # Now, we need the d_d_id
    # get driver id
    drivers = pd.read_sql("select d_id, d_name from base.drivers", con=conn)

    elo = elo.set_index("driver").join(drivers.set_index("d_name"))

    elo.rename(columns={
        "d_id" : "d_d_id"
        }, 
        inplace=True
    )

    assert elo["d_d_id"].isnull().sum() == 0, f"Was not able to identify all drivers: {elo[elo['d_d_id'].isnull()].index}"

    # cut to relevant columns
    elo = elo[["d_d_id","elo_ranking","elo_date"]]
    
    sql_upsert = read_sql_insert_template("65_upsert_elo.sql")
    
    for _, row in elo.iterrows():
        input_data = list(row)
        
        print("Upserting data for d_id:", input_data[0])
        print(row)
        
        conn.cursor().execute(sql_upsert, dict(zip(elo.columns, input_data)))
