"""
External Location Verification Service
Uses multiple free APIs to verify location accuracy and detect fraud
"""
import requests
import time
from typing import Tuple, Dict, List, Optional
from geopy.distance import geodesic
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Configuration
NOMINATIM_BASE_URL = "https://nominatim.openstreetmap.org/reverse"
BIGDATACLOUD_BASE_URL = "https://api.bigdatacloud.net/data/reverse-geocode-client"
LOCATIONIQ_BASE_URL = "https://us1.locationiq.com/v1/reverse.php"
OPENCAGE_BASE_URL = "https://api.opencagedata.com/geocode/v1/json"
GEOAPIFY_BASE_URL = "https://api.geoapify.com/v1/geocode/reverse"

# API Keys (optional - some APIs don't require keys)
LOCATIONIQ_API_KEY = os.getenv("LOCATIONIQ_API_KEY", "")
OPENCAGE_API_KEY = os.getenv("OPENCAGE_API_KEY", "")
GEOAPIFY_API_KEY = os.getenv("GEOAPIFY_API_KEY", "")

# Rate limiting
LAST_NOMINATIM_CALL = 0
NOMINATIM_DELAY = 1.0  # 1 second between calls (Nominatim requirement)

# Thresholds
CONSENSUS_THRESHOLD = 0.6  # 60% of APIs must agree
DISTANCE_THRESHOLD_KM = 2.0  # Max acceptable distance from claimed location


def call_nominatim_api(latitude: float, longitude: float) -> Optional[Dict]:
    """
    Call OpenStreetMap Nominatim API for reverse geocoding
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        
    Returns:
        dict: API response or None if failed
    """
    global LAST_NOMINATIM_CALL
    
    # Rate limiting - Nominatim requires 1 second between requests
    current_time = time.time()
    time_since_last_call = current_time - LAST_NOMINATIM_CALL
    if time_since_last_call < NOMINATIM_DELAY:
        time.sleep(NOMINATIM_DELAY - time_since_last_call)
    
    try:
        params = {
            'lat': latitude,
            'lon': longitude,
            'format': 'json',
            'addressdetails': 1,
            'zoom': 18  # High zoom for precise results
        }
        
        headers = {
            'User-Agent': 'RealEstateFraudDetection/1.0'  # Required by Nominatim
        }
        
        response = requests.get(NOMINATIM_BASE_URL, params=params, headers=headers, timeout=5)
        LAST_NOMINATIM_CALL = time.time()
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Nominatim API error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Nominatim API exception: {e}")
        return None


def call_bigdatacloud_api(latitude: float, longitude: float) -> Optional[Dict]:
    """
    Call BigDataCloud API for reverse geocoding
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        
    Returns:
        dict: API response or None if failed
    """
    try:
        params = {
            'latitude': latitude,
            'longitude': longitude,
            'localityLanguage': 'en'
        }
        
        response = requests.get(BIGDATACLOUD_BASE_URL, params=params, timeout=5)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"BigDataCloud API error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"BigDataCloud API exception: {e}")
        return None


def call_locationiq_api(latitude: float, longitude: float) -> Optional[Dict]:
    """
    Call LocationIQ API for reverse geocoding
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        
    Returns:
        dict: API response or None if failed
    """
    if not LOCATIONIQ_API_KEY:
        return None
    
    try:
        params = {
            'key': LOCATIONIQ_API_KEY,
            'lat': latitude,
            'lon': longitude,
            'format': 'json',
            'addressdetails': 1
        }
        
        response = requests.get(LOCATIONIQ_BASE_URL, params=params, timeout=5)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"LocationIQ API error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"LocationIQ API exception: {e}")
        return None


