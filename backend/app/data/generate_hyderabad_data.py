"""
Generate synthetic Hyderabad real estate dataset for fraud detection

This script creates a realistic dataset of Hyderabad properties with:
- 18 major localities
- Locality-specific price ranges
- Realistic property attributes
- Proper geospatial coordinates
"""

import pandas as pd
import numpy as np
import os

# Hyderabad localities with realistic price ranges (per sqft in INR)
HYDERABAD_LOCALITIES = {
    # Premium Areas
    'Banjara Hills': {
        'min_price_sqft': 6000, 'max_price_sqft': 15000,
        'lat': 17.4239, 'lon': 78.4738,
        'tier': 'premium'
    },
    'Jubilee Hills': {
        'min_price_sqft': 7000, 'max_price_sqft': 15000,
        'lat': 17.4326, 'lon': 78.4071,
        'tier': 'premium'
    },
    'Gachibowli': {
        'min_price_sqft': 4500, 'max_price_sqft': 8000,
        'lat': 17.4400, 'lon': 78.3489,
        'tier': 'premium'
    },
    'Madhapur': {
        'min_price_sqft': 5000, 'max_price_sqft': 8500,
        'lat': 17.4483, 'lon': 78.3915,
        'tier': 'premium'
    },
    'Hitech City': {
        'min_price_sqft': 5500, 'max_price_sqft': 9000,
        'lat': 17.4475, 'lon': 78.3667,
        'tier': 'premium'
    },
    'Kondapur': {
        'min_price_sqft': 4500, 'max_price_sqft': 7500,
        'lat': 17.4650, 'lon': 78.3647,
        'tier': 'premium'
    },
    
    # Mid-Range Areas
    'Kukatpally': {
        'min_price_sqft': 4000, 'max_price_sqft': 6500,
        'lat': 17.4948, 'lon': 78.3985,
        'tier': 'mid-range'
    },
    'Miyapur': {
        'min_price_sqft': 3800, 'max_price_sqft': 6000,
        'lat': 17.4967, 'lon': 78.3583,
        'tier': 'mid-range'
    },
    'Manikonda': {
        'min_price_sqft': 4200, 'max_price_sqft': 6800,
        'lat': 17.4019, 'lon': 78.3867,
        'tier': 'mid-range'
    },
    'Kompally': {
        'min_price_sqft': 3900, 'max_price_sqft': 6200,
        'lat': 17.5500, 'lon': 78.4900,
        'tier': 'mid-range'
    },
    'Bachupally': {
        'min_price_sqft': 3700, 'max_price_sqft': 5800,
        'lat': 17.5450, 'lon': 78.3850,
        'tier': 'mid-range'
    },
    'Nizampet': {
        'min_price_sqft': 3900, 'max_price_sqft': 6100,
        'lat': 17.5100, 'lon': 78.3900,
        'tier': 'mid-range'
    },
    
    # Budget Areas
    'LB Nagar': {
        'min_price_sqft': 3500, 'max_price_sqft': 5500,
        'lat': 17.3500, 'lon': 78.5520,
        'tier': 'budget'
    },
    'Dilsukhnagar': {
        'min_price_sqft': 3600, 'max_price_sqft': 5800,
        'lat': 17.3687, 'lon': 78.5244,
        'tier': 'budget'
    },
    'Uppal': {
        'min_price_sqft': 3700, 'max_price_sqft': 6000,
        'lat': 17.4062, 'lon': 78.5591,
        'tier': 'budget'
    },
    'Secunderabad': {
        'min_price_sqft': 4000, 'max_price_sqft': 6500,
        'lat': 17.4399, 'lon': 78.4983,
        'tier': 'mid-range'
    },
    'Ameerpet': {
        'min_price_sqft': 4200, 'max_price_sqft': 6800,
        'lat': 17.4374, 'lon': 78.4482,
        'tier': 'mid-range'
    },
    'SR Nagar': {
        'min_price_sqft': 4000, 'max_price_sqft': 6500,
        'lat': 17.4300, 'lon': 78.4550,
        'tier': 'mid-range'
    },
}


