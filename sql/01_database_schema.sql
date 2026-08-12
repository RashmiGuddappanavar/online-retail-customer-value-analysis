-- =============================================================================
-- ONLINE RETAIL II ANALYTICS — DATABASE SCHEMA & IMPORT SCRIPT
-- Database Engine: MySQL 8.x
-- Target Database: online_retail_analytics
-- =============================================================================

-- 1. DATABASE CREATION
CREATE DATABASE IF NOT EXISTS online_retail_analytics
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

USE online_retail_analytics;

-- =============================================================================
-- 2. TABLE DEFINITIONS
-- =============================================================================

-- -----------------------------------------------------------------------------
-- Table 1: retail_transactions
-- Description: Transaction-level retail dataset (Cleaned & Filtered)
-- Source File: data/processed/retail_cleaned.csv (1,027,071 rows)
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS retail_transactions;
CREATE TABLE retail_transactions (
    InvoiceNo VARCHAR(20) NOT NULL,
    StockCode VARCHAR(20) NOT NULL,
    Description VARCHAR(255) NULL,
    Quantity INT NOT NULL,
    InvoiceDate DATETIME NOT NULL,
    UnitPrice DECIMAL(10,4) NOT NULL,
    CustomerID INT NULL,
    Country VARCHAR(100) NOT NULL,
    IsCancelled TINYINT(1) NOT NULL DEFAULT 0,
    Revenue DECIMAL(12,4) NOT NULL,
    Year INT NOT NULL,
    Month INT NOT NULL,
    YearMonth VARCHAR(7) NOT NULL,
    MonthName VARCHAR(10) NOT NULL,
    Quarter VARCHAR(7) NOT NULL,
    DayOfWeek VARCHAR(10) NOT NULL,
    Hour INT NOT NULL,
    INDEX idx_customer_id (CustomerID),
    INDEX idx_invoice_no (InvoiceNo),
    INDEX idx_stock_code (StockCode),
    INDEX idx_invoice_date (InvoiceDate),
    INDEX idx_country (Country),
    INDEX idx_is_cancelled (IsCancelled),
    INDEX idx_year_month (YearMonth)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- Table 2: customer_rfm
-- Description: Customer-level RFM metrics, segmentations, and churn risk proxies
-- Source File: data/processed/customer_rfm.csv (5,878 rows)
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS customer_rfm;
CREATE TABLE customer_rfm (
    CustomerID INT NOT NULL PRIMARY KEY,
    Recency INT NOT NULL,
    Frequency INT NOT NULL,
    Monetary DECIMAL(12,2) NOT NULL,
    R_Score TINYINT NOT NULL,
    F_Score TINYINT NOT NULL,
    M_Score TINYINT NOT NULL,
    RFM_Score_Comb INT NOT NULL,
    RFM_Avg DECIMAL(3,2) NOT NULL,
    CustomerSegment VARCHAR(50) NOT NULL,
    ChurnRiskProxy VARCHAR(50) NOT NULL,
    INDEX idx_rfm_segment (CustomerSegment),
    INDEX idx_churn_risk (ChurnRiskProxy)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- Table 3: product_summary
-- Description: Aggregated metrics by product
-- Source File: data/processed/product_summary.csv (5,400 rows)
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS product_summary;
CREATE TABLE product_summary (
    StockCode VARCHAR(20) NOT NULL PRIMARY KEY,
    Description VARCHAR(255) NULL,
    TotalQuantity INT NOT NULL,
    TotalRevenue DECIMAL(12,2) NOT NULL,
    TotalOrders INT NOT NULL,
    AvgUnitPrice DECIMAL(10,4) NOT NULL,
    INDEX idx_prod_revenue (TotalRevenue DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- Table 4: country_summary
-- Description: Aggregated metrics by geographic region
-- Source File: data/processed/country_summary.csv (43 rows)
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS country_summary;
CREATE TABLE country_summary (
    Country VARCHAR(100) NOT NULL PRIMARY KEY,
    TotalRevenue DECIMAL(12,2) NOT NULL,
    TotalOrders INT NOT NULL,
    TotalCustomers INT NOT NULL,
    AvgOrderValue DECIMAL(12,2) NOT NULL,
    INDEX idx_country_revenue (TotalRevenue DESC)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- -----------------------------------------------------------------------------
-- Table 5: monthly_summary
-- Description: Aggregated time-series metrics by Year-Month
-- Source File: data/processed/monthly_summary.csv (25 rows)
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS monthly_summary;
CREATE TABLE monthly_summary (
    YearMonth VARCHAR(7) NOT NULL PRIMARY KEY,
    Year INT NOT NULL,
    Month INT NOT NULL,
    MonthName VARCHAR(10) NOT NULL,
    TotalRevenue DECIMAL(12,2) NOT NULL,
    TotalOrders INT NOT NULL,
    TotalCustomers INT NOT NULL,
    CancellationCount INT NOT NULL,
    CancellationRate DECIMAL(6,4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


-- =============================================================================
-- 3. DATA IMPORT INSTRUCTIONS & STATEMENTS
-- =============================================================================

/*
 METHOD 1: LOAD DATA LOCAL INFILE (Fastest for MySQL Server CLI / Workbench)
 Note: Requires local_infile=1 enabled on both server and client connections.
 Adjust file paths to point to absolute system location of processed CSV files.

 SET GLOBAL local_infile = 1;

 LOAD DATA LOCAL INFILE 'C:/path/to/project/data/processed/retail_cleaned.csv'
 INTO TABLE retail_transactions
 FIELDS TERMINATED BY ',' 
 OPTIONALLY ENCLOSED BY '"'
 LINES TERMINATED BY '\r\n'
 IGNORE 1 LINES
 (InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, @vCustomerID, Country, @vIsCancelled, Revenue, Year, Month, YearMonth, MonthName, Quarter, DayOfWeek, Hour)
 SET 
    CustomerID = NULLIF(@vCustomerID, ''),
    IsCancelled = IF(@vIsCancelled = 'True' OR @vIsCancelled = '1', 1, 0);

 LOAD DATA LOCAL INFILE 'C:/path/to/project/data/processed/customer_rfm.csv'
 INTO TABLE customer_rfm
 FIELDS TERMINATED BY ',' 
 OPTIONALLY ENCLOSED BY '"'
 LINES TERMINATED BY '\r\n'
 IGNORE 1 LINES;

 LOAD DATA LOCAL INFILE 'C:/path/to/project/data/processed/product_summary.csv'
 INTO TABLE product_summary
 FIELDS TERMINATED BY ',' 
 OPTIONALLY ENCLOSED BY '"'
 LINES TERMINATED BY '\r\n'
 IGNORE 1 LINES;

 LOAD DATA LOCAL INFILE 'C:/path/to/project/data/processed/country_summary.csv'
 INTO TABLE country_summary
 FIELDS TERMINATED BY ',' 
 OPTIONALLY ENCLOSED BY '"'
 LINES TERMINATED BY '\r\n'
 IGNORE 1 LINES;

 LOAD DATA LOCAL INFILE 'C:/path/to/project/data/processed/monthly_summary.csv'
 INTO TABLE monthly_summary
 FIELDS TERMINATED BY ',' 
 OPTIONALLY ENCLOSED BY '"'
 LINES TERMINATED BY '\r\n'
 IGNORE 1 LINES;
*/

/*
 METHOD 2: Python / SQLAlchemy Automated Data Loader (Recommended for Windows environments)
 Python script snippet to populate MySQL database directly without configuration hurdles:

 ```python
 import pandas as pd
 from sqlalchemy import create_engine

 engine = create_engine('mysql+pymysql://user:password@localhost:3306/online_retail_analytics')

 tables = {
     'retail_transactions': 'data/processed/retail_cleaned.csv',
     'customer_rfm': 'data/processed/customer_rfm.csv',
     'product_summary': 'data/processed/product_summary.csv',
     'country_summary': 'data/processed/country_summary.csv',
     'monthly_summary': 'data/processed/monthly_summary.csv'
 }

 for table_name, csv_path in tables.items():
     df = pd.read_csv(csv_path)
     df.to_sql(table_name, engine, if_exists='replace', index=False, chunksize=10000)
     print(f"Successfully loaded {len(df)} rows into {table_name}")
 ```
*/
