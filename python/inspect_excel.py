import pandas as pd
import numpy as np
import os
import sys

excel_path = os.path.join("data", "raw", "online_retail_II.xlsx")

print("Checking Excel file:", excel_path)
if not os.path.exists(excel_path):
    print("File not found!")
    sys.exit(1)

# Read Excel file sheet names using calamine engine for high performance
try:
    xl = pd.ExcelFile(excel_path, engine="calamine")
except Exception:
    xl = pd.ExcelFile(excel_path)
sheet_names = xl.sheet_names
print("Sheet Names:", sheet_names)

sheets_data = {}
for sheet in sheet_names:
    print(f"\n--- Loading sheet: {sheet} ---")
    try:
        df = pd.read_excel(xl, sheet_name=sheet, engine="calamine")
    except Exception:
        df = pd.read_excel(xl, sheet_name=sheet)
    sheets_data[sheet] = df
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"Data types:\n{df.dtypes}")
    print(f"Missing values:\n{df.isnull().sum()}")
    print(f"Duplicate rows count: {df.duplicated().sum()}")
    
    # Invoices starting with 'C'
    cancelled_mask = df['Invoice'].astype(str).str.upper().str.startswith('C')
    print(f"Cancelled Invoices count (starting with 'C'): {cancelled_mask.sum()}")
    
    # Negative / Zero Quantities
    neg_qty = (df['Quantity'] < 0).sum()
    zero_qty = (df['Quantity'] == 0).sum()
    print(f"Negative Quantities count: {neg_qty}")
    print(f"Zero Quantities count: {zero_qty}")
    
    # Negative / Zero Prices
    neg_price = (df['Price'] < 0).sum()
    zero_price = (df['Price'] == 0).sum()
    print(f"Negative Prices count: {neg_price}")
    print(f"Zero Prices count: {zero_price}")
    
    # Date range
    print(f"Min InvoiceDate: {df['InvoiceDate'].min()}")
    print(f"Max InvoiceDate: {df['InvoiceDate'].max()}")
    
    # Unique values
    print(f"Unique Customers (excluding NaN): {df['Customer ID'].dropna().nunique()}")
    print(f"Missing Customer IDs count: {df['Customer ID'].isnull().sum()}")
    print(f"Unique StockCodes: {df['StockCode'].astype(str).nunique()}")
    print(f"Unique Descriptions: {df['Description'].astype(str).nunique()}")
    print(f"Unique Countries: {df['Country'].nunique()}")
    
    # Suspicious records checks:
    # 1. Quantity < 0 but Invoice does NOT start with C
    neg_qty_no_c = df[(df['Quantity'] < 0) & (~cancelled_mask)]
    print(f"Quantity < 0 but Invoice does NOT start with 'C': {len(neg_qty_no_c)}")
    
    # 2. Invoice starts with C but Quantity >= 0
    c_inv_pos_qty = df[cancelled_mask & (df['Quantity'] >= 0)]
    print(f"Invoice starts with 'C' but Quantity >= 0: {len(c_inv_pos_qty)}")
    
    # 3. Price == 0 records
    print(f"Price == 0 records: {len(df[df['Price'] == 0])}")
    
    # 4. Customer ID missing for cancelled vs non-cancelled
    print(f"Missing Customer ID in cancelled invoices: {df[cancelled_mask]['Customer ID'].isnull().sum()}")
    print(f"Missing Customer ID in non-cancelled invoices: {df[~cancelled_mask]['Customer ID'].isnull().sum()}")

# Combined Analysis
df_all = pd.concat(sheets_data.values(), ignore_index=True)
print("\n================ COMBINED DATASET OVERVIEW ================")
print(f"Total Rows: {len(df_all)}")
print(f"Total Duplicate Rows (across all cols): {df_all.duplicated().sum()}")
print(f"Overall Date Range: {df_all['InvoiceDate'].min()} to {df_all['InvoiceDate'].max()}")
print(f"Overall Unique Customer IDs: {df_all['Customer ID'].dropna().nunique()}")
print(f"Overall Missing Customer IDs: {df_all['Customer ID'].isnull().sum()}")
print(f"Overall Unique StockCodes: {df_all['StockCode'].astype(str).nunique()}")
print(f"Overall Unique Countries: {df_all['Country'].nunique()}")
cancelled_all = df_all['Invoice'].astype(str).str.upper().str.startswith('C')
print(f"Overall Cancelled Invoices count: {cancelled_all.sum()}")
print(f"Overall Negative Quantities count: {(df_all['Quantity'] < 0).sum()}")
print(f"Overall Zero Price count: {(df_all['Price'] == 0).sum()}")
print(f"Overall Negative Price count: {(df_all['Price'] < 0).sum()}")
