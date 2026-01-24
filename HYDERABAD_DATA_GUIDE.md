# Adding India-Wide Data with Hyderabad Focus

## Overview

This guide explains how to add comprehensive India-wide real estate data with special focus on Hyderabad for improved fraud detection.

---

## Data Requirements

### Geographic Coverage

**Major Cities to Include**:
1. **Hyderabad** (Primary Focus - 40% of dataset)
2. Mumbai
3. Delhi NCR
4. Bangalore
5. Chennai
6. Pune
7. Kolkata
8. Ahmedabad

### Hyderabad Localities (High Priority)

**Premium Areas**:
- Banjara Hills
- Jubilee Hills
- Gachibowli
- Madhapur
- Hitech City
- Kondapur

**Mid-Range Areas**:
- Kukatpally
- Miyapur
- Manikonda
- Kompally
- Bachupally
- Nizampet

**Budget Areas**:
- LB Nagar
- Dilsukhnagar
- Uppal
- Secunderabad
- Ameerpet
- SR Nagar

---

## Sample Dataset Structure

### File: `backend/app/data/india_real_estate.csv`

**Required Columns**:
```
Price,Area,Location,No. of Bedrooms,City,Locality,Latitude,Longitude,Property_Type,Furnishing_Status
```

### Sample Data (Hyderabad Focus)

```csv
Price,Area,Location,No. of Bedrooms,City,Locality,Latitude,Longitude,Property_Type,Furnishing_Status
8500000,1400,Banjara Hills,3,Hyderabad,Banjara Hills,17.4239,78.4738,Apartment,Semi-Furnished
12000000,2200,Jubilee Hills,4,Hyderabad,Jubilee Hills,17.4326,78.4071,Villa,Fully-Furnished
6500000,1200,Gachibowli,2,Hyderabad,Gachibowli,17.4400,78.3489,Apartment,Semi-Furnished
9500000,1800,Madhapur,3,Hyderabad,Madhapur,17.4483,78.3915,Apartment,Fully-Furnished
15000000,3000,Hitech City,4,Hyderabad,Hitech City,17.4475,78.3667,Penthouse,Fully-Furnished
7200000,1500,Kondapur,3,Hyderabad,Kondapur,17.4650,78.3647,Apartment,Semi-Furnished
5500000,1100,Kukatpally,2,Hyderabad,Kukatpally,17.4948,78.3985,Apartment,Unfurnished
4800000,950,Miyapur,2,Hyderabad,Miyapur,17.4967,78.3583,Apartment,Unfurnished
6000000,1300,Manikonda,2,Hyderabad,Manikonda,17.4019,78.3867,Apartment,Semi-Furnished
5200000,1000,Kompally,2,Hyderabad,Kompally,17.5500,78.4900,Apartment,Unfurnished
4500000,900,Bachupally,2,Hyderabad,Bachupally,17.5450,78.3850,Apartment,Unfurnished
5800000,1200,Nizampet,2,Hyderabad,Nizampet,17.5100,78.3900,Apartment,Semi-Furnished
3500000,850,LB Nagar,2,Hyderabad,LB Nagar,17.3500,78.5520,Apartment,Unfurnished
3800000,900,Dilsukhnagar,2,Hyderabad,Dilsukhnagar,17.3687,78.5244,Apartment,Unfurnished
4200000,1000,Uppal,2,Hyderabad,Uppal,17.4062,78.5591,Apartment,Semi-Furnished
4500000,950,Secunderabad,2,Hyderabad,Secunderabad,17.4399,78.4983,Apartment,Semi-Furnished
5000000,1100,Ameerpet,2,Hyderabad,Ameerpet,17.4374,78.4482,Apartment,Semi-Furnished
4800000,1000,SR Nagar,2,Hyderabad,SR Nagar,17.4300,78.4550,Apartment,Unfurnished
```

---

## Hyderabad-Specific Fraud Patterns

### 1. Price Fraud Indicators

**Premium Areas (Banjara Hills, Jubilee Hills)**:
- Normal Range: ₹6,000-15,000 per sqft
- Fraud Alert: < ₹4,000 or > ₹20,000 per sqft

**Mid-Range Areas (Gachibowli, Madhapur, Hitech City)**:
- Normal Range: ₹4,500-8,000 per sqft
- Fraud Alert: < ₹3,000 or > ₹12,000 per sqft

**Budget Areas (LB Nagar, Dilsukhnagar)**:
- Normal Range: ₹3,500-5,500 per sqft
- Fraud Alert: < ₹2,500 or > ₹8,000 per sqft

### 2. Location-Specific Keywords (Text Fraud)

