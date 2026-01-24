# Dataset Download Guide

## 📊 Recommended Dataset

**Mumbai House Price Data (70k+ Entries)**
- **Source:** Kaggle
- **URL:** https://www.kaggle.com/datasets/sameep98/housing-prices-in-mumbai
- **Size:** 70,000+ entries
- **Year:** 2024
- **Source Website:** makaan.com

## ✅ Why This Dataset?

Perfect match for our frozen schema:
- ✅ **price** - House prices in INR
- ✅ **area** - Area in sq ft (matches our `area_sqft`)
- ✅ **locality** - Specific locality/neighborhood
- ✅ **city** - Mumbai (all entries)
- ✅ **latitude** - Geographic coordinates
- ✅ **longitude** - Geographic coordinates
- ✅ **title** - Can be derived from property type + bedrooms
- ✅ **description** - Can be derived from amenities

## 📥 How to Download

### Step 1: Install Kaggle CLI (One-time setup)

```powershell
# Install kaggle package
pip install kaggle
```

### Step 2: Get Kaggle API Token

1. Go to https://www.kaggle.com/
2. Sign in (create account if needed)
3. Click on your profile picture (top right)
4. Click "Settings"
5. Scroll to "API" section
6. Click "Create New Token"
7. This downloads `kaggle.json` file

### Step 3: Setup Kaggle Credentials

```powershell
# Create .kaggle directory in your user folder
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.kaggle"

# Move the downloaded kaggle.json to .kaggle folder
Move-Item -Path "$env:USERPROFILE\Downloads\kaggle.json" -Destination "$env:USERPROFILE\.kaggle\kaggle.json" -Force
```

### Step 4: Download the Dataset

```powershell
# Navigate to backend directory
cd c:\Users\kuruv\OneDrive\Desktop\major\backend

# Activate virtual environment
.\venv\Scripts\activate

# Download the dataset
kaggle datasets download -d sameep98/housing-prices-in-mumbai -p app/data --unzip

# The CSV will be in app/data/
```

## 🎯 Alternative: Manual Download

If Kaggle CLI doesn't work:

1. Go to: https://www.kaggle.com/datasets/sameep98/housing-prices-in-mumbai
2. Click "Download" button (you need to be logged in)
3. Extract the ZIP file
4. Copy the CSV file to: `c:\Users\kuruv\OneDrive\Desktop\major\backend\app\data\`
5. Rename it to: `real_estate.csv`

## 📋 Expected File Location

```
backend/
├── app/
│   ├── data/
│   │   └── real_estate.csv  ← Dataset goes here
│   ├── routers/
│   └── main.py
```

## 🔍 Dataset Columns (Expected)

Based on the dataset description, you should see columns like:
- `price` - House price in INR
- `area` - Area in square feet
- `locality` - Locality/neighborhood name
- `city` - City name (Mumbai)
- `latitude` - Latitude coordinate
- `longitude` - Longitude coordinate
- `bedrooms` - Number of bedrooms (BHK)
- `bathrooms` - Number of bathrooms
- `property_type` - Apartment/House/etc
- `furnishing` - Furnished/Semi-furnished/Unfurnished
- And more...

## ✅ Verification

After downloading, verify the file:

```powershell
# Check if file exists
Test-Path app/data/real_estate.csv

# Check file size (should be several MB)
(Get-Item app/data/real_estate.csv).Length / 1MB

# Preview first few lines
Get-Content app/data/real_estate.csv -Head 5
```

## 🎯 What's Next?

After downloading:
1. ✅ Dataset is in `backend/app/data/real_estate.csv`
2. ✅ Data will be messy (that's fine!)
3. ✅ Don't clean everything today
4. ✅ We'll use it for fraud detection logic

## 📝 Notes

- **Data is messy:** Yes, real-world data always is
- **Missing values:** Expected, we'll handle them
- **Inconsistent formats:** Normal, we'll deal with it
- **Don't over-clean:** We only need enough for fraud detection

## 🚨 Troubleshooting

### Kaggle CLI not working?
→ Use manual download method above

### File not found after download?
→ Check the extracted folder name, it might be different

### Permission denied?
→ Run PowerShell as Administrator

### Download too slow?
→ The file is large (70k+ entries), be patient

---

**Target:** `backend/app/data/real_estate.csv`

**Status:** Ready to download! 🚀
