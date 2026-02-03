# 🚀 Deployment Instructions for Render

## Backend Deployment to Render

Your backend is already deployed at:
**https://fraud-detection-api-8w4r.onrender.com**

### Update Your Deployed Backend

Since we've made CORS changes, you need to redeploy:

#### Option 1: Push to GitHub (Recommended)
```bash
cd backend
git add .
git commit -m "Fix CORS for Vercel frontend"
git push origin main
```

Render will automatically detect the changes and redeploy.

#### Option 2: Manual Redeploy on Render
1. Go to https://dashboard.render.com
2. Find your service: `fraud-detection-api-8w4r`
3. Click **Manual Deploy** → **Deploy latest commit**

### Environment Variables on Render

Make sure these are set in your Render dashboard:

```bash
# Go to: Dashboard → Your Service → Environment
PYTHON_VERSION=3.11
ALLOWED_ORIGINS=*
DEBUG=False
```

### Verify Deployment

After deployment, test these endpoints:

1. **Health Check:**
   ```
   https://fraud-detection-api-8w4r.onrender.com/health
   ```

2. **API Docs:**
   ```
   https://fraud-detection-api-8w4r.onrender.com/docs
   ```

3. **Test CORS:**
   Open browser console on Vercel site and run:
   ```javascript
   fetch('https://fraud-detection-api-8w4r.onrender.com/health')
     .then(res => res.json())
     .then(data => console.log('✅ CORS working:', data))
     .catch(err => console.error('❌ CORS error:', err));
   ```

## Files to Deploy

Make sure these files are in your GitHub repository:

### Required Files
- ✅ `backend/app/` (all Python files)
- ✅ `backend/requirements.txt`
- ✅ `backend/Procfile` (for Render)
- ✅ `backend/render.yaml` (optional, for configuration)

### Procfile Content
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### render.yaml Content (Optional)
```yaml
services:
  - type: web
    name: fraud-detection-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11
      - key: ALLOWED_ORIGINS
        value: "*"
```

## Testing After Deployment

### 1. Test Backend Directly
```bash
curl https://fraud-detection-api-8w4r.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "Truth in Listings",
  "version": "1.0.0"
}
```

### 2. Test from Vercel Frontend
1. Go to: https://realestate-fraud-frontend.vercel.app
2. Fill in the form
3. Submit
4. Should see results without CORS errors

## Troubleshooting

### Issue: "Service Unavailable" or 503 Error
**Cause:** Render free tier spins down after inactivity  
**Solution:** Wait 30-60 seconds for the service to wake up

### Issue: Still getting CORS errors
**Cause:** Old deployment is cached  
**Solution:**
1. Hard refresh Vercel site (Ctrl+Shift+R)
2. Clear browser cache
3. Check Render logs for errors

### Issue: Changes not reflected
**Cause:** Deployment didn't trigger  
**Solution:**
1. Check Render dashboard for latest deployment
2. Manually trigger deployment
3. Check GitHub webhook is connected

## Render Dashboard Links

- **Service Dashboard:** https://dashboard.render.com/web/srv-XXXXX
- **Logs:** Click on "Logs" tab in your service
- **Environment:** Click on "Environment" tab
- **Settings:** Click on "Settings" tab

## Important Notes

1. **Free Tier Limitations:**
   - Service spins down after 15 minutes of inactivity
   - First request after spin-down takes 30-60 seconds
   - 750 hours/month free (enough for testing)

2. **CORS Configuration:**
   - Currently set to allow all origins (`*`)
   - For production, restrict to specific domains
   - Update `backend/app/main.py` line 50

3. **Database:**
   - Currently using SQLite (file-based)
   - For production, consider PostgreSQL
   - Render offers free PostgreSQL instances

## Next Steps

1. ✅ Push code changes to GitHub
2. ✅ Wait for Render to redeploy
3. ✅ Test backend health endpoint
4. ✅ Test Vercel frontend
5. ✅ Verify no CORS errors

---

**Last Updated:** February 3, 2026, 3:58 PM IST
