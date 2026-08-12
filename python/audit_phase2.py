import pandas as pd
import numpy as np
import os

print("==================================================")
print("PHASE 2 VALIDATION AUDIT")
print("==================================================\n")

excel_path = os.path.join("data", "raw", "online_retail_II.xlsx")
xl = pd.ExcelFile(excel_path, engine="calamine")

df1 = pd.read_excel(xl, sheet_name="Year 2009-2010", engine="calamine")
df2 = pd.read_excel(xl, sheet_name="Year 2010-2011", engine="calamine")

print("--- 1. ROW-COUNT RECONCILIATION ---")
raw_sheet1 = len(df1)
raw_sheet2 = len(df2)
df_raw = pd.concat([df1, df2], ignore_index=True)
raw_total = len(df_raw)

# Standardize columns
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

# Duplicates count
duplicates_exact = df_raw.duplicated().sum()

# Deduplicated
df_dedup = df_raw.drop_duplicates().copy()
dedup_total = len(df_dedup)

# Identify filtered suspicious/admin rows in deduplicated dataset
is_bad_debt = df_dedup['UnitPrice'] < 0
is_test = df_dedup['StockCode'].str.startswith('TEST')
is_zero_price_no_cust = (df_dedup['UnitPrice'] == 0) & (df_dedup['CustomerID'].isnull())

filtered_rows = df_dedup[is_bad_debt | is_test | is_zero_price_no_cust].copy()
filtered_count = len(filtered_rows)

bad_debt_count = is_bad_debt.sum()
test_count = is_test.sum()
zero_price_no_cust_count = is_zero_price_no_cust.sum()

df_cleaned = df_dedup[~is_bad_debt & ~is_test & ~is_zero_price_no_cust].copy()
cleaned_total = len(df_cleaned)

print(f"Raw rows: {raw_total:,}")
print(f"Exact duplicates removed: {duplicates_exact:,}")
print(f"Deduplicated rows: {dedup_total:,}")
print(f"Invalid / Suspicious admin rows removed: {filtered_count:,}")
print(f"  - Bad debt write-offs (UnitPrice < 0): {bad_debt_count}")
print(f"  - Test stock codes (TEST*): {test_count}")
print(f"  - Zero price without CustomerID (inventory notes/audits): {zero_price_no_cust_count:,}")
print(f"Final Cleaned rows: {cleaned_total:,}")

reconciled_sum = raw_total - duplicates_exact - filtered_count
print(f"Reconciliation check: {raw_total:,} - {duplicates_exact:,} - {filtered_count:,} = {reconciled_sum:,}")
print(f"Exact match with cleaned total ({cleaned_total:,})? {reconciled_sum == cleaned_total}\n")

print("--- 2. TRANSACTION FILTER & REVENUE RECONCILIATION ---")
df_cleaned['IsCancelled'] = df_cleaned['InvoiceNo'].str.upper().str.startswith('C') | (df_cleaned['Quantity'] < 0)
df_cleaned['Revenue'] = (df_cleaned['Quantity'] * df_cleaned['UnitPrice']).round(2)

sales_df = df_cleaned[(~df_cleaned['IsCancelled']) & (df_cleaned['Quantity'] > 0) & (df_cleaned['UnitPrice'] > 0)].copy()

total_sales_revenue = sales_df['Revenue'].sum()
total_orders = sales_df['InvoiceNo'].nunique()
aov = total_sales_revenue / total_orders

print(f"Total Completed Sales Revenue: £{total_sales_revenue:,.2f}")
print(f"Total Completed Orders: {total_orders:,}")
print(f"Average Order Value (AOV): £{aov:,.2f}")
print(f"Independent AOV calculation (£{total_sales_revenue:,.2f} / {total_orders}): £{(total_sales_revenue / total_orders):,.4f}\n")

print("--- 3. CUSTOMER RECONCILIATION ---")
cust_sales = sales_df[sales_df['CustomerID'].notnull()].copy()
cust_sales['CustomerID'] = cust_sales['CustomerID'].astype(int)

guest_sales = sales_df[sales_df['CustomerID'].isnull()].copy()

cust_revenue = cust_sales['Revenue'].sum()
guest_revenue = guest_revenue = guest_sales['Revenue'].sum()
unique_purchasing_customers = cust_sales['CustomerID'].nunique()

print(f"Total Unique Purchasing Customers (with ID): {unique_purchasing_customers:,}")
print(f"Customer-Level Sales Revenue (with ID): £{cust_revenue:,.2f}")
print(f"Guest / Unknown Customer Sales Revenue (no ID): £{guest_revenue:,.2f}")
print(f"Sum of Customer + Guest Revenue: £{(cust_revenue + guest_revenue):,.2f}")
print(f"Reconciles with Total Completed Sales Revenue (£{total_sales_revenue:,.2f})? {np.isclose(cust_revenue + guest_revenue, total_sales_revenue)}\n")

print("--- 4. REPEAT CUSTOMER VALIDATION ---")
cust_orders = cust_sales.groupby('CustomerID').agg(
    Orders=('InvoiceNo', 'nunique'),
    Revenue=('Revenue', 'sum')
).reset_index()

