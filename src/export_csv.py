import os
from urllib.parse import quote_plus
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "db_churn")

safe_password = quote_plus(DB_PASSWORD)
uri = f"mysql+pymysql://{DB_USER}:{safe_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(uri)

output_dir = os.path.join("data", "processed")
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "prod_churn_predictions.csv")

print("Exporting prod_churn_predictions to CSV...")
df = pd.read_sql("SELECT * FROM prod_churn_predictions", con=engine)
df.to_csv(output_path, index=False)
print(f"Saved successfully as {output_path}")
