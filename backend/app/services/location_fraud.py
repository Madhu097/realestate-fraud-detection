"""
Location Fraud Detection Service
Detects misleading or fraudulent location information using geospatial analysis
and realistic metropolitan locality boundaries.
"""
import math
import json
import os
from pathlib import Path
from typing import Tuple, Optional, Dict

# Reference data file
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
LOCALITY_COORDS_FILE = DATA_DIR / "locality_coordinates.json"

# Realistic metropolitan distance thresholds (in kilometers)
ACCEPTABLE_DISTANCE_KM = 4.5  # Typical Indian metropolitan locality radius
SUSPICIOUS_DISTANCE_KM = 8.0   # Suburban extension
HIGH_RISK_DISTANCE_KM = 15.0   # Clear location spoofing / wrong district


def load_locality_coordinates() -> Dict[str, Dict]:
    """
    Load locality coordinate reference data
    
    Returns:
        dict: "city|locality" -> coordinate data mapping
    """
    if not LOCALITY_COORDS_FILE.exists():
        return {}
    
    try:
        with open(LOCALITY_COORDS_FILE, 'r', encoding='utf-8') as f:
            localities = json.load(f)
            
        locality_dict = {}
        for loc in localities:
            city = loc.get('city', '').lower().strip()
            locality = loc.get('locality', '').lower().strip()
            
            full_key = f"{city}|{locality}"
            locality_dict[full_key] = loc
            locality_dict[locality] = loc
        
        return locality_dict
    except Exception as e:
        print(f"Error loading locality coordinates: {e}")
        return {}


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate great-circle distance between two coordinates in km"""
    if lat1 == 0 or lon1 == 0 or lat2 == 0 or lon2 == 0:
        return 0.0
    R = 6371.0
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(max(0.0, min(1.0, a))))
    return R * c


def validate_coordinates(latitude: float, longitude: float) -> bool:
    """Validate coordinate bounds"""
    return -90 <= latitude <= 90 and -180 <= longitude <= 180


def detect_location_fraud(
    locality: str,
    latitude: float,
    longitude: float,
    city: str,
    price: Optional[float] = None
) -> Tuple[float, str]:
    """
    Detect location fraud using geospatial distance from verified locality boundaries.
    """
    locality_data = load_locality_coordinates()
    
    # Check if coordinates provided
    if latitude is None or longitude is None or (latitude == 0 and longitude == 0):
        return 0.0, "Coordinates not provided. Location verification skipped."
    
    if not validate_coordinates(latitude, longitude):
        return 0.85, (
            f"Invalid GPS coordinates provided (Lat: {latitude}, Lon: {longitude}). "
            f"Coordinates fall outside valid geographic bounds."
        )
    
    locality_key = locality.lower().strip()
    city_key = city.lower().strip()
    full_key = f"{city_key}|{locality_key}"
    
    ref_data = locality_data.get(full_key) or locality_data.get(locality_key)
    
    if ref_data is None:
        # Locality not explicitly cataloged
        return 0.0, (
            f"The locality '{locality}' is not yet mapped in our high-resolution geospatial registry. "
            f"No geospatial fraud detected."
        )
    
    ref_lat = ref_data.get('latitude')
    ref_lon = ref_data.get('longitude')
    
    if not ref_lat or not ref_lon:
        return 0.0, f"Geographic center data unavailable for '{locality}'."
        
    distance_km = haversine_distance(ref_lat, ref_lon, latitude, longitude)
    
    # 1. Within authentic locality radius
    if distance_km <= ACCEPTABLE_DISTANCE_KM:
        return 0.0, (
            f"The property is located approximately {distance_km:.2f} km from the center of '{locality}', "
            f"which is well within the authentic neighborhood radius. Location verified accurate."
        )
    # 2. Suburban extension (4.5 to 8 km)
    elif distance_km <= SUSPICIOUS_DISTANCE_KM:
        score = 0.15 + (distance_km - ACCEPTABLE_DISTANCE_KM) / (SUSPICIOUS_DISTANCE_KM - ACCEPTABLE_DISTANCE_KM) * 0.20
        return round(score, 2), (
            f"The property is located {distance_km:.2f} km from '{locality}' center. "
            f"This represents an adjoining or suburban extension of '{locality}'."
        )
    # 3. Moderate deviation (8 to 15 km)
    elif distance_km <= HIGH_RISK_DISTANCE_KM:
        score = 0.40 + (distance_km - SUSPICIOUS_DISTANCE_KM) / (HIGH_RISK_DISTANCE_KM - SUSPICIOUS_DISTANCE_KM) * 0.25
        return round(score, 2), (
            f"⚠️ LOCATION DISCREPANCY: The listing coordinates are {distance_km:.2f} km away "
            f"from the center of '{locality}'. The property may be outside the advertised neighborhood."
        )
    # 4. Severe location spoofing (> 15 km away)
    else:
        score = min(0.65 + (distance_km - HIGH_RISK_DISTANCE_KM) * 0.02, 0.95)
        return round(score, 2), (
            f"🚨 HIGH GEOSPATIAL MISMATCH: The property coordinates are {distance_km:.1f} km away "
            f"from '{locality}'. Claiming a property is in '{locality}' when coordinates are "
            f"{distance_km:.1f} km distant strongly indicates false or misleading location marketing."
        )
