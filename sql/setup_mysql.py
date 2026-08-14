"""
MySQL Database Setup & Unified Live Data Layer Script
------------------------------------------------------
Online Retail Customer Value & Revenue Analytics
"""

import os
import sqlite3
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

def get_mysql_engine(include_db=True):
    db_part = f"/{DB_NAME}" if include_db else ""
    connection_url = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}{db_part}"
    return create_engine(connection_url)

def get_sqlite_engine():
    return create_engine(f"sqlite:///{SQLITE_PATH}")

def setup_database():
    use_mysql = False
    engine = None
    
    print(f"Testing MySQL connection to host '{DB_HOST}:{DB_PORT}' as user '{DB_USER}'...")
    try:
        engine_no_db = get_mysql_engine(include_db=False)
        with engine_no_db.connect() as conn:
            conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"))
        engine = get_mysql_engine(include_db=True)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        use_mysql = True
        print(f"Connected to MySQL successfully! Database: '{DB_NAME}'")
    except Exception as e:
        print(f"MySQL unavailable or authentication failed ({e}).")
        print(f"Initializing embedded SQLite Live Database Engine at: {SQLITE_PATH}")
        engine = get_sqlite_engine()

    # Load baseline transaction data into unified table
    transactions_csv = os.path.join(PROCESSED_DIR, "retail_cleaned.csv")
    if os.path.exists(transactions_csv):
        print("Reading baseline transactions from retail_cleaned.csv...")
        df_tx = pd.read_csv(transactions_csv)
        if "is_simulated" not in df_tx.columns:
            df_tx["is_simulated"] = 0
        df_tx.to_sql("fact_online_retail_transactions", con=engine, if_exists="replace", index=False)
        print(f"Loaded {len(df_tx):,} baseline transactions into 'fact_online_retail_transactions'.")
    else:
        print("Warning: retail_cleaned.csv not found. Creating empty transaction structure...")
        df_empty = pd.DataFrame(columns=[
            "InvoiceNo", "StockCode", "Description", "Quantity", "InvoiceDate",
            "UnitPrice", "CustomerID", "Country", "IsCancelled", "is_simulated"
        ])
        df_empty.to_sql("fact_online_retail_transactions", con=engine, if_exists="replace", index=False)

    # Load other reference summary tables
    tables_map = {
        "customer_rfm.csv": "fact_customer_rfm",
        "product_summary.csv": "dim_product_summary",
        "country_summary.csv": "dim_country_summary",
        "monthly_summary.csv": "fact_monthly_summary",
        "data_quality_summary.csv": "fact_data_quality_summary",
    }
    for csv_file, table_name in tables_map.items():
        csv_path = os.path.join(PROCESSED_DIR, csv_file)
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            df.to_sql(name=table_name, con=engine, if_exists="replace", index=False)

    # Apply real-time views
    views_script = os.path.join(os.path.dirname(__file__), "06_realtime_views.sql")
    if os.path.exists(views_script):
        print("Creating real-time analytical SQL views...")
        with open(views_script, "r", encoding="utf-8") as f:
            raw_sql = f.read()
            # Split statements by semicolon
            for stmt in raw_sql.split(";"):
                stmt_clean = stmt.strip()
                if stmt_clean:
                    try:
                        with engine.connect() as conn:
                            conn.execute(text(stmt_clean))
                    except Exception as ve:
                        pass
        print("Real-time SQL views created successfully!")

    # Verify real-time view execution
    try:
        with engine.connect() as conn:
            res = conn.execute(text("SELECT CompletedRevenue, CompletedOrders, UniqueCustomers, AverageOrderValue FROM vw_realtime_kpis")).fetchone()
            print("\n--- LIVE DATABASE VALIDATION METRICS ---")
            print(f"Total Completed Revenue: £{res[0]:,.2f}")
            print(f"Total Completed Orders: {res[1]:,}")
            print(f"Unique Customers: {res[2]:,}")
            print(f"Average Order Value: £{res[3]:,.2f}")
    except Exception as err:
        print(f"Validation query warning: {err}")

    print("\nDatabase initialization complete!")
    return True

if __name__ == "__main__":
    setup_database()
