# Power BI Desktop Report Construction & Setup Manual

## Overview

This guide provides step-by-step instructions for constructing the interactive Power BI report (`retail_customer_analytics.pbix`) in Microsoft Power BI Desktop using the staged datasets in `powerbi/powerbi_data/` and the DAX specifications in `POWERBI_DAX.md`.

---

## Step 1: Source Data Import (Power Query)

1. Launch **Microsoft Power BI Desktop**.
2. Click **Get Data -> Text/CSV** and import each dataset from `powerbi/powerbi_data/`:
   - `retail_cleaned.csv` $\rightarrow$ Rename query to `Fact_Transactions`
   - `customer_rfm.csv` $\rightarrow$ Rename query to `Dim_Customer`
   - `product_summary.csv` $\rightarrow$ Rename query to `Dim_Product`
   - `country_summary.csv` $\rightarrow$ Rename query to `Dim_Country`
   - `data_quality_summary.csv` $\rightarrow$ Rename query to `Data_Quality_Summary`
3. Verify data types in **Power Query Editor**:
   - `Fact_Transactions[Revenue]`, `UnitPrice` $\rightarrow$ Fixed Decimal Number (`Currency`)
   - `Fact_Transactions[Quantity]`, `CustomerID` $\rightarrow$ Whole Number
   - `Fact_Transactions[InvoiceDate]` $\rightarrow$ Date/Time
   - `Fact_Transactions[IsCancelled]` $\rightarrow$ True/False (`Boolean`)
   - `Dim_Customer[Monetary]` $\rightarrow$ Fixed Decimal Number (`Currency`)
4. Click **Close & Apply**.

---

## Step 2: Date Table Creation (DAX)

1. Navigate to the **Data View** in Power BI Desktop.
2. Click **New Table** and paste the following DAX expression:
   ```dax
   Dim_Date = 
   ADDCOLUMNS(
       CALENDAR(DATE(2009, 12, 1), DATE(2011, 12, 31)),
       "Year", YEAR([Date]),
       "Quarter", "Q" & FORMAT([Date], "Q") & " " & YEAR([Date]),
       "Month Number", MONTH([Date]),
       "Month Name", FORMAT([Date], "MMM"),
       "Year-Month", FORMAT([Date], "YYYY-MM"),
       "Day of Week", FORMAT([Date], "DDDD")
   )
   ```
3. Mark `Dim_Date` as a Date Table (Right-click `Dim_Date` $\rightarrow$ **Mark as date table** $\rightarrow$ Select `Date` column).
4. Add a calculated column in `Fact_Transactions` for date linking:
   ```dax
   InvoiceDateKey = DATEVALUE(Fact_Transactions[InvoiceDate])
   ```

---

## Step 3: Establish Model Relationships

Navigate to **Model View** and set up the following relationships:

1. `Fact_Transactions[CustomerID]` $\rightarrow$ `Dim_Customer[CustomerID]` (Cardinality: `*:1`, Single)
2. `Fact_Transactions[StockCode]` $\rightarrow$ `Dim_Product[StockCode]` (Cardinality: `*:1`, Single)
3. `Fact_Transactions[Country]` $\rightarrow$ `Dim_Country[Country]` (Cardinality: `*:1`, Single)
4. `Fact_Transactions[InvoiceDateKey]` $\rightarrow$ `Dim_Date[Date]` (Cardinality: `*:1`, Single)

---

## Step 4: Create Measures Table & DAX Measures

1. Click **Enter Data**, name the empty table `_Measures`, and click Load.
2. Create all 14 DAX measures specified in [POWERBI_DAX.md](file:///c:/Users/mgras/OneDrive/Desktop/online-retail-customer-value-analysis/powerbi/POWERBI_DAX.md).
3. Hide the empty column in `_Measures` so it displays a measure folder icon.

---

## Step 5: Construct Dashboard Pages

### Page 1: `Executive Overview`
- **Page Layout**: Canvas 16:9, Background: Light Slate (`#F8F9FA`).
- **Header**: Banner titled *"Online Retail II — Executive Management Overview"*.
- **Top KPI Cards Row**:
  1. `Total Revenue` (£20.48M)
  2. `Total Orders` (40.07K)
  3. `Total Customers` (5,878)
  4. `Average Order Value` (£511.04)
  5. `Repeat Customer Rate` (72.39%)
  6. `High-Risk Customers` (1,731)
  7. `Cancellation Rate` (1.86%)
- **Visual 1 (Line Chart)**: `Monthly Revenue Trend` (`Dim_Date[Year-Month]` on X-Axis, `[Total Revenue]` on Y-Axis).
- **Visual 2 (Ranked Bar Chart)**: `Revenue by Country` (`Dim_Country[Country]` on Y-Axis, `[Total Revenue]` on X-Axis, top 10).
- **Visual 3 (Column Chart)**: `Revenue by Customer Segment` (`Dim_Customer[CustomerSegment]` on X-Axis, `[Total Revenue]` on Y-Axis).
- **Visual 4 (Bar Chart)**: `Top 10 Products by Revenue` (`Dim_Product[Description]` on Y-Axis, `[Total Revenue]` on X-Axis).
- **Slicers Panel**: Slicers for `Dim_Date[Year]`, `Dim_Date[Month Name]`, `Dim_Country[Country]`, `Dim_Customer[CustomerSegment]`.

---

### Page 2: `Customer Intelligence`
- **Visual 1 (Donut Chart)**: `Customer Count by Segment` (`Dim_Customer[CustomerSegment]`).
- **Visual 2 (Clustered Column Chart)**: `Revenue & Customer Count by Segment`.
- **Visual 3 (Card Cluster)**: Average Recency, Frequency, and Monetary Value by segment.
- **Visual 4 (Risk Matrix Table)**: High-Risk Customer Action Table:
  - Columns: `CustomerID`, `Recency`, `Frequency`, `Monetary`, `CustomerSegment`, `ChurnRiskProxy`
  - Filter: `Dim_Customer[ChurnRiskProxy] = "High Risk (Churn Proxy)"`
  - Sort Enabled: By Recency (descending), Monetary (descending), Frequency (descending).

---

### Page 3: `Product & Revenue`
- **Visual 1 (Bar Chart)**: `Top 10 Products by Revenue`.
- **Visual 2 (Bar Chart)**: `Top 10 Products by Volume (Quantity)`.
- **Visual 3 (Matrix Visual)**: Country Revenue & Order Breakdown:
  - Rows: `Dim_Country[Country]`
  - Values: `[Total Revenue]`, `[Total Orders]`, `[Total Customers]`, `[Average Order Value]`, `[Revenue Contribution %]`
- **Visual 4 (Combo Chart)**: Monthly Revenue & Order Volume Trajectory.

---

### Page 4: `Data Quality`
- **Summary Cards**:
  - `Raw Rows` (1,067,371)
  - `Duplicates Removed` (34,335)
  - `Admin Rows Removed` (5,965)
  - `Cleaned Rows` (1,027,071)
  - `Cancellation Line Rate` (1.86%)
  - `Validation Status` (**PASS**)
- **Data Audit Table**: Displaying validation metrics from `Data_Quality_Summary`.

---

## Step 6: Save Report

Save the completed project as `powerbi/retail_customer_analytics.pbix`.
