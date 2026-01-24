# Backend Setup and Testing Guide

## Quick Start

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Start the Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Verify Installation

Open browser and visit:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

---

## Testing the Refactored Backend

### Test 1: Health Check

```bash
curl http://localhost:8000/health
```

**Expected Response**:
```json
{
  "status": "healthy",
  "service": "Truth in Listings API",
  "version": "1.0.0",
  "message": "API is running successfully",
  "endpoints": {
    "health": "/health",
    "docs": "/docs",
    "redoc": "/redoc",
    "analyze": "/api/analyze",
    "upload": "/api/upload",
    "history": "/api/history"
  }
}
```

### Test 2: Validation Error Handling

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "listing_data": {
      "title": "",
      "description": "Test",
      "price": 0,
      "area_sqft": 1000,
      "city": "Mumbai",
      "locality": "Andheri",
      "latitude": 19.1,
      "longitude": 72.8
    }
  }'
```

**Expected Response** (Validation Error):
```json
{
  "success": false,
  "message": "Validation failed. Please check your input.",
  "error_code": "VALIDATION_ERROR",
  "validation_errors": [
    {
      "field": "title",
      "message": "Title is required and cannot be empty",
      "value": ""
    },
    {
      "field": "price",
      "message": "Price cannot be zero",
      "value": 0
    }
  ],
  "timestamp": "2026-01-20T10:00:00.000Z"
}
```

### Test 3: Successful Analysis

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "listing_data": {
      "title": "Spacious 3BHK Apartment",
      "description": "Beautiful apartment with modern amenities",
      "price": 5000000,
      "area_sqft": 1500,
      "city": "Mumbai",
      "locality": "Andheri West",
      "latitude": 19.1334,
      "longitude": 72.8291
    }
  }'
```

**Expected Response** (Success):
```json
{
  "success": true,
  "message": "Fraud analysis completed successfully",
  "data": {
    "fraud_probability": 0.15,
    "fraud_types": [],
    "explanations": [...],
    "module_scores": {
      "Price": 0.10,
      "Image": 0.0,
      "Text": 0.05,
      "Location": 0.20
    }
  },
  "timestamp": "2026-01-20T10:00:00.000Z"
}
```

---

## Verify Refactoring

### Check 1: Centralized Config

```bash
# Open Python shell
python

# Import and check config
from app.config import AppConstants, FraudConstants, ErrorMessages

print(AppConstants.APP_NAME)
# Output: Truth in Listings

print(FraudConstants.FUSION_WEIGHTS)
# Output: {'price': 0.3, 'image': 0.25, 'text': 0.25, 'location': 0.2}

print(ErrorMessages.EMPTY_TITLE)
# Output: Title is required and cannot be empty
```

### Check 2: Response Schemas

```bash
# In Python shell
from app.schemas import create_success_response, create_error_response

# Test success response
response = create_success_response(
    message="Test successful",
    data={"test": "value"}
)
print(response)
# Output: {'success': True, 'message': 'Test successful', 'data': {...}, 'timestamp': '...'}

# Test error response
error = create_error_response(
    message="Test error",
    error_code="TEST_ERROR"
)
print(error)
# Output: {'success': False, 'message': 'Test error', 'error_code': 'TEST_ERROR', 'timestamp': '...'}
```

### Check 3: Exception Handling

```bash
# In Python shell
from app.exceptions import ValidationException, DatasetNotFoundException

# Test custom exception
try:
    raise ValidationException("Test validation error")
except ValidationException as e:
    print(f"Code: {e.error_code}, Message: {e.message}")
# Output: Code: VALIDATION_ERROR, Message: Test validation error
```

---

## Common Issues and Solutions

### Issue 1: Module Not Found Error

**Error**: `ModuleNotFoundError: No module named 'pydantic_settings'`

**Solution**:
```bash
pip install pydantic-settings
```

### Issue 2: Import Error

**Error**: `ImportError: cannot import name 'settings' from 'app.config'`

**Solution**: Make sure you're in the backend directory and restart the server:
```bash
cd backend
uvicorn app.main:app --reload
```

### Issue 3: Dataset Not Loaded

**Warning**: `⚠️ Warning: Could not load dataset`

**Solution**: Ensure dataset file exists:
```bash
ls app/data/real_estate.csv
```

If missing, download the dataset (see DATASET_DOWNLOAD.md)

---

## Development Workflow

### 1. Make Changes

Edit files in `app/` directory:
- `config.py` - Update constants
- `schemas.py` - Add new response models
- `exceptions.py` - Add new exceptions
- `routers/*.py` - Update endpoints

### 2. Test Changes

```bash
# Restart server (if not using --reload)
uvicorn app.main:app --reload

# Test endpoint
curl http://localhost:8000/api/your-endpoint
```

### 3. Check Logs

Server logs will show:
- Startup messages
- Request logs
- Error logs with stack traces

---

## Production Checklist

Before deploying to production:

- [ ] Update `.env` file with production settings
- [ ] Set `debug=False` in settings
- [ ] Configure production CORS origins
- [ ] Set up proper logging (file-based, not console)
- [ ] Add authentication/authorization
- [ ] Set up database migrations (Alembic)
- [ ] Configure reverse proxy (Nginx)
- [ ] Set up SSL/TLS certificates
- [ ] Add rate limiting
- [ ] Set up monitoring (Prometheus/Grafana)

---

## API Documentation

### Interactive Docs (Swagger UI)

Visit: http://localhost:8000/docs

Features:
- Try out endpoints directly
- See request/response schemas
- View example requests
- Test authentication

### ReDoc Documentation

Visit: http://localhost:8000/redoc

Features:
- Clean, readable format
- Downloadable OpenAPI spec
- Code examples in multiple languages

---

## Troubleshooting

### Enable Debug Mode

Edit `app/config.py`:
```python
class Settings(BaseSettings):
    debug: bool = True  # Change to True
```

This will:
- Show detailed error messages
- Include stack traces in responses
- Enable auto-reload

### Check Logs

Server logs show:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
================================================================================
  Truth in Listings - Backend API
  Version: 1.0.0
================================================================================
✅ Application started successfully
📚 API Documentation: /docs
🔍 ReDoc Documentation: /redoc
================================================================================
INFO:     Application startup complete.
```

### Verify All Imports

```bash
python -c "from app.config import *; from app.schemas import *; from app.exceptions import *; print('✅ All imports successful')"
```

---

## Next Steps

1. **Test All Endpoints**: Use Swagger UI to test each endpoint
2. **Review Error Handling**: Trigger errors and verify responses
3. **Check Documentation**: Ensure all endpoints are documented
4. **Performance Testing**: Test with multiple concurrent requests
5. **Security Audit**: Review CORS, validation, error messages

---

**The refactored backend is ready for final submission!** 🎓

For questions or issues, refer to:
- `REFACTORING_SUMMARY.md` - Detailed refactoring documentation
- `/docs` - Interactive API documentation
- Server logs - Detailed error messages
