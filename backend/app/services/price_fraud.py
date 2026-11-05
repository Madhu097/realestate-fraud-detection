"""
Price Fraud Detection Service
Detects price anomalies, severe underpricing (advance-fee scams), and price gouging
using trained Machine Learning models and locality price-per-sqft distributions.
"""
from app.utils.ml_imports import pd, HAS_PANDAS
from app.utils.ml_code import estimate_fair_price

def detect_price_fraud(
    listing_price: float,
    locality: str,
    city: str,
    area_sqft: float = None,
    bedrooms: int = None,
    df=None
):
    """
    Detect price fraud using trained ML price predictor and locality distribution.
    
    Args:
        listing_price: Price of the listing to analyze
        locality: Locality name
        city: City name
        area_sqft: Floor area in sqft (crucial for per-sqft valuation)
        bedrooms: Bedroom count (optional)
        df: Real estate dataset (optional)
        
    Returns:
        tuple: (fraud_score, explanation)
            - fraud_score (float): 0.0 to 1.0
            - explanation (str): Human-readable explanation with statistics
    """
    if listing_price <= 0:
        return 0.9, "Invalid listing price (₹0 or negative). Property must have a valid non-zero price."
        
    # If area is provided, perform accurate price-per-sqft and ML valuation
    if area_sqft and area_sqft > 0:
        actual_pps = listing_price / area_sqft
        fair_price, fair_pps, base_pps, loc_std = estimate_fair_price(
            area=area_sqft,
            bedrooms=bedrooms or 2,
            city=city,
            locality=locality
        )
        
        ratio = listing_price / max(fair_price, 1000.0)
        
        # 1. Normal fair market price range (within 30% of fair market value)
        if 0.70 <= ratio <= 1.40:
            deviation_pct = abs(listing_price - fair_price) / fair_price * 100.0
            return 0.0, (
                f"The listed price of ₹{listing_price:,.0f} (₹{actual_pps:,.0f}/sqft) is consistent with "
                f"the ML-estimated fair market value of ₹{fair_price:,.0f} (₹{fair_pps:,.0f}/sqft) "
                f"for a {area_sqft:,.0f} sqft property in '{locality}', {city} "
                f"(deviation: {deviation_pct:.1f}%). No price anomaly detected."
            )
            
        # 2. Mildly discounted (30% to 50% below market value)
        elif 0.50 <= ratio < 0.70:
            discount_pct = (fair_price - listing_price) / fair_price * 100.0
            score = 0.25 + (0.70 - ratio) * 1.0  # Scales 0.25 - 0.45
            return round(score, 2), (
                f"The listed price of ₹{listing_price:,.0f} (₹{actual_pps:,.0f}/sqft) is {discount_pct:.1f}% below "
                f"the ML-estimated fair market value of ₹{fair_price:,.0f} in '{locality}', {city}. "
                f"While this may represent a good deal, buyers should verify legal ownership and documentation."
            )
            
        # 3. Severe Underpricing (> 50% below market value - Classic Deposit Bait Scam)
        elif ratio < 0.50:
            discount_pct = (fair_price - listing_price) / fair_price * 100.0
            score = min(0.60 + (0.50 - ratio) * 0.9, 0.98) # Scales 0.60 - 0.98
            return round(score, 2), (
                f"🚨 SEVERE UNDERPRICING / ADVANCE-FEE SCAM RISK: The listed price of ₹{listing_price:,.0f} "
                f"(₹{actual_pps:,.0f}/sqft) is {discount_pct:.1f}% below the ML-estimated fair market value "
                f"of ₹{fair_price:,.0f} (expected range: ₹{fair_price*0.75:,.0f} - ₹{fair_price*1.30:,.0f}) "
                f"for '{locality}'. Unusually low prices are a common hallmark of deposit fraud where scammers "
                f"demand token money before viewing."
            )
            
        # 4. Severe Overpricing (> 40% above fair market value)
        else:
            premium_pct = (listing_price - fair_price) / fair_price * 100.0
            score = min(0.35 + (ratio - 1.40) * 0.35, 0.85) # Scales 0.35 - 0.85
            return round(score, 2), (
                f"⚠️ SIGNIFICANT OVERPRICING: The listed price of ₹{listing_price:,.0f} "
                f"(₹{actual_pps:,.0f}/sqft) is {premium_pct:.1f}% higher than the ML-estimated fair "
                f"market value of ₹{fair_price:,.0f} in '{locality}', {city}. This may indicate price manipulation "
                f"or speculative inflation."
            )
            
    # Fallback if area_sqft is not provided:
    fair_price, fair_pps, base_pps, loc_std = estimate_fair_price(
        area=1000.0, bedrooms=2, city=city, locality=locality
    )
    ratio = listing_price / max(fair_price, 1000.0)
    if 0.5 <= ratio <= 2.0:
        return 0.0, f"Listed price ₹{listing_price:,.0f} appears within general parameters for '{locality}'."
    elif ratio < 0.5:
        return 0.75, f"Listed price ₹{listing_price:,.0f} is unusually low compared to locality averages."
    else:
        return 0.60, f"Listed price ₹{listing_price:,.0f} is unusually high compared to locality averages."
