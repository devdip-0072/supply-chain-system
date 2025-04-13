
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from faker import Faker
import random
#import mysql.connector
from sqlalchemy import create_engine

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

# Categories and seasonal patterns
CATEGORIES = {
    'Electronics': {'brands': ['Sony', 'Samsung', 'Apple', 'Bose'], 
                   'seasonality': [11,12], 'multiplier': 2.5},
    'Apparel': {'brands': ['Nike', 'Zara', 'Levi\'s', 'Patagonia'], 
               'seasonality': [12,1,2], 'multiplier': 3.0},
    'Ice Cream': {'brands': ['Ben & Jerry\'s', 'Haagen-Dazs', 'Magnum', 'Talenti'], 
                 'seasonality': [6,7,8], 'multiplier': 4.0},
    'Outdoor': {'brands': ['The North Face', 'Columbia', 'Patagonia', 'Arc\'teryx'], 
               'seasonality': [5,6,7,8], 'multiplier': 2.8},
    'Grocery': {'brands': ['Kellogg\'s', 'Heinz', 'Nestle', 'General Mills'], 
               'seasonality': None, 'multiplier': 1.0},
    'Home': {'brands': ['IKEA', 'Williams-Sonoma', 'Crate & Barrel', 'Bed Bath & Beyond'], 
             'seasonality': [11,12], 'multiplier': 2.0},
    'Toys': {'brands': ['LEGO', 'Hasbro', 'Mattel', 'Fisher-Price'], 
             'seasonality': [11,12], 'multiplier': 3.5},
    'Beauty': {'brands': ['L\'Oreal', 'Estee Lauder', 'Clinique', 'MAC'], 
               'seasonality': [11,12], 'multiplier': 2.0},
    'Sports': {'brands': ['Nike', 'Adidas', 'Under Armour', 'Puma'], 
               'seasonality': [1,5,6], 'multiplier': 1.8},
    'Books': {'brands': ['Penguin', 'HarperCollins', 'Simon & Schuster', 'Macmillan'], 
              'seasonality': [11,12], 'multiplier': 1.5}
}

# Generate Products
products = []
sku_id = 1000
suppliers = [f"SUP-{i:03d}" for i in range(1, 21)]

for category, details in CATEGORIES.items():
    for brand in details['brands']:
        for _ in range(random.randint(5, 8)):  # 5-8 SKUs per brand
            sku_id += 1
            cost = round(np.random.uniform(5, 200), 2)
            price = round(cost * np.random.uniform(1.3, 3.0), 2)  # 30-200% markup
            products.append({
                "product_id": f"{category[:3]}-{brand[:3]}-{sku_id}",
                "category": category,
                "brand": brand,
                "sku": f"SKU-{sku_id}",
                "price": price,
                "cost": cost,
                "supplier_id": random.choice(suppliers),
                "product_dimensions": f"{random.randint(5,50)}x{random.randint(5,50)}x{random.randint(5,50)} cm",
                "manufacture_date": fake.date_between(start_date='-5y', end_date='-6m'),
                "warranty_period_years": random.choice([1,2,3]),
                "lifecycle_stage": random.choice(['New','Growth','Maturity','Decline'])
            })
products_df = pd.DataFrame(products)

# Generate Suppliers
suppliers_data = []
for i, supplier_id in enumerate(suppliers, 1):
    suppliers_data.append({
        "supplier_id": supplier_id,
        "supplier_name": fake.company(),
        "contact_info": fake.email(),
        "supplier_rating": round(np.random.uniform(3.0, 5.0), 1),
        "lead_time_days": random.choice([7,14,21,30]),
        "contract_start_date": fake.date_between(start_date='-5y', end_date='-1y')
    })
suppliers_df = pd.DataFrame(suppliers_data)

# Generate Inventory
inventory = []
for product in products:
    for warehouse in [f"WH-{i:02d}" for i in range(1, NUM_WAREHOUSES+1)]:
        inventory.append({
            "product_id": product["product_id"],
            "warehouse": warehouse,
            "stock_level": random.randint(50, 1000),
            "restock_frequency_days": random.choice([7,14,30]),
            "stock_location": random.choice(['A1','B2','C3','D4']),
            "order_quantity": random.randint(50, 200),
            "restock_date": fake.date_between(start_date='-3y', end_date='today')
        })
inventory_df = pd.DataFrame(inventory)

# Generate Customers
customers = []
for i in range(1, NUM_CUSTOMERS+1):
    first_purchase = fake.date_between(start_date='-3y', end_date='today')
    last_purchase = fake.date_between(start_date=first_purchase, end_date='today')
    customers.append({
        "customer_id": f"CUST-{i:05d}",
        "customer_age": random.randint(18, 80),
        "customer_gender": random.choice(['M','F']),
        "customer_location": fake.state(),
        "first_purchase_date": first_purchase,
        "last_purchase_date": last_purchase,
        "lifetime_value": round(np.random.uniform(100, 5000), 2)
    })
customers_df = pd.DataFrame(customers)

