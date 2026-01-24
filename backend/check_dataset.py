"""
Simple Dataset Check
Quick verification of the downloaded dataset
"""
import pandas as pd
import os
import sys

# Set UTF-8 encoding for output
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DATA_FILE = "app/data/real_estate.csv"

print("=" * 60)
print("DATASET CHECK")
print("=" * 60)

# Check if file exists
if not os.path.exists(DATA_FILE):
    print(f"ERROR: File not found at {DATA_FILE}")
    sys.exit(1)

print(f"File found: {DATA_FILE}")

# Get file size
file_size = os.path.getsize(DATA_FILE) / (1024 * 1024)
print(f"File size: {file_size:.2f} MB")

# Load dataset
try:
    df = pd.read_csv(DATA_FILE, encoding='utf-8', on_bad_lines='skip')
    print(f"\nDataset loaded!")
    print(f"Total rows: {len(df):,}")
    print(f"Total columns: {len(df.columns)}")
    
    print("\nColumns:")
    for i, col in enumerate(df.columns, 1):
        print(f"  {i}. {col}")
    
    print("\nFirst row sample:")
    print(df.head(1).to_string())
    
    print("\n" + "=" * 60)
    print("SUCCESS! Dataset is ready!")
    print("=" * 60)
    
except Exception as e:
    print(f"\nERROR: {str(e)}")
    sys.exit(1)
