"""
Data Loader Utility
Loads the real estate dataset for fraud detection modules
"""
import pandas as pd
import os

# Dataset paths - Try India-wide dataset first, fallback to Mumbai
INDIA_DATA_FILE = "app/data/india_real_estate.csv"
MUMBAI_DATA_FILE = "app/data/real_estate.csv"

def load_dataset():
    """
    Load the real estate dataset
    
    Tries to load India-wide dataset first (Hyderabad + Mumbai),
    falls back to Mumbai-only dataset if not available.
    
    Returns:
        pd.DataFrame: Real estate dataset with columns:
            - Price: Property price
            - Area: Area in sqft
            - Location/Locality: Locality name
            - No. of Bedrooms: Number of bedrooms
            - City: City name (if available)
            - Plus other columns
    
    Raises:
        FileNotFoundError: If no dataset file exists
    """
    # Try India-wide dataset first
    if os.path.exists(INDIA_DATA_FILE):
        data_file = INDIA_DATA_FILE
        print(f"📂 Loading India-wide dataset: {INDIA_DATA_FILE}")
    elif os.path.exists(MUMBAI_DATA_FILE):
        data_file = MUMBAI_DATA_FILE
        print(f"📂 Loading Mumbai dataset: {MUMBAI_DATA_FILE}")
    else:
        raise FileNotFoundError(
            f"Dataset not found. Tried:\n"
            f"  1. {INDIA_DATA_FILE}\n"
            f"  2. {MUMBAI_DATA_FILE}\n"
            "Please generate the dataset first using generate_hyderabad_data.py"
        )
    
    # Load dataset
    df = pd.read_csv(data_file, encoding='utf-8', on_bad_lines='skip')
    
    # Standardize column names
    if 'Location' in df.columns and 'Locality' not in df.columns:
        df['Locality'] = df['Location']
    
    # Add City column if missing (for Mumbai-only dataset)
    if 'City' not in df.columns:
        df['City'] = 'Mumbai'
    
    print(f"✅ Dataset loaded: {len(df)} properties")
    if 'City' in df.columns:
        print(f"   Cities: {df['City'].unique().tolist()}")
    print(f"   Price range: ₹{df['Price'].min():,.0f} - ₹{df['Price'].max():,.0f}")
    
    return df
