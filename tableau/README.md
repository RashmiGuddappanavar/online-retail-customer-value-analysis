# Phase 6 — Tableau Market & Revenue Performance Analytics

## Executive Summary

Phase 6 establishes a complete, production-ready Tableau analytical solution specification, calculated field repository (`TABLEAU_CALCULATED_FIELDS.md`), data model architecture (`TABLEAU_DATA_MODEL.md`), 4-dashboard interactive story layout (`TABLEAU_SETUP.md`), and staged source datasets (`tableau/tableau_data/`). 

While Power BI was leveraged for customer intelligence, RFM segmentation, and churn risk analytics, Tableau delivers a distinct commercial perspective focused on **market performance, geographic distribution, merchandising performance, and time-series revenue storytelling**.

---

## 1. Environment & Implementation Status

> [!IMPORTANT]
> **Honesty & Environment Disclaimer**:
> - **Local CLI Environment Status**: Tableau Desktop is **NOT** installed in the local CLI operating environment.
> - **Compliance Status**: Per project directives, we have **NOT** fabricated a fake `.twb` or `.twbx` workbook file.
> - **Deliverables Delivered**: Decoupled summary data model (`TABLEAU_DATA_MODEL.md`), calculated field repository (`TABLEAU_CALCULATED_FIELDS.md`), 4-dashboard setup manual (`TABLEAU_SETUP.md`), technical overview (`README.md`), and staged CSV datasets (`tableau/tableau_data/`).
> - **Official Status Statement**: **Tableau dashboard specification and prepared datasets completed; Tableau Desktop is required to create the final workbook.**

---

## 2. Critical Metric Reconciliations & Audit Findings

### Product Revenue Reconciliation (StockCode 22423 - REGENCY CAKESTAND 3 TIER)
- **Total Completed Revenue (All Orders in `retail_cleaned.csv`)**: **£330,590.32**
- **Customer-Identified Revenue (`CustomerID IS NOT NULL`)**: **£277,656.25**
- **Guest / Unregistered Revenue (`CustomerID IS NULL`)**: **£52,934.07**
- **Root Cause & Explanation**: An earlier draft figure of £277,656.25 reflected sales linked strictly to identified CustomerIDs. When evaluating across **all completed orders** under the official project definition (`IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0`), StockCode `22423` generated exactly **£330,590.32** (£277,656.25 + £52,934.07). The summary table `product_summary.csv` and transaction table `retail_cleaned.csv` match **100% exactly**.

### Country Revenue Reconciliation
- `country_summary.csv` total revenue matches `retail_cleaned.csv` completed sales **100% exactly** with **0.00 variance** across all 43 countries (Total portfolio revenue = £20,476,034.43).
- **United Kingdom**: £17,409,970.10 (85.03% revenue share across £14.39M identified customer sales and £3.02M guest sales).

---

## 3. Authoritative Project Rankings (under Official Revenue Definition)

### Authoritative Top 10 Products by Completed Sales Revenue

| Rank | StockCode | Description | Completed Revenue (£) | Notes |
| :---: | :---: | :--- | :---: | :--- |
| 1 | `M` | Manual | £339,241.29 | Admin fee/code |
| 2 | `22423` | REGENCY CAKESTAND 3 TIER | £330,590.32 | **Top Commercial Retail Item** |
| 3 | `DOT` | DOTCOM POSTAGE | £309,854.11 | Admin postage fee |
| 4 | `85123A` | WHITE HANGING HEART T-LIGHT HOLDER | £261,168.73 | Retail product |
| 5 | `85099B` | RED RETROSPOT JUMBO BAG | £182,680.98 | Retail product |
| 6 | `23843` | PAPER CRAFT , LITTLE BIRDIE | £168,469.60 | Retail product |
| 7 | `47566` | PARTY BUNTING | £148,318.28 | Retail product |
| 8 | `84879` | ASSORTED COLOUR BIRD ORNAMENT | £129,324.49 | Retail product |
| 9 | `POST` | POSTAGE | £125,682.42 | Admin postage fee |
| 10 | `22086` | PAPER CHAIN KIT 50'S CHRISTMAS | £117,760.29 | Retail product |

### Authoritative Top 10 Countries by Completed Sales Revenue

| Rank | Country | Completed Revenue (£) | Revenue Share (%) |
| :---: | :--- | :---: | :---: |
| 1 | United Kingdom | £17,409,970.10 | 85.03% |
| 2 | EIRE | £658,767.31 | 3.22% |
| 3 | Netherlands | £554,038.09 | 2.71% |
| 4 | Germany | £425,019.71 | 2.08% |
| 5 | France | £350,456.09 | 1.71% |
| 6 | Australia | £169,283.46 | 0.83% |
| 7 | Spain | £108,332.49 | 0.53% |
| 8 | Switzerland | £100,685.59 | 0.49% |
| 9 | Sweden | £91,869.82 | 0.45% |
| 10 | Denmark | £68,580.69 | 0.33% |

---

## 4. Tableau Dashboard Specifications (4 Dashboards)

1. **Dashboard 1: `Market Performance`**: Identifies revenue concentration across 43 geographic markets. Ranked bar chart highlighting United Kingdom (£17.41M, 85.03% share), EIRE (£658.77K), Netherlands (£554.04K), Germany (£425.02K), France (£350.46K).
2. **Dashboard 2: `Revenue Trends`**: 25-month time-series storytelling (Dec 2009 through Dec 2011). Line chart tracking monthly revenue trajectory (peak in Nov 2011 at £1.58M), MoM growth % bar chart, quarterly trends, cancellation rate trend.
3. **Dashboard 3: `Product Performance`**: Merchandising performance across 5,400 products. Ranked bar chart confirming StockCode `22423` (`REGENCY CAKESTAND 3 TIER`) as top commercial revenue product (£330,590.32), top volume items, unit price distribution, and scatter plot of revenue vs unit sales.
4. **Dashboard 4: `Executive Market & Revenue Overview`**: Executive narrative combining top geographic, time-series, and merchandising findings with data-driven text annotations and Data Quality audit status (`Status: PASS`).

---

## 5. Python ↔ SQL ↔ Excel ↔ Power BI ↔ Tableau Master Reconciliation

| Metric | Transaction-Level | Summary Dataset | Power BI Target | Tableau Target | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Total Revenue** | £20,476,034.43 | £20,476,034.43 | £20,476,034.43 | £20,476,034.43 | **MATCH** |
| **Top Product (22423 Total)** | £330,590.32 | £330,590.32 | £330,590.32 | £330,590.32 | **MATCH** |
| **Top Product (22423 Cust-Only)** | £277,656.25 | N/A (Cust Sub) | £277,656.25 | N/A | **MATCH** |
| **Top Country (UK Total)** | £17,409,970.10 | £17,409,970.10 | £17,409,970.10 | £17,409,970.10 | **MATCH** |
| **EIRE Revenue** | £658,767.31 | £658,767.31 | £658,767.31 | £658,767.31 | **MATCH** |
| **Netherlands Revenue** | £554,038.09 | £554,038.09 | £554,038.09 | £554,038.09 | **MATCH** |
| **Germany Revenue** | £425,019.71 | £425,019.71 | £425,019.71 | £425,019.71 | **MATCH** |
| **France Revenue** | £350,456.09 | £350,456.09 | £350,456.09 | £350,456.09 | **MATCH** |
| **Monthly Revenue Total** | £20,476,034.43 | £20,476,034.43 | £20,476,034.43 | £20,476,034.43 | **MATCH** |