# Generate Promotions
promotions = []
promo_types = ['Discount','BOGO','Bundle','Flash Sale','Seasonal Offer']
channels = ['Online','In-Store','Social Media','Email','Mobile App']
responses = ['None','Price Match','Bundled Offer','Loyalty Program','Discount War']

for product in random.sample(products, 100):  # Promotions for 100 random products
    for _ in range(random.randint(1, 3)):  # 1-3 promos per product
        promo_type = random.choice(promo_types)
        start_date = fake.date_between(start_date='-4y', end_date='-2y')
        duration = random.choice([3,7,14,30]) if promo_type == 'Flash Sale' else random.randint(7, 60)
        promotions.append({
            "product_id": product["product_id"],
            "promotion_type": promo_type,
            "discount_percentage": random.randint(10, 70) if promo_type == 'Discount' else None,
            "campaign_duration_days": duration,
            "campaign_budget": round(np.random.uniform(1000, 10000), 2),
            "campaign_start_date": start_date,
            "campaign_end_date": start_date + timedelta(days=duration),
            "target_audience": random.choice(['Families','Teens','Adults','Seniors','All']),
            "channel": random.choice(channels),
            "competitor_response": random.choice(responses)
        })
promotions_df = pd.DataFrame(promotions)

# Generate Sales with Seasonality
sales = []
stores = [f"STORE-{i:03d}" for i in range(1, NUM_STORES+1)]
date_range = pd.date_range(START_DATE, END_DATE)

for date in date_range:
    month = date.month
    day = date.day
    year = date.year
    
    # Holiday flags
    holiday = None
    if month == 12 and day == 25:
        holiday = "Christmas"
    elif month == 11 and (20 <= day <= 30):
        holiday = "Black Friday"
    elif month == 8 and day == 15:
        holiday = "Independence Day"
    
    # Sample products for this day
    daily_products = random.sample(products, k=random.randint(50, 100))
    
    for product in daily_products:
        cat_info = CATEGORIES[product['category']]
        base_sales = random.randint(1, 50)
        
        # Seasonality
        if cat_info['seasonality'] and month in cat_info['seasonality']:
            sales_qty = int(base_sales * cat_info['multiplier'])
        else:
            sales_qty = base_sales
            
        # Holiday boost
        if holiday:
            sales_qty = int(sales_qty * 2.0)
            
        # Random noise
        sales_qty = max(1, int(sales_qty * np.random.uniform(0.7, 1.3)))
        
        # Check if product is on promotion
        promo = None
        for p in promotions:
            if (p['product_id'] == product['product_id'] and 
                p['campaign_start_date'] <= date.date() <= p['campaign_end_date']):
                promo = p
                break
                
        sales.append({
            "date": date.strftime("%Y-%m-%d"),
            "product_id": product["product_id"],
            "customer_id": random.choice(customers_df['customer_id']),
            "store_id": random.choice(stores),
            "sales_quantity": sales_qty,
            "sales_revenue": sales_qty * product["price"],
            "promo_flag": promo is not None,
            "holiday_flag": holiday
        })
sales_df = pd.DataFrame(sales)

# Generate Shipments
shipments = []
for i in range(1, 1001):
    product = random.choice(products)
    depart = fake.date_time_between(start_date='-2y', end_date='now')
    arrivals = [depart + timedelta(days=random.randint(1, 14))]
    shipments.append({
        "shipment_id": f"SHIP-{i:05d}",
        "product_id": product["product_id"],
        "transport_mode": random.choice(['Truck','Air','Sea','Rail']),
        "shipment_tracking_number": fake.uuid4()[:8].upper(),
        "shipment_departure_time": depart,
        "shipment_arrival_time": random.choice(arrivals),
        "status": random.choice(['Delivered','In Transit','Delayed'])
    })
shipments_df = pd.DataFrame(shipments)

# Generate Market Trends (weekly)
market_trends = []
for date in pd.date_range(START_DATE, END_DATE, freq='W'):
    month = date.month
    temp = 30 if month in [6,7,8] else -5 if month in [12,1,2] else random.randint(10, 25)
    market_trends.append({
        "date": date.strftime("%Y-%m-%d"),
        "product_id": random.choice(products_df['product_id']),
        "temperature": temp,
        "weather_condition": "Heatwave" if temp > 30 else "Snowy" if temp < 0 else random.choice(["Sunny","Rainy","Cloudy"]),
        "social_media_mentions": random.randint(50, 500),
        "competitor_analysis_score": round(np.random.uniform(60, 90), 2),
        "cpi_change": round(np.random.uniform(-0.02, 0.05), 4)
    })
market_df = pd.DataFrame(market_trends)

# Connect to MySQL and upload data
engine = create_engine('mysql+mysqlconnector://root:1234@localhost/retail_data')

tables = {
    'products': products_df,
    'suppliers': suppliers_df,
    'inventory': inventory_df,
    'customers': customers_df,
    'promotions': promotions_df,
    'sales': sales_df,
    'shipments': shipments_df,
    'market_trends': market_df
}

for table_name, df in tables.items():
    df.to_sql(
        name=table_name,
        con=engine,
        if_exists='append',
        index=False,
        chunksize=1000
    )
    print(f"Uploaded {len(df)} rows to {table_name}")