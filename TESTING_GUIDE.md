# Testing the Listing Form

## Quick Start Guide

### 1. Start the Backend
```powershell
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload
```

Backend will run at: http://localhost:8000

### 2. Start the Frontend
```powershell
cd frontend
npm run dev
```

Frontend will run at: http://localhost:5173

### 3. Test the Form

Open http://localhost:5173 in your browser and fill in the form with sample data:

**Sample Data:**
- **Title:** Spacious 3BHK Apartment in Prime Location
- **Description:** Beautiful 3BHK apartment with modern amenities, parking, and great view
- **Price:** 5000000
- **Area (sqft):** 1500
- **City:** Mumbai
- **Locality:** Andheri West
- **Latitude:** 19.1334
- **Longitude:** 72.8291

### 4. Submit and View Results

Click "🔍 Analyze for Fraud" button.

**Expected Response:**
```json
{
  "fraud_probability": 0.0,
  "fraud_types": [],
  "explanations": []
}
```

The result will show:
- ✅ Fraud Probability: 0.0% (green badge)
- ✅ Fraud Types: None detected
- ✅ Explanations: No issues found
- ✅ Raw JSON response (expandable)

## What's Working

✅ Form accepts all 8 fields from frozen schema
✅ Form validates required fields
✅ Form validates number ranges (lat/long, price, area)
✅ Submit button calls `/api/analyze` endpoint
✅ Backend receives data and validates it
✅ Backend returns dummy fraud report
✅ Frontend displays fraud report in readable format
✅ Raw JSON is available for inspection

## Troubleshooting

### Backend not running?
```powershell
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload
```

### Frontend not running?
```powershell
cd frontend
npm run dev
```

### CORS errors?
Check that backend is running on port 8000 and has CORS enabled in `app/main.py`

### Form not submitting?
- Check browser console for errors
- Ensure all required fields are filled
- Verify backend is accessible at http://localhost:8000
