"""
Location Fraud Detection Service
Detects misleading or fraudulent location information using geospatial analysis
"""
import math
import json
import os
from typing import Tuple, Optional, Dict
from geopy.distance import geodesic

# Reference data file
LOCALITY_COORDS_FILE = "app/data/locality_coordinates.json"

# Distance thresholds (in kilometers)
SUSPICIOUS_DISTANCE_KM = 1.5  # > 1.5 km is suspicious
HIGH_RISK_DISTANCE_KM = 3.0   # > 3 km is high risk

# Price deviation threshold (for combined fraud detection)
PRICE_DEVIATION_THRESHOLD = 0.3  # 30% deviation


def load_locality_coordinates() -> Dict[str, Dict]:
    """
    Load locality coordinate reference data
    
    Returns:
        dict: "city|locality" -> coordinate data mapping
    """
    if not os.path.exists(LOCALITY_COORDS_FILE):
        return {}
    
    try:
        with open(LOCALITY_COORDS_FILE, 'r', encoding='utf-8') as f:
            localities = json.load(f)
            
        # Convert list to dict for faster lookup
        locality_dict = {}
        for loc in localities:
            # Use composite key "city|locality" for precise matching
            # Also lowercase for case-insensitive matching
            city = loc.get('city', '').lower().strip()
            locality = loc['locality'].lower().strip()
            
            # Primary key: city|locality
            full_key = f"{city}|{locality}"
            locality_dict[full_key] = loc
            
            # Fallback key: just locality (if unique or for legacy support)
            # CAUTION: This might stick with the last loaded city if duplicates exist
            locality_dict[locality] = loc
        
        return locality_dict
    except Exception as e:
        print(f"Error loading locality coordinates: {e}")
        return {}


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two points using Haversine formula
    
    This is the great-circle distance between two points on a sphere
    given their longitudes and latitudes.
    
    Args:
        lat1: Latitude of point 1 (degrees)
        lon1: Longitude of point 1 (degrees)
        lat2: Latitude of point 2 (degrees)
        lon2: Longitude of point 2 (degrees)
        
    Returns:
        float: Distance in kilometers
    """
    # Earth's radius in kilometers
    R = 6371.0
    
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    distance = R * c
    
    return distance


def validate_coordinates(latitude: float, longitude: float) -> bool:
    """
    Validate if coordinates are within valid ranges
    
    Args:
        latitude: Latitude value
        longitude: Longitude value
        
    Returns:
        bool: True if valid, False otherwise
    """
    return -90 <= latitude <= 90 and -180 <= longitude <= 180


def detect_location_fraud(
    locality: str,
    latitude: float,
    longitude: float,
    city: str,
    price: Optional[float] = None
) -> Tuple[float, str]:
    """
    Detect location fraud using geospatial analysis
    
    Checks:
    1. Distance between claimed locality center and actual coordinates
    2. Price consistency with locality (if price provided)
    
    Args:
        locality: Claimed locality name
        latitude: Listing latitude
        longitude: Listing longitude
        city: Claimed city name
        price: Listing price (optional, for price-location sanity check)
        
    Returns:
        tuple: (location_fraud_score, explanation)
            - location_fraud_score (float): 0.0 to 1.0
            - explanation (str): Human-readable explanation
    """
    # Load reference data
    locality_data = load_locality_coordinates()
    
    # ============================================================
    # EDGE CASE 1: Missing or invalid coordinates
    # ============================================================
    if latitude is None or longitude is None:
        return 0.0, "Location coordinates not provided. Cannot perform location verification."
    
    if not validate_coordinates(latitude, longitude):
        return 0.8, (
            f"Invalid coordinates provided (Lat: {latitude}, Lon: {longitude}). "
            f"This may indicate fraudulent or incorrect location data."
        )
    
    # ============================================================
    # EDGE CASE 2: Unknown locality
    # ============================================================
    locality_key = locality.lower().strip()
    city_key = city.lower().strip()
    full_key = f"{city_key}|{locality_key}"
    
    ref_data = None
    
    # Try exact match first
    if full_key in locality_data:
        ref_data = locality_data[full_key]
    # Fallback to just locality match if city not found
    elif locality_key in locality_data:
        ref_data = locality_data[locality_key]
        # Check if the found locality belongs to a different city
        found_city = ref_data.get('city', '').lower()
        if found_city and found_city != city_key:
             # Match found but in different city
             # We treat this as "Locality not found in declared City"
             # But it's better to be conservative and say unknown
             ref_data = None

    if ref_data is None:
        # Unknown locality - cannot verify
        return 0.0, (
            f"The locality '{locality}' is not in our reference database. "
            f"Cannot verify location accuracy. This is not necessarily fraudulent, "
            f"but location verification is unavailable."
        )
    
    # ============================================================
    # EDGE CASE 3: Insufficient reference data
    # ============================================================
    # ref_data is already set from above logic
    
    if 'latitude' not in ref_data or 'longitude' not in ref_data:
        return 0.0, (
            f"Insufficient reference data for '{locality}'. "
            f"Cannot perform location verification."
        )
    
    # ============================================================
    # MAIN ANALYSIS: Calculate distance from locality center
    # ============================================================
    ref_lat = ref_data['latitude']
    ref_lon = ref_data['longitude']
    
    # Calculate distance using Haversine formula
    distance_km = haversine_distance(ref_lat, ref_lon, latitude, longitude)
    
    # Alternative: Use geopy for verification (more accurate)
    try:
        point1 = (ref_lat, ref_lon)
        point2 = (latitude, longitude)
        distance_km_geopy = geodesic(point1, point2).kilometers
        # Use geopy distance if available (more accurate)
        distance_km = distance_km_geopy
    except:
        # Fall back to Haversine if geopy fails
        pass
    
    # ============================================================
    # CALCULATE BASE FRAUD SCORE (based on distance)
    # ============================================================
    if distance_km <= SUSPICIOUS_DISTANCE_KM:
        # Within acceptable range
        distance_score = 0.0
        distance_risk = "low"
    elif distance_km <= HIGH_RISK_DISTANCE_KM:
        # Suspicious range (1.5 - 3 km)
        # Linear scaling: 1.5km -> 0.4, 3km -> 0.7
        distance_score = 0.4 + (distance_km - SUSPICIOUS_DISTANCE_KM) * 0.2
        distance_risk = "moderate"
    else:
        # High risk (> 3 km)
        # Cap at 0.9 to leave room for price boost
        distance_score = min(0.7 + (distance_km - HIGH_RISK_DISTANCE_KM) * 0.1, 0.9)
        distance_risk = "high"
    
    # ============================================================
    # PRICE-LOCATION SANITY CHECK (if price provided)
    # ============================================================
    price_boost = 0.0
    price_explanation = ""
    
    if price is not None and 'avg_price' in ref_data and ref_data['avg_price'] > 0:
        avg_price = ref_data['avg_price']
        price_deviation = abs(price - avg_price) / avg_price
        
        # If both distance AND price are anomalous, boost fraud score
        if distance_score > 0.3 and price_deviation > PRICE_DEVIATION_THRESHOLD:
            price_boost = 0.15  # Add 15% to fraud score
            price_explanation = (
                f" Additionally, the price (₹{price:,.0f}) deviates significantly "
                f"from the locality average (₹{avg_price:,.0f}), "
                f"which strengthens the suspicion of location fraud."
            )
    
    # ============================================================
    # FINAL FRAUD SCORE
    # ============================================================
    location_fraud_score = min(distance_score + price_boost, 1.0)
    
    # ============================================================
    # GENERATE EXPLANATION
    # ============================================================
    if distance_km <= SUSPICIOUS_DISTANCE_KM:
        explanation = (
            f"The property is located approximately {distance_km:.2f} km from the center of '{locality}', "
            f"which is within the acceptable range. Location information appears accurate."
        )
    elif distance_km <= HIGH_RISK_DISTANCE_KM:
        explanation = (
            f"⚠️ MODERATE RISK: The property is located approximately {distance_km:.2f} km away "
            f"from the claimed locality center of '{locality}'. "
            f"This distance is suspicious and may indicate misleading location information."
        )
    else:
        explanation = (
            f"⚠️ HIGH RISK: The property is located approximately {distance_km:.2f} km away "
            f"from the claimed locality center of '{locality}'. "
            f"This significant distance strongly suggests misleading or fraudulent location claims."
        )
    
    # Add price explanation if applicable
    explanation += price_explanation
    
    # Add reference coordinates for transparency
    explanation += (
        f"\n\nReference: '{locality}' center is at ({ref_lat:.4f}, {ref_lon:.4f}). "
        f"Listing coordinates: ({latitude:.4f}, {longitude:.4f})."
    )
    
    return location_fraud_score, explanation


def get_locality_info(locality: str) -> Optional[Dict]:
    """
    Get reference information for a locality
    
    Args:
        locality: Locality name
        
    Returns:
        dict: Locality information or None if not found
    """
    locality_data = load_locality_coordinates()
    locality_key = locality.lower().strip()
    return locality_data.get(locality_key)


def calculate_distance_between_localities(locality1: str, locality2: str) -> Optional[float]:
    """
    Calculate distance between two localities
    
    Args:
        locality1: First locality name
        locality2: Second locality name
        
    Returns:
        float: Distance in kilometers, or None if localities not found
    """
    locality_data = load_locality_coordinates()
    
    loc1_key = locality1.lower().strip()
    loc2_key = locality2.lower().strip()
    
    if loc1_key not in locality_data or loc2_key not in locality_data:
        return None
    
    loc1 = locality_data[loc1_key]
    loc2 = locality_data[loc2_key]
    
    if 'latitude' not in loc1 or 'latitude' not in loc2:
        return None
    
    distance = haversine_distance(
        loc1['latitude'], loc1['longitude'],
        loc2['latitude'], loc2['longitude']
    )
    
    return distance
