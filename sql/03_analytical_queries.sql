USE db_churn;

-- 1. Executive Baseline KPIs
SELECT 
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Customer_Status = 'Churned' THEN 1 ELSE 0 END) AS total_churned,
    ROUND(SUM(CASE WHEN Customer_Status = 'Churned' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN Customer_Status = 'Churned' THEN Total_Revenue ELSE 0 END), 2) AS churned_revenue_loss
FROM prod_churn;

-- 2. Churn by Contract Type
SELECT 
    Contract,
    COUNT(*) AS customer_count,
    SUM(CASE WHEN Customer_Status = 'Churned' THEN 1 ELSE 0 END) AS churned_count,
    ROUND(SUM(CASE WHEN Customer_Status = 'Churned' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN Customer_Status = 'Churned' THEN Total_Revenue ELSE 0 END), 2) AS churned_revenue_loss
FROM prod_churn
GROUP BY Contract
ORDER BY churn_rate_pct DESC;

-- 3. Churn by Category Breakdown
WITH category_ranked AS (
    SELECT 
        Churn_Category,
        COUNT(*) AS churned_count,
        ROUND(SUM(Total_Revenue), 2) AS revenue_lost,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS pct_of_total_churn
    FROM prod_churn
    WHERE Customer_Status = 'Churned'
    GROUP BY Churn_Category
)
SELECT * 
FROM category_ranked
ORDER BY churned_count DESC;

-- 4. Deep Dive: Top Competitor Churn Drivers
WITH competitor_reasons AS (
    SELECT 
        Churn_Reason,
        COUNT(*) AS churned_count,
        ROUND(SUM(Total_Revenue), 2) AS revenue_lost,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS pct_within_competitor,
        DENSE_RANK() OVER (ORDER BY COUNT(*) DESC) AS rank_order
    FROM prod_churn
    WHERE Churn_Category = 'Competitor'
    GROUP BY Churn_Reason
)
SELECT * 
FROM competitor_reasons
ORDER BY rank_order;

-- 5. Tenure Cohort Risk Distribution
SELECT 
    CASE 
        WHEN Tenure_in_Months <= 6 THEN '01. 0 - 6 Months'
        WHEN Tenure_in_Months <= 12 THEN '02. 7 - 12 Months'
        WHEN Tenure_in_Months <= 24 THEN '03. 13 - 24 Months'
        ELSE '04. Over 24 Months'
    END AS tenure_cohort,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Customer_Status = 'Churned' THEN 1 ELSE 0 END) AS churned_count,
    ROUND(SUM(CASE WHEN Customer_Status = 'Churned' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct,
    ROUND(SUM(CASE WHEN Customer_Status = 'Churned' THEN Total_Revenue ELSE 0 END), 2) AS revenue_lost
FROM prod_churn
GROUP BY 1
ORDER BY 1;

-- 6. Add-On Service Bundle Impact
SELECT 
    Internet_Service,
    Online_Security,
    Premium_Support,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN Customer_Status = 'Churned' THEN 1 ELSE 0 END) AS churned_count,
    ROUND(SUM(CASE WHEN Customer_Status = 'Churned' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM prod_churn
GROUP BY Internet_Service, Online_Security, Premium_Support
ORDER BY churn_rate_pct DESC;