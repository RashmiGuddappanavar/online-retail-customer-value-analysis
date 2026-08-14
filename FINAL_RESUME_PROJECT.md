# Final Resume Project Descriptions

Use these bullet points on your resume or portfolio site.

---

## A. Data Analyst Version

- **End-to-End E-Commerce Customer Analytics Platform**: Processed 1.06M+ retail transactions (£20.48M completed revenue) using Python (`pandas`, `numpy`) and SQL, purging 34K+ exact duplicates and administrative non-commercial rows.
- **RFM Customer Segmentation & Churn Risk Engine**: Segmented 5,878 purchasing customers using 5-quantile RFM scoring and authored a Churn Risk Proxy rule engine identifying 1,731 high-risk dormant customers representing £2.97M (17.1%) in historical sales.
- **Relational Data Modeling & Executive Reporting**: Authored MySQL schema DDLs, indexing strategies, and real-time analytical SQL views (`vw_realtime_kpis`) feeding automated Excel VBA management reporting macros and Power BI / Tableau DirectQuery model specifications.

---

## B. Python / Data Engineer Version

- **Near-Real-Time Ingestion Architecture & Database Engine**: Built a Python transaction simulator (`live_simulator.py`) streaming simulated retail orders/cancellations directly into a MySQL database layer (`is_simulated = 1` vs baseline `0`).
- **Flask REST API & Dynamic Web Dashboard**: Developed a modular Flask web application (`web/app.py`) serving JSON REST APIs consumed by Chart.js and JavaScript 3-second auto-refresh polling timers.
- **Automated Test Reconciliation**: Engineered a Python unit test suite (`unittest`) executing before/after transaction batch injections to verify 100% metric alignment across database views and API endpoints down to £0.01 precision.

---

## C. Full-Stack Analytics Engineer Version

- **Multi-Tool Analytics Platform & Web Presentation Layer**: Delivered a multi-tiered BI architecture combining Python ETL, MySQL relational data modeling, Flask web server, and a dark-mode browser dashboard.
- **Interactive Local Demo Control Panel**: Created browser-based local simulator controls (`[ +1 Transaction ]`, `[ Start Live Stream ]`) allowing interactive demonstration of live KPI updates and real-time transaction feeds.
- **Production Data Quality & System Resilience**: Implemented data validation assertions and database fallback exception handling to ensure server stability during network or payload anomalies.
