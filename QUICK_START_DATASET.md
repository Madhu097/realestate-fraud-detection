# 🚀 QUICK START: Download Dataset

## Option 1: Using Kaggle CLI (Recommended)

### Step 1: Install dependencies
```powershell
cd c:\Users\kuruv\OneDrive\Desktop\major\backend
.\venv\Scripts\activate
pip install -r requirements.txt
```

### Step 2: Setup Kaggle API
1. Go to https://www.kaggle.com/ and sign in
2. Click profile picture → Settings → API → "Create New Token"
3. This downloads `kaggle.json`
4. Run these commands:

```powershell
# Create .kaggle directory
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.kaggle"

# Move kaggle.json (adjust path if needed)
Move-Item -Path "$env:USERPROFILE\Downloads\kaggle.json" -Destination "$env:USERPROFILE\.kaggle\kaggle.json" -Force
```

### Step 3: Download dataset
```powershell
# Make sure you're in backend directory with venv activated
kaggle datasets download -d sameep98/housing-prices-in-mumbai -p app/data --unzip
```

### Step 4: Verify dataset
```powershell
python verify_dataset.py
```

---

## Option 2: Manual Download (If Kaggle CLI fails)

1. Go to: https://www.kaggle.com/datasets/sameep98/housing-prices-in-mumbai
2. Click "Download" (requires login)
3. Extract the ZIP file
4. Copy the CSV to: `c:\Users\kuruv\OneDrive\Desktop\major\backend\app\data\`
5. Rename to: `real_estate.csv`
6. Run: `python verify_dataset.py`

---

## ✅ Success Checklist

- [ ] File exists at: `backend/app/data/real_estate.csv`
- [ ] File size is several MB (70k+ rows)
- [ ] `python verify_dataset.py` runs without errors
- [ ] Dataset has columns: price, area, locality, city, latitude, longitude

---

## 🎯 What You Get

**Dataset:** Mumbai House Price Data
- **Rows:** 70,000+
- **Columns:** price, area, locality, city, lat, long, bedrooms, bathrooms, etc.
- **Year:** 2024
- **Source:** makaan.com

Perfect for fraud detection! 🔍

---

## 🚨 Troubleshooting

**Kaggle CLI not found?**
→ Make sure venv is activated and you ran `pip install -r requirements.txt`

**Permission denied on kaggle.json?**
→ Run PowerShell as Administrator

**Dataset download fails?**
→ Use Option 2 (Manual Download)

**verify_dataset.py shows errors?**
→ Check if CSV file is in correct location: `app/data/real_estate.csv`
