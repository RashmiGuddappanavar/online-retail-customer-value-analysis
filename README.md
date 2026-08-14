# Online Retail Customer Value & Revenue Analytics

![Python](https://img.shields.io/badge/Python-3.11-blue.svg)
![Flask](https://img.shields.io/badge/Flask-Live%20Dashboard-black.svg)
![MySQL](https://img.shields.io/badge/MySQL-8.0%20%2F%20Live%20Views-orange.svg)
![Excel](https://img.shields.io/badge/Excel-VBA%20Automated-green.svg)
![PowerBI](https://img.shields.io/badge/Power%20BI-Specification%20Prepared-yellow.svg)
![Tableau](https://img.shields.io/badge/Tableau-Specification%20Prepared-lightblue.svg)
![License](https://img.shields.io/badge/License-MIT-brightgreen.svg)

An enterprise multi-tool business intelligence and near-real-time local analytics platform analyzing 1.06M+ baseline transactions (£20.48M completed revenue) combined with a Python transaction simulator and MySQL analytical database layer.

---

## Executive Summary & Business Insights

Across 25 calendar months (December 2009 to December 2011), the retailer generated **£20,476,034.45** in completed baseline sales revenue across **40,067 completed orders** from **5,878 distinct purchasing customers**.

### Key Findings
1. **Repeat Customer Dependency**: Repeat buyers account for **72.39%** of the customer base (4,255 repeat buyers) and drive **£15.70M** (90.38%) of identified customer revenue.
2. **Geographic Concentration**: The United Kingdom generates **£17,409,970.10** (**85.03%** of baseline sales). Top European export markets include EIRE (£658.77K), Netherlands (£554.04K), Germany (£425.02K), and France (£350.46K).
3. **Commercial Churn Risk**: **1,731 customers** (29.45% of customer universe) are classified as **High Risk (Churn Proxy)** based on dormancy (>90 days inactive with >=2 prior orders), accounting for **£2,969,509.67** (17.09%) in past sales.
4. **Leading Products**: StockCode `22423` (**REGENCY CAKESTAND 3 TIER**) is the #1 merchandise product generating **£330,590.32** in completed revenue.
5. **Operational Quality Baseline**: Transaction line cancellations average **1.86%** (19,100 cancelled lines out of 1.027M clean rows).

---

## System Architecture

```
                                [Online Retail II Dataset]
                                            │
                                    (Python ETL Pipeline)
                                            │
                                 [Clean Data & RFM Files]
                                            │
   [Python Live Simulator] ────────> [MySQL / Live DB Engine] <────── (SQL Views: vw_realtime_kpis)
(is_simulated = 1 stream)          (fact_online_retail_transactions)             │
                                                    │                            │
                                ┌───────────────────┴────────────────────┬───────┴────────┐
                                ▼                                        ▼                ▼
                          [Flask Web API]                      [Excel + VBA Macro]  [Power BI & Tableau]
                        http://127.0.0.1:5000                   Refresh Macro      (Desktop Specifications)
                                │
                                ▼
                    [Browser Dashboard UI]
                   (3s JS Polling Refresh)
```

---

## Technical Stack & Implementation Status

| Technology | Actual Status | Technical Scope | Artifact Link |
| :--- | :---: | :--- | :--- |
| **Python** | **FULLY IMPLEMENTED** | Automated ETL, deduplication, RFM scoring, live ingestion simulator | [build_phase2_pipeline.py](file:///c:/Users/mgras/OneDrive/Desktop/online-retail-customer-value-analysis/python/build_phase2_pipeline.py) |
| **SQL / MySQL** | **FULLY IMPLEMENTED** | Database schema DDL, real-time views (`vw_realtime_kpis`), ingestion script | [setup_mysql.py](file:///c:/Users/mgras/OneDrive/Desktop/online-retail-customer-value-analysis/sql/setup_mysql.py) |
| **Flask / Web UI** | **FULLY IMPLEMENTED** | REST APIs (`/api/live-kpis`), interactive demo panel, 3s auto-refresh UI | [web/app.py](file:///c:/Users/mgras/OneDrive/Desktop/online-retail-customer-value-analysis/web/app.py) |
| **Excel & VBA** | **DESKTOP DEPENDENCY** | Executive management dashboard workbook, VBA live refresh macro module | [refresh_live_report.bas](file:///c:/Users/mgras/OneDrive/Desktop/online-retail-customer-value-analysis/excel/refresh_live_report.bas) |
| **Power BI** | **SPECIFICATION ONLY** | Star Schema data model design, 14 DAX production measures, setup guide | [POWERBI_SETUP.md](file:///c:/Users/mgras/OneDrive/Desktop/online-retail-customer-value-analysis/powerbi/POWERBI_SETUP.md) |
| **Tableau** | **SPECIFICATION ONLY** | Data model design, calculated fields catalog, Live Connection setup manual | [TABLEAU_SETUP.md](file:///c:/Users/mgras/OneDrive/Desktop/online-retail-customer-value-analysis/tableau/TABLEAU_SETUP.md) |

> [!NOTE]
> *Power BI and Tableau specifications are included; actual PBIX and TWBX file creation requires their respective desktop applications.*

---

## Quickstart & Local Execution Workflow

### 1. Single-Command Automated Windows Launch
Double-click **`run_project.bat`** or run in terminal:
```cmd
run_project.bat
```

### 2. Manual Terminal Commands
```bash
# Initialize database engine & real-time SQL views:
python sql/setup_mysql.py

# Launch Flask live web server:
python web/app.py

# Open browser: http://127.0.0.1:5000

# Ingest simulated live transactions:
python python/live_simulator.py --count 10

# Execute automated reconciliation test suite:
python tests/test_live_reconciliation.py
```

---

## Data Reconciliation Matrix

| Metric | Historical Baseline | Tested Local Live State (MySQL + Flask API) | Excel / BI Prepared Specification | Reconciliation Status |
| :--- | :---: | :---: | :---: | :---: |
| **Completed Revenue** | £20,476,034.45 | Dynamic Auto-Update (£20.48M Baseline + Live Stream) | DirectQuery / Live Spec Prepared | **TESTED & RECONCILED** |
| **Completed Orders** | 40,067 | Dynamic Auto-Update (40,067 Baseline + Live Orders) | DirectQuery / Live Spec Prepared | **TESTED & RECONCILED** |
| **Unique Customers** | 5,878 | 5,878 Identified Customers | Mapped Spec Prepared | **TESTED & RECONCILED** |
| **Repeat Customer Rate** | 72.39% | 72.39% (4,255 Repeat Buyers) | Mapped Spec Prepared | **TESTED & RECONCILED** |
| **High-Risk Churn Proxy** | 1,731 | 1,731 (£2.97M Prior Spend) | Mapped Spec Prepared | **TESTED & RECONCILED** |
| **Cancellation Line Rate** | 1.86% | Dynamic Auto-Update (19,100 Baseline Cancelled Lines) | DirectQuery / Live Spec Prepared | **TESTED & RECONCILED** |

---

## Project Documentation & Guides

- **[Demonstration Script (`FINAL_DEMO.md`)](file:///c:/Users/mgras/OneDrive/Desktop/online-retail-customer-value-analysis/FINAL_DEMO.md)**: 5–10 minute step-by-step presentation script.
- **[Interview Guide (`INTERVIEW_QA.md`)](file:///c:/Users/mgras/OneDrive/Desktop/online-retail-customer-value-analysis/INTERVIEW_QA.md)**: Technical Q&A covering Python, SQL, RFM, and Flask.
- **[Resume Bullets (`FINAL_RESUME_PROJECT.md`)](file:///c:/Users/mgras/OneDrive/Desktop/online-retail-customer-value-analysis/FINAL_RESUME_PROJECT.md)**: Resume bullet points for Data Analyst, Python Developer, and Full-Stack profiles.
- **[Technology Audit (`FINAL_TECHNOLOGY_STATUS.md`)](file:///c:/Users/mgras/OneDrive/Desktop/online-retail-customer-value-analysis/FINAL_TECHNOLOGY_STATUS.md)**: Technology audit matrix and status justifications.

---

## License

This project is licensed under the MIT License - see the [LICENSE](file:///c:/Users/mgras/OneDrive/Desktop/online-retail-customer-value-analysis/LICENSE) file for details.
