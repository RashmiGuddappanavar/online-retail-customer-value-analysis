# Interview Walkthrough & Architectural Defense Guide

This guide prepares you to present and defend the **Online Retail Customer Value & Revenue Analytics** project during technical interviews.

---

## 1. Project Pitch / Elevators

### 30-Second Explanation
> "I built an enterprise multi-tool customer value analytics platform analyzing 1.06 million retail transactions generating £20.48 million in completed revenue. I engineered a Python data pipeline with RFM customer segmentation, an automated live transaction ingestion engine, MySQL database views, and a local Flask browser dashboard featuring dynamic 3-second auto-refresh."

### 1-Minute Explanation
> "This project addresses customer retention and revenue analytics for a major UK online retailer across 25 months of sales data. Using Python, I cleaned 1.06M transaction lines down to 1.027M, purged 34K exact duplicates, and built an RFM model segmenting 5,878 customers. To model real-world business intelligence, I implemented a live transaction simulator in Python that streams simulated orders into a MySQL analytical database. I then built dynamic SQL views and a responsive Flask web application that updates KPIs in near-real-time every 3 seconds while maintaining exact reconciliation across Excel, Power BI DirectQuery, and Tableau specifications."

### 2-Minute Technical Explanation
> "Architecturally, the project operates in two tiers: historical baseline ETL and near-real-time live analytics. First, the Python pipeline (`pandas`, `numpy`) combined two raw Excel sheets, executed exact deduplication, filtered non-commercial administrative lines, and derived quantile RFM scores (`R_Score`, `F_Score`, `M_Score`) mapping customers into 7 segments. Because retail datasets lack explicit churn labels, I built a business logic rule engine classifying dormant repeat buyers as 'Churn Risk Proxy' (>90 days inactive with 2+ orders), identifying £2.97M in at-risk revenue.
> 
> Second, I designed a unified relational database schema in MySQL with real-time views (`vw_realtime_kpis`) calculating revenue, orders, and cancellation rates. I created a Python live ingestion simulator that writes new transactions with `is_simulated = 1` into MySQL. On the presentation layer, I built a dark-mode Flask web app exposing REST API endpoints consumed by Chart.js and JavaScript polling timers to reflect live database state without full page reloads. The entire platform is backed by automated reconciliation unit tests ensuring 100% metric alignment across tools."

---

## 2. Technical Q&A & Justifications

### Why Python?
Python provided the required library ecosystem (`pandas`, `numpy`) for scalable ETL, complex RFM quantile binning, and subprocess automation for live transaction streaming.

### Why MySQL & SQL Views?
MySQL serves as the central relational database engine. By encapsulating metric logic inside SQL Views (`vw_realtime_kpis`), downstream tools (Excel VBA, Power BI DirectQuery, Tableau Live) read consistent business metrics without duplicate logic.

### Why Excel + VBA?
Executive stakeholders often require familiar spreadsheet interfaces. VBA macros enable one-click refresh directly from database views.

### How is Churn Risk Defined without Churn Labels?
Since transactional retail datasets do not contain explicit account cancellation buttons, churn risk is classified using a **Churn Risk Proxy** rule engine:
- **High Risk**: Recency > 90 days AND Frequency >= 2 orders (1,731 customers, £2.97M historical spend).

---

## 3. Technology Implementation Matrix

| Technology | Implementation Status | Evidence / Artifact | How to Demonstrate |
| :--- | :---: | :--- | :--- |
| **Python** | **FULLY IMPLEMENTED** | `python/build_phase2_pipeline.py`, `python/live_simulator.py` | Run ETL pipeline or live simulator in terminal. |
| **SQL** | **FULLY IMPLEMENTED** | `sql/01` to `06_realtime_views.sql` | Inspect real-time views in MySQL workbench or SQLite. |
| **MySQL** | **FULLY IMPLEMENTED** | `sql/setup_mysql.py` | Run `python sql/setup_mysql.py` to create schema & load data. |
| **Flask** | **FULLY IMPLEMENTED** | `web/app.py` | Launch `python web/app.py` and open `http://127.0.0.1:5000`. |
| **HTML / CSS / JS** | **FULLY IMPLEMENTED** | `web/templates/`, `web/static/` | Demonstrate responsive auto-refresh dark-mode UI. |
| **Excel & VBA** | **FULLY IMPLEMENTED** | `excel/retail_management_dashboard.xlsx`, `refresh_live_report.bas` | Import `.bas` module into Excel and run macro. *(Requires Excel Desktop)* |
| **Power BI** | **SPECIFICATION READY** | `powerbi/POWERBI_SETUP.md`, `POWERBI_DAX.md` | Explain DirectQuery architecture for MySQL views. *(Requires PBI Desktop)* |
| **Tableau** | **SPECIFICATION READY** | `tableau/TABLEAU_SETUP.md`, `TABLEAU_DATA_MODEL.md` | Explain Live Connection setup for MySQL views. *(Requires Tableau Desktop)* |
| **Git / GitHub** | **FULLY IMPLEMENTED** | `.gitignore`, GitHub repository | Show clean commit history and git exclusion rules. |
