# Technical Interview Q&A Guide

Comprehensive technical questions and answers for interviewing with this project repository.

---

## 1. Python & Data Pipeline

### Q: Why did you use Pandas for data cleaning instead of doing it in SQL?
**A**: Raw transaction data arrived in a multi-sheet Excel file (`online_retail_II.xlsx`). Python (`pandas`, `openpyxl`, `calamine`) allowed programmatically merging sheets, standardizing column names, executing exact row deduplication across 1.06M rows, and applying complex quantile binning for RFM scoring before writing clean files to disk.

### Q: How did you handle duplicate rows and administrative test codes?
**A**: 
1. **Exact Duplicates**: Used `df.drop_duplicates()`, removing 34,335 identical transaction lines.
2. **Bad Debt / Write-offs**: Filtered out rows where `UnitPrice < 0` (5 rows).
3. **Test Codes**: Filtered out StockCodes starting with `TEST` (17 rows).
4. **Zero-price without Customer ID**: Purged 5,944 inventory audit lines lacking customer identifiers.

### Q: How is RFM calculated in Python?
**A**:
- **Reference Date**: `2011-12-10 12:50:00` (Max invoice timestamp + 1 day).
- **Recency**: Days inactive relative to reference date (`(ReferenceDate - MaxInvoiceDate).dt.days`).
- **Frequency**: Distinct completed invoice count per customer (`COUNTD(InvoiceNo)`).
- **Monetary**: Sum of completed line items (`Quantity * UnitPrice` where `IsCancelled = False`).
- **Quantile Scoring**: Applied `pd.qcut` into 5 quantiles (`R_Score`, `F_Score`, `M_Score`) mapping customers into 7 segments (`Champions`, `Loyal Customers`, `At Risk Spenders`, etc.).

---

## 2. SQL & Database Modeling

### Q: What complex SQL features did you utilize?
**A**: 
- **Real-Time Analytical Views (`vw_realtime_kpis`)**: Uses conditional aggregation (`COUNT(CASE WHEN...)`, `SUM(CASE WHEN...)`) to calculate revenue, completed order counts, and cancellation rates dynamically across historical (`is_simulated = 0`) and live transactions (`is_simulated = 1`).
- **CTEs and Window Functions**: Applied `ROW_NUMBER() OVER (PARTITION BY CustomerID ORDER BY InvoiceDate)` to isolate first vs repeat customer order behavior.

### Q: How did you index the MySQL database for query performance?
**A**: Created composite indexes on `(IsCancelled, Quantity, UnitPrice)` and `(InvoiceDate)` on table `fact_online_retail_transactions`, enabling fast scanning for completed sales filtering (`IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0`).

---

## 3. Analytics & Churn Risk Definition

### Q: How did you define Churn Risk when retail datasets lack explicit cancellation buttons?
**A**: Defined a **Churn Risk Proxy** rule engine based on inactivity thresholds and order history:
- **High Risk (Churn Proxy)**: Recency > 90 days AND Frequency >= 2 orders (1,731 customers representing £2.97M past spend).
- **Medium Risk (One-time Inactive)**: Recency > 90 days AND Frequency = 1 order (1,258 customers).
- **Low Risk (Active)**: Recency <= 60 days (2,396 customers).

---

## 4. Flask & Real-Time Architecture

### Q: Why is this platform described as "near-real-time"?
**A**: The transaction simulator generates simulated orders/cancellations and writes them to the database engine. The Flask application exposes REST API endpoints (`/api/live-kpis`) that query database views, while JavaScript timers poll the API every 3 seconds to update the browser UI without full page reloads.

### Q: How does Flask handle database connection failures?
**A**: `get_live_kpis()` wraps database calls in a `try/except` block. If MySQL drops or credentials are missing, the server logs the event and falls back to pre-aggregated summary CSV files (`monthly_summary.csv`, `customer_rfm.csv`) so the UI displays fallback baseline data rather than crashing.

---

## 5. Desktop BI Tooling (Power BI & Tableau)

### Q: Why are Power BI and Tableau marked as "Specification Only"?
**A**: I authored the complete Star Schema data models, DAX measure catalog (14 production measures), calculated fields, and setup guides. However, because Power BI Desktop and Tableau Desktop applications were unavailable in the execution environment, I adhered to strict engineering honesty and marked them as prepared specifications requiring Desktop software for `.pbix`/`.twbx` binary creation.
