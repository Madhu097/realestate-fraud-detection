#!/bin/bash

# Quick Deployment Script for Real Estate Fraud Detection
# This script helps you prepare your application for deployment

echo "🚀 Real Estate Fraud Detection - Deployment Preparation"
echo "========================================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Step 1: Checking backend dependencies...${NC}"
cd backend
if [ -f "requirements.txt" ]; then
    echo -e "${GREEN}✓ requirements.txt found${NC}"
else
    echo "❌ requirements.txt not found!"
    exit 1
fi

echo ""
echo -e "${YELLOW}Step 2: Checking frontend dependencies...${NC}"
cd ../frontend
if [ -f "package.json" ]; then
    echo -e "${GREEN}✓ package.json found${NC}"
else
    echo "❌ package.json not found!"
    exit 1
fi

echo ""
echo -e "${YELLOW}Step 3: Installing frontend dependencies...${NC}"
npm install

echo ""
echo -e "${YELLOW}Step 4: Building frontend...${NC}"
npm run build

if [ -d "dist" ]; then
    echo -e "${GREEN}✓ Frontend build successful!${NC}"
else
    echo "❌ Frontend build failed!"
    exit 1
fi

echo ""
echo "========================================================"
echo -e "${GREEN}✅ Deployment preparation complete!${NC}"
echo ""
echo "Next steps:"
echo "1. Push your code to GitHub"
echo "2. Follow the DEPLOYMENT_GUIDE.md for detailed instructions"
echo "3. Deploy backend on Render"
echo "4. Deploy frontend on Vercel"
echo ""
echo "For detailed instructions, see: DEPLOYMENT_GUIDE.md"
