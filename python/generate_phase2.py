import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import time

print("Starting Phase 2 generation...")
t0 = time.time()

os.makedirs(os.path.join("data", "processed"), exist_ok=True)
os.makedirs("images", exist_ok=True)

excel_path = os.path.join("data", "raw", "online_retail_II.xlsx")
xl = pd.ExcelFile(excel_path, engine="calamine")

df1 = pd.read_excel(xl, sheet_name="Year 2009-2010", engine="calamine")
df2 = pd.read_excel(xl, sheet_name="Year 2010-2011", engine="calamine")

df_raw = pd.concat([df1, df2], ignore_index=True)
rows_before = len(df_raw)

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

df_raw['InvoiceNo'] = df_raw['InvoiceNo'].astype(str).str.strip()
df_raw['StockCode'] = df_raw['StockCode'].astype(str).str.strip().str.upper()
df_raw['Description'] = df_raw['Description'].astype(str).str.strip()
df_raw['Country'] = df_raw['Country'].astype(str).str.strip()
df_raw['Quantity'] = pd.to_numeric(df_raw['Quantity'], errors='coerce')
df_raw['UnitPrice'] = pd.to_numeric(df_raw['UnitPrice'], errors='coerce')
df_raw['InvoiceDate'] = pd.to_datetime(df_raw['InvoiceDate'])

duplicates_raw = df_raw.duplicated().sum()

df_dedup = df_raw.drop_duplicates().copy()

is_bad_debt = df_dedup['UnitPrice'] < 0
is_test = df_dedup['StockCode'].str.startswith('TEST')
is_zero_price_no_cust = (df_dedup['UnitPrice'] == 0) & (df_dedup['CustomerID'].isnull())

filtered_count = (is_bad_debt | is_test | is_zero_price_no_cust).sum()

df_cleaned = df_dedup[~is_bad_debt & ~is_test & ~is_zero_price_no_cust].copy()
df_cleaned['IsCancelled'] = df_cleaned['InvoiceNo'].str.upper().str.startswith('C') | (df_cleaned['Quantity'] < 0)

rows_after = len(df_cleaned)

df_cleaned['Revenue'] = (df_cleaned['Quantity'] * df_cleaned['UnitPrice']).round(2)
df_cleaned['Year'] = df_cleaned['InvoiceDate'].dt.year
df_cleaned['Month'] = df_cleaned['InvoiceDate'].dt.month
df_cleaned['YearMonth'] = df_cleaned['InvoiceDate'].dt.to_period('M').astype(str)
df_cleaned['MonthName'] = df_cleaned['InvoiceDate'].dt.strftime('%b')
df_cleaned['Quarter'] = df_cleaned['InvoiceDate'].dt.to_period('Q').astype(str)
df_cleaned['DayOfWeek'] = df_cleaned['InvoiceDate'].dt.day_name()
df_cleaned['Hour'] = df_cleaned['InvoiceDate'].dt.hour

sales_df = df_cleaned[(~df_cleaned['IsCancelled']) & (df_cleaned['Quantity'] > 0) & (df_cleaned['UnitPrice'] > 0)].copy()

print("Exporting retail_cleaned.csv...")
df_cleaned.to_csv(os.path.join("data", "processed", "retail_cleaned.csv"), index=False)

# Customer RFM & Segmentation
cust_sales = sales_df[sales_df['CustomerID'].notnull()].copy()
cust_sales['CustomerID'] = cust_sales['CustomerID'].astype(int)

ref_date = sales_df['InvoiceDate'].max() + pd.Timedelta(days=1)

rfm = cust_sales.groupby('CustomerID').agg(
    Recency=('InvoiceDate', lambda x: (ref_date - x.max()).days),
    Frequency=('InvoiceNo', 'nunique'),
    Monetary=('Revenue', 'sum')
).reset_index()

rfm['Monetary'] = rfm['Monetary'].round(2)

rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1]).astype(int)
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)

rfm['RFM_Score_Comb'] = rfm['R_Score'].astype(str) + rfm['F_Score'].astype(str) + rfm['M_Score'].astype(str)
rfm['RFM_Avg'] = ((rfm['R_Score'] + rfm['F_Score'] + rfm['M_Score']) / 3.0).round(2)

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

print("Exporting customer_rfm.csv...")
rfm.to_csv(os.path.join("data", "processed", "customer_rfm.csv"), index=False)

print("Exporting product_summary.csv...")
prod_summary = sales_df.groupby(['StockCode', 'Description']).agg(
    TotalQuantity=('Quantity', 'sum'),
    TotalRevenue=('Revenue', 'sum'),
    TotalOrders=('InvoiceNo', 'nunique'),
    AvgUnitPrice=('UnitPrice', 'mean')
).reset_index().sort_values(by='TotalRevenue', ascending=False)
prod_summary['TotalRevenue'] = prod_summary['TotalRevenue'].round(2)
prod_summary['AvgUnitPrice'] = prod_summary['AvgUnitPrice'].round(2)
prod_summary.to_csv(os.path.join("data", "processed", "product_summary.csv"), index=False)

print("Exporting country_summary.csv...")
country_summary = sales_df.groupby('Country').agg(
    TotalRevenue=('Revenue', 'sum'),
    TotalOrders=('InvoiceNo', 'nunique'),
    TotalCustomers=('CustomerID', lambda x: x.dropna().nunique())
).reset_index().sort_values(by='TotalRevenue', ascending=False)
country_summary['AvgOrderValue'] = (country_summary['TotalRevenue'] / country_summary['TotalOrders']).round(2)
country_summary['TotalRevenue'] = country_summary['TotalRevenue'].round(2)
country_summary.to_csv(os.path.join("data", "processed", "country_summary.csv"), index=False)

