"""
Dataset Analysis - Save to file to avoid encoding issues
"""
import pandas as pd
import os

DATA_FILE = "app/data/real_estate.csv"
OUTPUT_FILE = "dataset_info.txt"

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write("=" * 80 + "\n")
    f.write("DATASET ANALYSIS\n")
    f.write("=" * 80 + "\n\n")
    
    if not os.path.exists(DATA_FILE):
        f.write(f"ERROR: File not found at {DATA_FILE}\n")
    else:
        # File info
        file_size = os.path.getsize(DATA_FILE) / (1024 * 1024)
        f.write(f"File: {DATA_FILE}\n")
        f.write(f"Size: {file_size:.2f} MB\n\n")
        
        # Load dataset
        try:
            df = pd.read_csv(DATA_FILE, encoding='utf-8', on_bad_lines='skip')
            
            f.write(f"Total Rows: {len(df):,}\n")
            f.write(f"Total Columns: {len(df.columns)}\n\n")
            
            f.write("COLUMNS:\n")
            f.write("-" * 80 + "\n")
            for i, col in enumerate(df.columns, 1):
                dtype = df[col].dtype
                non_null = df[col].notna().sum()
                null_count = df[col].isna().sum()
                f.write(f"{i:2d}. {col:30s} | Type: {str(dtype):10s} | Non-null: {non_null:6,} | Null: {null_count:6,}\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("FIRST 5 ROWS:\n")
            f.write("=" * 80 + "\n")
            f.write(df.head(5).to_string())
            
            f.write("\n\n" + "=" * 80 + "\n")
            f.write("BASIC STATISTICS:\n")
            f.write("=" * 80 + "\n")
            f.write(df.describe().to_string())
            
            f.write("\n\n" + "=" * 80 + "\n")
            f.write("CHECKING FOR REQUIRED FIELDS:\n")
            f.write("=" * 80 + "\n")
            
            required_fields = {
                'price': ['price', 'Price', 'PRICE'],
                'area': ['area', 'Area', 'AREA', 'area_sqft', 'sqft'],
                'locality': ['locality', 'Locality', 'Location', 'location'],
                'city': ['city', 'City', 'CITY'],
                'latitude': ['latitude', 'Latitude', 'lat', 'Lat'],
                'longitude': ['longitude', 'Longitude', 'long', 'Long', 'lng']
            }
            
            for field, possible_names in required_fields.items():
                found = None
                for col in df.columns:
                    if col in possible_names or any(name.lower() in col.lower() for name in possible_names):
                        found = col
                        break
                
                if found:
                    f.write(f"✓ {field:15s} -> Found as '{found}'\n")
                else:
                    f.write(f"✗ {field:15s} -> NOT FOUND\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("SUCCESS! Dataset loaded and analyzed.\n")
            f.write("=" * 80 + "\n")
            
        except Exception as e:
            f.write(f"\nERROR loading dataset: {str(e)}\n")

print(f"Analysis saved to: {OUTPUT_FILE}")
print("Check the file for full details!")
