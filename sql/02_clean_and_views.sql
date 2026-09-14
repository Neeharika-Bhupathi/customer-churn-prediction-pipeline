USE db_churn;

-- Drop prior production table and views
DROP VIEW IF EXISTS vw_churn_data;
DROP VIEW IF EXISTS vw_join_data;
DROP TABLE IF EXISTS prod_churn;

-- 1. Create Cleaned Production Table with Null Imputation
CREATE TABLE prod_churn AS
SELECT 
    Customer_ID,
    Gender,
    Age,
    Married,
    State,
    Number_of_Referrals,
    Tenure_in_Months,
    COALESCE(Value_Deal, 'None') AS Value_Deal,
    Phone_Service,
    COALESCE(Multiple_Lines, 'No') AS Multiple_Lines,
    Internet_Service,
    COALESCE(Internet_Type, 'None') AS Internet_Type,
    COALESCE(Online_Security, 'No') AS Online_Security,
    COALESCE(Online_Backup, 'No') AS Online_Backup,
    COALESCE(Device_Protection_Plan, 'No') AS Device_Protection_Plan,
    COALESCE(Premium_Support, 'No') AS Premium_Support,
    COALESCE(Streaming_TV, 'No') AS Streaming_TV,
    COALESCE(Streaming_Movies, 'No') AS Streaming_Movies,
    COALESCE(Streaming_Music, 'No') AS Streaming_Music,
    COALESCE(Unlimited_Data, 'No') AS Unlimited_Data,
    Contract,
    Paperless_Billing,
    Payment_Method,
    Monthly_Charge,
    Total_Charges,
    Total_Refunds,
    Total_Extra_Data_Charges,
    Total_Long_Distance_Charges,
    Total_Revenue,
    Customer_Status,
    COALESCE(Churn_Category, 'Others') AS Churn_Category,
    COALESCE(Churn_Reason, 'Others') AS Churn_Reason
FROM stg_churn;

-- Add Primary Key to prod_churn
ALTER TABLE prod_churn ADD PRIMARY KEY (Customer_ID);

-- 2. Create Historical View for ML Training & Evaluation
CREATE VIEW vw_churn_data AS
SELECT *
FROM prod_churn
WHERE Customer_Status IN ('Churned', 'Stayed');

-- 3. Create Unscored View for Predictive Inference on New Joiners
CREATE VIEW vw_join_data AS
SELECT *
FROM prod_churn
WHERE Customer_Status = 'Joined';
