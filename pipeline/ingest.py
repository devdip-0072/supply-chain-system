import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
import sqlalchemy
from config.db_config import DB_CONFIG

def fetch_table():
    engine = sqlalchemy.create_engine(DB_CONFIG)
    query = "SELECT * FROM retail_data.demand_forecasting_base"
    df = pd.read_sql(query, engine)
    df.to_csv(r"D:\Supply_chain_project\data\raw\table.csv", index=False)
    print("Data fetched from MySQL and saved")
    return df

if __name__ == "__main__":
    fetch_table()
