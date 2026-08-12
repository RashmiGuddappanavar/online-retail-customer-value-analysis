-- =============================================================================
-- ONLINE RETAIL II ANALYTICS — PRODUCT ANALYSIS SQL
-- File: 04_product_analysis.sql
-- Purpose: Product performance analysis including top items by revenue, volume,
--          order frequency, average price, contribution, and regional ranking.
-- Database: online_retail_analytics
-- =============================================================================

USE online_retail_analytics;

-- -----------------------------------------------------------------------------
-- 1. TOP 10 PRODUCTS BY REVENUE & RANKING
-- Ranks products by monetary performance using DENSE_RANK().
-- Top product target: StockCode '22423' - 'REGENCY CAKESTAND 3 TIER'
-- -----------------------------------------------------------------------------
WITH ProductRevenue AS (
    SELECT 
        StockCode,
        MAX(Description) AS Description,
        SUM(Quantity) AS TotalUnitsSold,
        COUNT(DISTINCT InvoiceNo) AS OrderCount,
        ROUND(SUM(Revenue), 2) AS ProductRevenue,
        ROUND(AVG(UnitPrice), 2) AS AvgPrice
    FROM retail_transactions
    WHERE IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0
    GROUP BY StockCode
)
SELECT 
    StockCode,
    Description,
    TotalUnitsSold,
    OrderCount,
    AvgPrice,
    ProductRevenue,
    ROUND(ProductRevenue * 100.0 / (SELECT SUM(Revenue) FROM retail_transactions WHERE IsCancelled = 0), 2) AS RevenueContributionPct,
    DENSE_RANK() OVER (ORDER BY ProductRevenue DESC) AS RevenueRank
FROM ProductRevenue
ORDER BY ProductRevenue DESC
LIMIT 10;


-- -----------------------------------------------------------------------------
-- 2. TOP 10 PRODUCTS BY QUANTITY / VOLUME SOLD
-- Identifies items driving the highest unit sales.
-- -----------------------------------------------------------------------------
SELECT 
    StockCode,
    MAX(Description) AS Description,
    SUM(Quantity) AS TotalUnitsSold,
    COUNT(DISTINCT InvoiceNo) AS OrderCount,
    ROUND(SUM(Revenue), 2) AS TotalRevenue,
    DENSE_RANK() OVER (ORDER BY SUM(Quantity) DESC) AS VolumeRank
FROM retail_transactions
WHERE IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0
GROUP BY StockCode
ORDER BY TotalUnitsSold DESC
LIMIT 10;


-- -----------------------------------------------------------------------------
-- 3. TOP 10 PRODUCTS BY ORDER FREQUENCY (BASKET PENETRATION)
-- Ranks products by appearance count across completed invoices.
-- -----------------------------------------------------------------------------
SELECT 
    StockCode,
    MAX(Description) AS Description,
    COUNT(DISTINCT InvoiceNo) AS OrderCount,
    SUM(Quantity) AS TotalUnitsSold,
    ROUND(SUM(Revenue), 2) AS TotalRevenue,
    ROUND(COUNT(DISTINCT InvoiceNo) * 100.0 / (SELECT COUNT(DISTINCT InvoiceNo) FROM retail_transactions WHERE IsCancelled = 0), 2) AS BasketPenetrationPct
FROM retail_transactions
WHERE IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0
GROUP BY StockCode
ORDER BY OrderCount DESC
LIMIT 10;


-- -----------------------------------------------------------------------------
-- 4. PRODUCT PRICE BAND ANALYSIS
-- Categorizes products into price tiers and analyzes revenue contribution.
-- -----------------------------------------------------------------------------
WITH ProductPriceTier AS (
    SELECT 
        StockCode,
        AVG(UnitPrice) AS MeanPrice,
        SUM(Revenue) AS Revenue
    FROM retail_transactions
    WHERE IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0
    GROUP BY StockCode
)
SELECT 
    CASE 
        WHEN MeanPrice < 1.00 THEN 'Budget (< £1.00)'
        WHEN MeanPrice BETWEEN 1.00 AND 4.99 THEN 'Mid-Low (£1.00 - £4.99)'
        WHEN MeanPrice BETWEEN 5.00 AND 14.99 THEN 'Mid-High (£5.00 - £14.99)'
        ELSE 'Premium (>= £15.00)'
    END AS PriceCategory,
    COUNT(*) AS ProductCount,
    ROUND(SUM(Revenue), 2) AS CategoryRevenue,
    ROUND(SUM(Revenue) * 100.0 / (SELECT SUM(Revenue) FROM retail_transactions WHERE IsCancelled = 0), 2) AS RevenuePct
FROM ProductPriceTier
GROUP BY 
    CASE 
        WHEN MeanPrice < 1.00 THEN 'Budget (< £1.00)'
        WHEN MeanPrice BETWEEN 1.00 AND 4.99 THEN 'Mid-Low (£1.00 - £4.99)'
        WHEN MeanPrice BETWEEN 5.00 AND 14.99 THEN 'Mid-High (£5.00 - £14.99)'
        ELSE 'Premium (>= £15.00)'
    END
ORDER BY CategoryRevenue DESC;


-- -----------------------------------------------------------------------------
-- 5. TOP 3 PRODUCTS WITHIN TOP 5 REVENUE COUNTRIES
-- Partitioning using ROW_NUMBER() window function to identify regional bestsellers.
-- -----------------------------------------------------------------------------
WITH CountryProductRevenue AS (
    SELECT 
        Country,
        StockCode,
        MAX(Description) AS Description,
        SUM(Revenue) AS ProductCountryRevenue,
        ROW_NUMBER() OVER (PARTITION BY Country ORDER BY SUM(Revenue) DESC) AS RegionalRank
    FROM retail_transactions
    WHERE IsCancelled = 0 AND Quantity > 0 AND UnitPrice > 0
      AND Country IN ('United Kingdom', 'EIRE', 'Netherlands', 'Germany', 'France')
    GROUP BY Country, StockCode
)
SELECT 
    Country,
    RegionalRank,
    StockCode,
    Description,
    ROUND(ProductCountryRevenue, 2) AS ProductCountryRevenue
FROM CountryProductRevenue
WHERE RegionalRank <= 3
ORDER BY 
    CASE Country
        WHEN 'United Kingdom' THEN 1
        WHEN 'EIRE' THEN 2
        WHEN 'Netherlands' THEN 3
        WHEN 'Germany' THEN 4
        WHEN 'France' THEN 5
    END,
    RegionalRank;
