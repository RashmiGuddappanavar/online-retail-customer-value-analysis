# Raw Data Directory (`data/raw/`)

## Overview

This directory contains the original raw transactional dataset used for the Online Retail Customer Value & Revenue Analytics project.

---

## Source Dataset Information

- **Dataset Name**: Online Retail II Data Set
- **Source**: [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/502/online+retail+ii)
- **File Name**: `online_retail_II.xlsx`
- **File Format**: Microsoft Excel Workbook (`.xlsx`) containing two sheets:
  - `Year 2009-2010`: Transactions from December 1, 2009 to December 9, 2010 (525,461 rows).
  - `Year 2010-2011`: Transactions from December 1, 2010 to December 9, 2011 (541,910 rows).
- **Total Combined Raw Rows**: **1,067,371 rows**

---

## Schema & Raw Attributes

| Field Name | Raw Excel Column | Data Type | Description |
| :--- | :--- | :--- | :--- |
| `InvoiceNo` | `Invoice` | String / Object | 6-digit invoice number (prefixed with 'C' if cancelled) |
| `StockCode` | `StockCode` | String / Object | 5-digit product code |
| `Description` | `Description` | String / Object | Product item description |
| `Quantity` | `Quantity` | Integer | Quantity per transaction (negative for returns/cancellations) |
| `InvoiceDate` | `InvoiceDate` | DateTime | Invoice date and time |
| `UnitPrice` | `Price` | Decimal | Unit price in Sterling (£) |
| `CustomerID` | `Customer ID` | Float / Nullable | 5-digit customer identification number |
| `Country` | `Country` | String | Customer country of residence |

---

## Usage Instructions

To run the automated Python data pipeline (`python/01_data_cleaning_eda.ipynb`), ensure that `online_retail_II.xlsx` is placed in this directory (`data/raw/`). The pipeline processes this file and outputs clean analytical tables into `data/processed/`.
