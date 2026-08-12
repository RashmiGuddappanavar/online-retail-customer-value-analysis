import pandas as pd
import numpy as np
import os
import time

t0 = time.time()
excel_path = os.path.join("data", "raw", "online_retail_II.xlsx")
print("Loading workbook...", excel_path)

xl = pd.ExcelFile(excel_path, engine="calamine")
df1 = pd.read_excel(xl, sheet_name="Year 2009-2010", engine="calamine")
df2 = pd.read_excel(xl, sheet_name="Year 2010-2011", engine="calamine")

print(f"Sheet 1 shape: {df1.shape}, Sheet 2 shape: {df2.shape}")

# Combine both sheets
df_raw = pd.concat([df1, df2], ignore_index=True)
rows_before = len(df_raw)
print(f"Raw Combined Shape: {df_raw.shape}")

# Standardize column names
df_raw.rename(columns={
    'Invoice': 'InvoiceNo',
    'StockCode': 'StockCode',
    'Description': 'Description',
    'Quantity': 'Quantity',
    'InvoiceDate': 'InvoiceDate',
    'Price': 'UnitPrice',
    'Customer ID': 'CustomerID',
    'Country': 'Country'
}, inplace=True)

# Data type conversions
df_raw['InvoiceNo'] = df_raw['InvoiceNo'].astype(str).str.strip()
df_raw['StockCode'] = df_raw['StockCode'].astype(str).str.strip()
df_raw['Description'] = df_raw['Description'].astype(str).str.strip()
df_raw['Country'] = df_raw['Country'].astype(str).str.strip()
df_raw['Quantity'] = pd.to_numeric(df_raw['Quantity'], errors='coerce')
df_raw['UnitPrice'] = pd.to_numeric(df_raw['UnitPrice'], errors='coerce')
df_raw['InvoiceDate'] = pd.to_datetime(df_raw['InvoiceDate'])

# Detect duplicates before any filtering
duplicates_count = df_raw.duplicated().sum()

# Identify IsCancelled
df_raw['IsCancelled'] = df_raw['InvoiceNo'].str.upper().str.startswith('C') | (df_raw['Quantity'] < 0)

# Identify Bad Debt / Admin Adjustments
is_bad_debt = df_raw['UnitPrice'] < 0
is_test = df_raw['StockCode'].str.upper().str.startswith('TEST')
is_zero_price_no_cust = (df_raw['UnitPrice'] == 0) & (df_raw['CustomerID'].isnull())

# Clean dataset:
# 1. Deduplicate exact duplicate rows
df_cleaned = df_raw.drop_duplicates().copy()

# 2. Exclude administrative adjustments (bad debt, zero-price non-customer records, test stockcodes)
df_cleaned = df_cleaned[~is_bad_debt & ~is_test & ~is_zero_price_no_cust].copy()

# Clean StockCode string formatting
df_cleaned['StockCode'] = df_cleaned['StockCode'].str.upper()

rows_after = len(df_cleaned)

# Feature engineering
df_cleaned['Revenue'] = df_cleaned['Quantity'] * df_cleaned['UnitPrice']
df_cleaned['Year'] = df_cleaned['InvoiceDate'].dt.year
df_cleaned['Month'] = df_cleaned['InvoiceDate'].dt.month
df_cleaned['YearMonth'] = df_cleaned['InvoiceDate'].dt.to_period('M').astype(str)
df_cleaned['MonthName'] = df_cleaned['InvoiceDate'].dt.strftime('%b')
df_cleaned['Quarter'] = df_cleaned['InvoiceDate'].dt.to_period('Q').astype(str)
df_cleaned['DayOfWeek'] = df_cleaned['InvoiceDate'].dt.day_name()
df_cleaned['Hour'] = df_cleaned['InvoiceDate'].dt.hour

print("\n--- DATA QUALITY VALIDATION METRICS ---")
print(f"Rows before cleaning: {rows_before}")
print(f"Rows after cleaning: {rows_after}")
print(f"Exact duplicates removed: {duplicates_count}")
print(f"Cancelled transactions count: {df_cleaned['IsCancelled'].sum()}")
print(f"Missing CustomerIDs count: {df_cleaned['CustomerID'].isnull().sum()}")
print(f"Invalid / zero prices count in cleaned data: {(df_cleaned['UnitPrice'] <= 0).sum()}")
print(f"Negative quantities count in cleaned data: {(df_cleaned['Quantity'] < 0).sum()}")
print(f"Date range: {df_cleaned['InvoiceDate'].min()} to {df_cleaned['InvoiceDate'].max()}")
print(f"Unique customers: {df_cleaned['CustomerID'].dropna().nunique()}")
print(f"Unique products (StockCode): {df_cleaned['StockCode'].nunique()}")
print(f"Unique countries: {df_cleaned['Country'].nunique()}")