**Hyderabad-Specific Scam Phrases**:
- "Near Hitech City" (when actually in outskirts)
- "Gachibowli vicinity" (vague location)
- "Financial District adjacent" (misleading)
- "Metro connectivity" (when no metro nearby)
- "IT corridor" (overused, vague)

### 3. Coordinate Fraud Hotspots

**Common Mismatches**:
- Claims "Jubilee Hills" but coordinates point to Kukatpally
- Claims "Gachibowli" but coordinates point to Miyapur
- Claims "Banjara Hills" but coordinates point to LB Nagar

---

## Implementation Guide

### Step 1: Download/Create Dataset

**Option A: Use Existing Public Datasets**
- Kaggle: "India House Price Prediction"
- MagicBricks/99acres scraped data (with permission)
- Government property registration data

**Option B: Create Synthetic Dataset**
```python
# backend/app/data/generate_hyderabad_data.py

import pandas as pd
import numpy as np

# Hyderabad localities with price ranges (per sqft)
localities = {
    'Banjara Hills': {'min': 6000, 'max': 15000, 'lat': 17.4239, 'lon': 78.4738},
    'Jubilee Hills': {'min': 7000, 'max': 15000, 'lat': 17.4326, 'lon': 78.4071},
    'Gachibowli': {'min': 4500, 'max': 8000, 'lat': 17.4400, 'lon': 78.3489},
    'Madhapur': {'min': 5000, 'max': 8500, 'lat': 17.4483, 'lon': 78.3915},
    'Hitech City': {'min': 5500, 'max': 9000, 'lat': 17.4475, 'lon': 78.3667},
    'Kondapur': {'min': 4500, 'max': 7500, 'lat': 17.4650, 'lon': 78.3647},
    'Kukatpally': {'min': 4000, 'max': 6500, 'lat': 17.4948, 'lon': 78.3985},
    'Miyapur': {'min': 3800, 'max': 6000, 'lat': 17.4967, 'lon': 78.3583},
    'Manikonda': {'min': 4200, 'max': 6800, 'lat': 17.4019, 'lon': 78.3867},
    'LB Nagar': {'min': 3500, 'max': 5500, 'lat': 17.3500, 'lon': 78.5520},
    'Dilsukhnagar': {'min': 3600, 'max': 5800, 'lat': 17.3687, 'lon': 78.5244},
    'Uppal': {'min': 3700, 'max': 6000, 'lat': 17.4062, 'lon': 78.5591},
}

def generate_hyderabad_data(num_properties=2000):
    data = []
    
    for _ in range(num_properties):
        # Select random locality
        locality = np.random.choice(list(localities.keys()))
        loc_info = localities[locality]
        
        # Generate area (sqft)
        area = np.random.randint(800, 3000)
        
        # Generate price per sqft within locality range
        price_per_sqft = np.random.randint(loc_info['min'], loc_info['max'])
        
        # Calculate total price
        price = area * price_per_sqft
        
        # Add some noise to coordinates (±0.01 degrees)
        lat = loc_info['lat'] + np.random.uniform(-0.01, 0.01)
        lon = loc_info['lon'] + np.random.uniform(-0.01, 0.01)
        
        # Generate other attributes
        bedrooms = np.random.choice([1, 2, 3, 4], p=[0.1, 0.5, 0.3, 0.1])
        property_type = np.random.choice(['Apartment', 'Villa', 'Penthouse'], p=[0.8, 0.15, 0.05])
        furnishing = np.random.choice(['Unfurnished', 'Semi-Furnished', 'Fully-Furnished'], p=[0.4, 0.4, 0.2])
        
        data.append({
            'Price': price,
            'Area': area,
            'Location': locality,
            'No. of Bedrooms': bedrooms,
            'City': 'Hyderabad',
            'Locality': locality,
            'Latitude': lat,
            'Longitude': lon,
            'Property_Type': property_type,
            'Furnishing_Status': furnishing
        })
    
    df = pd.DataFrame(data)
    return df

# Generate and save
df = generate_hyderabad_data(2000)
df.to_csv('backend/app/data/hyderabad_real_estate.csv', index=False)
print(f"Generated {len(df)} Hyderabad properties")
```

### Step 2: Update Data Loader

**File**: `backend/app/utils/data_loader.py`

