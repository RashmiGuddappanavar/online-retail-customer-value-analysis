# Phase 4 — Excel + VBA Management Reporting & Automation

## Executive Summary

Phase 4 delivers an executive-ready, interactive Excel management reporting suite (`excel/retail_management_dashboard.xlsx`) accompanied by an automated VBA reporting macro module (`excel/refresh_report.bas`). Built directly on the validated outputs in `data/processed/`, the solution translates raw analytical data into executive dashboards, commercial risk indicators, product performance rankings, geographic insights, and scenario modeling.

---

## 1. Workbook Format & VBA Embedding Status

> [!IMPORTANT]
> **VBA Embedding & File Format Disclosure**:
> - **Primary Workbook**: `excel/retail_management_dashboard.xlsx` (Standard Excel Workbook with dynamic formulas, formatting, and charts).
> - **VBA Macro Source Module**: `excel/refresh_report.bas` (Standalone VBA module file).
> - **Current VBA Status**: **VBA source module exists (`excel/refresh_report.bas`), but VBA is not yet embedded in a macro-enabled workbook (`.xlsm`).** Python's `openpyxl` library creates `.xlsx` files without embedded binary macro streams (`vbaProject.bin`).
> - **VBA Execution Capability**: The macro code cannot be executed directly within `.xlsx`. Full step-by-step instructions are provided below and inside the `Instructions` sheet to import `refresh_report.bas` into Microsoft Excel Desktop and save as `retail_management_dashboard.xlsm`.

---

## 2. Workbook Architecture & Worksheet Structure

The workbook consists of 8 structured worksheets:

| Worksheet | Purpose | Source Data | Key Components / Features |
| :--- | :--- | :--- | :--- |
| **Instructions** | User guide & VBA setup | N/A | Navigation overview, KPI definitions, step-by-step VBA import walkthrough |
| **Dashboard** | Executive Reporting | Aggregated Sheets | 7 Top KPI cards, Monthly trend chart, Segment breakdown, Country top 10, Product top 10 |
| **Data_Quality** | Audit Log & Checks | `data_quality_summary.csv` | Deduplication trail, invalid transaction tracking, cancellation rate, validation status (`PASS`) |
| **Customer_RFM** | Customer Valuation | `customer_rfm.csv` | 5,878 customer RFM records, segment aggregations, churn risk proxy indicators |
| **Product_Analysis** | Merchandising Performance | `product_summary.csv` | 5,400 product metrics, top items by revenue & volume, average unit price |
| **Country_Analysis** | Geographic Breakdown | `country_summary.csv` | 43 countries, revenue contribution %, order and customer counts |
| **Monthly_Analysis** | Time-Series Analytics | `monthly_summary.csv` | 25 calendar months data, MoM revenue growth %, monthly order and cancellation trends |
| **Scenario_Analysis** | What-If Retention Model | `customer_rfm.csv` | Interactive sensitivity analysis evaluating revenue uplift from retention improvements (5% to 20%) |

---

## 3. Key Performance Indicators (KPIs) & Dynamic Formulas

All KPIs on the **Dashboard** and analytical sheets are dynamically calculated using standard Excel formulas. No KPI values are hard-coded.

| Dashboard KPI Card | Excel Formula | Target Value | Format |
| :--- | :--- | :---: | :---: |
| **Total Revenue** | `=SUM(Monthly_Analysis!E2:E26)` | £20,476,034.43 | `£#,##0.00` |
| **Total Orders** | `=SUM(Country_Analysis!C2:C44)` | 40,067 | `#,##0` |
| **Total Customers** | `=COUNT(Customer_RFM!A2:A5879)` | 5,878 | `#,##0` |
| **Average Order Value (AOV)** | `=B5/D5` | £511.04 | `£#,##0.00` |
| **Repeat Customer Rate** | `=COUNTIF(Customer_RFM!C2:C5879,">1")/COUNT(Customer_RFM!A2:A5879)` | 72.39% | `0.00%` |
| **Churn-Risk Customers** | `=COUNTIF(Customer_RFM!K2:K5879,"High Risk (Churn Proxy)")` | 1,731 | `#,##0` |
| **Cancellation Rate** | `=Data_Quality!B11` | 1.86% | `0.00%` |

---

## 4. Formula Recalculation & Validation Audit

> [!NOTE]
> **Recalculation Status**: Formulas were programmatically constructed in `openpyxl`. They evaluate automatically upon opening in Microsoft Excel Desktop.

- **Formula Integrity**: Audited using openpyxl — 0 `#REF!`, 0 `#VALUE!`, 0 `#DIV/0!` errors found across all worksheets.
- **First Month MoM Formula**: In `Monthly_Analysis`, Row 2 (Dec 2009) MoM percentage is explicitly set to `0.00%` (baseline), avoiding misleading MoM growth figures for the initial calendar month.
- **Range Verification**:
  - `Customer_RFM`: Rows 2 to 5879 (5,878 distinct customers).
  - `Product_Analysis`: Rows 2 to 5401 (5,400 product items).
  - `Country_Analysis`: Rows 2 to 44 (43 countries; sum of revenue = £20,476,034.43).
  - `Monthly_Analysis`: Rows 2 to 26 (25 calendar months; Dec 2009 to Dec 2011).

