import os
import pandas as pd
import yaml

def load_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    config_path = os.path.join(project_root, "config", "settings.yaml")
    
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def extract_data():
    config = load_config()
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    raw_path = os.path.join(project_root, config["raw_data"]["file_path"])
    interim_path = os.path.join(project_root, config["interim_data"]["file_path"])
    
    print(f"Reading raw Excel sheets from {raw_path}...")
    
    # Read Excel sheets with text columns explicitly set to string
    dtype_mapping = {
        "Invoice": str,
        "StockCode": str,
        "Description": str,
        "Customer ID": str
    }
    
    sheets_dict = pd.read_excel(
        raw_path, 
        sheet_name=config["raw_data"]["sheets"],
        dtype=dtype_mapping
    )
    
    # Concatenate both sheets
    combined_df = pd.concat(sheets_dict.values(), ignore_index=True)
    
    # Ensure all key text columns are explicitly converted to string to prevent Pyarrow type errors
    for col in ["Invoice", "StockCode", "Description", "Customer ID"]:
        if col in combined_df.columns:
            combined_df[col] = combined_df[col].astype(str)
            
    print(f"Extraction complete. Total raw records: {len(combined_df):,}")
    
    # Save interim parquet file
    os.makedirs(os.path.dirname(interim_path), exist_ok=True)
    combined_df.to_parquet(interim_path, index=False)
    print(f"Interim raw file saved successfully to {interim_path}")
    
    return combined_df

if __name__ == "__main__":
    extract_data()