import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import random
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, Date, DateTime, Boolean, ForeignKey

fake = Faker()
np.random.seed(42)

# Configuration
START_DATE = '2021-01-01'
END_DATE = '2023-12-31'
DAYS = (datetime.strptime(END_DATE, "%Y-%m-%d") - datetime.strptime(START_DATE, "%Y-%m-%d")).days
NUM_PRODUCTS = 200
NUM_CUSTOMERS = 5000
NUM_STORES = 10
NUM_WAREHOUSES = 5

# Database Schema Creation
def create_database_schema(engine):
    metadata = MetaData()
    
    # Products Table
    Table('products', metadata,
          Column('product_id', String(50), primary_key=True),
          Column('category', String(50)),
          Column('brand', String(50)),
          Column('sku', String(50), unique=True),
          Column('price', Float),
          Column('cost', Float),
          Column('supplier_id', String(50)),
          Column('product_dimensions', String(50)),
          Column('manufacture_date', Date),
          Column('warranty_period_years', Integer),
          Column('lifecycle_stage', String(20))
          )
    
    # Suppliers Table
    Table('suppliers', metadata,
          Column('supplier_id', String(50), primary_key=True),
          Column('supplier_name', String(100)),
          Column('contact_info', String(100)),
          Column('supplier_rating', Float),
          Column('lead_time_days', Integer),
          Column('contract_start_date', Date),
          Column('supplier_city', String(50)),
          Column('supplier_region', String(50))
          )
    
    # Customers Table
    Table('customers', metadata,
          Column('customer_id', String(50), primary_key=True),
          Column('customer_age', Integer),
          Column('customer_gender', String(1)),
          Column('customer_location', String(50)),
          Column('customer_city', String(50)),
          Column('customer_region', String(50)),
          Column('first_purchase_date', Date),
          Column('last_purchase_date', Date),
          Column('lifetime_value', Float)
          )
    
    # Inventory Table
    Table('inventory', metadata,
          Column('id', Integer, primary_key=True, autoincrement=True),
          Column('product_id', String(50), ForeignKey('products.product_id')),
          Column('warehouse', String(50)),
          Column('stock_level', Integer),
          Column('restock_frequency_days', Integer),
          Column('stock_location', String(50)),
          Column('order_quantity', Integer),
          Column('restock_date', Date),
          Column('warehouse_city', String(50)),
          Column('warehouse_region', String(50))
          )
    
    # Promotions Table
    Table('promotions', metadata,
          Column('promotion_id', Integer, primary_key=True, autoincrement=True),
          Column('product_id', String(50), ForeignKey('products.product_id')),
          Column('promotion_type', String(50)),
          Column('discount_percentage', Float),
          Column('campaign_duration_days', Integer),
          Column('campaign_budget', Float),
          Column('campaign_start_date', Date),
          Column('campaign_end_date', Date),
          Column('target_audience', String(50)),
          Column('channel', String(50)),
          Column('competitor_response', String(50))
          )
    
    # Sales Table
    Table('sales', metadata,
          Column('sale_id', Integer, primary_key=True, autoincrement=True),
          Column('date', Date),
          Column('product_id', String(50), ForeignKey('products.product_id')),
          Column('customer_id', String(50), ForeignKey('customers.customer_id')),
          Column('store_id', String(50)),
          Column('sales_quantity', Integer),
          Column('sales_revenue', Float),
          Column('promo_flag', Boolean),
          Column('holiday_flag', String(50))
          )
    
    # Shipments Table
    Table('shipments', metadata,
          Column('shipment_id', String(50), primary_key=True),
          Column('product_id', String(50), ForeignKey('products.product_id')),
          Column('transport_mode', String(50)),
          Column('shipment_tracking_number', String(50)),
          Column('shipment_departure_time', DateTime),
          Column('shipment_arrival_time', DateTime),
          Column('status', String(50)),
          Column('destination_city', String(50)),
          Column('destination_region', String(50))
          )
    
    # Market Trends Table
    Table('market_trends', metadata,
          Column('trend_id', Integer, primary_key=True, autoincrement=True),
          Column('date', Date),
          Column('product_id', String(50), ForeignKey('products.product_id')),
          Column('temperature', Float),
          Column('weather_condition', String(50)),
          Column('social_media_mentions', Integer),
          Column('competitor_analysis_score', Float),
          Column('cpi_change', Float),
          Column('region', String(50)),
          Column('city', String(50))
          )
    
    # Create all tables
    metadata.create_all(engine)
    print("Database schema created successfully with all tables, primary keys, and foreign keys")

# US states by region
REGIONS = {
    'Northeast': ['Connecticut', 'Maine', 'Massachusetts', 'New Hampshire', 'Rhode Island', 'Vermont', 
                  'New Jersey', 'New York', 'Pennsylvania'],
    'Midwest': ['Illinois', 'Indiana', 'Michigan', 'Ohio', 'Wisconsin', 'Iowa', 'Kansas', 
                'Minnesota', 'Missouri', 'Nebraska', 'North Dakota', 'South Dakota'],
    'South': ['Delaware', 'Florida', 'Georgia', 'Maryland', 'North Carolina', 'South Carolina', 
              'Virginia', 'District of Columbia', 'West Virginia', 'Alabama', 'Kentucky', 
              'Mississippi', 'Tennessee', 'Arkansas', 'Louisiana', 'Oklahoma', 'Texas'],
    'West': ['Arizona', 'Colorado', 'Idaho', 'Montana', 'Nevada', 'New Mexico', 'Utah', 
             'Wyoming', 'Alaska', 'California', 'Hawaii', 'Oregon', 'Washington']
}

# [Rest of your data generation code remains exactly the same...]
# [Include all the data generation code from the previous solution]

# Main execution
if __name__ == "__main__":
    # Create database connection
    engine = create_engine('mysql+mysqlconnector://root:1234@localhost/my_data')
    
    # Create database schema with all tables and constraints
    create_database_schema(engine)
    
    # Generate all data
    # [Include all your data generation code here]
    
    # Upload data to database
    tables = {
        'products': products_df,
        'suppliers': suppliers_df,
        'customers': customers_df,
        'inventory': inventory_df,
        'promotions': promotions_df,
        'sales': sales_df,
        'shipments': shipments_df,
        'market_trends': market_df
    }

    for table_name, df in tables.items():
        # Replace any remaining NaN values with appropriate defaults
        df = df.fillna({
            'discount_percentage': 0,
            'promo_flag': False,
            'holiday_flag': 'None',
            'competitor_response': 'None'
        })
        
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists='append',
            index=False,
            chunksize=1000
        )
        print(f"Uploaded {len(df)} rows to {table_name}")

    print("Database population completed successfully")