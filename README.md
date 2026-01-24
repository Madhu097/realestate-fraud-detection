# Truth in Listings

A comprehensive fraud detection system for online listings.

## 📁 Project Structure

```
major/
├── backend/                 # FastAPI Backend Server
│   ├── app/
│   │   ├── main.py         # FastAPI application
│   │   ├── routers/        # API endpoints
│   │   └── services/       # Business logic
│   ├── venv/               # Python virtual environment
│   ├── requirements.txt    # Python dependencies
│   ├── test_api.py         # API tests
│   └── README.md           # Backend documentation
│
├── frontend/               # React Frontend Application
│   └── README.md           # Frontend documentation
│
├── .gitignore
└── README.md               # This file
```

## 📊 Listing Data Schema (FROZEN)

**This schema is frozen and used by:**
- All fraud detection modules
- Database storage
- Frontend forms
- Evaluation systems

```json
{
  "title": "string",
  "description": "string",
  "price": 0,
  "area_sqft": 0,
  "city": "string",
  "locality": "string",
  "latitude": 0.0,
  "longitude": 0.0
}
```

### Field Descriptions:
- **title** (string): The listing title/headline
- **description** (string): Detailed description of the property
- **price** (number): Price in the local currency
- **area_sqft** (number): Area in square feet
- **city** (string): City name
- **locality** (string): Specific locality/neighborhood
- **latitude** (number): Geographic latitude coordinate
- **longitude** (number): Geographic longitude coordinate

## 🚀 Quick Start

### Backend Setup

```bash
# Navigate to backend
cd backend

# Activate virtual environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/Mac

# Install dependencies (if needed)
pip install -r requirements.txt

# Run the backend server
uvicorn app.main:app --reload
```

Backend will run at: **http://localhost:8000**
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Choose your framework and initialize
# Option 1: Vite (Recommended)
npm create vite@latest . -- --template react
npm install
npm run dev

# Option 2: Next.js
npx create-next-app@latest .
npm run dev
```

Frontend will run at: **http://localhost:3000** (or http://localhost:5173 for Vite)

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **Python 3.8+**

### Frontend
- **React** - UI library
- **Vite/Next.js** - Build tool/framework
- **Tailwind CSS** - Styling (recommended)
- **Axios** - API communication

## 📋 Development Workflow

1. **Start Backend Server** (Terminal 1)
   ```bash
   cd backend
   .\venv\Scripts\activate
   uvicorn app.main:app --reload
   ```

2. **Start Frontend Server** (Terminal 2)
   ```bash
   cd frontend
   npm run dev
   ```

3. **Develop Features**
   - Backend: Add routes in `backend/app/routers/`
   - Frontend: Add components in `frontend/src/components/`

## 📚 API Endpoints

### Health Check
- `GET /` - Basic health check
- `GET /health` - Detailed health information

### Analysis (Fraud Detection)

#### `POST /api/analyze` - Analyze Listing for Fraud

**Description:** Single entry point for fraud detection. Accepts listing data and returns a fraud analysis report.

**Request Body:**
```json
{
  "listing_data": {
    "title": "string",
    "description": "string",
    "price": 0,
    "area_sqft": 0,
    "city": "string",
    "locality": "string",
    "latitude": 0.0,
    "longitude": 0.0
  }
}
```

**Response (FraudReport):**
```json
{
  "fraud_probability": 0.0,
  "fraud_types": [],
  "explanations": []
}
```

**Response Fields:**
- `fraud_probability` (float): Probability of fraud (0.0 = no fraud, 1.0 = definite fraud)
- `fraud_types` (array): List of detected fraud types (e.g., `["price_manipulation", "fake_location"]`)
- `explanations` (array): Human-readable explanations for detected fraud indicators

**Status:** Currently returns dummy data (all zeros/empty arrays). Will be connected to fraud detection modules.

#### `GET /api/analyze/status` - Get Analysis Service Status

Returns the operational status of the analysis service.

## 🎯 Next Steps

### Backend
- [ ] Implement fraud detection algorithms
- [ ] Add database integration
- [ ] Set up authentication
- [ ] Add logging and monitoring

### Frontend
- [ ] Initialize React/Next.js project
- [ ] Create listing analysis interface
- [ ] Build results dashboard
- [ ] Add responsive design
- [ ] Implement API integration

## 📖 Documentation

- [Backend Documentation](./backend/README.md)
- [Frontend Documentation](./frontend/README.md)

## 🤝 Contributing

1. Create a new branch for your feature
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📝 License

This project is private and proprietary.

---

**Happy Coding! 🚀**
