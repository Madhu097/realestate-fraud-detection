# 🏠 Real Estate Fraud Detection System

A professional fraud detection system to verify property listings and identify fraudulent real estate advertisements.

## 🌐 Live Demo

- **Frontend**: [Deploy on Vercel](https://vercel.com) - See [QUICK_DEPLOY.md](QUICK_DEPLOY.md)
- **Backend API**: [Deploy on Render](https://render.com) - See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

## ✨ Features

- **Price Fraud Detection** - Identifies suspiciously low or high property prices
- **Text Analysis** - Scans for fraud keywords and suspicious language
- **Area Validation** - Verifies realistic property measurements
- **Professional UI** - Clean, modern interface with Inter font
- **Instant Results** - Real-time fraud analysis with detailed reports
- **Risk Classification** - FAKE, SUSPICIOUS, CAUTION, or REAL verdicts

## 🚀 Quick Start (Local Development)

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python fraud_checker.py
```

### 3. Open in Browser

```
http://localhost:9000
```

## 📋 How to Use

1. **Enter Property Details**
   - Property title and description
   - Price and area
   - City and locality
   - Bedrooms, bathrooms, property type

2. **Click "Analyze Property for Fraud"**

3. **View Results**
   - Fraud probability percentage
   - Verdict (FAKE/SUSPICIOUS/CAUTION/REAL)
   - Detailed analysis of price, text, and area
   - Recommendations

## 🎯 Supported Cities

- Hyderabad
- Mumbai
- Bangalore
- Delhi
- Pune
- Chennai
- Kolkata
- Ahmedabad

## 📊 Fraud Detection Criteria

### Price Analysis
- Compares with market average prices
- Flags properties 50% below or 200% above market rate
- Considers city-specific pricing

### Text Analysis
- Scans for fraud keywords: "urgent", "limited time", "grab now", etc.
- Identifies suspicious language patterns
- Checks for professional vs. scam-like descriptions

### Area Validation
- Verifies realistic property sizes
- Checks against typical ranges for property types
- Flags unusually small or large areas

## 🎨 UI Design

- **Professional** - Clean white background with blue accents
- **Modern** - Inter font from Google Fonts
- **Responsive** - Works on all devices
- **Accessible** - Good contrast and readability

## 📁 Project Structure

```
major/
├── backend/
│   ├── app/
│   │   ├── routers/        # API endpoints
│   │   ├── services/       # Fraud detection logic
│   │   ├── data/           # Dataset
│   │   ├── main.py         # FastAPI application
│   │   └── config.py       # Configuration
│   ├── fraud_checker.py    # Standalone fraud checker (MAIN APP)
│   └── requirements.txt    # Python dependencies
├── frontend/               # React frontend (optional)
├── README.md              # This file
├── USER_GUIDE.md          # Detailed user guide
└── PROFESSIONAL_UI_REDESIGN.md  # UI design documentation
```

## 🔧 Configuration

Edit `backend/.env` to configure:
- Database settings
- API keys for external services
- Fraud detection thresholds

## 📖 Documentation

- **USER_GUIDE.md** - Detailed usage instructions with examples
- **PROFESSIONAL_UI_REDESIGN.md** - UI design documentation

## 🛠️ Technology Stack

- **Backend:** FastAPI, Python
- **Frontend:** HTML, CSS, JavaScript (embedded in fraud_checker.py)
- **Fonts:** Inter (Google Fonts)
- **Database:** SQLite (optional, for advanced features)

## ⚡ Performance

- **Response Time:** < 100ms for fraud analysis
- **Concurrent Users:** Supports multiple simultaneous checks
- **Accuracy:** Based on market data and fraud patterns

## 🔒 Security

- Input validation on all fields
- CORS protection
- Safe data handling

## � Deployment

Want to deploy this application for free? Follow our guides:

- **Quick Deploy** (30 minutes): [QUICK_DEPLOY.md](QUICK_DEPLOY.md)
- **Detailed Guide**: [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Checklist**: [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md)

**Recommended Free Hosting:**
- Backend: [Render](https://render.com) (Free tier)
- Frontend: [Vercel](https://vercel.com) (Free tier)

## �📝 License

This project is for educational and demonstration purposes.

## 🤝 Contributing

This is a demonstration project. For production use, consider:
- Integrating real-time market data APIs
- Adding image fraud detection
- Implementing user authentication
- Connecting to a production database

## 📞 Support

For issues or questions, refer to the USER_GUIDE.md for detailed instructions.

---

**Made with ❤️ for safer real estate transactions**
