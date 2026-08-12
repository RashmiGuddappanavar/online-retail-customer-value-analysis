# Tableau Data Model Architecture & Dataset Grain Specification

## 1. Data Model Strategy Overview

Unlike traditional single-fact data models, Tableau excels when visualizations are powered by datasets tailored to their specific analytical grain. For the Online Retail II project, the Tableau architecture uses a **Decoupled Summary Model** supplemented by a granular transaction table.

By powering high-level executive dashboards (`Market Performance`, `Revenue Trends`, `Product Performance`) with pre-aggregated summary datasets (`country_summary`, `monthly_summary`, `product_summary`), Tableau workbook rendering is instantaneous while avoiding row-multiplication joins across 1M+ rows.

---

## 2. Dataset Grain & Schema Specifications

### A. Country Market Summary (`country_summary.csv`)
- **Grain**: 1 record per Geographic Country (43 rows).
- **Primary Key**: `Country`
- **Used For**: `Dashboard 1: Market Performance` (Country revenue ranking, order count, customer count, AOV, revenue contribution %).

| Field Name | Tableau Data Type | Role | Description |
| :--- | :--- | :--- | :--- |
| `Country` | Geographic (Country/Region) | Dimension | Country name |
| `TotalRevenue` | Number (Decimal) | Measure | Completed sales revenue (£) |
| `TotalOrders` | Number (Whole) | Measure | Distinct completed order count |
| `TotalCustomers` | Number (Whole) | Measure | Distinct customer count |
| `AvgOrderValue` | Number (Decimal) | Measure | Average order value (`TotalRevenue / TotalOrders`) |

---

### B. Monthly Time-Series Summary (`monthly_summary.csv`)
- **Grain**: 1 record per Calendar YearMonth (25 rows).
- **Primary Key**: `YearMonth`
- **Timeline**: December 2009 through December 2011 (25 distinct calendar months).
- **Used For**: `Dashboard 2: Revenue Trends` (Monthly revenue trajectory, order volume, cancellation rates, MoM growth).

| Field Name | Tableau Data Type | Role | Description |
| :--- | :--- | :--- | :--- |
| `YearMonth` | String / Date (`YYYY-MM`) | Dimension | Calendar year-month identifier |
| `Year` | Number (Whole) | Dimension | Calendar year (2009, 2010, 2011) |
| `Month` | Number (Whole) | Dimension | Calendar month number (1 to 12) |
| `MonthName` | String | Dimension | Month abbreviation (Jan, Feb, etc.) |
| `TotalRevenue` | Number (Decimal) | Measure | Monthly completed revenue (£) |
| `TotalOrders` | Number (Whole) | Measure | Monthly distinct order count |
| `TotalCustomers` | Number (Whole) | Measure | Monthly active purchasing customers |
| `CancellationCount` | Number (Whole) | Measure | Monthly cancelled transaction line count |
| `CancellationRate` | Number (Decimal) | Measure | Monthly cancellation line rate |

---

### C. Product Summary (`product_summary.csv`)
- **Grain**: 1 record per Product Stock Code (5,400 rows).
- **Primary Key**: `StockCode`
- **Used For**: `Dashboard 3: Product Performance` (Top 10 products by revenue, volume, and orders, average price analysis).

| Field Name | Tableau Data Type | Role | Description |
| :--- | :--- | :--- | :--- |
| `StockCode` | String | Dimension | Stock item identifier |
| `Description` | String | Dimension | Product description |
| `TotalQuantity` | Number (Whole) | Measure | Total completed units sold |
| `TotalRevenue` | Number (Decimal) | Measure | Total completed revenue (£) |
| `TotalOrders` | Number (Whole) | Measure | Total completed orders containing item |
| `AvgUnitPrice` | Number (Decimal) | Measure | Average unit price (£) |

---

### D. Cleaned Transaction Detail (`retail_cleaned.csv`)
- **Grain**: 1 record per transaction line item (1,027,071 rows).
- **Primary Key**: Composite `(InvoiceNo, StockCode, InvoiceDate)`
- **Used For**: Deep line-item inspection, cross-filtering, and granular customer/product analysis.

| Field Name | Tableau Data Type | Role | Description |
| :--- | :--- | :--- | :--- |
| `InvoiceNo` | String | Dimension | Invoice identifier |
| `StockCode` | String | Dimension | Stock item code |
| `Description` | String | Dimension | Product description |
| `Quantity` | Number (Whole) | Measure | Item quantity |
| `InvoiceDate` | Date & Time | Dimension | Timestamp |
| `UnitPrice` | Number (Decimal) | Measure | Unit price (£) |
| `CustomerID` | Number (Whole) | Dimension | Customer ID |
| `Country` | Geographic (Country/Region) | Dimension | Destination country |
| `IsCancelled` | Boolean | Dimension | Cancellation flag (`TRUE`/`FALSE`) |
| `Revenue` | Number (Decimal) | Measure | Line revenue (`Quantity * UnitPrice`) |

---

## 3. Data Relationships & Data Blending Guidelines

When building multi-entity views using `retail_cleaned.csv` as a primary data source in Tableau Data Source Manager:

```
[retail_cleaned] (1,027,071 rows)
    |-- Left Join on CustomerID --> [customer_rfm] (5,878 rows)
    |-- Left Join on StockCode  --> [product_summary] (5,400 rows)
```

> [!TIP]
> **Performance Recommendation**: For Dashboards 1, 2, and 3, use the dedicated summary CSVs (`country_summary.csv`, `monthly_summary.csv`, `product_summary.csv`) as standalone Data Sources. This completely avoids joins and maximizes Tableau rendering speed.
