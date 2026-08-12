import pandas as pd
import os

excel_path = os.path.join("data", "raw", "online_retail_II.xlsx")
xl = pd.ExcelFile(excel_path, engine="calamine")

df1 = pd.read_excel(xl, sheet_name="Year 2009-2010", engine="calamine")
df2 = pd.read_excel(xl, sheet_name="Year 2010-2011", engine="calamine")

print("Sheet 1 Date Range:", df1['InvoiceDate'].min(), "to", df1['InvoiceDate'].max())
print("Sheet 2 Date Range:", df2['InvoiceDate'].min(), "to", df2['InvoiceDate'].max())

# Check overlap
overlap_records = pd.merge(df1, df2, on=list(df1.columns), how="inner")
print("Exact duplicate rows across both sheets:", len(overlap_records))

# Check negative prices
print("\nNegative Price Records:")
df_all = pd.concat([df1, df2], ignore_index=True)
print(df_all[df_all['Price'] < 0][['Invoice', 'StockCode', 'Description', 'Quantity', 'Price', 'Customer ID']])

# Check non-standard stock codes
print("\nNon-standard StockCodes sample:")
non_numeric_stock = df_all[df_all['StockCode'].astype(str).str.contains(r'^[A-Za-z]', regex=True)]
print(non_numeric_stock['StockCode'].value_counts().head(20))

# Check zero prices with missing customer IDs
print("\nZero price breakdown:")
print("Zero price rows total:", len(df_all[df_all['Price'] == 0]))
print("Zero price with missing Customer ID:", df_all[df_all['Price'] == 0]['Customer ID'].isnull().sum())
print("Zero price with valid Customer ID:", df_all[df_all['Price'] == 0]['Customer ID'].notnull().sum())
print("Sample Descriptions for Zero Price & Valid Customer ID:")
print(df_all[(df_all['Price'] == 0) & (df_all['Customer ID'].notnull())]['Description'].value_counts().head(10))
