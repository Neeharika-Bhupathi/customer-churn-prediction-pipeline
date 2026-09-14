-- Create Database
CREATE DATABASE IF NOT EXISTS db_churn;
USE db_churn;

-- Drop table if exists for idempotency
DROP TABLE IF EXISTS stg_churn;

-- Create Raw Staging Table
CREATE TABLE stg_churn (
    Customer_ID VARCHAR(50) PRIMARY KEY,
    Gender VARCHAR(10),
    Age INT,
    Married VARCHAR(5),
    State VARCHAR(50),
    Number_of_Referrals INT,
    Tenure_in_Months INT,
    Value_Deal VARCHAR(50),
    Phone_Service VARCHAR(5),
    Multiple_Lines VARCHAR(5),
    Internet_Service VARCHAR(5),
    Internet_Type VARCHAR(50),
    Online_Security VARCHAR(5),
    Online_Backup VARCHAR(5),
    Device_Protection_Plan VARCHAR(5),
    Premium_Support VARCHAR(5),
    Streaming_TV VARCHAR(5),
    Streaming_Movies VARCHAR(5),
    Streaming_Music VARCHAR(5),
    Unlimited_Data VARCHAR(5),
    Contract VARCHAR(50),
    Paperless_Billing VARCHAR(5),
    Payment_Method VARCHAR(50),
    Monthly_Charge DECIMAL(10, 2),
    Total_Charges DECIMAL(10, 2),
    Total_Refunds DECIMAL(10, 2),
    Total_Extra_Data_Charges DECIMAL(10, 2),
    Total_Long_Distance_Charges DECIMAL(10, 2),
    Total_Revenue DECIMAL(10, 2),
    Customer_Status VARCHAR(20),
    Churn_Category VARCHAR(50),
    Churn_Reason VARCHAR(100)
);
