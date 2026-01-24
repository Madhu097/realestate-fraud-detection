# Truth in Listings - Backend API

FastAPI backend for the Truth in Listings fraud detection system.

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── routers/
│   │   ├── __init__.py
│   │   └── analyze.py       # Analysis endpoints
│   └── services/            # Business logic and services
│       └── __init__.py
├── venv/                    # Virtual environment
├── .env.example             # Environment variables template
├── requirements.txt         # Python dependencies
├── test_api.py              # API test suite
└── README.md                # This file
```

## Setup Instructions

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Virtual Environment (if not exists)

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
.\venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
uvicorn app.main:app --reload
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc

## API Endpoints

### Health Check
- `GET /` - Basic health check
- `GET /health` - Detailed health check with endpoint information

### Analysis
- `POST /api/analyze` - Analyze a listing (placeholder for fraud detection)
- `GET /api/analyze/status` - Get analysis service status

## Development

### Adding New Routers

1. Create a new file in `app/routers/`
2. Define your router using `APIRouter()`
3. Import and include it in `app/main.py`

### Adding Services

1. Create service files in `app/services/`
2. Implement business logic
3. Import and use in routers

### Testing

Run the test suite:
```bash
python test_api.py
```

## Environment Variables

Copy `.env.example` to `.env` and update with your values:
```bash
cp .env.example .env
```

## Next Steps

- [ ] Implement fraud detection logic in `/api/analyze`
- [ ] Add database integration (PostgreSQL/MongoDB)
- [ ] Implement authentication/authorization
- [ ] Add logging and monitoring
- [ ] Write comprehensive tests
- [ ] Add environment configuration management

## Technologies

- **FastAPI** - Modern, fast web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **Python 3.8+** - Programming language