def generate_hyderabad_dataset(num_properties=2000, output_file=None):
    """
    Generate synthetic Hyderabad real estate dataset
    
    Args:
        num_properties: Number of properties to generate (default: 2000)
        output_file: Output CSV file path (default: auto-generated)
    
    Returns:
        pandas DataFrame
    """
    print(f"🏗️  Generating {num_properties} Hyderabad properties...")
    
    data = []
    
    for i in range(num_properties):
        # Select random locality
        locality = np.random.choice(list(HYDERABAD_LOCALITIES.keys()))
        loc_info = HYDERABAD_LOCALITIES[locality]
        
        # Generate area (sqft) - realistic distribution
        if loc_info['tier'] == 'premium':
            area = np.random.randint(1200, 3500)
        elif loc_info['tier'] == 'mid-range':
            area = np.random.randint(900, 2000)
        else:  # budget
            area = np.random.randint(700, 1500)
        
        # Generate price per sqft within locality range
        price_per_sqft = np.random.randint(
            loc_info['min_price_sqft'], 
            loc_info['max_price_sqft']
        )
        
        # Calculate total price
        price = area * price_per_sqft
        
        # Add some realistic variance (±10%)
        price = int(price * np.random.uniform(0.9, 1.1))
        
        # Add coordinate noise (±0.01 degrees ≈ 1km)
        lat = loc_info['lat'] + np.random.uniform(-0.01, 0.01)
        lon = loc_info['lon'] + np.random.uniform(-0.01, 0.01)
        
        # Generate bedrooms based on area
        if area < 800:
            bedrooms = 1
        elif area < 1200:
            bedrooms = 2
        elif area < 1800:
            bedrooms = 3
        else:
            bedrooms = np.random.choice([3, 4], p=[0.7, 0.3])
        
        # Property type distribution
        if loc_info['tier'] == 'premium':
            property_type = np.random.choice(
                ['Apartment', 'Villa', 'Penthouse'],
                p=[0.7, 0.2, 0.1]
            )
        else:
            property_type = np.random.choice(
                ['Apartment', 'Villa'],
                p=[0.9, 0.1]
            )
        
        # Furnishing status
        furnishing = np.random.choice(
            ['Unfurnished', 'Semi-Furnished', 'Fully-Furnished'],
            p=[0.4, 0.4, 0.2]
        )
        
        data.append({
            'Price': price,
            'Area': area,
            'Location': locality,
            'No. of Bedrooms': bedrooms,
            'City': 'Hyderabad',
            'Locality': locality,
            'Latitude': round(lat, 6),
            'Longitude': round(lon, 6),
            'Property_Type': property_type,
            'Furnishing_Status': furnishing
        })
        
        # Progress indicator
        if (i + 1) % 500 == 0:
            print(f"   Generated {i + 1}/{num_properties} properties...")
    
    df = pd.DataFrame(data)
    
    # Statistics
    print(f"\n✅ Generated {len(df)} properties")
    print(f"\n📊 Dataset Statistics:")
    print(f"   Price range: ₹{df['Price'].min():,.0f} - ₹{df['Price'].max():,.0f}")
    print(f"   Average price: ₹{df['Price'].mean():,.0f}")
    print(f"   Area range: {df['Area'].min()} - {df['Area'].max()} sqft")
    print(f"   Average area: {df['Area'].mean():.0f} sqft")
    print(f"\n🏘️  Localities: {len(df['Locality'].unique())}")
    print(f"   {', '.join(df['Locality'].unique()[:5])}...")
    print(f"\n🏠 Property Types:")
    print(df['Property_Type'].value_counts().to_string())
    
    # Save to CSV
    if output_file is None:
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, 'hyderabad_real_estate.csv')
    
    df.to_csv(output_file, index=False)
    print(f"\n💾 Saved to: {output_file}")
    
    return df


def generate_combined_india_dataset(hyderabad_properties=2000, 
                                    mumbai_properties=1500,
                                    other_properties=500):
    """
    Generate combined India-wide dataset
    
    Args:
        hyderabad_properties: Number of Hyderabad properties
        mumbai_properties: Number of Mumbai properties
        other_properties: Number of other city properties
    
    Returns:
        pandas DataFrame
    """
    print("🇮🇳 Generating India-wide dataset...\n")
    
    # Generate Hyderabad data
    hyderabad_df = generate_hyderabad_dataset(hyderabad_properties)
    
    # Load existing Mumbai data if available
    mumbai_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'real_estate.csv')
    
    if os.path.exists(mumbai_file):
        print(f"\n📂 Loading existing Mumbai data from {mumbai_file}...")
        mumbai_df = pd.read_csv(mumbai_file)
        
        # Standardize columns
        if 'City' not in mumbai_df.columns:
            mumbai_df['City'] = 'Mumbai'
        if 'Latitude' not in mumbai_df.columns:
            mumbai_df['Latitude'] = 19.0760  # Mumbai default
        if 'Longitude' not in mumbai_df.columns:
            mumbai_df['Longitude'] = 72.8777
        if 'Property_Type' not in mumbai_df.columns:
            mumbai_df['Property_Type'] = 'Apartment'
        if 'Furnishing_Status' not in mumbai_df.columns:
            mumbai_df['Furnishing_Status'] = 'Semi-Furnished'
        
        # Limit to requested number
        mumbai_df = mumbai_df.head(mumbai_properties)
        print(f"   Loaded {len(mumbai_df)} Mumbai properties")
    else:
        print(f"   Mumbai data not found, skipping...")
        mumbai_df = pd.DataFrame()
    
    # Combine datasets
    if not mumbai_df.empty:
        combined_df = pd.concat([hyderabad_df, mumbai_df], ignore_index=True)
    else:
        combined_df = hyderabad_df
    
    # Save combined dataset
    output_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'india_real_estate.csv')
    combined_df.to_csv(output_file, index=False)
    
    print(f"\n✅ Combined dataset created: {len(combined_df)} total properties")
    print(f"   Hyderabad: {len(hyderabad_df)}")
    if not mumbai_df.empty:
        print(f"   Mumbai: {len(mumbai_df)}")
    print(f"\n💾 Saved to: {output_file}")
    
    return combined_df


if __name__ == "__main__":
    print("=" * 60)
    print("  HYDERABAD REAL ESTATE DATA GENERATOR")
    print("=" * 60)
    print()
    
    # Option 1: Generate Hyderabad-only dataset
    print("Option 1: Generate Hyderabad-only dataset (2000 properties)")
    print("Option 2: Generate India-wide dataset (Hyderabad + Mumbai)")
    print()
    
    choice = input("Enter choice (1 or 2, default=2): ").strip() or "2"
    
    if choice == "1":
        df = generate_hyderabad_dataset(num_properties=2000)
    else:
        df = generate_combined_india_dataset(
            hyderabad_properties=2000,
            mumbai_properties=1500
        )
    
    print("\n" + "=" * 60)
    print("  GENERATION COMPLETE!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Update backend/app/data/locality_coordinates.json")
    print("2. Restart backend server")
    print("3. Test with Hyderabad test cases")
    print()
