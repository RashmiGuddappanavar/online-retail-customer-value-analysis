import nbformat as nbf
import os

nb = nbf.v4.new_notebook()

# Section 1: Title and Project Objective
markdown_1 = """# Online Retail II — Customer Value, Retention & Revenue Analytics
## Notebook 01: Data Cleaning, Quality Assessment & Exploratory Data Analysis

---

### 1. Project Objective
The goal of this project is to analyze transaction data from an online retail store operating between December 2009 and December 2011. The retailer leadership wants to identify:
1. **High-Value Customer Segments**: Which customers generate the most revenue and repeat business.
2. **Churn Risk**: Which customer segments are at risk of churning so retention campaigns can be targeted.
3. **Product & Country Revenue Drivers**: Top performing items, key geographical markets, and revenue drivers.
4. **Operations & Inventory Insights**: Cancellation patterns, return rates, seasonal demand trends, and stock allocations.

---

### 2. Business Questions
- **Q1**: What is the overall revenue trend across the 2-year period, and what seasonal patterns exist?
- **Q2**: Which customer segments (RFM-based) contribute the most revenue, and which represent high churn risk?
- **Q3**: What are the top revenue-generating products and countries?
- **Q4**: Where are cancellations concentrated, and how do they impact net revenue?
- **Q5**: What actionable recommendations can be made for retention, product stocking, and marketing?

---

### 3. Import Libraries
"""

code_3 = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings

warnings.filterwarnings('ignore')

# Set plotting style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 11

print("Pandas version:", pd.__version__)
"""

# Section 4: Load Data
markdown_4 = """### 4. Load Raw Data
The dataset is stored in `data/raw/online_retail_II.xlsx` containing two sheets:
- Sheet `Year 2009-2010` (Dec 1, 2009 to Dec 9, 2010)
- Sheet `Year 2010-2011` (Dec 1, 2010 to Dec 9, 2011)

*Note: Raw data is preserved without modification.*
"""

code_4 = """data_path = os.path.join("..", "data", "raw", "online_retail_II.xlsx")
if not os.path.exists(data_path):
    data_path = os.path.join("data", "raw", "online_retail_II.xlsx")

excel_file = pd.ExcelFile(data_path, engine="calamine")
print("Sheets in workbook:", excel_file.sheet_names)

df_2009_2010 = pd.read_excel(excel_file, sheet_name="Year 2009-2010", engine="calamine")
df_2010_2011 = pd.read_excel(excel_file, sheet_name="Year 2010-2011", engine="calamine")

print(f"Year 2009-2010 shape: {df_2009_2010.shape}")
print(f"Year 2010-2011 shape: {df_2010_2011.shape}")
"""

# Section 5: Dataset Overview
markdown_5 = """### 5. Dataset Overview
Let's inspect sample records, column names, data types, and initial summary statistics for both sheets.
"""

code_5 = """print("--- Year 2009-2010 Data Info ---")
print(df_2009_2010.info())
print("\nHead 2009-2010:")
display(df_2009_2010.head())

print("\n--- Year 2010-2011 Data Info ---")
print(df_2010_2011.info())
print("\nHead 2010-2011:")
display(df_2010_2011.head())
"""

# Section 6: Data Quality Assessment (Phase 1 Report)
markdown_6 = """### 6. Data Quality Assessment & Phase 1 Findings

#### Summary of Inspection Results Across Both Sheets

| Metric / Dimension | Year 2009-2010 Sheet | Year 2010-2011 Sheet | Combined Raw Total |
| :--- | :--- | :--- | :--- |
| **Total Rows** | 525,461 | 541,910 | 1,067,371 |
| **Columns** | 8 | 8 | 8 |
| **Date Range** | 2009-12-01 to 2010-12-09 | 2010-12-01 to 2011-12-09 | 2009-12-01 to 2011-12-09 |
| **Missing Descriptions** | 2,928 (0.56%) | 1,454 (0.27%) | 4,382 (0.41%) |
| **Missing Customer IDs** | 107,927 (20.54%) | 135,080 (24.93%) | 243,007 (22.77%) |
| **Exact Duplicate Rows (internal)** | 6,865 | 5,268 | 34,335 (incl 23,221 cross-sheet overlap) |
| **Unique Customer IDs** | 4,383 | 4,372 | 5,942 |
| **Unique StockCodes** | 4,632 | 4,070 | 5,305 |
| **Unique Countries** | 40 | 38 | 43 |
| **Cancelled Invoices ('C')** | 10,206 | 9,288 | 19,494 |
| **Negative Quantities** | 12,326 | 10,624 | 22,950 |
| **Zero Unit Prices (£0.00)** | 3,687 | 2,515 | 6,202 |
| **Negative Unit Prices (< £0.00)** | 3 | 2 | 5 (Adjust bad debt) |

#### Critical Data Quality Anomalies Identified:
1. **Date Range Overlap**: December 1, 2010 through December 9, 2010 is present in BOTH sheets. Concatenating the sheets blindly creates **23,221 exact duplicate records** across sheets.
2. **Missing Customer IDs**: 243,007 rows (22.77%) do not have a Customer ID. While these transactions contribute to total store revenue, they cannot be assigned to specific individual customer RFM profiles.
3. **Cancelled Invoices**: 19,494 transactions start with invoice prefix **'C'**. They correspond to product returns and cancellations with negative quantities.
4. **Unmatched Negative Quantities**: 3,457 rows have negative quantities without a 'C' prefix in the Invoice number. These represent internal inventory adjustments, damaged items, write-offs, or stock audits.
5. **Zero & Negative Prices**:
   - 6,202 records have `Price == 0.00` (6,131 missing Customer ID; 71 promotional samples with Customer ID).
   - 5 records have negative prices (`Price < 0`), all under StockCode `B` and Description `"Adjust bad debt"`.
6. **Non-Standard Stock Codes**: Transactions contain administrative codes such as `POST` (Postage), `D` (Discount), `M` (Manual), `BANK CHARGES`, `AMAZONFEE`, `CRUK`, `TEST001/002`, `PADS`.

---
"""

code_6 = """# Data quality summary script execution in notebook
dq_summary = pd.DataFrame({
    'Metric': [
        'Total Rows', 'Columns', 'Date Start', 'Date End',
        'Missing Description', 'Missing Customer ID', '% Missing Customer ID',
        'Internal Duplicate Rows', 'Unique Customers', 'Unique StockCodes', 'Unique Countries',
        'Cancelled Invoices (C)', 'Negative Quantities', 'Zero Unit Prices', 'Negative Unit Prices'
    ],
    'Year 2009-2010': [
        525461, 8, '2009-12-01', '2010-12-09',
        2928, 107927, '20.54%',
        6865, 4383, 4632, 40,
        10206, 12326, 3687, 3
    ],
    'Year 2010-2011': [
        541910, 8, '2010-12-01', '2011-12-09',
        1454, 135080, '24.93%',
        5268, 4372, 4070, 38,
        9288, 10624, 2515, 2
    ]
})
display(dq_summary)
"""

nb.cells = [
    nbf.v4.new_markdown_cell(markdown_1),
    nbf.v4.new_code_cell(code_3),
    nbf.v4.new_markdown_cell(markdown_4),
    nbf.v4.new_code_cell(code_4),
    nbf.v4.new_markdown_cell(markdown_5),
    nbf.v4.new_code_cell(code_5),
    nbf.v4.new_markdown_cell(markdown_6),
    nbf.v4.new_code_cell(code_6),
]

notebook_path = os.path.join("python", "01_data_cleaning_eda.ipynb")
with open(notebook_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Created 01_data_cleaning_eda.ipynb successfully.")