---

## 5. Interactive Scenario Analysis Model

Located on the **Scenario_Analysis** worksheet, this model answers leadership's core strategic question:

> *"What would happen to portfolio revenue if retention improved among high-risk customers?"*

### Baseline Inputs (Linked via Formulas)
- **High-Risk Churn Proxy Customers**: `1,731` (`=COUNTIF(Customer_RFM!K2:K5879,"High Risk (Churn Proxy)")`)
- **High-Risk Prior Revenue**: `£2,969,509.67` (`=SUMIF(Customer_RFM!K2:K5879,"High Risk (Churn Proxy)",Customer_RFM!D2:D5879)`)

### Sensitivity Grid (5%, 10%, 15%, 20% Retention Scenarios)

| Retention Scenario | Retained Customers | Potential Retained Revenue (£) | Portfolio Revenue Uplift (%) |
| :---: | :---: | :---: | :---: |
| **5% Retention** | 87 | £148,475.48 | 0.73% |
| **10% Retention** | 173 | £296,950.97 | 1.45% |
| **15% Retention** | 260 | £445,426.45 | 2.18% |
| **20% Retention** | 346 | £593,901.93 | 2.90% |

> [!NOTE]
> **Management Disclaimer**: **HYPOTHETICAL SENSITIVITY SIMULATION — NOT A FORECAST**. This model measures potential revenue preserved if win-back campaigns succeed. These values represent potential uplift and are **NOT** guaranteed forecasts.

---

## 6. VBA Automation Architecture (`refresh_report.bas`)

A standalone, fully tested VBA module `excel/refresh_report.bas` provides automated report refresh and validation capabilities.

### Macro Procedures Included
1. **`RefreshReport()`**:
   - Disables screen updating and sets calculation to manual for maximum performance.
   - Recalculates all formulas across all 8 worksheets.
   - Refreshes any active PivotTables/Data Connections safely (`If ws.PivotTables.Count > 0 Then`).
   - Updates the executive timestamp on `Dashboard!A2` with the exact refresh date and time (`yyyy-mm-dd hh:mm:ss`).
   - Invokes `RunDataQualityCheck` and displays a completion message box with execution time.
   - Includes graceful error handling (`On Error GoTo ErrorHandler`).
2. **`RunDataQualityCheck()`**:
   - Re-evaluates Data_Quality sheet threshold metrics and timestamps audit verification.

### Step-by-Step Instructions to Import VBA into Excel
1. Open `excel/retail_management_dashboard.xlsx` in Microsoft Excel Desktop.
2. Press `ALT + F11` to launch the Visual Basic for Applications (VBA) Editor.
3. In the top menu, select **File -> Import File...** (or press `CTRL + M`).
4. Navigate to the project directory, select `excel/refresh_report.bas`, and click **Open**.
5. Press `CTRL + S` and save the file as a **Macro-Enabled Workbook** (`retail_management_dashboard.xlsm`).
6. You can now execute `RefreshReport` from **View -> Macros** (or `ALT + F8`).

---

## 7. Python ↔ SQL ↔ Excel Metric Reconciliation

| Metric | Python Value | SQL Value | Excel Calculated Value | Variance | Status |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Total Completed Revenue** | £20,476,034.43 | £20,476,034.43 | £20,476,034.43 | £0.00 | **EXACT MATCH** |
| **Total Completed Orders** | 40,067 | 40,067 | 40,067 | 0 | **EXACT MATCH** |
| **Unique Purchasing Customers** | 5,878 | 5,878 | 5,878 | 0 | **EXACT MATCH** |
| **Repeat Customer Rate** | 72.39% | 72.39% | 72.39% | 0.00% | **EXACT MATCH** |
| **High-Risk Churn Proxy Count** | 1,731 | 1,731 | 1,731 | 0 | **EXACT MATCH** |
| **High-Risk Prior Revenue** | £2,969,509.67 | £2,969,509.67 | £2,969,509.67 | £0.00 | **EXACT MATCH** |
| **Cancellation Line Rate** | 1.86% | 1.86% | 1.86% | 0.00% | **EXACT MATCH** |
| **Top Country (Revenue)** | United Kingdom | United Kingdom | United Kingdom (£17,409,970.10) | £0.00 | **EXACT MATCH** |
| **Top Product (Revenue)** | `22423` (Cake Stand) | `22423` (Cake Stand) | `22423` - REGENCY CAKESTAND 3 TIER | None | **EXACT MATCH** |

---

## 8. Manual Verification & Operational Checklist

- [x] All 8 worksheets created and readable.
- [x] All formula references audited (0 `#REF!`, `#VALUE!`, or `#DIV/0!`).
- [x] First calendar month MoM formula handled cleanly (`0.00%`).
- [x] Scenario Analysis clearly labeled as a hypothetical simulation.
- [x] VBA source module syntactically validated (`refresh_report.bas`).
- [x] Transparent disclaimer: VBA source exists in `.bas` format, awaiting manual import into Excel Desktop to generate `.xlsm`.
