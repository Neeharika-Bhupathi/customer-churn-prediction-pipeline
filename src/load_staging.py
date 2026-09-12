import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

# --- Database Configuration ---
# Put your EXACT MySQL root password here inside the quotes (special characters are handled automatically)
DB_USER = 'root'
DB_PASSWORD = 'Bhupathi@2004'
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_NAME = 'db_churn'

# Create a connection URL that safely handles special characters
connection_url = URL.create(
    drivername="mysql+pymysql",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

engine = create_engine(connection_url)

# Read the raw CSV dataset
csv_file_path = r"data\raw\Customer_Data.csv"
print("Reading CSV data...")
df = pd.read_csv(csv_file_path)

# Load DataFrame into MySQL staging table
print(f"Loading {len(df)} rows into 'stg_churn' table...")
df.to_sql(name='stg_churn', con=engine, if_exists='replace', index=False)

print("Load completed successfully!")