```python
import pandas as pd
import os

# Support multiple datasets
DATASETS = {
    'mumbai': 'app/data/real_estate.csv',  # Original
    'hyderabad': 'app/data/hyderabad_real_estate.csv',  # New
    'india': 'app/data/india_real_estate.csv',  # Combined
}

def load_dataset(dataset_name='india'):
    """
    Load real estate dataset
    
    Args:
        dataset_name: 'mumbai', 'hyderabad', or 'india' (default)
    
    Returns:
        pandas DataFrame
    """
    dataset_path = DATASETS.get(dataset_name, DATASETS['india'])
    
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")
    
    df = pd.read_csv(dataset_path)
    
    # Standardize column names
    column_mapping = {
        'Price': 'price',
        'Area': 'area_sqft',
        'Location': 'locality',
        'No. of Bedrooms': 'bedrooms',
        'City': 'city',
        'Locality': 'locality',
        'Latitude': 'latitude',
        'Longitude': 'longitude'
    }
    
    df = df.rename(columns=column_mapping)
    
    print(f"✅ Loaded {len(df)} properties from {dataset_name} dataset")
    print(f"   Cities: {df['city'].unique()}")
    print(f"   Price range: ₹{df['price'].min():,.0f} - ₹{df['price'].max():,.0f}")
    
    return df
```

### Step 3: Update Locality Coordinates

**File**: `backend/app/data/locality_coordinates.json`

```json
{
  "Hyderabad": {
    "Banjara Hills": {"latitude": 17.4239, "longitude": 78.4738},
    "Jubilee Hills": {"latitude": 17.4326, "longitude": 78.4071},
    "Gachibowli": {"latitude": 17.4400, "longitude": 78.3489},
    "Madhapur": {"latitude": 17.4483, "longitude": 78.3915},
    "Hitech City": {"latitude": 17.4475, "longitude": 78.3667},
    "Kondapur": {"latitude": 17.4650, "longitude": 78.3647},
    "Kukatpally": {"latitude": 17.4948, "longitude": 78.3985},
    "Miyapur": {"latitude": 17.4967, "longitude": 78.3583},
    "Manikonda": {"latitude": 17.4019, "longitude": 78.3867},
    "Kompally": {"latitude": 17.5500, "longitude": 78.4900},
    "Bachupally": {"latitude": 17.5450, "longitude": 78.3850},
    "Nizampet": {"latitude": 17.5100, "longitude": 78.3900},
    "LB Nagar": {"latitude": 17.3500, "longitude": 78.5520},
    "Dilsukhnagar": {"latitude": 17.3687, "longitude": 78.5244},
    "Uppal": {"latitude": 17.4062, "longitude": 78.5591},
    "Secunderabad": {"latitude": 17.4399, "longitude": 78.4983},
    "Ameerpet": {"latitude": 17.4374, "longitude": 78.4482},
    "SR Nagar": {"latitude": 17.4300, "longitude": 78.4550}
  },
  "Mumbai": {
    "Andheri West": {"latitude": 19.1334, "longitude": 72.8291},
    "Bandra West": {"latitude": 19.0596, "longitude": 72.8295},
    "Malad East": {"latitude": 19.1868, "longitude": 72.8493}
  },
  "Bangalore": {
    "Koramangala": {"latitude": 12.9352, "longitude": 77.6245},
    "Whitefield": {"latitude": 12.9698, "longitude": 77.7500},
    "Electronic City": {"latitude": 12.8456, "longitude": 77.6603}
  },
  "Delhi": {
    "Dwarka": {"latitude": 28.5921, "longitude": 77.0460},
    "Rohini": {"latitude": 28.7495, "longitude": 77.0736},
    "Saket": {"latitude": 28.5244, "longitude": 77.2066}
  }
}
```

---

## Hyderabad-Specific Test Cases

### Test Case H1: Normal Hyderabad Listing

```json
{
  "title": "Spacious 3BHK Apartment in Gachibowli",
  "description": "Well-maintained 3BHK apartment in Gachibowli with modern amenities, close to IT parks and metro station. Includes covered parking and 24/7 security.",
  "price": 8500000,
  "area_sqft": 1500,
  "city": "Hyderabad",
  "locality": "Gachibowli",
  "latitude": 17.4400,
  "longitude": 78.3489
}
```

**Expected**: Low fraud (0.10-0.20)

### Test Case H2: Hyderabad Price Fraud (Underpriced)

```json
{
  "title": "4BHK Villa in Jubilee Hills",
  "description": "Luxurious 4BHK villa in prime Jubilee Hills location with private garden, swimming pool, and premium finishes.",
  "price": 5000000,
  "area_sqft": 3000,
  "city": "Hyderabad",
  "locality": "Jubilee Hills",
  "latitude": 17.4326,
  "longitude": 78.4071
}
```

**Expected**: High fraud (0.75-0.90) - Jubilee Hills villa should be ₹20-30 crores

