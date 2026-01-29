"""
COMPLETE REAL ESTATE FRAUD DETECTION SYSTEM
Users can check if a property listing is FAKE or REAL
"""
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict, List, Optional
import json
from datetime import datetime
import uvicorn

# ============================================================
# DATA MODELS
# ============================================================

class PropertyListing(BaseModel):
    title: str
    description: str
    price: float
    area_sqft: float
    city: str
    locality: str
    bedrooms: Optional[int] = 2
    bathrooms: Optional[int] = 2
    property_type: Optional[str] = "Apartment"

# ============================================================
# FRAUD DETECTION ENGINE
# ============================================================

class FraudDetector:
    def __init__(self):
        # Average prices per sqft for major cities (in INR)
        self.city_avg_prices = {
            "hyderabad": 4500,
            "mumbai": 12000,
            "bangalore": 6500,
            "delhi": 8000,
            "pune": 5500,
            "chennai": 5000,
            "kolkata": 4000,
            "ahmedabad": 3500
        }
        
        # Suspicious keywords in title/description
        self.fraud_keywords = [
            "urgent", "limited time", "hurry", "grab now", "once in lifetime",
            "unbelievable", "too good", "guaranteed", "100% profit",
            "no questions", "cash only", "wire transfer", "western union"
        ]
    
    def analyze(self, listing: PropertyListing) -> dict:
        """
        Analyze a property listing for fraud
        Returns detailed fraud report
        """
        fraud_scores = []
        fraud_types = []
        details = []
        
        # 1. Price Fraud Detection
        price_analysis = self._check_price_fraud(listing)
        fraud_scores.append(price_analysis["score"])
        if price_analysis["is_fraud"]:
            fraud_types.append("Price Fraud")
        details.append(price_analysis)
        
        # 2. Text Fraud Detection
        text_analysis = self._check_text_fraud(listing)
        fraud_scores.append(text_analysis["score"])
        if text_analysis["is_fraud"]:
            fraud_types.append("Text Fraud")
        details.append(text_analysis)
        
        # 3. Area Validation
        area_analysis = self._check_area_fraud(listing)
        fraud_scores.append(area_analysis["score"])
        if area_analysis["is_fraud"]:
            fraud_types.append("Area Fraud")
        details.append(area_analysis)
        
        # Calculate overall fraud probability
        fraud_probability = sum(fraud_scores) / len(fraud_scores)
        
        # Determine verdict
        if fraud_probability >= 0.7:
            verdict = "FAKE - High Risk of Fraud"
            verdict_emoji = "🚨"
            verdict_color = "red"
        elif fraud_probability >= 0.5:
            verdict = "SUSPICIOUS - Moderate Risk"
            verdict_emoji = "⚠️"
            verdict_color = "orange"
        elif fraud_probability >= 0.3:
            verdict = "CAUTION - Some Red Flags"
            verdict_emoji = "⚡"
            verdict_color = "yellow"
        else:
            verdict = "REAL - Looks Legitimate"
            verdict_emoji = "✅"
            verdict_color = "green"
        
        return {
            "fraud_probability": round(fraud_probability, 2),
            "verdict": verdict,
            "verdict_emoji": verdict_emoji,
            "verdict_color": verdict_color,
            "fraud_types": fraud_types,
            "details": details,
            "recommendation": self._get_recommendation(fraud_probability),
            "analyzed_at": datetime.now().isoformat()
        }
    
    def _check_price_fraud(self, listing: PropertyListing) -> dict:
        """Check if price is suspiciously low or high"""
        city_key = listing.city.lower()
        avg_price = self.city_avg_prices.get(city_key, 5000)
        
        price_per_sqft = listing.price / listing.area_sqft
        
        # Calculate deviation from average
        deviation = abs(price_per_sqft - avg_price) / avg_price
        
        is_too_low = price_per_sqft < avg_price * 0.5  # 50% below average
        is_too_high = price_per_sqft > avg_price * 2.0  # 200% above average
        
        if is_too_low:
            score = 0.8
            is_fraud = True
            reason = f"Price is {int((1 - price_per_sqft/avg_price) * 100)}% BELOW market average"
            warning = "⚠️ Suspiciously LOW price - possible scam!"
        elif is_too_high:
            score = 0.6
            is_fraud = True
            reason = f"Price is {int((price_per_sqft/avg_price - 1) * 100)}% ABOVE market average"
            warning = "⚠️ Overpriced property - inflated value!"
        elif deviation > 0.3:
            score = 0.4
            is_fraud = False
            reason = f"Price deviates {int(deviation * 100)}% from market average"
            warning = "⚡ Price seems unusual, verify carefully"
        else:
            score = 0.1
            is_fraud = False
            reason = "Price is within normal market range"
            warning = "✅ Price looks reasonable"
        
        return {
            "type": "Price Analysis",
            "score": score,
            "is_fraud": is_fraud,
            "price_per_sqft": round(price_per_sqft, 2),
            "market_avg": avg_price,
            "deviation": round(deviation * 100, 1),
            "reason": reason,
            "warning": warning
        }
    
    def _check_text_fraud(self, listing: PropertyListing) -> dict:
        """Check for suspicious keywords in title/description"""
        text = (listing.title + " " + listing.description).lower()
        
        found_keywords = [kw for kw in self.fraud_keywords if kw in text]
        
        if len(found_keywords) >= 3:
            score = 0.9
            is_fraud = True
            warning = "🚨 Multiple fraud keywords detected!"
        elif len(found_keywords) >= 2:
            score = 0.6
            is_fraud = True
            warning = "⚠️ Suspicious keywords found"
        elif len(found_keywords) >= 1:
            score = 0.3
            is_fraud = False
            warning = "⚡ Some questionable language used"
        else:
            score = 0.1
            is_fraud = False
            warning = "✅ Text looks professional"
        
        return {
            "type": "Text Analysis",
            "score": score,
            "is_fraud": is_fraud,
            "suspicious_keywords": found_keywords,
            "keyword_count": len(found_keywords),
            "warning": warning
        }
    
    def _check_area_fraud(self, listing: PropertyListing) -> dict:
        """Check if area seems unrealistic"""
        area = listing.area_sqft
        
        # Typical ranges for different property types
        if listing.property_type == "Apartment":
            min_area, max_area = 300, 3000
        elif listing.property_type == "Villa":
            min_area, max_area = 1000, 10000
        elif listing.property_type == "Plot":
            min_area, max_area = 500, 50000
        else:
            min_area, max_area = 200, 5000
        
        if area < min_area:
            score = 0.7
            is_fraud = True
            warning = f"⚠️ Area too small for {listing.property_type}"
        elif area > max_area:
            score = 0.6
            is_fraud = True
            warning = f"⚠️ Area unusually large for {listing.property_type}"
        else:
            score = 0.1
            is_fraud = False
            warning = f"✅ Area is reasonable for {listing.property_type}"
        
        return {
            "type": "Area Validation",
            "score": score,
            "is_fraud": is_fraud,
            "area_sqft": area,
            "expected_range": f"{min_area}-{max_area} sqft",
            "warning": warning
        }
    
    def _get_recommendation(self, fraud_probability: float) -> str:
        """Get recommendation based on fraud probability"""
        if fraud_probability >= 0.7:
            return "🚨 DO NOT PROCEED! This listing shows multiple red flags. Likely a SCAM. Report to authorities."
        elif fraud_probability >= 0.5:
            return "⚠️ PROCEED WITH EXTREME CAUTION! Verify all details, visit property in person, check documents thoroughly."
        elif fraud_probability >= 0.3:
            return "⚡ BE CAREFUL! Some concerns detected. Verify seller credentials and property documents before proceeding."
        else:
            return "✅ Looks legitimate, but always verify documents, visit property, and use legal channels for transaction."

# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="Real Estate Fraud Detection",
    description="Check if a property listing is FAKE or REAL",
    version="3.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

detector = FraudDetector()

# ============================================================
# HTML INTERFACE
# ============================================================

html_interface = """
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Real Estate Fraud Detection System - Professional Property Verification</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Professional real estate fraud detection system to verify property listings">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { 
            margin: 0; 
            padding: 0; 
            box-sizing: border-box; 
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f8fafc;
            color: #1e293b;
            line-height: 1.6;
            min-height: 100vh;
        }
        
        /* Header */
        .header {
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            padding: 2rem 1.5rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        
        .header-content {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .logo {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 0.5rem;
        }
        
        .logo-icon {
            font-size: 2rem;
        }
        
        h1 {
            color: #ffffff;
            font-size: 1.875rem;
            font-weight: 700;
            letter-spacing: -0.025em;
        }
        
        .subtitle {
            color: #94a3b8;
            font-size: 1rem;
            font-weight: 400;
            margin-top: 0.25rem;
        }
        
        /* Container */
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            padding: 2rem 1.5rem;
        }
        
        /* Card */
        .card {
            background: #ffffff;
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            border: 1px solid #e2e8f0;
        }
        
        .card-title {
            font-size: 1.25rem;
            font-weight: 600;
            color: #0f172a;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        /* Form */
        .form-group {
            margin-bottom: 1.5rem;
        }
        
        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: 500;
            color: #334155;
            font-size: 0.875rem;
        }
        
        input, textarea, select {
            width: 100%;
            padding: 0.75rem 1rem;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            font-size: 0.9375rem;
            font-family: 'Inter', sans-serif;
            transition: all 0.2s;
            background: #ffffff;
            color: #1e293b;
        }
        
        input:focus, textarea:focus, select:focus {
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }
        
        textarea {
            min-height: 100px;
            resize: vertical;
        }
        
        .form-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
        }
        
        /* Button */
        button {
            width: 100%;
            padding: 1rem 1.5rem;
            background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
            font-family: 'Inter', sans-serif;
            box-shadow: 0 4px 6px -1px rgba(59, 130, 246, 0.3);
        }
        
        button:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.4);
        }
        
        button:active {
            transform: translateY(0);
        }
        
        button:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }
        
        .btn-secondary {
            background: #64748b;
            box-shadow: 0 4px 6px -1px rgba(100, 116, 139, 0.3);
        }
        
        .btn-secondary:hover {
            background: #475569;
            box-shadow: 0 10px 15px -3px rgba(100, 116, 139, 0.4);
        }
        
        /* Result */
        .result {
            display: none;
            animation: fadeInUp 0.5s ease-out;
        }
        
        @keyframes fadeInUp {
            from { 
                opacity: 0; 
                transform: translateY(20px); 
            }
            to { 
                opacity: 1; 
                transform: translateY(0); 
            }
        }
        
        /* Verdict */
        .verdict-card {
            text-align: center;
            padding: 2.5rem 2rem;
            border-radius: 12px;
            margin-bottom: 1.5rem;
            border: 2px solid;
        }
        
        .verdict-card.red { 
            background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
            border-color: #fca5a5;
            color: #991b1b;
        }
        
        .verdict-card.orange { 
            background: linear-gradient(135deg, #fffbeb 0%, #fed7aa 100%);
            border-color: #fdba74;
            color: #9a3412;
        }
        
        .verdict-card.yellow { 
            background: linear-gradient(135deg, #fefce8 0%, #fef3c7 100%);
            border-color: #fde047;
            color: #854d0e;
        }
        
        .verdict-card.green { 
            background: linear-gradient(135deg, #f0fdf4 0%, #d1fae5 100%);
            border-color: #86efac;
            color: #065f46;
        }
        
        .verdict-emoji {
            font-size: 4rem;
            margin-bottom: 1rem;
            display: block;
        }
        
        .verdict-text {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }
        
        .fraud-score-container {
            text-align: center;
            padding: 2rem;
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            border-radius: 12px;
            margin-bottom: 1.5rem;
            border: 1px solid #e2e8f0;
        }
        
        .fraud-score-label {
            font-size: 0.875rem;
            color: #64748b;
            font-weight: 500;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }
        
        .fraud-score {
            font-size: 3.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* Details */
        .details-section {
            margin-bottom: 1.5rem;
        }
        
        .section-title {
            font-size: 1.125rem;
            font-weight: 600;
            color: #0f172a;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .detail-item {
            padding: 1.25rem;
            background: #f8fafc;
            border-radius: 8px;
            margin-bottom: 0.75rem;
            border-left: 4px solid #3b82f6;
            transition: all 0.2s;
        }
        
        .detail-item:hover {
            background: #f1f5f9;
            transform: translateX(4px);
        }
        
        .detail-header {
            font-weight: 600;
            color: #0f172a;
            margin-bottom: 0.5rem;
            font-size: 1rem;
        }
        
        .detail-content {
            color: #475569;
            line-height: 1.7;
            font-size: 0.9375rem;
        }
        
        .detail-content strong {
            color: #1e293b;
            font-weight: 600;
        }
        
        /* Recommendation */
        .recommendation-card {
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            padding: 1.5rem;
            border-radius: 12px;
            border: 1px solid #93c5fd;
            margin-top: 1.5rem;
        }
        
        .recommendation-title {
            font-weight: 600;
            color: #1e40af;
            margin-bottom: 0.75rem;
            font-size: 1.125rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .recommendation-text {
            color: #1e40af;
            line-height: 1.7;
            font-size: 0.9375rem;
        }
        
        /* Loading */
        .loading {
            display: none;
            text-align: center;
            padding: 3rem 2rem;
        }
        
        .spinner {
            border: 4px solid #e2e8f0;
            border-top: 4px solid #3b82f6;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            animation: spin 1s linear infinite;
            margin: 0 auto 1rem;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .loading-text {
            color: #64748b;
            font-size: 1rem;
            font-weight: 500;
        }
        
        /* Responsive */
        @media (max-width: 768px) {
            .header {
                padding: 1.5rem 1rem;
            }
            
            h1 {
                font-size: 1.5rem;
            }
            
            .container {
                padding: 1.5rem 1rem;
            }
            
            .card {
                padding: 1.5rem;
            }
            
            .form-row {
                grid-template-columns: 1fr;
            }
            
            .fraud-score {
                font-size: 2.5rem;
            }
            
            .verdict-text {
                font-size: 1.25rem;
            }
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div class="logo">
                <span class="logo-icon">🏠</span>
                <div>
                    <h1>Real Estate Fraud Detection System</h1>
                    <p class="subtitle">Professional Property Verification & Risk Analysis</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="container">
        <div class="card">
            <h2 class="card-title">
                <span>📋</span>
                Property Information
            </h2>
            
            <form id="fraudCheckForm">
                <div class="form-group">
                    <label>Property Title *</label>
                    <input type="text" id="title" required placeholder="e.g., 3BHK Luxury Apartment in Gachibowli">
                </div>
                
                <div class="form-group">
                    <label>Description *</label>
                    <textarea id="description" required placeholder="Describe the property features, amenities, and location..."></textarea>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label>Price (₹) *</label>
                        <input type="number" id="price" required placeholder="e.g., 5000000">
                    </div>
                    
                    <div class="form-group">
                        <label>Area (sqft) *</label>
                        <input type="number" id="area_sqft" required placeholder="e.g., 1200">
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label>City *</label>
                        <select id="city" required>
                            <option value="">Select City</option>
                            <option value="Hyderabad">Hyderabad</option>
                            <option value="Mumbai">Mumbai</option>
                            <option value="Bangalore">Bangalore</option>
                            <option value="Delhi">Delhi</option>
                            <option value="Pune">Pune</option>
                            <option value="Chennai">Chennai</option>
                            <option value="Kolkata">Kolkata</option>
                            <option value="Ahmedabad">Ahmedabad</option>
                        </select>
                    </div>
                    
                    <div class="form-group">
                        <label>Locality *</label>
                        <input type="text" id="locality" required placeholder="e.g., Gachibowli">
                    </div>
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label>Bedrooms</label>
                        <input type="number" id="bedrooms" value="2" min="1" max="10">
                    </div>
                    
                    <div class="form-group">
                        <label>Bathrooms</label>
                        <input type="number" id="bathrooms" value="2" min="1" max="10">
                    </div>
                </div>
                
                <div class="form-group">
                    <label>Property Type</label>
                    <select id="property_type">
                        <option value="Apartment">Apartment</option>
                        <option value="Villa">Villa</option>
                        <option value="Plot">Plot/Land</option>
                        <option value="House">Independent House</option>
                    </select>
                </div>
                
                <button type="submit">🔍 Analyze Property for Fraud</button>
            </form>
            
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p class="loading-text">Analyzing property listing...</p>
            </div>
        </div>
        
        <div class="card result" id="result">
            <div class="verdict-card" id="verdict">
                <span class="verdict-emoji" id="verdictEmoji"></span>
                <div class="verdict-text" id="verdictText"></div>
            </div>
            
            <div class="fraud-score-container">
                <div class="fraud-score-label">Fraud Probability</div>
                <div class="fraud-score" id="fraudScore"></div>
            </div>
            
            <div class="details-section">
                <h3 class="section-title">
                    <span>📊</span>
                    Detailed Analysis
                </h3>
                <div id="detailsContainer"></div>
            </div>
            
            <div class="recommendation-card">
                <div class="recommendation-title">
                    <span>💡</span>
                    Recommendation
                </div>
                <div class="recommendation-text" id="recommendationText"></div>
            </div>
            
            <button onclick="checkAnother()" class="btn-secondary" style="margin-top: 1.5rem;">
                ← Check Another Property
            </button>
        </div>
    </div>
    
    <script>
        document.getElementById('fraudCheckForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Show loading
            document.getElementById('loading').style.display = 'block';
            document.getElementById('result').style.display = 'none';
            
            // Get form data
            const data = {
                title: document.getElementById('title').value,
                description: document.getElementById('description').value,
                price: parseFloat(document.getElementById('price').value),
                area_sqft: parseFloat(document.getElementById('area_sqft').value),
                city: document.getElementById('city').value,
                locality: document.getElementById('locality').value,
                bedrooms: parseInt(document.getElementById('bedrooms').value),
                bathrooms: parseInt(document.getElementById('bathrooms').value),
                property_type: document.getElementById('property_type').value
            };
            
            try {
                // Call API
                const response = await fetch('/api/check-fraud', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                });
                
                const result = await response.json();
                
                // Hide loading
                document.getElementById('loading').style.display = 'none';
                
                // Show result
                displayResult(result);
                
            } catch (error) {
                alert('Error: ' + error.message);
                document.getElementById('loading').style.display = 'none';
            }
        });
        
        function displayResult(result) {
            // Set verdict
            const verdictDiv = document.getElementById('verdict');
            verdictDiv.className = 'verdict-card ' + result.verdict_color;
            document.getElementById('verdictEmoji').textContent = result.verdict_emoji;
            document.getElementById('verdictText').textContent = result.verdict;
            
            // Set fraud score
            const scorePercent = (result.fraud_probability * 100).toFixed(0);
            document.getElementById('fraudScore').textContent = scorePercent + '%';
            
            // Set details
            const detailsContainer = document.getElementById('detailsContainer');
            detailsContainer.innerHTML = '';
            
            result.details.forEach(detail => {
                const detailDiv = document.createElement('div');
                detailDiv.className = 'detail-item';
                detailDiv.innerHTML = `
                    <div class="detail-header">${detail.type}</div>
                    <div class="detail-content">
                        <strong>${detail.warning}</strong><br>
                        ${detail.reason || ''}
                        ${detail.price_per_sqft ? `<br>Price per sqft: ₹${detail.price_per_sqft} (Market avg: ₹${detail.market_avg})` : ''}
                        ${detail.suspicious_keywords && detail.suspicious_keywords.length > 0 ? `<br>Suspicious words: ${detail.suspicious_keywords.join(', ')}` : ''}
                    </div>
                `;
                detailsContainer.appendChild(detailDiv);
            });
            
            // Set recommendation
            document.getElementById('recommendationText').textContent = result.recommendation;
            
            // Show result
            document.getElementById('result').style.display = 'block';
            document.getElementById('result').scrollIntoView({ behavior: 'smooth' });
        }
        
        function checkAnother() {
            document.getElementById('result').style.display = 'none';
            document.getElementById('fraudCheckForm').reset();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    </script>
</body>
</html>
"""

# ============================================================
# ROUTES
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def get_interface():
    """Serve the fraud detection interface"""
    return html_interface

@app.post("/api/check-fraud")
async def check_fraud(listing: PropertyListing):
    """
    Check if a property listing is fraudulent
    
    Returns detailed fraud analysis
    """
    result = detector.analyze(listing)
    return result

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Real Estate Fraud Detection",
        "version": "3.0.0",
        "port": 9000
    }

@app.on_event("startup")
async def startup_event():
    print("=" * 80)
    print("  🏠 REAL ESTATE FRAUD DETECTION SYSTEM")
    print("  Check if Property is FAKE or REAL")
    print("  Version: 3.0.0")
    print("=" * 80)
    print("✅ Server started successfully!")
    print("")
    print("📝 Open your browser and go to:")
    print("   👉 http://localhost:9000")
    print("")
    print("🔍 How to use:")
    print("   1. Enter property details (title, price, area, city, etc.)")
    print("   2. Click 'Check if FAKE or REAL'")
    print("   3. Get instant fraud analysis!")
    print("=" * 80)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
