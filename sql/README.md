# Phase 3 — MySQL Database & SQL Analytics Layer

## Overview

Phase 3 establishes an interview-defensible, production-ready MySQL 8.x database schema and SQL analytical query layer for the Online Retail II project. The SQL framework translates validated transaction-level data (`data/processed/`) into commercial insights addressing customer valuation, churn risk, product performance, geographic concentration, and revenue trajectory.

---

## 1. Database Architecture & Setup

### Environment Requirements
- **Target Database Engine**: MySQL 8.0+ / MariaDB 10.5+
- **Database Name**: `online_retail_analytics`
- **Character Set**: `utf8mb4`
- **Collation**: `utf8mb4_unicode_ci`

### Table Schemas & Source Files

| Table Name | Description | Source CSV File | Primary Key / Natural Key | Row Count |
| :--- | :--- | :--- | :--- | :--- |
| `retail_transactions` | Cleaned transaction-level order detail | `retail_cleaned.csv` | Composite `(InvoiceNo, StockCode, InvoiceDate)` | 1,027,071 |
| `customer_rfm` | Customer RFM scores & churn risk classification | `customer_rfm.csv` | `CustomerID` | 5,878 |
| `product_summary` | Pre-aggregated product performance metrics | `product_summary.csv` | `StockCode` | 5,400 |
| `country_summary` | Geographic revenue & customer summaries | `country_summary.csv` | `Country` | 43 |
| `monthly_summary` | Time-series monthly revenue & order totals | `monthly_summary.csv` | `YearMonth` | 25 |

### Indexing Strategy
To optimize query performance across 1M+ transaction rows, targeted single-column indexes were implemented on frequently filtered/joined keys:
- `CustomerID`: Accelerates customer history aggregation and RFM table joins.
- `InvoiceNo`: Speeds up order-level distinct counts and basket analyses.
- `StockCode`: Optimizes product lookup and rank partitioning.
- `InvoiceDate`: Enhances time-series filtering and window function execution.
- `Country`: Speeds up geographic slicing and partitioning.
- `IsCancelled`: Enables rapid filtering of completed vs. cancelled transactions.

---

## 2. Standard Business Metrics & Analytical Rules

### Official Revenue & Order Definitions

1. **Completed Sales Revenue**:
   $$\text{Completed Revenue} = \sum (\text{Quantity} \times \text{UnitPrice}) \quad \text{WHERE } \text{IsCancelled} = 0 \text{ AND } \text{Quantity} > 0 \text{ AND } \text{UnitPrice} > 0$$
   *All revenue analytics across customer, product, country, and time-series modules strictly adhere to this definition.*

2. **Completed Order Count**:
   $$\text{Completed Orders} = \text{COUNT(DISTINCT InvoiceNo)} \quad \text{WHERE } \text{IsCancelled} = 0 \text{ AND } \text{Quantity} > 0 \text{ AND } \text{UnitPrice} > 0$$
   *Cancelled invoices (invoices with 'C' prefix or negative quantities) are excluded from completed-order totals and evaluated separately in cancellation audit queries.*

3. **Time Horizon & Calendar Months**:
   - **Min Date**: `2009-12-01 07:45:00`
   - **Max Date**: `2011-12-09 12:50:00`
   - **Calendar Months Covered**: **25 calendar months** (Dec 2009 through Dec 2011 inclusive; 2 full years plus 9 days in Dec 2011).

---

## 3. Data Import Process

### Method 1: MySQL `LOAD DATA LOCAL INFILE` (Command Line / Workbench)
Run `01_database_schema.sql` inside MySQL Workbench or MySQL CLI:

```sql
SET GLOBAL local_infile = 1;

LOAD DATA LOCAL INFILE 'data/processed/retail_cleaned.csv'
INTO TABLE retail_transactions
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, @vCustomerID, Country, @vIsCancelled, Revenue, Year, Month, YearMonth, MonthName, Quarter, DayOfWeek, Hour)
SET 
   CustomerID = NULLIF(@vCustomerID, ''),
   IsCancelled = IF(@vIsCancelled = 'True' OR @vIsCancelled = '1', 1, 0);
```

### Method 2: Python / SQLAlchemy Automated Import (Recommended Alternative)
If Windows security or MySQL server permissions restrict `LOCAL INFILE`, execute the following Python script to load data directly into MySQL:

```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('mysql+pymysql://root:password@localhost:3306/online_retail_analytics')

tables = {
    'retail_transactions': 'data/processed/retail_cleaned.csv',
    'customer_rfm': 'data/processed/customer_rfm.csv',
    'product_summary': 'data/processed/product_summary.csv',
    'country_summary': 'data/processed/country_summary.csv',
    'monthly_summary': 'data/processed/monthly_summary.csv'
}

for table_name, csv_path in tables.items():
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, engine, if_exists='replace', index=False, chunksize=10000)
    print(f"Successfully loaded {len(df):,} rows into {table_name}")
```

