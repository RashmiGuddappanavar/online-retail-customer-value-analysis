-- =============================================================================
-- ONLINE RETAIL II ANALYTICS — CUSTOMER ANALYSIS SQL
-- File: 03_customer_analysis.sql
-- Purpose: Analytical queries answering core customer value, repeat purchasing,
--          RFM segmentation, and churn-risk proxy business questions.
-- Database: online_retail_analytics
-- =============================================================================

USE online_retail_analytics;

-- -----------------------------------------------------------------------------
-- 1. TOTAL, REPEAT, AND ONE-TIME CUSTOMER SUMMARY
-- Analyzes repeat customer rate across identified purchasing customers.
-- Target Repeat Rate: ~72.39% (4,255 repeat out of 5,878 total customers)
-- -----------------------------------------------------------------------------
WITH CustomerOrderCounts AS (
    SELECT 
        CustomerID,
        COUNT(DISTINCT InvoiceNo) AS TotalOrders,
        SUM(Revenue) AS CustomerRevenue
    FROM retail_transactions
    WHERE CustomerID IS NOT NULL AND IsCancelled = 0
    GROUP BY CustomerID
)
SELECT 
    COUNT(*) AS TotalIdentifiedCustomers,
    SUM(CASE WHEN TotalOrders > 1 THEN 1 ELSE 0 END) AS RepeatCustomersCount,
    SUM(CASE WHEN TotalOrders = 1 THEN 1 ELSE 0 END) AS OneTimeCustomersCount,
    ROUND(SUM(CASE WHEN TotalOrders > 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS RepeatCustomerRatePct,
    ROUND(SUM(CASE WHEN TotalOrders = 1 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS OneTimeCustomerRatePct
FROM CustomerOrderCounts;


-- -----------------------------------------------------------------------------
-- 2. TOP 10 CUSTOMERS BY REVENUE & RANKING
-- Uses DENSE_RANK() and RANK() window functions to order customer monetary value.
-- -----------------------------------------------------------------------------
WITH CustomerTotals AS (
    SELECT 
        CustomerID,
        COUNT(DISTINCT InvoiceNo) AS OrderCount,
        SUM(Quantity) AS TotalItemsPurchased,
        ROUND(SUM(Revenue), 2) AS TotalRevenue
    FROM retail_transactions
    WHERE CustomerID IS NOT NULL AND IsCancelled = 0
    GROUP BY CustomerID
)
SELECT 
    CustomerID,
    OrderCount,
    TotalItemsPurchased,
    TotalRevenue,
    RANK() OVER (ORDER BY TotalRevenue DESC) AS RevenueRank,
    DENSE_RANK() OVER (ORDER BY TotalRevenue DESC) AS RevenueDenseRank
FROM CustomerTotals
ORDER BY TotalRevenue DESC
LIMIT 10;


-- -----------------------------------------------------------------------------
-- 3. CUSTOMER ORDER FREQUENCY DISTRIBUTION
-- Groups customers by number of orders placed to analyze purchase cadence.
-- -----------------------------------------------------------------------------
WITH OrderFreq AS (
    SELECT 
        CustomerID,
        COUNT(DISTINCT InvoiceNo) AS OrderCount,
        SUM(Revenue) AS CustomerRevenue
    FROM retail_transactions
    WHERE CustomerID IS NOT NULL AND IsCancelled = 0
    GROUP BY CustomerID
)
SELECT 
    CASE 
        WHEN OrderCount = 1 THEN '1 Order (One-Time)'
        WHEN OrderCount BETWEEN 2 AND 5 THEN '2-5 Orders'
        WHEN OrderCount BETWEEN 6 AND 10 THEN '6-10 Orders'
        WHEN OrderCount BETWEEN 11 AND 20 THEN '11-20 Orders'
        ELSE '21+ Orders (Power Buyers)'
    END AS OrderBucket,
    COUNT(*) AS CustomerCount,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM OrderFreq), 2) AS CustomerPct,
    ROUND(SUM(CustomerRevenue), 2) AS TotalRevenueGenerated,
    ROUND(AVG(CustomerRevenue), 2) AS AvgSpendPerCustomer
FROM OrderFreq
GROUP BY 
    CASE 
        WHEN OrderCount = 1 THEN '1 Order (One-Time)'
        WHEN OrderCount BETWEEN 2 AND 5 THEN '2-5 Orders'
        WHEN OrderCount BETWEEN 6 AND 10 THEN '6-10 Orders'
        WHEN OrderCount BETWEEN 11 AND 20 THEN '11-20 Orders'
        ELSE '21+ Orders (Power Buyers)'
    END
ORDER BY MIN(OrderCount);


-- -----------------------------------------------------------------------------
-- 4. AVERAGE CUSTOMER REVENUE & SUMMARY METRICS
-- -----------------------------------------------------------------------------
SELECT 
    COUNT(DISTINCT CustomerID) AS TotalPurchasingCustomers,
    ROUND(SUM(Revenue), 2) AS TotalCustomerRevenue,
    ROUND(AVG(CustomerSpend), 2) AS MeanCustomerRevenue,
    ROUND(MAX(CustomerSpend), 2) AS MaxCustomerRevenue
FROM (
    SELECT CustomerID, SUM(Revenue) AS CustomerSpend
    FROM retail_transactions
    WHERE CustomerID IS NOT NULL AND IsCancelled = 0
    GROUP BY CustomerID
) t;


-- -----------------------------------------------------------------------------
-- 5. RFM SEGMENT DISTRIBUTION & METRICS
-- Queries customer_rfm table for segment count, revenue contribution,
-- average recency, frequency, and monetary values per segment.
-- -----------------------------------------------------------------------------
SELECT 
    CustomerSegment,
    COUNT(*) AS CustomerCount,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customer_rfm), 2) AS CustomerPct,
    ROUND(SUM(Monetary), 2) AS SegmentTotalRevenue,
    ROUND(SUM(Monetary) * 100.0 / (SELECT SUM(Monetary) FROM customer_rfm), 2) AS RevenueContributionPct,
    ROUND(AVG(Recency), 1) AS AvgRecencyDays,
    ROUND(AVG(Frequency), 1) AS AvgFrequencyOrders,
    ROUND(AVG(Monetary), 2) AS AvgMonetaryValue
