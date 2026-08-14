# Final 5-Minute Live Demonstration Script

Use this timed 5-minute presentation script during technical interviews.

---

## Timed Script Flow

- **00:00 — Business Problem & Dataset**:
  > *"I analyzed 1.06 million retail transaction lines from the Online Retail II dataset spanning 25 months. The core business objective was identifying revenue drivers, measuring repeat buyer dependency, quantifying churn risk, and delivering executive business intelligence."*

- **00:30 — Architecture & Data Pipeline**:
  > *"Architecturally, the project operates in two tiers: Python baseline ETL and a near-real-time live database presentation layer. Python (`pandas`) cleaned raw Excel data, purged 34K exact duplicates, and scored 5,878 customers using RFM quantile binning and a Churn Risk Proxy rule engine."*

- **01:00 — MySQL Relational Database Layer**:
  > *"The baseline data and live streams flow into a MySQL analytical database. Real-time SQL views (`vw_realtime_kpis`) aggregate sales metrics across completed lines (`IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0`), ensuring consistent logic across all presentation layers."*

- **01:30 — Flask Live Browser Dashboard**:
  > *"On the presentation layer, I built a Flask web server serving interactive pages and REST APIs. The browser UI (`http://127.0.0.1:5000`) features dark-mode styling, Chart.js visual trends, and JavaScript auto-polling."*

- **02:00 — Live Transaction Ingestion Demo**:
  > *"Using the Interactive Demo Control Panel on the UI, I click `[ +1 Transaction ]` or `[ Start Live Stream ]`. Notice how Python live simulator ingests transactions into MySQL (`is_simulated = 1`), and the browser KPI cards and transaction activity feed update dynamically every 3 seconds."*

- **02:30 — Metric Reconciliation & Testing**:
  > *"To ensure data integrity, I engineered an automated test suite (`tests/test_live_reconciliation.py`). Running this script injects a unique test batch, reconciles BEFORE vs AFTER revenue down to £0.01 precision, and verifies API resilience."*

- **03:00 — SQL & Database Querying**:
  > *"Here in the SQL layer, views automatically separate simulated volume from historical baseline £20.48M revenue, maintaining clean data provenance."*

- **03:30 — Excel & VBA Macro Integration**:
  > *"For spreadsheet stakeholders, `excel/retail_management_dashboard.xlsx` contains executive KPI formulas and `refresh_live_report.bas` VBA macro module for one-click desktop database refreshes."*

- **04:00 — Power BI & Tableau Specifications**:
  > *"For enterprise BI, I authored the complete Star Schema model, DAX catalog, and Tableau calculated fields, prepared for DirectQuery / Live connections in desktop environments."*

- **04:30 — Code Quality & GitHub Engineering**:
  > *"The GitHub repository follows clean engineering practices with `.gitignore` excluding raw Excel files and large transaction logs while keeping standard test coverage."*

- **05:00 — Commercial Impact & Conclusion**:
  > *"In summary, the project revealed that repeat buyers generate 90.4% of customer revenue, while identifying 1,731 high-risk customers representing £2.97M in historical revenue for targeted retention campaigns."*
