-- =============================================================================
-- ONLINE RETAIL II ANALYTICS — DATA QUALITY & RECONCILIATION SQL
-- File: 02_data_quality.sql
-- Purpose: Verify data integrity, check for missing/invalid values, duplicates,
--          and perform reconciliation against Phase 2 Python metrics.
-- Database: online_retail_analytics
-- =============================================================================

USE online_retail_analytics;

-- -----------------------------------------------------------------------------
-- 1. ROW COUNT & INTEGRITY CHECKS
-- Expected output: 1,027,071 rows in retail_transactions
-- -----------------------------------------------------------------------------
SELECT 
    'retail_transactions' AS TableName,
    COUNT(*) AS TotalRowCount
FROM retail_transactions;


-- -----------------------------------------------------------------------------
-- 2. NULL VALUE AUDIT ACROSS KEY FIELDS
-- Identifies missing critical fields in the transaction table.
-- Note: CustomerID is expected to have NULL values for guest/unregistered transactions.
-- -----------------------------------------------------------------------------
SELECT 
    COUNT(*) AS TotalRows,
    SUM(CASE WHEN InvoiceNo IS NULL THEN 1 ELSE 0 END) AS Null_InvoiceNo,
    SUM(CASE WHEN StockCode IS NULL THEN 1 ELSE 0 END) AS Null_StockCode,
    SUM(CASE WHEN InvoiceDate IS NULL THEN 1 ELSE 0 END) AS Null_InvoiceDate,
    SUM(CASE WHEN CustomerID IS NULL THEN 1 ELSE 0 END) AS Null_CustomerID,
    ROUND(SUM(CASE WHEN CustomerID IS NULL THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS Pct_Null_CustomerID
FROM retail_transactions;


-- -----------------------------------------------------------------------------
-- 3. VALUE RANGE & ANOMALY CHECKS (QUANTITY & UNIT PRICE)
-- Checks for negative or zero quantities and unit prices.
-- Cleaned dataset contains negative quantities ONLY for cancelled orders.
-- -----------------------------------------------------------------------------
SELECT 
    SUM(CASE WHEN Quantity <= 0 AND IsCancelled = 0 THEN 1 ELSE 0 END) AS NonPositiveQty_NonCancelled,
    SUM(CASE WHEN Quantity < 0 AND IsCancelled = 1 THEN 1 ELSE 0 END) AS NegativeQty_Cancelled,
    SUM(CASE WHEN UnitPrice <= 0 THEN 1 ELSE 0 END) AS NonPositiveUnitPrice,
    MIN(UnitPrice) AS MinUnitPrice,
    MAX(UnitPrice) AS MaxUnitPrice,
    MIN(Quantity) AS MinQuantity,
    MAX(Quantity) AS MaxQuantity
FROM retail_transactions;


-- -----------------------------------------------------------------------------
-- 4. DUPLICATE TRANSACTION COMBINATIONS AUDIT
-- Checks for potential duplicate rows on composite natural keys (InvoiceNo, StockCode, InvoiceDate).
-- Exact row duplicates were removed in Phase 2 pipeline.
-- -----------------------------------------------------------------------------
SELECT 
    InvoiceNo,
    StockCode,
    InvoiceDate,
    COUNT(*) AS OccurrenceCount
FROM retail_transactions
GROUP BY InvoiceNo, StockCode, InvoiceDate
HAVING COUNT(*) > 1
LIMIT 10;


-- -----------------------------------------------------------------------------
-- 5. DATE RANGE BOUNDS & TEMPORAL COVERAGE
-- Confirms dataset timeline spans from December 1, 2009 to December 9, 2011.
-- -----------------------------------------------------------------------------
SELECT 
    MIN(InvoiceDate) AS EarliestInvoiceDate,
    MAX(InvoiceDate) AS LatestInvoiceDate,
    TIMESTAMPDIFF(DAY, MIN(InvoiceDate), MAX(InvoiceDate)) AS TotalDaysSpanned
FROM retail_transactions;


-- -----------------------------------------------------------------------------
-- 6. UNIQUE ENTITY COUNTS
-- Audit of distinct customers, products (StockCodes), and geographic countries.
-- -----------------------------------------------------------------------------
SELECT 
    COUNT(DISTINCT CustomerID) AS UniquePurchasingCustomers,
    COUNT(DISTINCT StockCode) AS UniqueProducts,
    COUNT(DISTINCT Country) AS UniqueCountries
FROM retail_transactions
WHERE CustomerID IS NOT NULL;


-- =============================================================================
-- 7. PHASE 2 RECONCILIATION QUERIES
-- Validates SQL output targets against Python Phase 2 baseline numbers.
-- Targets:
--   - Total Revenue: £20,476,034.43
--   - Total Completed Orders: 40,067
--   - Unique Purchasing Customers: 5,878
--   - Cancellation Line Rate: 1.86%
-- =============================================================================

-- 7a. Total Completed Sales Revenue & Order Metrics
SELECT 
    ROUND(SUM(Revenue), 2) AS CalculatedTotalRevenue,
    COUNT(DISTINCT InvoiceNo) AS CompletedOrdersCount,
    ROUND(SUM(Revenue) / COUNT(DISTINCT InvoiceNo), 2) AS CalculatedAOV,
    20476034.43 AS TargetRevenue,
    ROUND(SUM(Revenue) - 20476034.43, 2) AS RevenueVariance
FROM retail_transactions
WHERE IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0;

-- 7b. Identified Customer Revenue vs. Guest / Unknown Customer Revenue
SELECT 
    CASE WHEN CustomerID IS NOT NULL THEN 'Identified Customer' ELSE 'Guest / Unknown' END AS CustomerType,
    COUNT(DISTINCT CustomerID) AS CustomerCount,
    COUNT(DISTINCT InvoiceNo) AS OrderCount,
    ROUND(SUM(Revenue), 2) AS TotalRevenue,
    ROUND(SUM(Revenue) * 100.0 / (SELECT SUM(Revenue) FROM retail_transactions WHERE IsCancelled = 0), 2) AS RevenuePct
FROM retail_transactions
WHERE IsCancelled = 0
GROUP BY CASE WHEN CustomerID IS NOT NULL THEN 'Identified Customer' ELSE 'Guest / Unknown' END;

-- 7c. Cancellation Rate Audit
SELECT 
    COUNT(*) AS TotalLines,
    SUM(CASE WHEN IsCancelled = 1 THEN 1 ELSE 0 END) AS CancelledLines,
    SUM(CASE WHEN IsCancelled = 0 THEN 1 ELSE 0 END) AS CompletedLines,
    ROUND(SUM(CASE WHEN IsCancelled = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 4) AS CancellationRatePct
FROM retail_transactions;
