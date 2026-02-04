# ⚡ Quick Fix - Set Vercel Environment Variable

## 🎯 What You Need to Do NOW

Your code changes are deployed, but you need to add one environment variable on Vercel:

### Step 1: Go to Vercel Dashboard

1. Open: https://vercel.com/dashboard
2. Click on your project: **realestate-fraud-frontend**

### Step 2: Add Environment Variable

1. Click on **Settings** tab
2. Click on **Environment Variables** in the sidebar
3. Add this variable:

```
Name:  VITE_API_BASE_URL
Value: https://fraud-detection-api-8w4r.onrender.com
```

4. Select all environments: **Production**, **Preview**, **Development**
5. Click **Save**

### Step 3: Redeploy

1. Go to **Deployments** tab
2. Find the latest deployment (should be deploying now)
3. Wait for it to finish OR
4. Click the **⋯** menu → **Redeploy** to trigger a new deployment

### Step 4: Test

After deployment completes (1-2 minutes):

1. Go to: https://realestate-fraud-frontend.vercel.app
2. Fill the form with any data
3. Click **"Detect Fraud"** button
4. You should see results! ✅

---

## 🎉 Expected Result

No more errors! You should see:
- ✅ Fraud score displayed
- ✅ Analysis results shown
- ✅ No CORS errors in browser console

---

## 📸 Screenshot Guide

### Environment Variable Settings Should Look Like:

```
┌─────────────────────────────────────────────┐
│ Add Environment Variable                    │
├─────────────────────────────────────────────┤
│ Name                                        │
│ VITE_API_BASE_URL                           │
│                                             │
│ Value                                       │
│ https://fraud-detection-api-8w4r.onrender.com│
│                                             │
│ Environments                                │
│ ☑ Production                                │
│ ☑ Preview                                   │
│ ☑ Development                               │
└─────────────────────────────────────────────┘
```

---

## ⏱️ Timeline

- **Backend (Render):** Already deploying - Wait 2-3 minutes
- **Frontend (Vercel):** Already deploying - Wait 1-2 minutes
- **Total Time:** ~5 minutes for everything to be live

---

## ✅ Success Indicators

### Backend is Ready:
Visit: https://fraud-detection-api-8w4r.onrender.com/health

Should return:
```json
{"status": "healthy", "message": "Truth in Listings API is running"}
```

### Frontend is Ready:
- No errors in browser console (F12)
- Fraud detection button works
- Results appear correctly

---

## 🆘 Troubleshooting

### "Still seeing CORS errors"
- Wait 5 minutes for both deployments to complete
- Hard refresh browser: `Ctrl + Shift + R`
- Clear browser cache
- Try incognito/private window

### "Connection refused"
- Check if Render backend is awake (first request may take 30 seconds)
- Visit the health endpoint to wake it up
- Try the analysis again

### "Environment variable not working"
- Make sure you saved it
- Make sure you redeployed AFTER adding it
- Check spelling: `VITE_API_BASE_URL` (exact case)

---

**Current Status:** ✅ Code deployed, waiting for environment variable setup

**Next Step:** Add environment variable on Vercel (5 minutes)
