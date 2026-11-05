"""
Data Loader Utility
Loads the real estate dataset for fraud detection modules
"""
import pandas as pd
import os
from pathlib import Path

# Base data directory
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
INDIA_DATA_FILE = DATA_DIR / "india_real_estate.csv"
MUMBAI_DATA_FILE = DATA_DIR / "real_estate.csv"
HYDERABAD_DATA_FILE = DATA_DIR / "hyderabad_real_estate.csv"

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
    data_file = None
    if INDIA_DATA_FILE.exists():
        data_file = INDIA_DATA_FILE
    elif HYDERABAD_DATA_FILE.exists():
        data_file = HYDERABAD_DATA_FILE
    elif MUMBAI_DATA_FILE.exists():
        data_file = MUMBAI_DATA_FILE
    else:
        raise FileNotFoundError(
            f"Dataset not found. Tried:\n"
            f"  1. {INDIA_DATA_FILE}\n"
            f"  2. {HYDERABAD_DATA_FILE}\n"
            f"  3. {MUMBAI_DATA_FILE}\n"
            "Please run train_models.py to generate datasets."
        )
    
    try:
        print(f"[DataLoader] Loading dataset from {data_file.name}")
    except Exception:
        pass
        
    df = pd.read_csv(data_file, encoding='utf-8', on_bad_lines='skip')
    
    # Standardize column names
    if 'Location' in df.columns and 'Locality' not in df.columns:
        df['Locality'] = df['Location']
    elif 'Locality' in df.columns and 'Location' not in df.columns:
        df['Location'] = df['Locality']
        
    if 'No. of Bedrooms' in df.columns and 'Bedrooms' not in df.columns:
        df['Bedrooms'] = df['No. of Bedrooms']
        
    # Add City column if missing (for Mumbai-only dataset)
    if 'City' not in df.columns:
        df['City'] = 'Mumbai'
        
    # Ensure numeric columns
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df['Area'] = pd.to_numeric(df['Area'], errors='coerce')
    df = df.dropna(subset=['Price', 'Area'])
    
    if 'Price_Per_Sqft' not in df.columns:
        df['Price_Per_Sqft'] = df['Price'] / df['Area']
        
    try:
        print(f"[DataLoader] Dataset loaded: {len(df)} properties across {len(df['Locality'].unique())} localities.")
    except Exception:
        pass
        
    return df
