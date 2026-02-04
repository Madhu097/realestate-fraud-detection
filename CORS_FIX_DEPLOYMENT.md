# 🔧 CORS Error Fix - Deployment Instructions

## ✅ Issues Fixed

1. **CORS Policy Error** - Backend now allows Vercel frontend origin
2. **Credentials Mismatch** - Frontend and backend now aligned on credentials setting
3. **Connection Refused** - Proper backend URL configured

---

## 📝 Changes Made

### Backend ([main.py](backend/app/main.py))
- ✅ Added Vercel frontend URL to allowed origins
- ✅ Configured proper CORS headers
- ✅ Removed wildcard origin for security

### Frontend ([api.js](frontend/src/services/api.js))
- ✅ Set `withCredentials: false` to match backend
- ✅ Increased timeout to 30 seconds for analysis requests
- ✅ Better error messages

### Environment ([.env](frontend/.env))
- ✅ Set correct backend URL: `https://fraud-detection-api-8w4r.onrender.com`

---

## 🚀 Deployment Steps

### Step 1: Deploy Backend Changes

```powershell
# Navigate to backend directory
cd backend

# Check git status
git status

# Add changes
git add .

# Commit changes
git commit -m "Fix CORS for Vercel frontend"

# Push to GitHub (triggers Render auto-deploy)
git push origin main
```

**Wait 2-3 minutes** for Render to rebuild and deploy.

### Step 2: Deploy Frontend Changes

```powershell
# Navigate to frontend directory  
cd ../frontend

# Make sure node_modules are installed
npm install

# Build for production
npm run build

# Check git status
git status

# Add changes
git add .

# Commit changes
git commit -m "Fix CORS and API configuration"

# Push to GitHub (triggers Vercel auto-deploy)
git push origin main
```

**Vercel will automatically deploy** within 1-2 minutes.

---

## 🔍 Verify Deployment

### 1. Check Backend Health

Open in browser:
```
https://fraud-detection-api-8w4r.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "message": "Truth in Listings API is running"
}
```

### 2. Check CORS Headers

Open browser console on your Vercel site and run:
```javascript
fetch('https://fraud-detection-api-8w4r.onrender.com/health')
  .then(r => r.json())
  .then(console.log)
```

Should work without CORS errors.

### 3. Test Fraud Detection

1. Go to: `https://realestate-fraud-frontend.vercel.app`
2. Fill in the form with test data
3. Click "Detect Fraud"
4. Should see analysis results without errors

---

## 📌 Environment Variables on Vercel

Make sure these are set in your Vercel dashboard:

1. Go to: https://vercel.com/dashboard
2. Select your project: `realestate-fraud-frontend`
3. Go to: **Settings** → **Environment Variables**
4. Add/Update:

```
VITE_API_BASE_URL=https://fraud-detection-api-8w4r.onrender.com
```

5. Click **Save**
6. **Redeploy** (Deployments tab → Latest deployment → Redeploy)

---

## 🐛 If Still Getting Errors

### Error: "net::ERR_CONNECTION_REFUSED"

**Cause:** Backend is not running or wrong URL

**Fix:**
1. Check backend is live: https://fraud-detection-api-8w4r.onrender.com/health
2. Verify `.env` file has correct URL
3. Rebuild frontend: `npm run build`
4. Redeploy to Vercel

### Error: "No 'Access-Control-Allow-Origin' header"

**Cause:** Backend CORS not configured or old version deployed

**Fix:**
1. Check backend logs on Render dashboard
2. Manually redeploy backend on Render
3. Clear browser cache (Ctrl + Shift + R)
4. Test again

### Error: "CORS credentials mode is 'include'"

**Cause:** Mismatch between frontend and backend credentials

**Fix:**
- ✅ Already fixed in [api.js](frontend/src/services/api.js)
- Make sure to redeploy frontend

---

## 📱 Test URLs

- **Frontend (Vercel):** https://realestate-fraud-frontend.vercel.app
- **Backend (Render):** https://fraud-detection-api-8w4r.onrender.com
- **API Docs:** https://fraud-detection-api-8w4r.onrender.com/docs

---

## 💡 Quick Test Commands

### Local Testing
```powershell
# Backend (Terminal 1)
cd backend
uvicorn app.main:app --reload --port 8000

# Frontend (Terminal 2)
cd frontend
npm run dev
```

### Production Testing
```powershell
# Build and preview frontend
cd frontend
npm run build
npm run preview
```

Then open: http://localhost:4173

---

## ✅ Checklist

- [ ] Backend changes pushed to GitHub
- [ ] Render shows successful deployment
- [ ] Frontend changes pushed to GitHub
- [ ] Vercel shows successful deployment
- [ ] Environment variable set on Vercel
- [ ] Backend health check works
- [ ] Frontend loads without console errors
- [ ] Fraud detection button works
- [ ] Analysis results display correctly

---

## 📞 Need Help?

If errors persist:

1. Check browser console (F12) for detailed error messages
2. Check Render logs for backend errors
3. Check Vercel logs for frontend build errors
4. Verify all environment variables are set correctly

---

**Date Created:** February 3, 2026  
**Status:** Ready to Deploy