FROM customer_rfm
GROUP BY CustomerSegment
ORDER BY SegmentTotalRevenue DESC;


-- -----------------------------------------------------------------------------
-- 6. CHURN-RISK PROXY DISTRIBUTION & PRIOR REVENUE IMPACT
-- Analyzes customer counts and historical monetary spend by risk tier.
-- High Risk (Churn Proxy): Recency > 90 days AND Frequency >= 2 orders.
-- -----------------------------------------------------------------------------
SELECT 
    ChurnRiskProxy,
    COUNT(*) AS CustomerCount,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM customer_rfm), 2) AS CustomerPct,
    ROUND(SUM(Monetary), 2) AS PriorHistoricalRevenue,
    ROUND(SUM(Monetary) * 100.0 / (SELECT SUM(Monetary) FROM customer_rfm), 2) AS RevenuePct,
    ROUND(AVG(Recency), 1) AS AvgRecencyDays,
    ROUND(AVG(Frequency), 1) AS AvgFrequencyOrders
FROM customer_rfm
GROUP BY ChurnRiskProxy
ORDER BY CustomerCount DESC;


-- -----------------------------------------------------------------------------
-- 7. DETAILED LIST OF TOP HIGH-RISK (CHURN PROXY) CUSTOMERS AT RISK
-- Extracts top high-risk customers sorted by past spend to prioritize win-back campaigns.
-- -----------------------------------------------------------------------------
SELECT 
    CustomerID,
    CustomerSegment,
    Recency AS DaysInactive,
    Frequency AS TotalOrdersPlaced,
    Monetary AS HistoricalRevenue,
    RFM_Score_Comb
FROM customer_rfm
WHERE ChurnRiskProxy = 'High Risk (Churn Proxy)'
ORDER BY Monetary DESC
LIMIT 15;
