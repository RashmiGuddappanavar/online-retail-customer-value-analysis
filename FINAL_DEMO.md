# Final Demonstration Guide (5 to 10 Minutes)

Follow this step-by-step presentation script to conduct a complete, flawless 5–10 minute live demonstration of the **Online Retail Customer Value & Revenue Analytics** platform.

---

## Demonstration Script & Step-by-Step Flow

### Step 1: Initialize Database Engine (30 Seconds)
Open a terminal in the project directory and run:
```bash
python sql/setup_mysql.py
```
*Explanation for Audience*:
> "This initializes our relational database schema in MySQL (or embedded engine) and loads dynamic real-time SQL views (`vw_realtime_kpis`) calculating revenue, completed orders, customer count, and cancellation rates across baseline and live transactions."

---

### Step 2: Start Flask Web Application (30 Seconds)
In terminal (or by double-clicking `run_project.bat`), launch Flask:
```bash
python web/app.py
```
Open your browser to **`http://127.0.0.1:5000`**.

---

### Step 3: Present Baseline Executive Dashboard (1.5 Minutes)
Show the audience the browser UI:
- Point to **Top KPI Cards**:
  - Total Completed Revenue: **£20,476,034.45**
  - Total Completed Orders: **40,067**
  - Purchasing Customers: **5,878**
  - Repeat Customer Rate: **72.39%**
  - High-Risk Customers: **1,731** (£2.97M prior spend)
  - Cancellation Rate: **1.86%**
- Navigate to `/customers`, `/products`, `/countries`, `/revenue`, and `/data-quality` to demonstrate comprehensive analytical breadth.

---

### Step 4: Demonstrate Near-Real-Time Live Transaction Ingestion (2 Minutes)
1. Return to the main dashboard (`http://127.0.0.1:5000`).
2. Point out the **Live Badge**: `● LIVE | Last updated: YYYY-MM-DD HH:MM:SS | Auto-refresh: 3s`.
3. Use the **Interactive Demo Control Panel**:
   - Click `[ +1 Transaction ]`: Point to the Instant KPI update and new transaction appearing in the **Real-Time Activity Feed**.
   - Click `[ +10 Transactions ]`: Show total completed revenue and order count incrementing.
   - Click `[ Start Live Stream ]`: Show continuous transaction arrival with 3-second auto-refresh.
4. *Explanation for Audience*:
   - Highlight data provenance: Simulated live transactions are tagged with `is_simulated = 1` while historical baseline rows remain preserved with `is_simulated = 0`.

---

### Step 5: Verify Live SQL Database State (1 Minute)
Open a separate terminal and run:
```bash
python -c "import sqlite3; conn = sqlite3.connect('data/processed/online_retail_live.db'); print('Total DB Transactions:', conn.execute('SELECT COUNT(*) FROM fact_online_retail_transactions').fetchone()[0])"
```
Or query MySQL directly:
```sql
SELECT * FROM vw_realtime_kpis;
```
Show that database view values match browser UI metrics 100%.

---

### Step 6: Present Desktop BI & Reconciliation Specifications (1.5 Minutes)
- **Excel + VBA**: Show `excel/retail_management_dashboard.xlsx` and explain how `refresh_live_report.bas` VBA macro executes database refreshes in Microsoft Excel Desktop.
- **Power BI DirectQuery**: Present `POWERBI_SETUP.md` & `POWERBI_DAX.md` explaining DirectQuery connectivity to MySQL views.
- **Tableau Live Connection**: Present `TABLEAU_SETUP.md` & `TABLEAU_CALCULATED_FIELDS.md` explaining Live Connection data model setup.

---

### Step 7: Run Automated Reconciliation Tests (1 Minute)
In terminal, execute:
```bash
python tests/test_live_reconciliation.py
```
Show the terminal output displaying **Ran 3 tests OK** and the **Before / After Reconciliation Table** confirming 100% precision.

---

## Quick Reference Summary

- **Local Web URL**: **`http://127.0.0.1:5000`**
- **Single-Command Windows Launcher**: `run_project.bat`
- **Automated Test Command**: `python tests/test_live_reconciliation.py`