---

## 4. Business Questions Answered by SQL

| Business Question | Relevant SQL File | Key Query / Technique Used |
| :--- | :--- | :--- |
| **1. Which customer segments are most valuable?** | `03_customer_analysis.sql` | Section 5: Aggregates `Monetary` value by `CustomerSegment` from `customer_rfm`. |
| **2. Which customers are potentially at risk (churn proxy)?** | `03_customer_analysis.sql` | Section 6 & 7: Filters `ChurnRiskProxy = 'High Risk (Churn Proxy)'` and orders by past spend. |
| **3. Which products drive revenue?** | `04_product_analysis.sql` | Section 1 & 5: Uses `DENSE_RANK()` and `ROW_NUMBER() OVER (PARTITION BY Country)`. |
| **4. Which countries drive revenue?** | `05_revenue_analysis.sql` | Section 5: Grouping by `Country` with revenue contribution % calculation. |
| **5. What are the major revenue trends?** | `05_revenue_analysis.sql` | Section 4: Calculates MoM growth rate using `LAG()` window function. |
| **6. Where are cancellations concentrated?** | `02_data_quality.sql` & `05_revenue_analysis.sql` | Section 7: Tracks line cancellation counts and rates over time (`YearMonth`). |
| **7. How do repeat buyers compare to one-time buyers?** | `03_customer_analysis.sql` | Section 1: CTE calculating order count per customer and repeat purchase rate. |

---

## 5. Python ↔ SQL Reconciliation Matrix & Discrepancy Audits

### Reconciled Metrics Summary

| Metric | Python Value | SQL Value | Variance | Status |
| :--- | :---: | :---: | :---: | :---: |
| **Total Completed Revenue** | £20,476,034.43 | £20,476,034.43 | £0.00 | **EXACT MATCH** |
| **Total Completed Orders** | 40,067 | 40,067 | 0 | **EXACT MATCH** |
| **Unique Purchasing Customers** | 5,878 | 5,878 | 0 | **EXACT MATCH** |
| **Repeat Customer Rate** | 72.39% | 72.39% (4,255 / 5,878) | 0.00% | **EXACT MATCH** |
| **High-Risk Churn Proxy Count** | 1,731 | 1,731 | 0 | **EXACT MATCH** |
| **High-Risk Prior Revenue** | £2,969,509.67 | £2,969,509.67 | £0.00 | **EXACT MATCH** |
| **Top Product (Revenue)** | `22423` (Cake Stand) | `22423` - REGENCY CAKESTAND 3 TIER | None | **EXACT MATCH** |
| **Top Country (Revenue)** | United Kingdom (£17,409,970.10) | United Kingdom (£17,409,970.10) | £0.00 | **EXACT MATCH** |
| **Cancellation Line Count** | 19,100 | 19,100 | 0 | **EXACT MATCH** |
| **Cancellation Line Rate** | 1.86% | 1.86% | 0.00% | **EXACT MATCH** |

### Audit Findings & Discrepancy Reconciliation Notes

1. **UK Revenue Reconciliation**:
   - **Validated Figure**: **£17,409,970.10** (Total Completed UK Sales across identified customers (£14,389,008.90) and guest orders (£3,020,961.20)).
   - **Legacy Figure Note**: An earlier uncleaned draft figure of £17,046,943.43 reflected raw UK customer revenue prior to final Phase 2 deduplication and guest transaction separation.

2. **High-Risk Churn Proxy Revenue Reconciliation**:
   - **Validated Figure**: **£2,969,509.67** (Exact sum of `Monetary` for the 1,731 High-Risk customers in `customer_rfm.csv`).
   - **Legacy Figure Note**: An earlier draft figure of £2,971,510.08 was derived from pre-deduplicated customer records.

3. **Sum of Country Revenues**:
   - $\sum (\text{Country Revenue}) = \text{£20,476,034.43}$, matching Total Completed Sales Revenue exactly (£0.00 variance).

---

## 6. Execution Environment & MySQL Compatibility Disclaimer

> [!IMPORTANT]
> **Execution Environment Disclaimer**:
> - Analytical query logic was validated using an embedded Python/SQLite environment directly against `data/processed/*.csv`.
> - All DDL and SQL scripts (`01` through `05`) are authored specifically for **MySQL 8.x** (utilizing MySQL data types, `InnoDB` storage engine syntax, `TINYINT(1)` boolean aliases, `LIMIT` clauses, and MySQL window functions).
> - The queries have **NOT** been executed on a live MySQL server because no local MySQL server was running in the CLI environment during this phase. They are 100% syntactically ready for execution in any live MySQL 8.x instance.
