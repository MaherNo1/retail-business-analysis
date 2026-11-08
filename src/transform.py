import os
import pandas as pd
import yaml

def load_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    config_path = os.path.join(project_root, "config", "settings.yaml")
    
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    config = load_config()
    rules = config["cleaning_rules"]
    
    print("Starting data transformation and cleaning...")
    initial_rows = len(df)
    
    # 1. Rename columns to match standard schema from settings.yaml
    df = df.rename(columns=config["column_mappings"])
    
    # 2. Filter out rows with missing Customer IDs (critical for customer-level analytics)
    df = df.dropna(subset=["customer_id"])
    
    # 3. Filter out cancellations (Invoice starting with 'C' or Quantity < min_quantity)
    df["invoice_no"] = df["invoice_no"].astype(str)
    cancellation_mask = (
        df["invoice_no"].str.startswith(rules["cancellation_prefix"]) | 
        (df["quantity"] < rules["min_quantity"])
    )
    df = df[~cancellation_mask]
    
    # 4. Remove non-inventory administrative stock codes
    df["stock_code"] = df["stock_code"].astype(str).str.strip().str.upper()
    df = df[~df["stock_code"].isin(rules["excluded_stock_codes"])]
    
    # 5. Remove price anomalies (UnitPrice <= 0)
    df = df[df["unit_price"] >= rules["min_unit_price"]]
    
    # 6. Type conversions
    df["invoice_date"] = pd.to_datetime(df["invoice_date"])
    # Clean up customer_id string format (removes trailing decimals if read as float previously)
    df["customer_id"] = df["customer_id"].astype(str).str.split(".").str[0]
    
    # 7. Drop exact duplicate rows
    df = df.drop_duplicates()
    
    # 8. Feature Engineering: Calculate Total Sales per transaction line
    df["total_sales"] = df["quantity"] * df["unit_price"]
    
    final_rows = len(df)
    print(f"Cleaning complete. Kept {final_rows:,} rows out of {initial_rows:,} ({initial_rows - final_rows:,} rows removed/filtered).")
    
    return df

if __name__ == "__main__":
    config = load_config()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    interim_path = os.path.join(project_root, config["interim_data"]["file_path"])
    processed_path = os.path.join(project_root, config["processed_data"]["file_path"])
    
    print(f"Loading interim raw data from {interim_path}...")
    raw_df = pd.read_parquet(interim_path)
    
    clean_df = transform_data(raw_df)
    
    # Save processed clean data
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    clean_df.to_parquet(processed_path, index=False)
    print(f"Processed clean dataset successfully saved to {processed_path}") 