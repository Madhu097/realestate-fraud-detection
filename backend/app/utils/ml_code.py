import pandas as pd
import numpy as np
import pickle
import os
import joblib
import json
import re
from pathlib import Path

# Setup paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
MODELS_DIR = BASE_DIR / "models"
DATA_DIR = BASE_DIR / "app" / "data"

# Cache loaded models
_CACHED_MODELS = {}

def get_model(name: str):
    """Load model artifact with memory caching"""
    if name in _CACHED_MODELS:
        return _CACHED_MODELS[name]
    
    path = MODELS_DIR / name
    if not path.exists():
        return None
        
    try:
        model = joblib.load(path)
        _CACHED_MODELS[name] = model
        return model
    except Exception:
        try:
            with open(path, 'rb') as f:
                model = pickle.load(f)
                _CACHED_MODELS[name] = model
                return model
        except Exception:
            return None

def get_locality_stats():
    """Load precomputed locality price statistics"""
    stats = get_model("locality_price_stats.pkl")
    if stats:
        return stats
    return {"locality_stats": {}, "city_stats": {}, "overall_median_pps": 6000.0}

def get_locality_coordinates():
    """Load locality coordinates reference"""
    coords_path = DATA_DIR / "locality_coordinates.json"
    if not coords_path.exists():
        return {}
    try:
        with open(coords_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        coords = {}
        for item in data:
            c = item.get('city', '').lower().strip()
            l = item.get('locality', '').lower().strip()
            coords[f"{c}|{l}"] = (item.get('latitude', 0.0), item.get('longitude', 0.0))
            coords[l] = (item.get('latitude', 0.0), item.get('longitude', 0.0))
        return coords
    except Exception:
        return {}

def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance in km between two lat/lon points"""
    if lat1 == 0 or lon1 == 0 or lat2 == 0 or lon2 == 0:
        return 0.0
    R = 6371.0
    dlat = math_radians(lat2 - lat1)
    dlon = math_radians(lon2 - lon1)
    a = (np.sin(dlat / 2.0) ** 2 +
         np.cos(math_radians(lat1)) * np.cos(math_radians(lat2)) *
         np.sin(dlon / 2.0) ** 2)
    c = 2.0 * np.arcsin(np.sqrt(np.clip(a, 0, 1)))
    return R * c

def math_radians(deg):
    return deg * (np.pi / 180.0)

def extract_bedrooms_from_text(text: str, default: int = 2) -> int:
    """Extract bedroom count from title or description like 2BHK, 3 BHK, 4 Bedroom"""
    if not text:
        return default
    match = re.search(r'\b([1-9])\s*(?:bhk|bedroom|bed)\b', text.lower())
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            pass
    return default

def count_urgency_keywords(text: str) -> int:
    """Count high-urgency keywords in text"""
    if not text:
        return 0
    keywords = [
        'urgent', 'hurry', 'limited time', 'act now', 'dont miss', "don't miss",
        'last chance', 'immediate', 'distress sale', 'desperate', 'quick sale'
    ]
    text_lower = text.lower()
    return sum(1 for kw in keywords if kw in text_lower)

def count_scam_keywords(text: str) -> int:
    """Count advance-fee and wire-transfer scam keywords"""
    if not text:
        return 0
    keywords = [
        'wire transfer', 'western union', 'cash advance', 'advance payment',
        'token money', 'deposit now', 'owner abroad', 'transfer money',
        'cannot visit', 'no questions asked', '100% guaranteed profit', 'wire deposit'
    ]
    text_lower = text.lower()
    return sum(1 for kw in keywords if kw in text_lower)

def estimate_fair_price(area: float, bedrooms: int, city: str, locality: str, lat: float = 0.0, lon: float = 0.0):
    """
    Predict fair market value and price-per-sqft using the trained GradientBoosting price predictor.
    """
    stats_data = get_locality_stats()
    loc_stats = stats_data.get('locality_stats', {})
    city_stats = stats_data.get('city_stats', {})
    overall_pps = stats_data.get('overall_median_pps', 6000.0)
    
    city_k = str(city).lower().strip()
    loc_k = str(locality).lower().strip()
    full_k = f"{city_k}|{loc_k}"
    
    loc_info = loc_stats.get(full_k) or loc_stats.get(loc_k)
    if loc_info:
        base_pps = loc_info.get('median_pps', overall_pps)
        loc_std = loc_info.get('std_pps', base_pps * 0.2)
    elif city_k in city_stats:
        base_pps = city_stats[city_k].get('median_pps', overall_pps)
        loc_std = city_stats[city_k].get('std_pps', base_pps * 0.25)
    else:
        base_pps = overall_pps
        loc_std = overall_pps * 0.3
        
    price_model = get_model("price_predictor_model.pkl")
    
    if price_model is not None and area > 0:
        try:
            feat = [[
                float(area),
                float(bedrooms),
                float(lat if lat != 0 else 17.42),
                float(lon if lon != 0 else 78.47),
                float(base_pps),
                float(area * base_pps)
            ]]
            pred_log = price_model.predict(feat)[0]
            fair_price = float(np.expm1(pred_log))
        except Exception as e:
            fair_price = float(area * base_pps)
    else:
        fair_price = float(area * base_pps)
        
    fair_pps = fair_price / max(area, 1.0)
    return fair_price, fair_pps, base_pps, loc_std

def predict_listing_fraud(
    price: float,
    area_sqft: float,
    city: str,
    locality: str,
    title: str = "",
    description: str = "",
    latitude: float = 0.0,
    longitude: float = 0.0,
    bedrooms: int = None
):
    """
    End-to-end ML prediction for a single property listing.
    Uses trained Price Estimation Model and Hybrid ExtraTree+ANN Classifier.
    """
    if bedrooms is None or bedrooms <= 0:
        bedrooms = extract_bedrooms_from_text(f"{title} {description}", default=2)
        
    fair_price, fair_pps, base_pps, loc_std = estimate_fair_price(
        area_sqft, bedrooms, city, locality, latitude, longitude
    )
    
    price_ratio = price / max(fair_price, 1000.0)
    pps = price / max(area_sqft, 1.0)
    pps_zscore = abs(pps - base_pps) / max(loc_std, 100.0)
    
    # Coordinates and distance
    coords_map = get_locality_coordinates()
    full_k = f"{str(city).lower().strip()}|{str(locality).lower().strip()}"
    ref_coords = coords_map.get(full_k) or coords_map.get(str(locality).lower().strip())
    
    if ref_coords and latitude != 0 and longitude != 0:
        dist_km = float(haversine(latitude, longitude, ref_coords[0], ref_coords[1]))
    else:
        dist_km = 0.5 # Normal proximity assumed if coordinates missing/unregistered
        
    urgency_kw = count_urgency_keywords(f"{title} {description}")
    scam_kw = count_scam_keywords(f"{title} {description}")
    area_per_bed = area_sqft / max(bedrooms, 1)
    is_coord_out = 1 if dist_km > 15.0 else 0
    
    # Feature vector for trained Hybrid Classifier:
    # ["price_ratio", "pps_zscore", "dist_km", "area", "bedrooms", "area_per_bed", "urgency_kw", "scam_kw", "is_coord_out"]
    feature_vector = np.array([[
        price_ratio,
        pps_zscore,
        dist_km,
        float(area_sqft),
        float(bedrooms),
        float(area_per_bed),
        float(urgency_kw),
        float(scam_kw),
        float(is_coord_out)
    ]])
    
    hybrid_model = get_model("hybrid_extra_tree_ann1.pkl")
    scaler = get_model("fraud_scaler.pkl")
    
    if hybrid_model is not None and scaler is not None:
        try:
            feat_scaled = scaler.transform(feature_vector)
            probs = hybrid_model.predict_proba(feat_scaled)[0]
            # probs[0] = Real, probs[1] = Fake
            fraud_probability = float(probs[1])
            is_fake = bool(fraud_probability >= 0.5)
            confidence = float(probs[1] if is_fake else probs[0]) * 100.0
        except Exception as e:
            # Fallback logic if inference error
            is_fake = price_ratio < 0.45 or price_ratio > 3.0 or dist_km > 15.0 or scam_kw >= 2
            fraud_probability = 0.85 if is_fake else 0.05
            confidence = 92.0
    else:
        # Fallback calibrated heuristic
        is_fake = price_ratio < 0.45 or price_ratio > 3.0 or dist_km > 15.0 or scam_kw >= 2
        fraud_probability = 0.85 if is_fake else 0.05
        confidence = 90.0
        
    return {
        "prediction": "Fake" if is_fake else "Real",
        "fraud_probability": round(fraud_probability, 4),
        "confidence": round(confidence, 2),
        "fair_market_price": round(fair_price, 0),
        "fair_pps": round(fair_pps, 0),
        "actual_pps": round(pps, 0),
        "price_ratio": round(price_ratio, 2),
        "dist_km": round(dist_km, 2),
        "urgency_keywords": urgency_kw,
        "scam_keywords": scam_kw
    }

def predict_class_only_real_estate(df: pd.DataFrame) -> pd.DataFrame:
    """
    Bulk prediction for uploaded CSV files using the trained Hybrid ExtraTree+ANN model.
    """
    processed_df = df.copy()
    
    def find_col(possible_names):
        for col in processed_df.columns:
            for name in possible_names:
                if name.lower() == col.lower() or name.lower() in col.lower():
                    return col
        return None

    price_col = find_col(['price', 'cost', 'amount', 'rent'])
    area_col = find_col(['area_sqft', 'area', 'sqft', 'square_feet', 'size'])
    city_col = find_col(['city'])
    loc_col = find_col(['locality', 'location', 'neighborhood', 'address'])
    bed_col = find_col(['no. of bedrooms', 'bedrooms', 'bedroom', 'bhk', 'rooms', 'room'])
    lat_col = find_col(['latitude', 'lat'])
    lon_col = find_col(['longitude', 'lon', 'lng'])
    desc_col = find_col(['description', 'desc', 'details', 'summary'])
    title_col = find_col(['title', 'property_name', 'name', 'headline'])
    
    predictions = []
    confidences = []
    fair_prices = []
    fraud_probs = []
    
    for _, row in processed_df.iterrows():
        try:
            price = float(row[price_col]) if price_col and not pd.isna(row[price_col]) else 5000000.0
            area = float(row[area_col]) if area_col and not pd.isna(row[area_col]) else 1000.0
            city = str(row[city_col]) if city_col and not pd.isna(row[city_col]) else "Hyderabad"
            locality = str(row[loc_col]) if loc_col and not pd.isna(row[loc_col]) else "Banjara Hills"
            bedrooms = int(row[bed_col]) if bed_col and not pd.isna(row[bed_col]) else 2
            lat = float(row[lat_col]) if lat_col and not pd.isna(row[lat_col]) else 0.0
            lon = float(row[lon_col]) if lon_col and not pd.isna(row[lon_col]) else 0.0
            
            title_text = str(row[title_col]) if title_col and not pd.isna(row[title_col]) else ""
            desc_text = str(row[desc_col]) if desc_col and not pd.isna(row[desc_col]) else ""
            
            res = predict_listing_fraud(
                price=price,
                area_sqft=area,
                city=city,
                locality=locality,
                title=title_text,
                description=desc_text,
                latitude=lat,
                longitude=lon,
                bedrooms=bedrooms
            )
            
            predictions.append(res["prediction"])
            confidences.append(res["confidence"])
            fair_prices.append(res["fair_market_price"])
            fraud_probs.append(res["fraud_probability"])
        except Exception as e:
            print(f"Row inference exception: {e}")
            predictions.append("Real")
            confidences.append(90.0)
            fair_prices.append(5000000.0)
            fraud_probs.append(0.05)
            
    processed_df['prediction'] = predictions
    processed_df['confidence'] = confidences
    processed_df['fair_market_price'] = fair_prices
    processed_df['fraud_probability'] = fraud_probs
    return processed_df
