import os
import pandas as pd
import yaml
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def load_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    config_path = os.path.join(project_root, "config", "settings.yaml")
    
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def load_data():
    config = load_config()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    processed_path = os.path.join(project_root, config["processed_data"]["file_path"])
    
    print(f"Loading processed clean dataset from {processed_path}...")
    if not os.path.exists(processed_path):
        raise FileNotFoundError(f"Clean dataset not found at {processed_path}. Please run transform.py first.")
        
    df = pd.read_parquet(processed_path)
    print(f"Loaded {len(df):,} clean records ready for loading.")
    
    # 1. Local Storage Check (Parquet is already saved during transform, but we verify it here)
    print(f"Local storage confirmed: Parquet file is active at {processed_path}")
    
    # 2. Optional: Stream to SQL Database if credentials exist in .env
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "5432")
    db_name = os.getenv("DB_NAME")
    
    if db_password and db_password != "your_password_here":
        try:
            print("Connecting to PostgreSQL database...")
            connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            engine = create_engine(connection_string)
            
            # Write dataframe to SQL table (fact_sales)
            df.to_sql("fact_sales", engine, if_exists="replace", index=False)
            print("Successfully streamed clean dataset to PostgreSQL table 'fact_sales'.")
        except Exception as e:
            print(f"Database streaming skipped due to connection error: {e}")
    else:
        print("Database credentials not configured in .env. Skipping database load (local Parquet is fully sufficient for Power BI).")

if __name__ == "__main__":
    load_data()