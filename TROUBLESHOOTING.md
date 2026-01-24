# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### 1. CORS Errors

**Symptom:** Browser console shows CORS-related errors like:
- `Access to XMLHttpRequest has been blocked by CORS policy`
- `No 'Access-Control-Allow-Origin' header is present`

**Solutions:**
✅ **Fixed!** The following changes have been made:
- Updated `backend/app/main.py` with comprehensive CORS configuration
- Added all necessary origins (localhost:5173, localhost:3000, etc.)
- Enabled credentials, all methods, and all headers
- Added `expose_headers` and `max_age` for better performance

**Verify the fix:**
```bash
# In backend directory
python test_comprehensive.py
```

### 2. Connection Refused / Network Errors

**Symptom:** 
- `ERR_CONNECTION_REFUSED`
- `Network Error`
- Frontend can't connect to backend

**Solutions:**
1. **Check if backend is running:**
   ```bash
   # Should see uvicorn process
   Get-Process | Where-Object {$_.ProcessName -like "*uvicorn*"}
   ```

2. **Check if frontend is running:**
   ```bash
   # Should see node process
   Get-Process | Where-Object {$_.ProcessName -like "*node*"}
   ```

3. **Restart both servers:**
   ```bash
   # From project root
   .\restart.ps1
   ```

4. **Manual restart:**
   ```bash
   # Backend
   cd backend
   .\venv\Scripts\activate
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   
   # Frontend (in new terminal)
   cd frontend
   npm run dev
   ```

### 3. Port Already in Use

**Symptom:**
- `Address already in use`
- `Port 8000 is already allocated`

**Solutions:**
1. **Kill process on port 8000 (Backend):**
   ```powershell
   Get-NetTCPConnection -LocalPort 8000 | Select-Object -ExpandProperty OwningProcess | ForEach-Object { Stop-Process -Id $_ -Force }
   ```

2. **Kill process on port 5173 (Frontend):**
   ```powershell
   Get-NetTCPConnection -LocalPort 5173 | Select-Object -ExpandProperty OwningProcess | ForEach-Object { Stop-Process -Id $_ -Force }
   ```

3. **Or use the restart script (does this automatically):**
   ```bash
   .\restart.ps1
   ```

### 4. Module Not Found Errors

**Symptom:**
- `ModuleNotFoundError: No module named 'dotenv'`
- `ModuleNotFoundError: No module named 'fastapi'`

**Solutions:**
```bash
cd backend
python -m pip install -r requirements.txt
```

### 5. Vite/React Errors

**Symptom:**
- White screen
- `Failed to fetch dynamically imported module`
- React component errors

**Solutions:**
1. **Clear Vite cache:**
   ```bash
   cd frontend
   Remove-Item -Recurse -Force node_modules\.vite
   npm run dev
   ```

2. **Reinstall dependencies:**
   ```bash
   cd frontend
   Remove-Item -Recurse -Force node_modules
   npm install
   npm run dev
   ```

### 6. Environment Variables Not Loading

**Symptom:**
- Backend not reading `.env` file
- CORS still not working after configuration

**Solutions:**
1. **Ensure `.env` file exists:**
   ```bash
   # Should exist in backend directory
   Test-Path backend\.env
   ```

2. **Verify python-dotenv is installed:**
   ```bash
   cd backend
   python -m pip show python-dotenv
   ```

3. **Restart backend server** (environment variables are loaded on startup)

## Quick Health Check

Run this command to verify everything is working:

```bash
# From backend directory
python test_comprehensive.py
```

This will test:
- ✅ Backend health endpoints
- ✅ API endpoints
- ✅ CORS configuration
- ✅ Request/Response flow

## Configuration Files Changed

The following files have been updated to fix errors:

### Backend:
1. **`backend/app/main.py`**
   - Enhanced CORS configuration
   - Added environment variable loading
   - Added more allowed origins

2. **`backend/requirements.txt`**
   - Added `python-dotenv==1.0.0`

3. **`backend/.env`** (NEW)
   - Environment configuration file

### Frontend:
1. **`frontend/vite.config.js`**
   - Enhanced proxy configuration
   - Added error logging
   - Added CORS support

2. **`frontend/src/services/api.js`**
   - Added request/response interceptors
   - Better error handling
   - Added debugging logs

## Testing Checklist

- [ ] Backend running on http://localhost:8000
- [ ] Frontend running on http://localhost:5173
- [ ] Can access http://localhost:8000/docs
- [ ] No CORS errors in browser console
- [ ] API requests successful from frontend
- [ ] `test_comprehensive.py` passes all tests

## Still Having Issues?

1. **Check browser console** (F12) for specific error messages
2. **Check backend terminal** for Python errors
3. **Check frontend terminal** for Vite/React errors
4. **Verify all dependencies are installed**
5. **Try the restart script:** `.\restart.ps1`

## Useful Commands

```bash
# View all running processes
Get-Process | Where-Object {$_.ProcessName -like "*python*" -or $_.ProcessName -like "*node*" -or $_.ProcessName -like "*uvicorn*"}

# Test backend directly
Invoke-WebRequest -Uri "http://localhost:8000/" -UseBasicParsing

# Test frontend directly
Invoke-WebRequest -Uri "http://localhost:5173/" -UseBasicParsing

# View backend logs
cd backend
uvicorn app.main:app --reload --log-level debug

# View frontend logs (already shown in terminal)
cd frontend
npm run dev
```

## Project Structure

```
major/
├── backend/
│   ├── app/
│   │   ├── main.py          # ✅ UPDATED - CORS fixed
│   │   ├── routers/
│   │   └── services/
│   ├── .env                 # ✅ NEW - Environment config
│   ├── requirements.txt     # ✅ UPDATED - Added python-dotenv
│   └── test_comprehensive.py # ✅ NEW - Test script
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── services/
│   │       └── api.js       # ✅ UPDATED - Better error handling
│   ├── vite.config.js       # ✅ UPDATED - Enhanced proxy
│   └── package.json
└── restart.ps1              # ✅ NEW - Restart script
```

## Next Steps

After fixing these errors, you can:
1. Start implementing fraud detection logic
2. Add database integration
3. Create more UI components
4. Add authentication
5. Deploy to production