### Test Case H3: Hyderabad Location Fraud

```json
{
  "title": "Premium 2BHK in Hitech City",
  "description": "Brand new 2BHK apartment in Hitech City with excellent connectivity to IT companies and shopping malls.",
  "price": 7000000,
  "area_sqft": 1200,
  "city": "Hyderabad",
  "locality": "Hitech City",
  "latitude": 17.3500,
  "longitude": 78.5520
}
```

**Expected**: Medium fraud (0.50-0.65) - Coordinates point to LB Nagar, not Hitech City

### Test Case H4: Hyderabad Text Fraud

```json
{
  "title": "URGENT SALE! Gachibowli 3BHK - BEST DEAL!",
  "description": "HURRY! LIMITED TIME OFFER! This is a GUARANTEED investment in Gachibowli IT corridor. 100% SAFE property. Cash only, advance payment required. Don't miss this ONCE IN A LIFETIME opportunity!",
  "price": 9000000,
  "area_sqft": 1600,
  "city": "Hyderabad",
  "locality": "Gachibowli",
  "latitude": 17.4400,
  "longitude": 78.3489
}
```

**Expected**: Medium-High fraud (0.60-0.75) - Suspicious urgency keywords

---

## Data Sources for India-Wide Coverage

### Recommended Sources

1. **Kaggle Datasets**:
   - "India House Price Prediction"
   - "Real Estate Price Prediction India"
   - Search: "india real estate" on Kaggle

2. **Government Data**:
   - RERA (Real Estate Regulatory Authority) websites
   - State housing board data
   - Property registration data (public records)

3. **Web Scraping** (with permission):
   - MagicBricks.com
   - 99acres.com
   - Housing.com
   - **Note**: Check robots.txt and terms of service

4. **APIs**:
   - PropTiger API
   - CommonFloor API
   - **Note**: May require commercial license

---

## Quick Implementation Steps

### Step 1: Generate Hyderabad Data (5 minutes)

```bash
cd backend/app/data
python generate_hyderabad_data.py
```

### Step 2: Update Data Loader (2 minutes)

Edit `backend/app/utils/data_loader.py` to support multiple datasets

### Step 3: Update Coordinates File (3 minutes)

Add Hyderabad localities to `locality_coordinates.json`

### Step 4: Test with Hyderabad Data (5 minutes)

```bash
# Restart backend
cd backend
uvicorn app.main:app --reload

# Test with Hyderabad test cases
```

### Step 5: Update Frontend (Optional)

Add city dropdown in form:
```jsx
<select name="city">
  <option value="Hyderabad">Hyderabad</option>
  <option value="Mumbai">Mumbai</option>
  <option value="Bangalore">Bangalore</option>
  <option value="Delhi">Delhi</option>
</select>
```

---

## Expected Improvements

### With Hyderabad Data:

**Before**:
- Dataset: 6,347 properties (Mumbai only)
- Coverage: Limited to Mumbai localities
- Fraud detection: Mumbai-specific patterns

**After**:
- Dataset: 10,000+ properties (India-wide)
- Coverage: Hyderabad (40%), Mumbai (30%), Others (30%)
- Fraud detection: City-specific patterns
- Better price analysis per city
- Improved location verification

### Performance Impact:

- Analysis time: Still 2-5 seconds (efficient filtering)
- Memory usage: Slightly higher (acceptable)
- Accuracy: Improved for Hyderabad listings

---

## Maintenance

### Regular Updates:

1. **Quarterly**: Update price ranges based on market trends
2. **Monthly**: Add new localities as cities expand
3. **Weekly**: Review fraud patterns and update keywords

### Data Quality:

- Remove duplicates
- Validate coordinates
- Check price outliers
- Verify locality names

---

## Summary

**To add India-wide data with Hyderabad focus**:

1. ✅ Generate/download Hyderabad dataset (2,000+ properties)
2. ✅ Add Hyderabad localities to coordinates file
3. ✅ Update data loader to support multiple cities
4. ✅ Create Hyderabad-specific test cases
5. ✅ Test fraud detection with Hyderabad data

**Files to Create/Update**:
- `backend/app/data/hyderabad_real_estate.csv` (NEW)
- `backend/app/data/generate_hyderabad_data.py` (NEW)
- `backend/app/data/locality_coordinates.json` (UPDATE)
- `backend/app/utils/data_loader.py` (UPDATE)

**Result**: Comprehensive India-wide fraud detection with strong Hyderabad coverage!

---

**Guide Version**: 1.0  
**Last Updated**: January 20, 2026  
**Status**: ✅ Ready for Implementation
