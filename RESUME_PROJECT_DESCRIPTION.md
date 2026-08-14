# Resume-Ready Project Descriptions

Use these tailored bullet points on your resume or LinkedIn profile.

---

## Option A: ATS-Friendly (2-3 Bullet Version)
- **Engineered an End-to-End Retail Analytics Platform**: Analyzed 1.06M+ transactions (£20.48M completed revenue) using Python (Pandas/Numpy), MySQL, and Flask to deliver near-real-time executive BI dashboards.
- **Built Customer Segmentation & Churn Risk Engine**: Segmented 5,878 customers using RFM quantile scoring and a Churn Risk Proxy rule engine, uncovering 1,731 high-risk customers representing £2.97M (17.1%) in historical revenue.
- **Developed Live Transaction Streaming & Web Layer**: Designed an automated Python transaction ingestion simulator and real-time SQL views feeding a responsive Flask dashboard with 3-second auto-refresh and 100% metric reconciliation.

---

## Option B: Data Analyst / BI Specialist Version
- **Multi-Tool Business Intelligence Architecture**: Processed 1.06M raw retail transaction lines down to 1.027M clean rows, purging 34K+ exact duplicates and administrative test codes.
- **RFM Customer Segmentation & Revenue Analytics**: Mapped purchasing customer behaviors into 7 quantile RFM segments (`Champions`, `Loyal Customers`, `At Risk Spenders`) and quantified repeat customer reliance (72.39% repeat buyers driving 90.38% of customer spend).
- **SQL Data Layer & Executive Reporting**: Authored MySQL schema DDLs, indexed tables, and real-time analytical SQL views (`vw_realtime_kpis`) connected to automated Excel VBA management reporting macros and Power BI / Tableau DirectQuery specifications.

---

## Option C: Python / Full-Stack Data Engineer Version
- **Near-Real-Time Data Ingestion & API Backend**: Created an asynchronous Python transaction simulator (`live_simulator.py`) streaming simulated retail orders/cancellations into a MySQL relational database (`is_simulated = 1` vs historical `0`).
- **Flask REST API & Auto-Refresh Web UI**: Developed a modular Flask web application (`web/app.py`) serving JSON REST API endpoints consumed by Chart.js and JavaScript polling timers for real-time browser visual updates.
- **Automated Test Reconciliation & Data Pipeline**: Built a Python unit test suite (`unittest`) validating exact metric reconciliation between raw data files, SQL analytical views, and REST API endpoints down to £0.01 precision.