total_cust_count = len(cust_orders)
repeat_cust_count = (cust_orders['Orders'] > 1).sum()
onetime_cust_count = (cust_orders['Orders'] == 1).sum()
repeat_rate = (repeat_cust_count / total_cust_count) * 100

print(f"Total Identified Purchasing Customers: {total_cust_count:,}")
print(f"Repeat Customers (>1 order): {repeat_cust_count:,}")
print(f"One-Time Customers (1 order): {onetime_cust_count:,}")
print(f"Repeat Customer Rate: {repeat_rate:.4f}% ({repeat_rate:.2f}%)\n")

print("--- 5. RFM & CUSTOMER SEGMENT VALIDATION ---")
ref_date = sales_df['InvoiceDate'].max() + pd.Timedelta(days=1)
print(f"Derived Reference Date: {ref_date}")

rfm = cust_sales.groupby('CustomerID').agg(
    Recency=('InvoiceDate', lambda x: (ref_date - x.max()).days),
    Frequency=('InvoiceNo', 'nunique'),
    Monetary=('Revenue', 'sum')
).reset_index()

rfm['Monetary'] = rfm['Monetary'].round(2)
rfm['R_Score'] = pd.qcut(rfm['Recency'], 5, labels=[5, 4, 3, 2, 1]).astype(int)
rfm['F_Score'] = pd.qcut(rfm['Frequency'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm['M_Score'] = pd.qcut(rfm['Monetary'].rank(method='first'), 5, labels=[1, 2, 3, 4, 5]).astype(int)

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

seg_table = rfm.groupby('CustomerSegment').agg(
    Customers=('CustomerID', 'count'),
    Revenue=('Monetary', 'sum'),
    Avg_Recency=('Recency', 'mean'),
    Avg_Frequency=('Frequency', 'mean')
).reset_index().sort_values(by='Revenue', ascending=False)

seg_table['Avg_Recency'] = seg_table['Avg_Recency'].round(2)
seg_table['Avg_Frequency'] = seg_table['Avg_Frequency'].round(2)

print(seg_table.to_string(index=False))
print(f"Total customers across all segments: {rfm['CustomerSegment'].count()}")
print(f"Any missing segment assignments? {rfm['CustomerSegment'].isnull().sum() > 0}\n")

print("--- 6. CHURN-RISK PROXY VALIDATION ---")
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

churn_table = rfm.groupby('ChurnRiskProxy').agg(
    Customers=('CustomerID', 'count'),
    Revenue=('Monetary', 'sum'),
    Avg_Recency=('Recency', 'mean'),
    Avg_Frequency=('Frequency', 'mean')
).reset_index().sort_values(by='Customers', ascending=False)

churn_table['Avg_Recency'] = churn_table['Avg_Recency'].round(2)
churn_table['Avg_Frequency'] = churn_table['Avg_Frequency'].round(2)

print(churn_table.to_string(index=False))
high_risk_cust = rfm[rfm['ChurnRiskProxy'] == 'High Risk (Churn Proxy)']
print(f"High-Risk Customers Count: {len(high_risk_cust):,}")
print(f"High-Risk Customer Prior Revenue: £{high_risk_cust['Monetary'].sum():,.2f}\n")

print("--- 7. PRODUCT & COUNTRY RECONCILIATION ---")
top_prod = sales_df.groupby(['StockCode', 'Description']).agg(
    TotalRevenue=('Revenue', 'sum')
).reset_index().sort_values(by='TotalRevenue', ascending=False).iloc[0]
print(f"Top Product: {top_prod['StockCode']} - {top_prod['Description']}: £{top_prod['TotalRevenue']:,.2f}")

top_countries = sales_df.groupby('Country')['Revenue'].sum().reset_index().sort_values(by='Revenue', ascending=False).head(5)
print("Top 5 Countries:")
print(top_countries.to_string(index=False))
print(f"Sum of ALL country revenues: £{sales_df.groupby('Country')['Revenue'].sum().sum():,.2f}")
print(f"Matches total completed revenue (£{total_sales_revenue:,.2f})? {np.isclose(sales_df.groupby('Country')['Revenue'].sum().sum(), total_sales_revenue)}\n")

print("--- 8. CANCELLATION VALIDATION ---")
cancelled_lines = df_cleaned['IsCancelled'].sum()
cleaned_lines = len(df_cleaned)
canc_rate = (cancelled_lines / cleaned_lines) * 100
print(f"Cancelled transaction lines: {cancelled_lines:,}")
print(f"Total cleaned transaction lines: {cleaned_lines:,}")
print(f"Cancelled transaction-line rate: {canc_rate:.4f}% ({canc_rate:.2f}%)\n")

print("--- 9. OUTPUT FILE VALIDATION ---")
files_to_check = [
    "retail_cleaned.csv", "customer_rfm.csv", "product_summary.csv",
    "country_summary.csv", "monthly_summary.csv", "data_quality_summary.csv"
]
for fname in files_to_check:
    fpath = os.path.join("data", "processed", fname)
    if os.path.exists(fpath):
        df_chk = pd.read_csv(fpath)
        print(f"File {fname}: Exists | Rows={len(df_chk):,} | Cols={len(df_chk.columns)} | Nulls={df_chk.isnull().sum().sum()}")
    else:
        print(f"File {fname}: MISSING!")
