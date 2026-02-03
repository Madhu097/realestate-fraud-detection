@echo off
echo ===================================================
echo   Real Estate Fraud Detection - Deployment Fixer
echo ===================================================
echo.
echo This script will commit and push the fixes for:
echo 1. CORS "Network Error" on Vercel
echo 2. Frontend API connection
echo 3. Unwanted file cleanup
echo.

echo Step 1: Staging changes...
git add .

echo.
echo Step 2: Committing changes...
git commit -m "Fix CORS, Environment Variables, and Cleanup for Deployment"

echo.
echo Step 3: Pushing to GitHub...
echo (You may be asked to sign in)
git push origin main

echo.
echo ===================================================
echo   SUCCESS! Deployment Triggered
echo ===================================================
echo.
echo 1. Render will redeploy the backend (Wait ~3 mins)
echo 2. Vercel will redeploy the frontend (Wait ~1 min)
echo.
echo Verify here:
echo Backend: https://fraud-detection-api-8w4r.onrender.com/health
echo Frontend: https://realestate-fraud-frontend.vercel.app
echo.
pause
