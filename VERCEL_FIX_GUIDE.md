# Vercel Deployment Fix Guide

## 🔴 Problem
Your Vercel frontend (`https://realestate-fraud-frontend.vercel.app`) cannot connect to your backend because:
1. CORS is not allowing your Vercel domain
2. The backend needs to be deployed and accessible from the internet

## ✅ Solutions Applied

### 1. Frontend Fix (Already Done)
- ✅ Updated `App.jsx` to use environment variable for API URL
- ✅ Frontend will now use `VITE_API_BASE_URL` from `.env`

### 2. Backend CORS Fix (Already Done)
- ✅ Added Vercel domain to CORS allowed origins
- ✅ Updated `backend/app/config.py`
- ✅ Updated `backend/.env`

### 3. Backend Deployment (Required)

Your backend is already deployed on Render:
**URL:** https://fraud-detection-api-8w4r.onrender.com

## 🚀 Steps to Fix Vercel Deployment

### Step 1: Update Backend Environment Variables on Render

1. Go to your Render dashboard: https://dashboard.render.com
2. Find your backend service: `fraud-detection-api-8w4r`
3. Go to **Environment** tab
4. Add/Update this environment variable:

```
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000,https://realestate-fraud-frontend.vercel.app,https://*.vercel.app
```

Or use wildcard for all origins (less secure but works):
```
CORS_ORIGINS=*
```

5. Click **Save Changes**
6. Wait for the service to redeploy

### Step 2: Verify Backend CORS

Test the backend CORS by running this in your browser console on Vercel:

```javascript
fetch('https://fraud-detection-api-8w4r.onrender.com/health')
  .then(res => res.json())
  .then(data => console.log('Backend is accessible:', data))
  .catch(err => console.error('CORS Error:', err));
```

### Step 3: Redeploy Frontend on Vercel

1. Go to Vercel dashboard: https://vercel.com/dashboard
2. Find your project: `realestate-fraud-frontend`
3. Go to **Settings** → **Environment Variables**
4. Verify this variable exists:
   ```
   VITE_API_BASE_URL=https://fraud-detection-api-8w4r.onrender.com
   ```
5. Go to **Deployments** tab
6. Click **Redeploy** on the latest deployment

### Step 4: Test the Deployed Site

1. Visit: https://realestate-fraud-frontend.vercel.app
2. Fill in the form with test data
3. Submit and check if it works

## 🔧 Alternative: Quick Fix with CORS Middleware

If you have access to the Render backend code, update `backend/app/main.py`:

```python
# Update CORS middleware to allow all origins temporarily
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for testing)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)
```

Then redeploy on Render.

## 📝 Environment Variables Summary

### Backend (Render)
```bash
ALLOWED_ORIGINS=https://realestate-fraud-frontend.vercel.app,http://localhost:5173
# OR for all origins:
CORS_ORIGINS=*
```

### Frontend (Vercel)
```bash
VITE_API_BASE_URL=https://fraud-detection-api-8w4r.onrender.com
```

## 🧪 Testing Locally

Your local setup is already fixed! Test it:

1. **Backend:** http://localhost:8000
2. **Frontend:** http://localhost:5173

Both should work together now.

## ⚠️ Important Notes

1. **Render Free Tier:** Your backend may spin down after inactivity. First request might take 30-60 seconds.
2. **CORS Security:** Using `*` for CORS is not recommended for production. Use specific domains.
3. **Environment Variables:** Make sure to set them on both Render and Vercel platforms, not just in local files.

## 🎯 Quick Checklist

- [ ] Update ALLOWED_ORIGINS on Render dashboard
- [ ] Redeploy backend on Render
- [ ] Verify VITE_API_BASE_URL on Vercel
- [ ] Redeploy frontend on Vercel
- [ ] Test the deployed site

## 🔗 Useful Links

- **Render Dashboard:** https://dashboard.render.com
- **Vercel Dashboard:** https://vercel.com/dashboard
- **Your Backend:** https://fraud-detection-api-8w4r.onrender.com
- **Your Frontend:** https://realestate-fraud-frontend.vercel.app

---

**Last Updated:** February 3, 2026, 3:58 PM IST
