import pandas as pd
import numpy as np
import math
from pathlib import Path
from connection import Cursor


with Cursor() as cur:
    drivers = pd.read_csv("data/drivers.csv", na_filter=False)
    
    sql_upsert = Path("sql/inserts/60_upsert_drivers.sql").read_text().replace('\n', '')

    drivers.loc[drivers["two_letter_country_code"]=="x", "two_letter_country_code"] = None
    
    drivers.rename(columns={
            "id" : "d_id",
            "driver" : "d_name",
            "two_letter_country_code" : "d_two_letter_country_code",
            "two_letter_continent_code" : "d_two_letter_continent_code",
            "steering_device" : "d_steering_device"
        }, 
        inplace=True
    )
    
    for _, row in drivers.iterrows():
        input_data = list(row)
        
        print("Upserting data from driver:", input_data[1])
        print(row)
        input_data = [element if isinstance(element, str) or (not element is None and not math.isnan(element)) else None for element in input_data]

        cur.execute(sql_upsert, dict(zip(drivers.columns, input_data)))