# Sales subset for revenue, time-series, product, country analysis
sales_df = df_cleaned[(~df_cleaned['IsCancelled']) & (df_cleaned['Quantity'] > 0) & (df_cleaned['UnitPrice'] > 0)].copy()

total_revenue = sales_df['Revenue'].sum()
total_orders = sales_df['InvoiceNo'].nunique()
total_customers = sales_df['CustomerID'].dropna().nunique()
avg_order_value = total_revenue / total_orders

print("\n--- REVENUE ANALYSIS ---")
print(f"Total Sales Revenue: £{total_revenue:,.2f}")
print(f"Total Completed Orders: {total_orders:,}")
print(f"Total Unique Purchasing Customers: {total_customers:,}")
print(f"Average Order Value (AOV): £{avg_order_value:,.2f}")

# Customer Level Analysis
cust_sales = sales_df[sales_df['CustomerID'].notnull()].copy()
cust_sales['CustomerID'] = cust_sales['CustomerID'].astype(int)

# RFM Calculation
ref_date = sales_df['InvoiceDate'].max() + pd.Timedelta(days=1)
print(f"\nRFM Reference Date: {ref_date}")

rfm = cust_sales.groupby('CustomerID').agg({
    'InvoiceDate': lambda x: (ref_date - x.max()).days,
    'InvoiceNo': 'nunique',
    'Revenue': 'sum'
}).reset_index()

rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

print(f"RFM Dataframe Shape: {rfm.shape}")
print(rfm.describe())

# RFM Scoring using rank/qcut
# Recency: lower is better (1 = highest recency days / worst, 5 = lowest recency days / best)
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1])

# Frequency: higher is better. Note: many customers have 1 order, so use custom bins/rank
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])

# Monetary: higher is better
rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5])

rfm['R_Score'] = rfm['R_Score'].astype(int)
rfm['F_Score'] = rfm['F_Score'].astype(int)
rfm['M_Score'] = rfm['M_Score'].astype(int)

rfm['RFM_Score_Comb'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
rfm['RFM_Avg'] = ((rfm['R_Score'] + rfm['F_Score'] + rfm['M_Score']) / 3.0).round(2)

# Customer Segmentation Rules
def segment_customer(row):
    r, f, m = row['R_Score'], row['F_Score'], row['M_Score']
    if r >= 4 and f >= 4 and m >= 4:
        return 'Champions'
    elif r >= 3 and f >= 3 and m >= 3:
        return 'Loyal Customers'
    elif r >= 4 and f <= 2:
        return 'Potential Loyalists'
    elif r <= 2 and f >= 3:
        return 'At Risk Spenders'
    elif r <= 2 and f <= 2 and m <= 2:
        return 'Lost Customers'
    elif r == 3 and f <= 2:
        return 'Needs Attention'
    else:
        return 'Promising / Average'

rfm['CustomerSegment'] = rfm.apply(segment_customer, axis=1)

# Churn-Risk Proxy Definition
# High Risk: Inactive > 90 days AND previously made >= 2 orders (or At Risk/Lost segments)
# Medium Risk: Inactive > 90 days with 1 order OR Inactive 60-90 days with >= 2 orders
# Low Risk: Active within 60 days
def get_churn_risk_proxy(row):
    rec = row['Recency']
    freq = row['Frequency']
    if rec > 90 and freq >= 2:
        return 'High Risk (Churn Proxy)'
    elif rec > 90 and freq == 1:
        return 'Medium Risk (One-time Inactive)'
    elif 60 < rec <= 90 and freq >= 2:
        return 'Medium Risk (Dormant Frequent)'
    elif rec <= 60:
        return 'Low Risk (Active)'
    else:
        return 'Low Risk'

rfm['ChurnRiskProxy'] = rfm.apply(get_churn_risk_proxy, axis=1)

print("\n--- CUSTOMER SEGMENTATION SUMMARY ---")
seg_summary = rfm.groupby('CustomerSegment').agg(
    Customer_Count=('CustomerID', 'count'),
    Total_Revenue=('Monetary', 'sum'),
    Avg_Revenue=('Monetary', 'mean'),
    Avg_Recency=('Recency', 'mean'),
    Avg_Frequency=('Frequency', 'mean')
).reset_index().sort_values(by='Total_Revenue', ascending=False)
print(seg_summary)

print("\n--- CHURN RISK PROXY SUMMARY ---")
churn_summary = rfm.groupby('ChurnRiskProxy').agg(
    Customer_Count=('CustomerID', 'count'),
    Total_Revenue=('Monetary', 'sum'),
    Avg_Revenue=('Monetary', 'mean'),
    Avg_Recency=('Recency', 'mean')
).reset_index().sort_values(by='Customer_Count', ascending=False)
print(churn_summary)

print(f"\nPipeline finished in {time.time()-t0:.2f}s")
