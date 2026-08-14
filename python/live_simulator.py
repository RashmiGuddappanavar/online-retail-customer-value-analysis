"""
Live Transaction Simulator & Ingestion Service
------------------------------------------------
Online Retail Customer Value & Revenue Analytics

Generates realistic commercial retail transactions (orders & cancellations)
and ingests them directly into the live database table 'fact_online_retail_transactions'
tagged with is_simulated = 1.
"""

import os
import sys
import time
import random
import argparse
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "online_retail_analytics")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PROCESSED_DIR = os.path.join(BASE_DIR, "data", "processed")
SQLITE_PATH = os.path.join(PROCESSED_DIR, "online_retail_live.db")

PRODUCTS = [
    {"StockCode": "22423", "Description": "REGENCY CAKESTAND 3 TIER", "UnitPrice": 12.75},
    {"StockCode": "85123A", "Description": "WHITE HANGING HEART T-LIGHT HOLDER", "UnitPrice": 2.95},
    {"StockCode": "85099B", "Description": "RED RETROSPOT JUMBO BAG", "UnitPrice": 2.08},
    {"StockCode": "47566", "Description": "PARTY BUNTING", "UnitPrice": 4.95},
    {"StockCode": "84879", "Description": "ASSORTED COLOUR BIRD ORNAMENT", "UnitPrice": 1.69},
    {"StockCode": "22086", "Description": "PAPER CHAIN KIT 50'S CHRISTMAS", "UnitPrice": 2.95},
    {"StockCode": "79321", "Description": "CHILLI LIGHTS", "UnitPrice": 5.95},
    {"StockCode": "21212", "Description": "PACK OF 72 RETROSPOT TINY TINS", "UnitPrice": 1.25},
    {"StockCode": "23284", "Description": "DOORMAT KEEP CALM AND CALL MOM", "UnitPrice": 7.95},
    {"StockCode": "22138", "Description": "BAKING SET SPACEBOY DESIGN", "UnitPrice": 4.95}
]

COUNTRIES = ["United Kingdom", "EIRE", "Netherlands", "Germany", "France", "Australia", "Spain", "Switzerland"]
CUSTOMERS = [12346, 12347, 12348, 12349, 12350, 13798, 14646, 14911, 15311, 17841, 18102, 18287]

def get_db_engine():
    try:
        connection_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(connection_url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return engine
    except Exception:
        return create_engine(f"sqlite:///{SQLITE_PATH}")

def generate_transaction():
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    is_cancelled = 1 if random.random() < 0.05 else 0
    invoice_num = f"{'C' if is_cancelled else ''}SIM{random.randint(100000, 999999)}"
    
    prod = random.choice(PRODUCTS)
    quantity = -random.randint(1, 5) if is_cancelled else random.randint(1, 24)
    unit_price = prod["UnitPrice"]
    customer_id = random.choice(CUSTOMERS) if random.random() > 0.15 else None
    country = random.choice(COUNTRIES) if random.random() > 0.1 else "United Kingdom"
    
    return {
        "InvoiceNo": invoice_num,
        "StockCode": prod["StockCode"],
        "Description": prod["Description"],
        "Quantity": quantity,
        "InvoiceDate": now_str,
        "UnitPrice": unit_price,
        "CustomerID": customer_id,
        "Country": country,
        "IsCancelled": is_cancelled,
        "is_simulated": 1
    }

def inject_transactions(count=1, delay=0.0):
    engine = get_db_engine()
    inserted_records = []
    
    for i in range(count):
        tx = generate_transaction()
        df_single = pd.DataFrame([tx])
        df_single.to_sql("fact_online_retail_transactions", con=engine, if_exists="append", index=False)
        inserted_records.append(tx)
        line_val = tx['Quantity'] * tx['UnitPrice'] if not tx['IsCancelled'] else 0.0
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Ingested Simulated Transaction: Invoice={tx['InvoiceNo']}, StockCode={tx['StockCode']}, Qty={tx['Quantity']}, Price=£{tx['UnitPrice']:.2f}, LineVal=£{line_val:.2f}, Country={tx['Country']}")
        if delay > 0 and i < count - 1:
            time.sleep(delay)
            
    return inserted_records

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Live Transaction Ingestion Simulator")
    parser.add_argument("--count", type=int, default=1, help="Number of simulated transactions to generate")
    parser.add_argument("--delay", type=float, default=0.0, help="Delay in seconds between transactions")
    parser.add_argument("--continuous", action="store_true", help="Run continuously in background")
    args = parser.parse_args()

    if args.continuous:
        print("Starting Live Transaction Ingestion Stream (Press Ctrl+C to stop)...")
        try:
            while True:
                inject_transactions(count=1, delay=0.0)
                time.sleep(args.delay if args.delay > 0 else 3.0)
        except KeyboardInterrupt:
            print("Ingestion stream stopped by user.")
    else:
        print(f"Ingesting {args.count} simulated transactions into live database...")
        inject_transactions(count=args.count, delay=args.delay)
        print("Done!")
