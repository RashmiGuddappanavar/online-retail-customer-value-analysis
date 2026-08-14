# Demonstration & Setup Guide: Online Retail Customer Value Analytics

Welcome to the **Online Retail Customer Value & Revenue Analytics** platform setup and demonstration manual.

---

## 1. Prerequisites

- **Python**: Version 3.9+ installed (`python --version`)
- **Web Browser**: Chrome, Edge, or Firefox
- **Optional Database**: MySQL 8.0+ (If MySQL is not running, the application automatically uses an embedded SQLite live database engine so you can run the project out-of-the-box).

---

## 2. Local Database & Environment Setup

1. (Optional) Configure local MySQL credentials in `.env`:
   ```env
   DB_HOST=localhost
   DB_PORT=3306
   DB_NAME=online_retail_analytics
   DB_USER=root
   DB_PASSWORD=your_password
   ```

2. Initialize the database engine & SQL views:
   ```bash
   python sql/setup_mysql.py
   ```

---

## 3. Starting the Application

### Option A: Automated Single-Command Startup (Windows)
Double-click **`run_project.bat`** or run in terminal:
```cmd
run_project.bat
```

### Option B: Manual Terminal Startup
```bash
pip install -r web/requirements.txt
python web/app.py
```

---

## 4. Demonstrating Near-Real-Time Ingestion

1. Open your browser to **`http://127.0.0.1:5000`**.
2. Notice the baseline metrics:
   - **Total Completed Revenue**: £20,476,034.45
   - **Completed Orders**: 40,067
3. Use the **Interactive Demo Control Panel** directly on the dashboard UI:
   - Click `[ +1 Transaction ]` or `[ +10 Transactions ]` to inject live transactions.
   - Click `[ Start Live Stream ]` to simulate continuous orders arriving every 3 seconds.
4. Watch the KPI cards, live timestamp badge (`● LIVE`), and **Real-Time Transaction Activity Feed** update automatically without refreshing your browser window.

---

## 5. Running Automated Reconciliation Tests

In a terminal, execute:
```bash
python tests/test_live_reconciliation.py
```
This test suite injects a unique test batch (`TEST_BATCH_PHASE8`), queries the REST API, prints a **Before / After Reconciliation Table**, verifies 100% metric precision, and cleans up test data.

---

## 6. Desktop Tool Integration Setup

### Excel & VBA Macro
- Open `excel/retail_management_dashboard.xlsx`.
- Press `ALT + F11` to open the VBA Editor and import `excel/refresh_live_report.bas`.
- Run `RefreshLiveReport` to refresh queries directly from MySQL / live database views.
- *Requires Microsoft Excel Desktop.*

### Power BI DirectQuery
- Open Power BI Desktop and select **Get Data -> MySQL Database**.
- Server: `localhost:3306`, Database: `online_retail_analytics`.
- Data Connectivity mode: Select **DirectQuery**.
- Load table `vw_realtime_kpis` or `fact_online_retail_transactions`.
- *DirectQuery configuration specification ready; `.pbix` creation requires Power BI Desktop.*

### Tableau Live Connection
- Open Tableau Desktop and select **To a Server -> MySQL**.
- Server: `localhost`, Port: `3306`, Database: `online_retail_analytics`.
- Select Connection type: **Live**.
- Drag `vw_realtime_kpis` onto the canvas.
- *Live connection specification ready; `.twbx` creation requires Tableau Desktop.*
