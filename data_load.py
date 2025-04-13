import pandas as pd
from sqlalchemy import create_engine

# Replace with your actual credentials
username = 'root'
password = '1234'
host = 'localhost'
port = '3306'
database = 'retail_data'

# Create connection
engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}')

# Fetch the joined table (change table name if needed)
query = "SELECT * FROM demand_forecasting_base;"  # Or clean_sales_data if already cleaned in SQL
df = pd.read_sql(query, engine)

# Preview
print(df.head())
