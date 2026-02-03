@echo off
REM Quick Deployment Script for Real Estate Fraud Detection (Windows)
REM This script helps you prepare your application for deployment

echo ================================
echo Real Estate Fraud Detection - Deployment Preparation
echo ================================
echo.

echo Step 1: Checking backend dependencies...
cd backend
if exist requirements.txt (
    echo [OK] requirements.txt found
) else (
    echo [ERROR] requirements.txt not found!
    exit /b 1
)

echo.
echo Step 2: Checking frontend dependencies...
cd ..\frontend
if exist package.json (
    echo [OK] package.json found
) else (
    echo [ERROR] package.json not found!
    exit /b 1
)

echo.
echo Step 3: Installing frontend dependencies...
call npm install

echo.
echo Step 4: Building frontend...
call npm run build

if exist dist (
    echo [OK] Frontend build successful!
) else (
    echo [ERROR] Frontend build failed!
    exit /b 1
)

echo.
echo ================================
echo [SUCCESS] Deployment preparation complete!
echo ================================
echo.
echo Next steps:
echo 1. Push your code to GitHub
echo 2. Follow the DEPLOYMENT_GUIDE.md for detailed instructions
echo 3. Deploy backend on Render
echo 4. Deploy frontend on Vercel
echo.
echo For detailed instructions, see: DEPLOYMENT_GUIDE.md
echo.
pause
