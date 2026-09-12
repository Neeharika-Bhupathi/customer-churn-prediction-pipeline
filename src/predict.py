import os
from urllib.parse import quote_plus
import joblib
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load credentials
load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "db_churn")

safe_password = quote_plus(DB_PASSWORD)
DATABASE_URI = f"mysql+pymysql://{DB_USER}:{safe_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URI)

# Load artifacts
print("Loading model and feature metadata...")
rf_model = joblib.load("models/rf_churn_model.pkl")
model_features = joblib.load("models/model_features.pkl")

# Fetch unlabelled new customer data
print("Fetching unscored records from vw_join_data...")
query = "SELECT * FROM vw_join_data"
df_join = pd.read_sql(query, con=engine)

# Keep identifiers aside
customer_ids = df_join['Customer_ID']

# Clean and align features
columns_to_drop = [
    'Customer_ID', 
    'Customer_Status', 
    'Churn_Category', 
    'Churn_Reason'
]
X_unseen = df_join.drop(columns=[col for col in columns_to_drop if col in df_join.columns])
X_unseen_encoded = pd.get_dummies(X_unseen, drop_first=True)

# Reindex so feature names exactly match model training layout
X_unseen_aligned = X_unseen_encoded.reindex(columns=model_features, fill_value=0)

# Generate churn probabilities & predictions
print("Generating churn predictions...")
pred_probabilities = rf_model.predict_proba(X_unseen_aligned)[:, 1]
pred_labels = rf_model.predict(X_unseen_aligned)

# Build results dataframe
df_scored = df_join.copy()
df_scored['Churn_Prediction'] = pred_labels
df_scored['Churn_Probability'] = pred_probabilities.round(4)

# Assign risk segments
def assign_risk_segment(prob):
    if prob >= 0.65:
        return 'High Risk'
    elif prob >= 0.35:
        return 'Medium Risk'
    return 'Low Risk'

df_scored['Risk_Tier'] = df_scored['Churn_Probability'].apply(assign_risk_segment)

# Summary distribution
print("\n--- Churn Risk Cohort Distribution ---")
print(df_scored['Risk_Tier'].value_counts())

# Write back to MySQL
target_table = "prod_churn_predictions"
print(f"\nWriting scored results to MySQL table: {target_table}...")
df_scored.to_sql(target_table, con=engine, if_exists="replace", index=False)
print("Scoring process completed successfully.")