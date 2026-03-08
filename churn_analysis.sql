-- ============================================================
-- TELCO CUSTOMER CHURN ANALYSIS — SQL QUERIES
-- Author: Keerthi RK | Data Analyst
-- ============================================================

-- 1. Overall Churn Rate
SELECT 
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM customers;

-- 2. Churn Rate by Contract Type
SELECT 
    Contract,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS churned,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY Contract
ORDER BY churn_rate_pct DESC;

-- 3. Churn Rate by Tenure Group
SELECT 
    CASE 
        WHEN tenure BETWEEN 0  AND 12 THEN '0-12 months'
        WHEN tenure BETWEEN 13 AND 24 THEN '13-24 months'
        WHEN tenure BETWEEN 25 AND 36 THEN '25-36 months'
        WHEN tenure BETWEEN 37 AND 48 THEN '37-48 months'
        WHEN tenure BETWEEN 49 AND 60 THEN '49-60 months'
        ELSE '61+ months'
    END AS tenure_group,
    COUNT(*) AS total_customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY tenure_group
ORDER BY MIN(tenure);

-- 4. Average Monthly Charges: Churned vs Retained
SELECT 
    Churn,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges,
    ROUND(AVG(TotalCharges), 2)   AS avg_total_charges,
    COUNT(*) AS customer_count
FROM customers
GROUP BY Churn;

-- 5. Revenue at Risk by Contract Type
SELECT 
    Contract,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN MonthlyCharges ELSE 0 END), 2) AS monthly_revenue_lost,
    ROUND(SUM(CASE WHEN Churn = 'No'  THEN MonthlyCharges ELSE 0 END), 2) AS monthly_revenue_retained
FROM customers
GROUP BY Contract;

-- 6. High Risk Segment (most likely to churn)
SELECT 
    Contract,
    InternetService,
    PaymentMethod,
    COUNT(*) AS customers,
    ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(AVG(MonthlyCharges), 2) AS avg_monthly_charges
FROM customers
GROUP BY Contract, InternetService, PaymentMethod
HAVING COUNT(*) > 50
ORDER BY churn_rate_pct DESC
LIMIT 10;

-- 7. Customer Retention Funnel
SELECT 
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Churn = 'No' THEN 1 ELSE 0 END) AS active_customers,
    SUM(CASE WHEN Churn = 'No' AND tenure > 24 THEN 1 ELSE 0 END) AS longterm_customers,
    SUM(CASE WHEN Churn = 'No' AND tenure > 24 AND MonthlyCharges > 70 THEN 1 ELSE 0 END) AS high_value_customers
FROM customers;
