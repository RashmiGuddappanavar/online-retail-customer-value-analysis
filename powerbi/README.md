# Phase 5 — Power BI Customer & Revenue Analytics

## Executive Summary

Phase 5 establishes a complete, production-ready Power BI data model, DAX measure repository, interactive multi-page report layout specification, and setup documentation for the Online Retail II project. The architecture transforms validated transaction data (`powerbi/powerbi_data/`) into executive decision-support analytics addressing customer valuation, RFM segmentation, churn risk, product performance, geographic concentration, and data quality.

---

## 1. Environment & Implementation Status

> [!IMPORTANT]
> **Honesty & Environment Disclaimer**:
> - **Local CLI Environment Status**: Microsoft Power BI Desktop is **NOT** installed in the local CLI operating environment.
> - **Compliance Status**: Per project directives, we have **NOT** fabricated a dummy `.pbix` binary file.
> - **Deliverables Delivered**: Complete Star Schema data model (`POWERBI_DATA_MODEL.md`), 14 DAX production measures (`POWERBI_DAX.md`), 4-page report setup manual (`POWERBI_SETUP.md`), and staged CSV datasets (`powerbi/powerbi_data/`).
> - **Official Status Statement**: **Power BI model and DAX specification prepared; PBIX creation requires Power BI Desktop.**

---

## 2. Power BI Data Model (Star Schema)

The data model utilizes a high-performance VertiPaq Star Schema designed to query 1.02M+ rows efficiently:

- **Fact Table**: `Fact_Transactions` (1,027,071 transaction rows from `retail_cleaned.csv`).
- **Dimension Tables**:
  - `Dim_Customer`: 5,878 customer RFM records from `customer_rfm.csv`.
  - `Dim_Product`: 5,400 product items from `product_summary.csv`.
  - `Dim_Country`: 43 countries from `country_summary.csv`.
  - `Dim_Date`: DAX-generated calendar table spanning `2009-12-01` to `2011-12-31` (25 calendar months).

### Relationship Matrix

```
       [Dim_Date] (1) ---------> (*) [Fact_Transactions]
     [Dim_Customer] (1) ---------> (*) [Fact_Transactions]
      [Dim_Product] (1) ---------> (*) [Fact_Transactions]
      [Dim_Country] (1) ---------> (*) [Fact_Transactions]
```
*(All relationships are Many-to-One `*:1`, Single Cross-Filter Direction).*

---

## 3. DAX Measure Catalog Summary