def call_opencage_api(latitude: float, longitude: float) -> Optional[Dict]:
    """
    Call OpenCage API for reverse geocoding
    
    Args:
        latitude: Latitude coordinate
        longitude: Longitude coordinate
        
    Returns:
        dict: API response or None if failed
    """
    if not OPENCAGE_API_KEY:
        return None
    
    try:
        params = {
            'key': OPENCAGE_API_KEY,
            'q': f'{latitude},{longitude}',
            'language': 'en',
            'pretty': 0
        }
        
        response = requests.get(OPENCAGE_BASE_URL, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('results'):
                return data['results'][0]
            return None
        else:
            print(f"OpenCage API error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"OpenCage API exception: {e}")
        return None


def extract_location_info(api_name: str, api_response: Dict) -> Dict:
    """
    Extract standardized location information from API response
    
    Args:
        api_name: Name of the API
        api_response: Raw API response
        
    Returns:
        dict: Standardized location info
    """
    location_info = {
        'city': None,
        'locality': None,
        'suburb': None,
        'neighbourhood': None,
        'state': None,
        'country': None,
        'confidence': 0.0
    }
    
    try:
        if api_name == 'nominatim':
            address = api_response.get('address', {})
            location_info['city'] = (
                address.get('city') or 
                address.get('town') or 
                address.get('village') or
                address.get('municipality')
            )
            location_info['locality'] = address.get('suburb') or address.get('neighbourhood')
            location_info['suburb'] = address.get('suburb')
            location_info['neighbourhood'] = address.get('neighbourhood')
            location_info['state'] = address.get('state')
            location_info['country'] = address.get('country')
            location_info['confidence'] = 0.8  # Nominatim doesn't provide confidence
            
        elif api_name == 'bigdatacloud':
            location_info['city'] = api_response.get('city')
            location_info['locality'] = api_response.get('locality')
            location_info['suburb'] = api_response.get('localityInfo', {}).get('administrative', [{}])[0].get('name')
            location_info['state'] = api_response.get('principalSubdivision')
            location_info['country'] = api_response.get('countryName')
            location_info['confidence'] = 0.7
            
        elif api_name == 'locationiq':
            address = api_response.get('address', {})
            location_info['city'] = (
                address.get('city') or 
                address.get('town') or 
                address.get('village')
            )
            location_info['locality'] = address.get('suburb') or address.get('neighbourhood')
            location_info['suburb'] = address.get('suburb')
            location_info['neighbourhood'] = address.get('neighbourhood')
            location_info['state'] = address.get('state')
            location_info['country'] = address.get('country')
            location_info['confidence'] = 0.8
            
        elif api_name == 'opencage':
            components = api_response.get('components', {})
            location_info['city'] = (
                components.get('city') or 
                components.get('town') or 
                components.get('village')
            )
            location_info['locality'] = components.get('suburb') or components.get('neighbourhood')
            location_info['suburb'] = components.get('suburb')
            location_info['neighbourhood'] = components.get('neighbourhood')
            location_info['state'] = components.get('state')
            location_info['country'] = components.get('country')
            location_info['confidence'] = api_response.get('confidence', 0) / 10.0  # OpenCage uses 0-10 scale
            
    except Exception as e:
        print(f"Error extracting location info from {api_name}: {e}")
    
    return location_info


def normalize_string(s: Optional[str]) -> str:
    """Normalize string for comparison"""
    if not s:
        return ""
    return s.lower().strip().replace('-', ' ').replace('_', ' ')


def calculate_location_match(claimed_city: str, claimed_locality: str, api_results: List[Dict]) -> float:
    """
    Calculate how well the API results match the claimed location
    
    Args:
        claimed_city: Claimed city name
        claimed_locality: Claimed locality name
        api_results: List of location info from different APIs
        
    Returns:
        float: Match score (0.0 to 1.0)
    """
    if not api_results:
        return 0.0
    
    claimed_city_norm = normalize_string(claimed_city)
    claimed_locality_norm = normalize_string(claimed_locality)
    
    city_matches = 0
    locality_matches = 0
    total_apis = len(api_results)
    
    for result in api_results:
        # Check city match
        api_city = normalize_string(result.get('city'))
        if api_city and claimed_city_norm in api_city or api_city in claimed_city_norm:
            city_matches += 1
        
        # Check locality match (check multiple fields)
        api_locality = normalize_string(result.get('locality'))
        api_suburb = normalize_string(result.get('suburb'))
        api_neighbourhood = normalize_string(result.get('neighbourhood'))
        
        if any([
            claimed_locality_norm in api_locality or api_locality in claimed_locality_norm,
            claimed_locality_norm in api_suburb or api_suburb in claimed_locality_norm,
            claimed_locality_norm in api_neighbourhood or api_neighbourhood in claimed_locality_norm
        ]):
            locality_matches += 1
    
    # Calculate match score
    city_score = city_matches / total_apis
    locality_score = locality_matches / total_apis
    
    # Weighted average (city is more important)
    match_score = (city_score * 0.6) + (locality_score * 0.4)
    
    return match_score


def verify_location_with_external_apis(
    latitude: float,
    longitude: float,
    claimed_city: str,
    claimed_locality: str
) -> Tuple[float, str, Dict]:
    """
    Verify location using multiple external APIs
    
    Args:
        latitude: Listing latitude
        longitude: Listing longitude
        claimed_city: Claimed city name
        claimed_locality: Claimed locality name
        
    Returns:
        tuple: (fraud_score, explanation, details)
            - fraud_score (float): 0.0 to 1.0
            - explanation (str): Human-readable explanation
            - details (dict): Detailed verification results
    """
    # Validate coordinates
    if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
        return 0.9, "Invalid coordinates provided.", {}
    
    # Call multiple APIs
    api_results = []
    api_responses = {}
    
    # 1. Nominatim (always call - no key required)
    nominatim_response = call_nominatim_api(latitude, longitude)
    if nominatim_response:
        location_info = extract_location_info('nominatim', nominatim_response)
        api_results.append(location_info)
        api_responses['nominatim'] = location_info
    
    # 2. BigDataCloud (always call - no key required)
    bigdatacloud_response = call_bigdatacloud_api(latitude, longitude)
    if bigdatacloud_response:
        location_info = extract_location_info('bigdatacloud', bigdatacloud_response)
        api_results.append(location_info)
        api_responses['bigdatacloud'] = location_info
    
    # 3. LocationIQ (if API key available)
    if LOCATIONIQ_API_KEY:
        locationiq_response = call_locationiq_api(latitude, longitude)
        if locationiq_response:
            location_info = extract_location_info('locationiq', locationiq_response)
            api_results.append(location_info)
            api_responses['locationiq'] = location_info
    
    # 4. OpenCage (if API key available)
    if OPENCAGE_API_KEY:
        opencage_response = call_opencage_api(latitude, longitude)
        if opencage_response:
            location_info = extract_location_info('opencage', opencage_response)
            api_results.append(location_info)
            api_responses['opencage'] = location_info
    
    # Check if we got any results
    if not api_results:
        return 0.5, (
            "⚠️ Unable to verify location using external APIs. "
            "This could indicate network issues or invalid coordinates."
        ), {}
    
    # Calculate consensus match score
    match_score = calculate_location_match(claimed_city, claimed_locality, api_results)
    
    # Calculate fraud score (inverse of match score)
    fraud_score = 1.0 - match_score
    
    # Generate explanation
    num_apis = len(api_results)
    city_matches = sum(1 for r in api_results if normalize_string(claimed_city) in normalize_string(r.get('city', '')))
    locality_matches = sum(1 for r in api_results if any([
        normalize_string(claimed_locality) in normalize_string(r.get('locality', '')),
        normalize_string(claimed_locality) in normalize_string(r.get('suburb', '')),
        normalize_string(claimed_locality) in normalize_string(r.get('neighbourhood', ''))
    ]))
    
    if fraud_score < 0.3:
        explanation = (
            f"✅ VERIFIED: Location verified by {num_apis} external API(s). "
            f"{city_matches}/{num_apis} APIs confirmed the city '{claimed_city}', "
            f"and {locality_matches}/{num_apis} APIs confirmed the locality '{claimed_locality}'. "
            f"The coordinates appear accurate."
        )
    elif fraud_score < 0.6:
        explanation = (
            f"⚠️ MODERATE RISK: Partial verification from {num_apis} external API(s). "
            f"Only {city_matches}/{num_apis} APIs confirmed the city, "
            f"and {locality_matches}/{num_apis} APIs confirmed the locality. "
            f"The location may be inaccurate or misleading."
        )
    else:
        explanation = (
            f"🚨 HIGH RISK: Location could not be verified by external APIs. "
            f"Out of {num_apis} API(s), only {city_matches} confirmed the city "
            f"and {locality_matches} confirmed the locality. "
            f"This strongly suggests fraudulent or incorrect location information."
        )
    
    # Add API details
    if api_results:
        explanation += f"\n\nVerified locations from APIs:"
        for api_name, result in api_responses.items():
            city = result.get('city', 'Unknown')
            locality = result.get('locality') or result.get('suburb') or result.get('neighbourhood', 'Unknown')
            explanation += f"\n- {api_name.capitalize()}: {locality}, {city}"
    
    details = {
        'apis_called': num_apis,
        'city_matches': city_matches,
        'locality_matches': locality_matches,
        'match_score': match_score,
        'api_responses': api_responses
    }
    
    return fraud_score, explanation, details


def get_external_verification_status() -> Dict:
    """
    Get status of external verification service
    
    Returns:
        dict: Service status
    """
    return {
        'service': 'external_location_verification',
        'status': 'operational',
        'apis_available': {
            'nominatim': True,
            'bigdatacloud': True,
            'locationiq': bool(LOCATIONIQ_API_KEY),
            'opencage': bool(OPENCAGE_API_KEY),
            'geoapify': bool(GEOAPIFY_API_KEY)
        },
        'rate_limits': {
            'nominatim': '1 request/second',
            'bigdatacloud': 'unlimited',
            'locationiq': '10,000/day' if LOCATIONIQ_API_KEY else 'not configured',
            'opencage': '2,500/day' if OPENCAGE_API_KEY else 'not configured'
        }
    }
