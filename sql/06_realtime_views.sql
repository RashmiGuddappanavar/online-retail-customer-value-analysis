-- ================================================================================
-- ONLINE RETAIL CUSTOMER VALUE & REVENUE ANALYTICS
-- Script 06: Near-Real-Time Analytical SQL Views & Dynamic Data Layer
-- Description: Defines SQL views for real-time KPI aggregation across combined
--              baseline (historical) and simulated live transactions.
-- Engine: MySQL 8.0+ / SQLite Compatible
-- ================================================================================

-- Drop existing views if present
DROP VIEW IF EXISTS vw_realtime_kpis;
DROP VIEW IF EXISTS vw_realtime_monthly;
DROP VIEW IF EXISTS vw_realtime_top_products;
DROP VIEW IF EXISTS vw_realtime_top_countries;

-- 1. Real-Time Overall KPI Aggregation View
CREATE VIEW vw_realtime_kpis AS
SELECT 
    COUNT(CASE WHEN IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0 THEN 1 END) AS TotalCompletedLines,
    COALESCE(SUM(CASE WHEN IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0 THEN Quantity * UnitPrice ELSE 0 END), 0.0) AS CompletedRevenue,
    COUNT(DISTINCT CASE WHEN IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0 THEN InvoiceNo END) AS CompletedOrders,
    COUNT(DISTINCT CASE WHEN IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0 AND CustomerID IS NOT NULL AND CustomerID != '' THEN CustomerID END) AS UniqueCustomers,
    CASE 
        WHEN COUNT(DISTINCT CASE WHEN IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0 THEN InvoiceNo END) > 0 
        THEN COALESCE(SUM(CASE WHEN IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0 THEN Quantity * UnitPrice ELSE 0 END), 0.0) / 
             COUNT(DISTINCT CASE WHEN IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0 THEN InvoiceNo END)
        ELSE 0.0 
    END AS AverageOrderValue,
    COUNT(CASE WHEN IsCancelled = 1 OR Quantity < 0 THEN 1 END) AS CancelledLines,
    COUNT(*) AS TotalLines,
    CASE 
        WHEN COUNT(*) > 0 
        THEN (CAST(COUNT(CASE WHEN IsCancelled = 1 OR Quantity < 0 THEN 1 END) AS FLOAT) / COUNT(*)) * 100.0 
        ELSE 0.0 
    END AS CancellationRatePct,
    COUNT(CASE WHEN is_simulated = 1 THEN 1 END) AS SimulatedTransactionCount,
    COALESCE(SUM(CASE WHEN is_simulated = 1 AND IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0 THEN Quantity * UnitPrice ELSE 0 END), 0.0) AS SimulatedRevenue
FROM fact_online_retail_transactions;

-- 2. Real-Time Monthly Time-Series View
CREATE VIEW vw_realtime_monthly AS
SELECT 
    SUBSTR(InvoiceDate, 1, 7) AS YearMonth,
    COALESCE(SUM(CASE WHEN IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0 THEN Quantity * UnitPrice ELSE 0 END), 0.0) AS CompletedRevenue,
    COUNT(DISTINCT CASE WHEN IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0 THEN InvoiceNo END) AS CompletedOrders,
    COUNT(DISTINCT CASE WHEN IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0 AND CustomerID IS NOT NULL AND CustomerID != '' THEN CustomerID END) AS UniqueCustomers
FROM fact_online_retail_transactions
GROUP BY SUBSTR(InvoiceDate, 1, 7)
ORDER BY YearMonth ASC;

-- 3. Real-Time Top Products View
CREATE VIEW vw_realtime_top_products AS
SELECT 
    StockCode,
    MAX(Description) AS Description,
    COALESCE(SUM(CASE WHEN IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0 THEN Quantity * UnitPrice ELSE 0 END), 0.0) AS CompletedRevenue,
    COALESCE(SUM(CASE WHEN IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0 THEN Quantity ELSE 0 END), 0) AS TotalQuantity,
    COUNT(DISTINCT CASE WHEN IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0 THEN InvoiceNo END) AS CompletedOrders
FROM fact_online_retail_transactions
WHERE StockCode IS NOT NULL AND StockCode != ''
GROUP BY StockCode
ORDER BY CompletedRevenue DESC;

-- 4. Real-Time Top Countries View
CREATE VIEW vw_realtime_top_countries AS
SELECT 
    Country,
    COALESCE(SUM(CASE WHEN IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0 THEN Quantity * UnitPrice ELSE 0 END), 0.0) AS CompletedRevenue,
    COUNT(DISTINCT CASE WHEN IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0 THEN InvoiceNo END) AS CompletedOrders,
    COUNT(DISTINCT CASE WHEN IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0 AND CustomerID IS NOT NULL AND CustomerID != '' THEN CustomerID END) AS UniqueCustomers
FROM fact_online_retail_transactions
WHERE Country IS NOT NULL AND Country != ''
GROUP BY Country
ORDER BY CompletedRevenue DESC;
