# 🚨 URGENT FIX - Set Vercel Environment Variable

## The Problem:
You're testing on: `https://realestate-fraud-frontend.vercel.app`  
But it's trying to connect to: `localhost:8000` ❌

## The Solution (Takes 2 Minutes):

### Step 1: Go to Vercel Dashboard
🔗 **Click here:** https://vercel.com/dashboard

### Step 2: Select Your Project
Click on: **realestate-fraud-frontend**

### Step 3: Go to Settings
Click the **"Settings"** tab at the top

### Step 4: Click Environment Variables
In the left sidebar, click **"Environment Variables"**

### Step 5: Add the Variable
Click **"Add New"** button and enter:

```
Name (Key):
VITE_API_BASE_URL

Value:
https://fraud-detection-api-8w4r.onrender.com

Environments (select all 3):
☑ Production
☑ Preview  
☑ Development
```

### Step 6: Save
Click **"Save"** button

### Step 7: Redeploy
1. Go to **"Deployments"** tab
2. Find the latest deployment
3. Click the **"⋯"** (three dots) menu
4. Click **"Redeploy"**
5. Confirm the redeploy

### Step 8: Wait 1-2 Minutes
Vercel will rebuild and redeploy your site

### Step 9: Test Again
1. Go to: https://realestate-fraud-frontend.vercel.app
2. Hard refresh: **Ctrl + Shift + R**
3. Fill the form
4. Click "Detect Fraud"
5. **It will work!** ✅

---

## 🎯 Alternative: Test Locally RIGHT NOW

If you want to test immediately while Vercel deploys:

1. **Make sure dev server is running**
   ```powershell
   cd frontend
   npm run dev
   ```

2. **Open:** http://localhost:5173

3. **Test the fraud detection** - Should work immediately!

---

## 📸 What You Should See on Vercel:

After setting the environment variable correctly:

**Settings → Environment Variables should show:**
```
┌────────────────────────────────────────────────┐
│ VITE_API_BASE_URL                             │
│ https://fraud-detection-api-8w4r.onrender.com │
│ Production, Preview, Development              │
└────────────────────────────────────────────────┘
```

---

## ✅ How to Verify It Worked:

After redeploying, open browser console (F12) on Vercel site:

**Should see:**
```
🔗 API Base URL: https://fraud-detection-api-8w4r.onrender.com
```

**NOT this:**
```
🔗 API Base URL: http://localhost:8000  ❌
```

---

**Current Problem:** Environment variable missing on Vercel  
**Time to Fix:** 2 minutes  
**What to Do:** Follow steps above to set environment variable

---

Need help? Tell me which step you're on!
