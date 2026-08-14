# Flask Local Web Presentation Layer (`web/`)

## Overview

The `web/` directory implements a local interactive web presentation layer built on top of the project's processed datasets (`data/processed/`). It provides a clean, responsive dark-mode browser interface to view and explore all executive KPIs, customer RFM & churn risk proxy analytics, commercial product performance, international market metrics, and data quality logs.

---

## Technical Stack & Architecture

- **Backend**: Python 3.11, Flask 3.0+, Pandas, SQLAlchemy
- **Frontend**: HTML5, CSS3 (Custom Dark Mode Layout with Inter typography), JavaScript (ES6)
- **Visualizations**: Chart.js 4.x via CDN
- **Data Source**: Automatically reads validated project datasets (`customer_rfm.csv`, `product_summary.csv`, `country_summary.csv`, `monthly_summary.csv`, `data_quality_summary.csv`).

---

## How to Launch the Web Application

1. Ensure the Python pipeline has run to populate `data/processed/`:
   ```bash
   python python/build_phase2_pipeline.py
   ```

2. Install dependencies:
   ```bash
   pip install -r web/requirements.txt
   ```

3. Launch the Flask web server:
   ```bash
   python web/app.py
   ```

4. Open your browser and navigate to:
   **`http://127.0.0.1:5000`**

---

## Navigation & Page Breakdown

- **`/` (Dashboard)**: Executive management KPI cards (£20.48M revenue, 40,067 completed orders, 5,878 customers, AOV £511.04, repeat rate 72.39%, churn risk count 1,731) and dynamic Chart.js visualizations.
- **`/customers`**: Customer RFM segment table & Churn Risk Proxy breakdown (High, Medium, Low Risk tiers). Includes customer search filter.
- **`/products`**: Top commercial product catalog by revenue, unit prices, order volume, and search bar.
- **`/countries`**: International sales performance across 43 purchasing countries.
- **`/revenue`**: 25-month time-series revenue growth and MoM trajectory table.
- **`/data-quality`**: Audit trail metrics and pass/fail validation check badges.
