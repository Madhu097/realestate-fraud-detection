"""
Dataset Verification Script
Run this after downloading the dataset to verify it's working
"""
import pandas as pd
import os

# File path
DATA_FILE = "app/data/real_estate.csv"

def verify_dataset():
    """Verify the dataset exists and show basic info"""
    
    print("=" * 60)
    print("DATASET VERIFICATION")
    print("=" * 60)
    
    # Check if file exists
    if not os.path.exists(DATA_FILE):
        print(f"❌ ERROR: File not found at {DATA_FILE}")
        print("\nPlease download the dataset first!")
        print("See DATASET_DOWNLOAD.md for instructions")
        return
    
    print(f"✅ File found: {DATA_FILE}")
    
    # Get file size
    file_size = os.path.getsize(DATA_FILE) / (1024 * 1024)  # MB
    print(f"📦 File size: {file_size:.2f} MB")
    
    try:
        # Load the dataset
        print("\n📊 Loading dataset...")
        df = pd.read_csv(DATA_FILE)
        
        print(f"✅ Dataset loaded successfully!")
        print(f"📈 Total rows: {len(df):,}")
        print(f"📋 Total columns: {len(df.columns)}")
        
        # Show column names
        print("\n📋 Columns found:")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i}. {col}")
        
        # Show data types
        print("\n🔢 Data types:")
        print(df.dtypes)
        
        # Show first few rows
        print("\n👀 First 3 rows:")
        print(df.head(3))
        
        # Check for our required fields
        print("\n🔍 Checking for required fields:")
        required_fields = ['price', 'area', 'locality', 'city', 'latitude', 'longitude']
        
        for field in required_fields:
            # Check for exact match or similar column names
            matches = [col for col in df.columns if field.lower() in col.lower()]
            if matches:
                print(f"  ✅ {field}: Found as '{matches[0]}'")
            else:
                print(f"  ⚠️  {field}: Not found (we'll need to handle this)")
        
        # Show missing values
        print("\n🕳️  Missing values:")
        missing = df.isnull().sum()
        missing = missing[missing > 0]
        if len(missing) > 0:
            print(missing)
        else:
            print("  ✅ No missing values!")
        
        # Show basic statistics
        print("\n📊 Basic statistics:")
        print(df.describe())
        
        print("\n" + "=" * 60)
        print("✅ VERIFICATION COMPLETE!")
        print("=" * 60)
        print("\nDataset is ready to use! 🚀")
        
    except Exception as e:
        print(f"\n❌ ERROR loading dataset: {str(e)}")
        print("\nThe file might be corrupted or in wrong format.")
        print("Try downloading it again.")

if __name__ == "__main__":
    verify_dataset()
