# Python Data Pipeline & EDA (`python/`)

## Overview

The `python/` directory contains the automated data cleaning, deduplication, exploratory data analysis (EDA), RFM segmentation modeling, and summary dataset generation pipeline for the Online Retail II project.

---

## Deliverables & Notebooks

- **[01_data_cleaning_eda.ipynb](file:///c:/Users/mgras/OneDrive/Desktop/online-retail-customer-value-analysis/python/01_data_cleaning_eda.ipynb)**: Executable Jupyter Notebook implementing end-to-end data processing from raw Excel sheets (`data/raw/online_retail_II.xlsx`) to production CSV outputs (`data/processed/`).

---

## Data Cleaning & Deduplication Audit Trail

```
Raw Excel Sheets Combined: 1,067,371 Rows
   │
   ├── Exact Duplicate Rows Removed: 34,335 Rows
   │
   ├── Invalid / Administrative Rows Filtered: 5,965 Rows
   │     ├─ Bad debt write-offs (UnitPrice < 0): 5 Rows
   │     ├─ Test stock codes (TEST*): 17 Rows
   │     └─ Zero price without CustomerID (inventory notes/audits): 5,944 Rows
   │
   └── Final Cleaned Transaction Dataset: 1,027,071 Rows
```

---

## Analytical Methodology

### 1. Official Revenue Filter
$$\text{Completed Revenue} = \sum (\text{Quantity} \times \text{UnitPrice}) \quad \text{WHERE } \text{IsCancelled} = \text{False} \text{ AND } \text{Quantity} > 0 \text{ AND } \text{UnitPrice} > 0$$

### 2. RFM Segmentation Logic
- **Reference Date**: Derived as max transaction timestamp + 1 day (`2011-12-10 12:50:00`).
- **Recency**: Days inactive relative to reference date.
- **Frequency**: Distinct completed invoice count per customer (`COUNTD(InvoiceNo)`).
- **Monetary**: Sum of completed revenue per customer.
- **Quantile Scoring**: 5-quantile binning (`R_Score`, `F_Score`, `M_Score`) mapping customers into 7 segments (`Champions`, `Loyal Customers`, `At Risk Spenders`, `Promising / Average`, `Potential Loyalists`, `Lost Customers`, `Needs Attention`).

### 3. Churn Risk Proxy Classification
Because explicit customer cancellation labels do not exist in retail data, a **Churn Risk Proxy** rule engine classifies customer retention risk:
- **High Risk (Churn Proxy)**: Recency > 90 days AND Frequency >= 2 orders (1,731 customers, £2.97M prior spend).
- **Medium Risk (One-time Inactive)**: Recency > 90 days AND Frequency = 1 order (1,258 customers).
- **Medium Risk (Dormant Frequent)**: 60 < Recency <= 90 days AND Frequency >= 2 orders (373 customers).
- **Low Risk (Active)**: Recency <= 60 days (2,396 customers).

---

## How to Execute Notebook

1. Ensure Python 3.9+ environment is active.
2. Install required packages: `pip install pandas numpy openpyxl calamine jupyter matplotlib seaborn`.
3. Open and run all cells in `01_data_cleaning_eda.ipynb`.