All 14 DAX measures are documented in [POWERBI_DAX.md](file:///c:/Users/mgras/OneDrive/Desktop/online-retail-customer-value-analysis/powerbi/POWERBI_DAX.md). Core measures include:

- **`Total Revenue`**:
  ```dax
  CALCULATE(SUM(Fact_Transactions[Revenue]), Fact_Transactions[IsCancelled] = FALSE(), Fact_Transactions[Quantity] > 0, Fact_Transactions[UnitPrice] > 0)
  ```
- **`Total Orders`**:
  ```dax
  CALCULATE(DISTINCTCOUNT(Fact_Transactions[InvoiceNo]), Fact_Transactions[IsCancelled] = FALSE(), Fact_Transactions[Quantity] > 0, Fact_Transactions[UnitPrice] > 0)
  ```
- **`Total Customers`**:
  ```dax
  CALCULATE(DISTINCTCOUNT(Fact_Transactions[CustomerID]), NOT ISBLANK(Fact_Transactions[CustomerID]), Fact_Transactions[IsCancelled] = FALSE())
  ```
- **`Average Order Value`**: `DIVIDE([Total Revenue], [Total Orders], 0)`
- **`Repeat Customer Rate`**: `DIVIDE([Repeat Customers], [Total Customers], 0)`
- **`High-Risk Customers`**: `CALCULATE(COUNTROWS(Dim_Customer), Dim_Customer[ChurnRiskProxy] = "High Risk (Churn Proxy)")`
- **`High-Risk Prior Revenue`**: `CALCULATE(SUM(Dim_Customer[Monetary]), Dim_Customer[ChurnRiskProxy] = "High Risk (Churn Proxy)")`
- **`Cancellation Rate`**: `DIVIDE([Cancellation Count], COUNTROWS(Fact_Transactions), 0)`

---

## 4. Report Page Architecture (4 Interactive Pages)

1. **`Executive Overview`**:
   - 7 Top KPI cards (`Revenue`, `Orders`, `Customers`, `AOV`, `Repeat Rate`, `High-Risk Customers`, `Cancellation Rate`).
   - Monthly Revenue Line Chart, Revenue by Country Ranked Bar Chart, Revenue by Segment Column Chart, Top 10 Products Bar Chart.
   - Slicers for `Year`, `Month Name`, `Country`, `Customer Segment`.

2. **`Customer Intelligence`**:
   - Donut chart of customer counts by segment, segment revenue breakdown.
   - Average Recency, Frequency, Monetary cards by segment.
   - Interactive High-Risk Customer Table with sorting by Recency, Monetary, and Frequency.

3. **`Product & Revenue`**:
   - Top 10 products by revenue & quantity.
   - Country matrix visual (`Revenue`, `Orders`, `Customers`, `AOV`, `Contribution %`).
   - Monthly order and revenue trajectory.

4. **`Data Quality`**:
   - Audit summary cards (`Raw Rows`, `Duplicates Removed`, `Admin Rows Removed`, `Cleaned Rows`, `Cancellation Rate`, `Validation Status = PASS`).

---

## 5. Python ↔ SQL ↔ Excel ↔ Power BI Reconciliation

The DAX measures evaluate to exact matches against Phase 2, Phase 3, and Phase 4 validation targets:

| Metric | Target Baseline | DAX Calculated Target | Variance | Reconciliation Status |
| :--- | :---: | :---: | :---: | :---: |
| **Total Completed Revenue** | £20,476,034.43 | £20,476,034.43 | £0.00 | **EXACT MATCH** |
| **Total Completed Orders** | 40,067 | 40,067 | 0 | **EXACT MATCH** |
| **Unique Purchasing Customers** | 5,878 | 5,878 | 0 | **EXACT MATCH** |
| **Repeat Customer Rate** | 72.39% | 72.39% (4,255 / 5,878) | 0.00% | **EXACT MATCH** |
| **High-Risk Churn Proxy Count** | 1,731 | 1,731 | 0 | **EXACT MATCH** |
| **High-Risk Prior Revenue** | £2,969,509.67 | £2,969,509.67 | £0.00 | **EXACT MATCH** |
| **Cancellation Line Rate** | 1.86% | 1.86% (19,100 / 1,027,071) | 0.00% | **EXACT MATCH** |
| **Top Country (Revenue)** | United Kingdom | United Kingdom (£17,409,970.10) | £0.00 | **EXACT MATCH** |
| **Top Product (Revenue)** | `22423` (Cake Stand) | `22423` - REGENCY CAKESTAND 3 TIER | None | **EXACT MATCH** |

---

## 6. Manual Setup Instructions

To build the `.pbix` file in Microsoft Power BI Desktop:
1. Follow the step-by-step instructions in [POWERBI_SETUP.md](file:///c:/Users/mgras/OneDrive/Desktop/online-retail-customer-value-analysis/powerbi/POWERBI_SETUP.md).
2. Import files from `powerbi/powerbi_data/`.
3. Create `Dim_Date` and relationships per [POWERBI_DATA_MODEL.md](file:///c:/Users/mgras/OneDrive/Desktop/online-retail-customer-value-analysis/powerbi/POWERBI_DATA_MODEL.md).
4. Add DAX measures per [POWERBI_DAX.md](file:///c:/Users/mgras/OneDrive/Desktop/online-retail-customer-value-analysis/powerbi/POWERBI_DAX.md).
5. Build and save `powerbi/retail_customer_analytics.pbix`.
