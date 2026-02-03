# 🚀 Quick Start Guide - Truth in Listings

## Current Status: ✅ RUNNING

Both backend and frontend are currently running and operational!

---

## 🌐 Access Your Application

### Frontend (User Interface)
**URL:** http://localhost:5173

Open this in your browser to:
- Submit property listings for fraud analysis
- View detailed fraud reports
- Check analysis history

### Backend API (Documentation)
**URL:** http://localhost:8000/docs

Interactive API documentation where you can:
- Test API endpoints directly
- View request/response schemas
- Explore all available endpoints

---

## 🎮 How to Use

### 1. Open the Frontend
1. Open your browser
2. Navigate to: http://localhost:5173
3. You'll see the "Truth in Listings" fraud detection interface

### 2. Analyze a Property
Fill in the form with property details:
- **Title:** Property name/title
- **Description:** Detailed description
- **Price:** Property price in ₹
- **Area:** Property area in square feet
- **City:** City name (e.g., Mumbai, Hyderabad)
- **Locality:** Specific locality/neighborhood
- **Latitude & Longitude:** Geographic coordinates

### 3. View Results
After submission, you'll see:
- **Fraud Probability Score** (0-100%)
- **Fraud Types Detected** (if any)
- **Detailed Explanations** for each fraud indicator
- **Recommendations** on how to proceed

### 4. Check History
Click on "Fraud Database" tab to view:
- All previous analyses
- Saved property listings
- Historical fraud reports

---

## 🛠️ If You Need to Restart

### Stop Services
Press `Ctrl+C` in each terminal window to stop the services

### Start Backend
```bash
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload --port 8000
```

### Start Frontend
```bash
cd frontend
npm run dev
```

---

## 📊 Test the System

### Example Property Data
Use this sample data to test the system:

```
Title: Luxury 3BHK Apartment in Prime Location
Description: Beautiful 3BHK apartment with modern amenities, swimming pool, gym, and parking. Located in a prime area with excellent connectivity.
Price: 5000000
Area (sqft): 1500
City: Mumbai
Locality: Andheri West
Latitude: 19.1334
Longitude: 72.8291
```

---

## ✅ Everything is Working!

- ✅ Backend API running on port 8000
- ✅ Frontend UI running on port 5173
- ✅ CORS properly configured
- ✅ All endpoints responding correctly
- ✅ Database initialized
- ✅ No errors in console

---

## 🎯 What's Working

### Fraud Detection Features
- Price anomaly detection
- Description text analysis
- Location verification
- Geospatial accuracy checking
- Comprehensive fraud scoring

### User Interface
- Modern, professional design
- Responsive layout
- Real-time form validation
- Detailed result visualization
- Analysis history tracking

---

## 📝 Important Notes

1. **Both services must be running** for the application to work
2. **Backend runs on port 8000**, Frontend on port 5173
3. **Don't close the terminal windows** while using the application
4. **Check DEPLOYMENT_STATUS.md** for detailed system information

---

## 🐛 Troubleshooting

### If Frontend Can't Connect to Backend
- Make sure backend is running on port 8000
- Check that CORS is enabled (it is!)
- Verify no firewall blocking localhost

### If You See Errors
- Check terminal windows for error messages
- Restart both services
- Check that all dependencies are installed

---

## 🎉 You're All Set!

Your Real Estate Fraud Detection system is running smoothly with no errors!

**Start using it now:** http://localhost:5173

---

**Last Updated:** February 3, 2026, 3:48 PM IST
