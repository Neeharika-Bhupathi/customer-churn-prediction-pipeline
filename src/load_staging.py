import os
from urllib.parse import quote_plus
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "db_churn")

safe_password = quote_plus(DB_PASSWORD)
connection_uri = f"mysql+pymysql://{DB_USER}:{safe_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(connection_uri)

# Read raw CSV data
csv_file_path = os.path.join("p1", "data", "raw", "Customer_Data.csv")
if not os.path.exists(csv_file_path):
    csv_file_path = os.path.join("data", "raw", "Customer_Data.csv")

print("Reading CSV data...")
df = pd.read_csv(csv_file_path)

# Load DataFrame into MySQL staging table
print(f"Loading {len(df)} rows into 'stg_churn' table...")
df.to_sql(name="stg_churn", con=engine, if_exists="replace", index=False)
print("Staging load completed successfully.")
