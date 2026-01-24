# Truth in Listings - Frontend

React frontend for the Truth in Listings fraud detection system.

## 🚀 Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Axios** - HTTP client for API calls
- **Modern CSS** - Glassmorphism design

## 📁 Project Structure

```
frontend/
├── src/
│   ├── App.jsx          # Main app component with backend test
│   ├── App.css          # App styles
│   ├── main.jsx         # React entry point
│   ├── index.css        # Global styles
│   └── services/
│       └── api.js       # Backend API service
├── index.html           # HTML template
├── vite.config.js       # Vite configuration
├── package.json         # Dependencies
└── README.md            # This file
```

## 🎯 Features

✅ **Backend Connectivity Test** - Automatic connection test on load  
✅ **Axios Integration** - Configured API client  
✅ **Modern UI** - Glassmorphism design with gradients  
✅ **Error Handling** - Graceful error messages  
✅ **Loading States** - Visual feedback during API calls  
✅ **Responsive Design** - Works on all screen sizes  

## 🔧 Setup

### Prerequisites
- Node.js 16+ installed
- Backend server running on port 8000

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (already done)
npm install

# Start development server
npm run dev
```

The app will run at: **http://localhost:5173**

## 🌐 Backend Connection

The frontend connects to the backend at `http://localhost:8000`

### API Service Usage

```javascript
import api from './services/api';

// Health check
const status = await api.healthCheck();

// Analyze listing
const result = await api.analyzeListing({
  listing_id: "123",
  listing_url: "https://example.com/listing/123"
});
```

### Available Endpoints

- `GET /` - Health check
- `GET /health` - Detailed health
- `POST /api/analyze` - Analyze listing
- `GET /api/analyze/status` - Analysis service status

## 🎨 UI Components

### Main Features

1. **Connection Test Card**
   - Automatic backend connection test on load
   - Manual retry button
   - Visual status indicators (loading/success/error)

2. **Response Display**
   - JSON response from backend
   - Formatted and color-coded

3. **Info Card**
   - Connection details
   - Quick links to backend and docs

## 🧪 Testing Backend Connection

When you load the page, you should see:

```json
{
  "status": "healthy",
  "service": "Truth in Listings API",
  "version": "1.0.0",
  "message": "API is running successfully"
}
```

This confirms the frontend-backend connection is working! ✅

## 📝 Development

### Adding New Components

```bash
# Create new component
touch src/components/MyComponent.jsx
```

### Making API Calls

```javascript
import { useState, useEffect } from 'react';
import api from './services/api';

function MyComponent() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      const result = await api.healthCheck();
      setData(result);
    };
    fetchData();
  }, []);

  return <div>{JSON.stringify(data)}</div>;
}
```

## 🏗️ Build for Production

```bash
npm run build
```

This creates an optimized build in the `dist/` folder.

## 🔍 Troubleshooting

### CORS Errors
- Make sure backend CORS is configured to allow `http://localhost:5173`
- Backend already has CORS enabled for all origins in development

### Connection Refused
- Ensure backend server is running: `cd backend && uvicorn app.main:app --reload`
- Check backend is on port 8000

### Module Not Found
```bash
rm -rf node_modules package-lock.json
npm install
```

## 📚 Resources

- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)
- [Axios Documentation](https://axios-http.com/)

---

**Frontend-Backend Connection: ✅ Working!**
