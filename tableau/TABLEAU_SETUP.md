# Tableau Desktop Dashboard Construction & Setup Manual

## Overview

This guide provides step-by-step instructions for building the interactive Tableau workbook (`retail_market_revenue_analytics.twbx`) in Tableau Desktop using the staged datasets in `tableau/tableau_data/` and calculated field specifications in `TABLEAU_CALCULATED_FIELDS.md`.

---

## Step 1: Connect to Source Datasets

1. Launch **Tableau Desktop**.
2. Under **Connect -> To a File**, select **Text File** and connect to each dataset in `tableau/tableau_data/`:
   - `country_summary.csv` $\rightarrow$ Name data source `Country Summary`
   - `monthly_summary.csv` $\rightarrow$ Name data source `Monthly Summary`
   - `product_summary.csv` $\rightarrow$ Name data source `Product Summary`
   - `retail_cleaned.csv` $\rightarrow$ Name data source `Transaction Detail`
   - `data_quality_summary.csv` $\rightarrow$ Name data source `Data Quality`
3. Verify data types:
   - `Country Summary` $\rightarrow$ Change `Country` field role to **Geographic Role -> Country/Region**.

---

## Step 2: Build Worksheets & Calculated Fields

For each data source, add the calculated fields specified in [TABLEAU_CALCULATED_FIELDS.md](file:///c:/Users/mgras/OneDrive/Desktop/online-retail-customer-value-analysis/tableau/TABLEAU_CALCULATED_FIELDS.md).

---

## Step 3: Construct Dashboard 1 — "Market Performance"

- **Objective**: Identify country revenue concentration, orders, customers, AOV, and market contribution %.
- **Source Data**: `Country Summary`
- **Worksheets to Build**:
  1. `KPI Summary`: 4 BANs (Big Angry Numbers) for `Total Revenue` (£20.48M), `Total Orders` (40.07K), `Total Customers` (5,878), `AOV` (£511.04).
  2. `Revenue by Country Bar Chart`: Horizontal ranked bar chart (`Country` on Rows, `TotalRevenue` on Columns, sorted descending). Highlight United Kingdom bar in Navy (`#1F497D`).
  3. `Revenue Contribution %`: Pareto / Percentage bar (`Revenue Contribution %` formula).
  4. `Orders & Customers by Country`: Dual-axis or side-by-side bar chart showing `TotalOrders` and `TotalCustomers`.
  5. `AOV by Country`: Ranked horizontal bar chart displaying average order value per country.
- **Dashboard Assembly**:
  - Size: Fixed Desktop (1366 x 768).
  - Title: *"Market Performance & Geographic Concentration Analysis"*.
  - Add `Country` quick filter (Single Value Dropdown or Multiple Values List).

---

## Step 4: Construct Dashboard 2 — "Revenue Trends"

- **Objective**: Analyze time-series performance across the 25 calendar months (Dec 2009 to Dec 2011).
- **Source Data**: `Monthly Summary`
- **Worksheets to Build**:
  1. `Monthly Revenue Trajectory`: Line chart (`YearMonth` on Columns, `TotalRevenue` on Rows). Add trend line and peak annotation (Nov 2011 peak at £1.58M).
  2. `Monthly Orders Trajectory`: Line chart (`YearMonth` on Columns, `TotalOrders` on Rows).
  3. `Monthly Active Customers`: Area chart (`YearMonth` on Columns, `TotalCustomers` on Rows).
  4. `MoM Revenue Growth %`: Bar chart (`MoM Revenue Growth %` formula on Rows, `YearMonth` on Columns). Color red for negative growth, blue for positive. Baseline month Dec 2009 set to 0%.
  5. `Cancellation Rate Trend`: Line chart (`CancellationRate` on Rows, `YearMonth` on Columns).
- **Dashboard Assembly**:
  - Title: *"Time-Series Revenue Trajectory & MoM Growth Dynamics (25 Calendar Months)"*.
  - Add `Year` and `Quarter` interactive filters.

---

## Step 5: Construct Dashboard 3 — "Product Performance"

- **Objective**: Identify top revenue-generating items, unit sales volume, price distribution, and basket penetration.
- **Source Data**: `Product Summary`
- **Worksheets to Build**:
  1. `Top 10 Products by Revenue`: Horizontal bar chart (`Description` on Rows, `TotalRevenue` on Columns, sorted top 10). Confirms StockCode `22423` - `REGENCY CAKESTAND 3 TIER` as top product (£277,656.25).
  2. `Top 10 Products by Quantity`: Horizontal bar chart (`Description` on Rows, `TotalQuantity` on Columns, sorted top 10).
  3. `Top 10 Products by Order Count`: Horizontal bar chart (`Description` on Rows, `TotalOrders` on Columns, sorted top 10).
  4. `Product Revenue vs Volume Scatter`: Scatter plot (`TotalQuantity` on X-Axis, `TotalRevenue` on Y-Axis, `StockCode` on Detail).
- **Dashboard Assembly**:
  - Title: *"Merchandising Performance & Product Valuation"*.
  - Add Top N parameter control (Top 5, 10, 20).

---

## Step 6: Construct Dashboard 4 — "Executive Market & Revenue Overview"

- **Objective**: Executive narrative combining key findings across markets, time trends, products, and data quality.
- **Worksheets Combined**:
  - KPI BAN Cards
  - Monthly Revenue Line Chart
  - Top 5 Countries Ranked Bar
  - Top 5 Products Ranked Bar
  - Data Quality Audit Panel (`Raw Rows: 1.07M`, `Cleaned Rows: 1.03M`, `Cancellation Rate: 1.86%`, `Status: PASS`).
- **Data-Driven Annotations**:
  - *"United Kingdom generates £17.41M (85.03%) of completed sales revenue."*
  - *"Peak commercial volume achieved in November 2011 (£1.58M revenue, 3,472 orders)."*
  - *"StockCode 22423 (REGENCY CAKESTAND 3 TIER) is the leading revenue driver at £277,656.25."*

---

## Step 7: Save Tableau Workbook

Save the packaged workbook as `tableau/retail_market_revenue_analytics.twbx`.
