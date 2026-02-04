# 🚀 FINAL FIX - Testing Guide

## ✅ What Was Fixed

1. **Added environment-specific config files**
   - `.env.development` - for local testing
   - `.env.production` - for Vercel builds

2. **Added debug logging** 
   - Console will show which API URL is being used
   - Check browser console (F12) to verify

3. **Restarted dev server**
   - Frontend now running at: http://localhost:5173

---

## 🧪 Test Locally NOW

### Step 1: Open Your Browser

Go to: **http://localhost:5173**

### Step 2: Open Browser Console

Press **F12** to open DevTools, then click **Console** tab

You should see:
```
🔗 API Base URL: https://fraud-detection-api-8w4r.onrender.com
🔧 Environment: development
📦 VITE_API_BASE_URL: https://fraud-detection-api-8w4r.onrender.com
```

### Step 3: Test Fraud Detection

Fill in the form with ANY data (example):

```
Property Type: Apartment
Price: 5000000
Area (sqft): 1200
Bedrooms: 2
Bathrooms: 2
Locality: Banjara Hills
City: Hyderabad
Description: Beautiful apartment with modern amenities
```

Click **"Detect Fraud"** button

### Expected Result: ✅

- Loading spinner appears
- After 3-10 seconds, results display:
  - Fraud Score
  - Risk Level
  - Analysis breakdown

### If You See Errors in Console: ❌

**Error 1: Still showing `localhost:8000`**
```
🔗 API Base URL: http://localhost:8000
```
**Fix:** The .env file didn't load. Stop the server (Ctrl+C) and restart:
```powershell
npm run dev
```

**Error 2: "CORS policy" error**
```
Access to XMLHttpRequest at '...' has been blocked by CORS
```
**Fix:** Backend is still deploying on Render. Wait 2-3 minutes.

**Error 3: "ERR_CONNECTION_REFUSED"**
```
Failed to load resource: net::ERR_CONNECTION_REFUSED
```
**Fix:** Backend might be asleep (Render free tier). The first request takes 30 seconds. Try again.

---

## 🌐 Test on Vercel (Production)

### Important: Set Environment Variable First!

Before testing on Vercel, you MUST:

1. Go to: https://vercel.com/dashboard
2. Select project: **realestate-fraud-frontend**
3. **Settings** → **Environment Variables**
4. Add:
   ```
   Name:  VITE_API_BASE_URL
   Value: https://fraud-detection-api-8w4r.onrender.com
   ```
5. Select all: Production, Preview, Development
6. Click **Save**
7. Go to **Deployments** tab
8. Wait for current deployment to finish OR click **Redeploy**

### Then Test on Vercel:

1. Go to: https://realestate-fraud-frontend.vercel.app
2. Open browser console (F12)
3. Look for debug logs:
   ```
   🔗 API Base URL: https://fraud-detection-api-8w4r.onrender.com
   ```
4. Fill form and click **"Detect Fraud"**
5. Should work! ✅

---

## 🔍 Debug Checklist

If it's STILL not working, check these in browser console:

### ✅ Good Signs:
- `🔗 API Base URL: https://fraud-detection-api-8w4r.onrender.com`
- `🚀 API Request: POST /api/analyze`
- `✅ API Response: 200 /api/analyze`

### ❌ Bad Signs (and fixes):

| Console Message | Problem | Solution |
|----------------|---------|----------|
| `localhost:8000` | Wrong URL | Restart dev server |
| `CORS policy error` | Backend not deployed | Wait 3 minutes |
| `ERR_CONNECTION_REFUSED` | Backend asleep | Try again (wait 30s) |
| `404 Not Found` | Wrong endpoint | Check API URL spelling |
| `500 Internal Error` | Backend crash | Check Render logs |

---

## 🎯 Quick Commands Reference

### Restart Frontend (Local)
```powershell
cd frontend
npm run dev
```

### Check What URL is Being Used
Open browser console at http://localhost:5173 and look for:
```
🔗 API Base URL: ...
```

### Test Backend Directly
Open in browser:
```
https://fraud-detection-api-8w4r.onrender.com/health
```
Should return: `{"status":"healthy",...}`

### Build for Production (to test like Vercel)
```powershell
cd frontend
npm run build
npm run preview
```
Then open: http://localhost:4173

---

## ⏱️ Current Status

- ✅ Frontend dev server running: http://localhost:5173
- ✅ Backend deployed on Render: https://fraud-detection-api-8w4r.onrender.com
- ✅ Code pushed to GitHub → Vercel auto-deploying
- ⏳ Waiting for Vercel deployment: ~2 minutes
- ⚠️ **Need to set Vercel environment variable!**

---

## 📞 Still Having Issues?

1. **Screenshot the browser console** (F12 → Console tab)
2. **Screenshot the Network tab** (F12 → Network tab → try the request again)
3. **Tell me what you see** in the console logs

The debug logs will tell us exactly what's wrong!

---

**Test NOW:** http://localhost:5173
**Expected:** Should work immediately! 🎉
