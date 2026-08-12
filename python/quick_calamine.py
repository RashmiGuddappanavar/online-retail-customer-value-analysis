import pandas as pd
import time
import os

start = time.time()
excel_path = os.path.join("data", "raw", "online_retail_II.xlsx")
print("Reading file with calamine...", excel_path)

xl = pd.ExcelFile(excel_path, engine="calamine")
print("Sheet names found:", xl.sheet_names, f"Time: {time.time()-start:.2f}s")

for sheet in xl.sheet_names:
    t0 = time.time()
    df = pd.read_excel(xl, sheet_name=sheet, engine="calamine")
    print(f"Sheet {sheet}: shape={df.shape}, loaded in {time.time()-t0:.2f}s")
    print(f"Columns: {list(df.columns)}")
    print(f"Missing values:\n{df.isnull().sum()}")
    print(f"Duplicates: {df.duplicated().sum()}")
    print(f"Min date: {df['InvoiceDate'].min()}, Max date: {df['InvoiceDate'].max()}")
    print(f"Unique Customer IDs: {df['Customer ID'].dropna().nunique()}")
    print(f"Missing Customer IDs: {df['Customer ID'].isnull().sum()}")
    cancelled = df['Invoice'].astype(str).str.upper().str.startswith('C')
    print(f"Cancelled invoices (starts with C): {cancelled.sum()}")
    print(f"Quantity < 0: {(df['Quantity'] < 0).sum()}, Quantity == 0: {(df['Quantity'] == 0).sum()}")
    print(f"Price < 0: {(df['Price'] < 0).sum()}, Price == 0: {(df['Price'] == 0).sum()}")
    print(f"Unique StockCodes: {df['StockCode'].astype(str).nunique()}")
    print(f"Unique Countries: {df['Country'].nunique()}")
    print("-" * 50)

print(f"Total script execution time: {time.time()-start:.2f}s")