print("Exporting monthly_summary.csv...")
monthly_sales = sales_df.groupby(['YearMonth', 'Year', 'Month', 'MonthName']).agg(
    TotalRevenue=('Revenue', 'sum'),
    TotalOrders=('InvoiceNo', 'nunique'),
    TotalCustomers=('CustomerID', lambda x: x.dropna().nunique())
).reset_index()
monthly_sales['AvgOrderValue'] = (monthly_sales['TotalRevenue'] / monthly_sales['TotalOrders']).round(2)

monthly_cancels = df_cleaned[df_cleaned['IsCancelled']].groupby('YearMonth').agg(
    CancellationCount=('InvoiceNo', 'count')
).reset_index()

monthly_summary = pd.merge(monthly_sales, monthly_cancels, on='YearMonth', how='left')
monthly_summary['CancellationCount'] = monthly_summary['CancellationCount'].fillna(0).astype(int)
monthly_summary['CancellationRate'] = (monthly_summary['CancellationCount'] / (monthly_summary['TotalOrders'] + monthly_summary['CancellationCount'])).round(4)
monthly_summary['TotalRevenue'] = monthly_summary['TotalRevenue'].round(2)
monthly_summary.sort_values(by='YearMonth', inplace=True)
monthly_summary.to_csv(os.path.join("data", "processed", "monthly_summary.csv"), index=False)

print("Exporting data_quality_summary.csv...")
dq_df = pd.DataFrame([
    {'Metric': 'Raw Total Rows', 'Count': rows_before},
    {'Metric': 'Exact Duplicate Rows Removed', 'Count': duplicates_raw},
    {'Metric': 'Bad Debt Rows Removed (UnitPrice < 0)', 'Count': is_bad_debt.sum()},
    {'Metric': 'Test Code Rows Removed (TEST*)', 'Count': is_test.sum()},
    {'Metric': 'Zero Price No-Customer Rows Removed', 'Count': is_zero_price_no_cust.sum()},
    {'Metric': 'Final Cleaned Rows', 'Count': rows_after},
    {'Metric': 'Flagged Cancelled Lines (IsCancelled)', 'Count': int(df_cleaned['IsCancelled'].sum())},
    {'Metric': 'Missing CustomerIDs in Cleaned Data', 'Count': int(df_cleaned['CustomerID'].isnull().sum())},
    {'Metric': 'Unique Purchasing Customers (with ID)', 'Count': int(df_cleaned['CustomerID'].dropna().nunique())},
    {'Metric': 'Unique StockCodes', 'Count': int(df_cleaned['StockCode'].nunique())},
    {'Metric': 'Unique Countries', 'Count': int(df_cleaned['Country'].nunique())}
])
dq_df.to_csv(os.path.join("data", "processed", "data_quality_summary.csv"), index=False)

print("Generating visualization dashboard image: images/python_eda.png...")
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle("Online Retail II — Exploratory Data Analysis & Business Dashboard", fontsize=16, fontweight='bold')

ax1 = axes[0, 0]
sns.lineplot(data=monthly_summary, x='YearMonth', y='TotalRevenue', marker='o', ax=ax1, color='#1f77b4', linewidth=2.5)
ax1.set_title("Monthly Revenue Trend (Dec 2009 - Dec 2011)", fontweight='bold')
ax1.set_xlabel("Year-Month")
ax1.set_ylabel("Revenue (£)")
ax1.tick_params(axis='x', rotation=45)
ax1.yaxis.set_major_formatter('£{x:,.0f}')

ax2 = axes[0, 1]
seg_rev = rfm.groupby('CustomerSegment')['Monetary'].sum().reset_index().sort_values(by='Monetary', ascending=False)
sns.barplot(data=seg_rev, x='Monetary', y='CustomerSegment', palette='Blues_r', ax=ax2, hue='CustomerSegment', legend=False)
ax2.set_title("Revenue Contribution by Customer Segment", fontweight='bold')
ax2.set_xlabel("Total Revenue (£)")
ax2.set_ylabel("Customer Segment")
ax2.xaxis.set_major_formatter('£{x:,.0f}')

ax3 = axes[1, 0]
top_prod = prod_summary.head(10)
sns.barplot(data=top_prod, x='TotalRevenue', y='Description', palette='viridis', ax=ax3, hue='Description', legend=False)
ax3.set_title("Top 10 Products by Revenue", fontweight='bold')
ax3.set_xlabel("Total Revenue (£)")
ax3.set_ylabel("Product Description")
ax3.xaxis.set_major_formatter('£{x:,.0f}')

ax4 = axes[1, 1]
top_countries = country_summary[country_summary['Country'] != 'United Kingdom'].head(10)
sns.barplot(data=top_countries, x='TotalRevenue', y='Country', palette='Greens_r', ax=ax4, hue='Country', legend=False)
ax4.set_title("Top 10 International Markets by Revenue (excl. UK)", fontweight='bold')
ax4.set_xlabel("Total Revenue (£)")
ax4.set_ylabel("Country")
ax4.xaxis.set_major_formatter('£{x:,.0f}')

plt.tight_layout(rect=[0, 0, 1, 0.96])
fig.savefig(os.path.join("images", "python_eda.png"), dpi=300)
plt.close(fig)

print("Visual dashboard saved to images/python_eda.png")
print(f"All files exported successfully in {time.time()-t0:.2f}s!")
