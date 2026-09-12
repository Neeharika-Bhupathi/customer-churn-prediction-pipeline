import os
from urllib.parse import quote_plus
import joblib
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score

# Load environment variables
load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "db_churn")

safe_password = quote_plus(DB_PASSWORD)
DATABASE_URI = f"mysql+pymysql://{DB_USER}:{safe_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URI)

print("Fetching training data from vw_churn_data...")
query = "SELECT * FROM vw_churn_data"
df = pd.read_sql(query, con=engine)

# Exclude target, identifier, and leak columns
columns_to_drop = [
    'Customer_ID', 
    'Customer_Status', 
    'Churn_Category', 
    'Churn_Reason'
]
X = df.drop(columns=[col for col in columns_to_drop if col in df.columns])
y = (df['Customer_Status'] == 'Churned').astype(int)

# One-hot encode categorical features
X_encoded = pd.get_dummies(X, drop_first=True)

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X_encoded, y, test_size=0.2, random_state=42, stratify=y
)

# Train Random Forest
print("Training Random Forest Classifier...")
rf = RandomForestClassifier(
    n_estimators=100, 
    max_depth=10, 
    random_state=42, 
    n_jobs=-1
)
rf.fit(X_train, y_train)

# Evaluation
y_pred = rf.predict(X_test)
y_prob = rf.predict_proba(X_test)[:, 1]

print("\n--- Model Evaluation ---")
print(classification_report(y_test, y_pred))
print(f"ROC-AUC Score: {roc_auc_score(y_test, y_prob):.4f}")

# Persist trained model and feature alignment
os.makedirs("models", exist_ok=True)
joblib.dump(rf, "models/rf_churn_model.pkl")
joblib.dump(X_encoded.columns.tolist(), "models/model_features.pkl")
print("\nTrained model and feature list saved to models/")