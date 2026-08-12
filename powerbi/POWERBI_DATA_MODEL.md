# Power BI Data Model Architecture & Schema Design

## 1. Data Model Overview

The Power BI data model for the Online Retail II project is structured as an analytical **Star Schema**. Designed for high-performance querying across 1.02M+ transaction rows, the model decouples transaction facts from descriptive dimension entities (`Customer`, `Product`, `Country`, `Date`).

---

## 2. Table Schemas & Source Mapping

### A. Fact Table: `Fact_Transactions`
- **Source File**: `powerbi_data/retail_cleaned.csv` (1,027,071 rows)
- **Role**: Primary transaction fact table containing line-item detail for completed and cancelled orders.

| Column Name | Power BI Data Type | Format / Constraints | Description |
| :--- | :--- | :--- | :--- |
| `InvoiceNo` | Text | `VARCHAR(20)` | Invoice identifier (starts with 'C' if cancelled) |
| `StockCode` | Text | `VARCHAR(20)` | Stock item code |
| `Description` | Text | `VARCHAR(255)` | Product item description |
| `Quantity` | Whole Number | `Int64` | Purchased or returned item quantity |
| `InvoiceDate` | Date/Time | `DateTime` | Transaction timestamp |
| `InvoiceDateKey` | Date | `Date` | Date key linked to `Dim_Date[Date]` |
| `UnitPrice` | Fixed Decimal | `£#,##0.00` | Unit price in GBP |
| `CustomerID` | Whole Number | `Int64` (Nullable) | Unique customer ID (blank for guest orders) |
| `Country` | Text | `VARCHAR(100)` | Destination country |
| `IsCancelled` | True/False | `Boolean` | Cancellation flag (`TRUE` = cancelled, `FALSE` = completed) |
| `Revenue` | Fixed Decimal | `£#,##0.00` | Line total (`Quantity * UnitPrice`) |

---

### B. Dimension Table: `Dim_Customer`
- **Source File**: `powerbi_data/customer_rfm.csv` (5,878 rows)
- **Role**: Customer dimension containing RFM metrics, segment classifications, and churn risk proxies.

| Column Name | Power BI Data Type | Primary Key | Description |
| :--- | :--- | :---: | :--- |
| `CustomerID` | Whole Number | **PK** | Unique customer identifier |
| `Recency` | Whole Number | No | Days since last completed purchase (ref: 2011-12-10) |
| `Frequency` | Whole Number | No | Total distinct completed order count |
| `Monetary` | Fixed Decimal | No | Total historical completed spend (£) |
| `R_Score` | Whole Number | No | Recency score (1 to 5) |
| `F_Score` | Whole Number | No | Frequency score (1 to 5) |
| `M_Score` | Whole Number | No | Monetary score (1 to 5) |
| `RFM_Score_Comb` | Whole Number | No | Combined score (R*100 + F*10 + M) |
| `CustomerSegment` | Text | No | Segment name (7 categories, e.g., Champions, At Risk Spenders) |
| `ChurnRiskProxy` | Text | No | Risk classification (High Risk, Medium Risk, Low Risk) |

---

### C. Dimension Table: `Dim_Product`
- **Source File**: `powerbi_data/product_summary.csv` (5,400 rows)
- **Role**: Product dimension containing stock codes, descriptions, and pre-aggregated performance stats.

| Column Name | Power BI Data Type | Primary Key | Description |
| :--- | :--- | :---: | :--- |
| `StockCode` | Text | **PK** | Unique product stock code |
| `Description` | Text | No | Master product description |
| `TotalQuantity` | Whole Number | No | Aggregate historical units sold |
| `TotalRevenue` | Fixed Decimal | No | Aggregate historical revenue (£) |
| `TotalOrders` | Whole Number | No | Aggregate order count |
| `AvgUnitPrice` | Fixed Decimal | No | Mean unit price (£) |

---

### D. Dimension Table: `Dim_Country`
- **Source File**: `powerbi_data/country_summary.csv` (43 rows)
- **Role**: Geographic dimension containing country market summaries.

| Column Name | Power BI Data Type | Primary Key | Description |
| :--- | :--- | :---: | :--- |
| `Country` | Text | **PK** | Country name |
| `TotalRevenue` | Fixed Decimal | No | Aggregate country revenue (£) |
| `TotalOrders` | Whole Number | No | Aggregate country order count |
| `TotalCustomers` | Whole Number | No | Distinct customer count |
| `AvgOrderValue` | Fixed Decimal | No | Average order value (£) |

---

### E. Dimension Table: `Dim_Date` (DAX Generated)
- **Generation Method**: DAX `CALENDAR(DATE(2009,12,1), DATE(2011,12,31))`
- **Role**: Dedicated Calendar table spanning 25 distinct calendar months (`2009-12` through `2011-12`).

| Column Name | Data Type | DAX Expression / Description |
| :--- | :--- | :--- |
| `Date` | Date | **PK** (`2009-12-01` to `2011-12-31`) |
| `Year` | Whole Number | `YEAR([Date])` |
| `Quarter` | Text | `"Q" & FORMAT([Date], "Q") & " " & YEAR([Date])` |
| `Month Number` | Whole Number | `MONTH([Date])` |
| `Month Name` | Text | `FORMAT([Date], "MMM")` |
| `Year-Month` | Text | `FORMAT([Date], "YYYY-MM")` |
| `Day of Week` | Text | `FORMAT([Date], "DDDD")` |

---

## 3. Relationship Matrix & Cardinality

All relationships are configured as **Single-Direction** cross-filtering to prevent ambiguity and ensure optimal VertiPaq engine performance:

```
           +--------------------+
           |     Dim_Date       |
           +--------------------+
                     | (1)
                     | 
                     | (*)
           +--------------------+
           |  Fact_Transactions |
           +--------------------+
            /        |        \
        (*) /        | (*)     \ (*)
           /         |          \
   +--------------+  +-------------+  +-------------+
   | Dim_Customer |  | Dim_Product |  | Dim_Country |
   +--------------+  +-------------+  +-------------+
         (1)               (1)              (1)
```

| From Table | From Column | To Table | To Column | Cardinality | Cross Filter Direction | Active |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: |
| `Fact_Transactions` | `CustomerID` | `Dim_Customer` | `CustomerID` | Many to One (`*:1`) | Single | Yes |
| `Fact_Transactions` | `StockCode` | `Dim_Product` | `StockCode` | Many to One (`*:1`) | Single | Yes |
| `Fact_Transactions` | `Country` | `Dim_Country` | `Country` | Many to One (`*:1`) | Single | Yes |
| `Fact_Transactions` | `InvoiceDateKey` | `Dim_Date` | `Date` | Many to One (`*:1`) | Single | Yes |

---

## 4. Performance & Data Model Best Practices

1. **Storage Mode**: All tables use **Import Mode** for maximum DAX calculation speed and full VertiPaq compression.
2. **Key Formatting**: Clean integer and string keys (`CustomerID`, `StockCode`, `Date`) prevent uncompressed object columns.
3. **No Bi-Directional Cross-Filtering**: Bi-directional relationships are avoided to eliminate circular dependency risks and unwanted measure evaluation contexts.
