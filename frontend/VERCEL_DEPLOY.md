# Environment Variables Configuration for Vercel Deployment

## Required Environment Variable

When deploying to Vercel, set this environment variable:

**Variable Name:** `VITE_API_BASE_URL`  
**Value:** `https://fraud-detection-api-8w4r.onrender.com`

## How to Set in Vercel:

1. Go to your Vercel project dashboard
2. Click on **Settings** tab
3. Click on **Environment Variables** in the sidebar
4. Add the variable:
   - **Name:** VITE_API_BASE_URL
   - **Value:** https://fraud-detection-api-8w4r.onrender.com
   - **Environment:** Production, Preview, Development (select all)
5. Click **Save**
6. Redeploy your application

## For Local Development:

Copy `.env.example` to `.env` and update:
```
VITE_API_BASE_URL=http://localhost:8000
```
