"""
Amenity Verification Service
Verifies claims about nearby amenities using OpenStreetMap Overpass API
"""
import requests
from typing import Tuple, Dict, List, Optional
from geopy.distance import geodesic
import time

# Overpass API Configuration
OVERPASS_API_URL = "https://overpass-api.de/api/interpreter"
OVERPASS_TIMEOUT = 10  # seconds

# Distance thresholds for "nearby" claims (in kilometers)
NEARBY_THRESHOLD_KM = 2.0  # Within 2km is considered "nearby"
VERY_CLOSE_THRESHOLD_KM = 0.5  # Within 500m is "very close"

# Common amenity keywords in property descriptions
AMENITY_KEYWORDS = {
    'metro': ['metro', 'subway', 'metro station', 'railway station'],
    'school': ['school', 'college', 'university', 'educational institution'],
    'hospital': ['hospital', 'clinic', 'medical center', 'health center'],
    'mall': ['mall', 'shopping center', 'shopping complex'],
    'park': ['park', 'garden', 'green space'],
    'airport': ['airport', 'international airport'],
    'it_park': ['it park', 'tech park', 'software park', 'it hub', 'hitech city'],
    'restaurant': ['restaurant', 'food court', 'dining'],
    'bank': ['bank', 'atm'],
    'gym': ['gym', 'fitness center', 'sports complex']
}

# Overpass query templates
OVERPASS_QUERIES = {
    'metro': """
    [out:json][timeout:10];
    (
      node["railway"="station"](around:{radius},{lat},{lon});
      node["railway"="subway_entrance"](around:{radius},{lat},{lon});
      node["public_transport"="station"](around:{radius},{lat},{lon});
    );
    out body;
    """,
    'school': """
    [out:json][timeout:10];
    (
      node["amenity"="school"](around:{radius},{lat},{lon});
      node["amenity"="college"](around:{radius},{lat},{lon});
      node["amenity"="university"](around:{radius},{lat},{lon});
    );
    out body;
    """,
    'hospital': """
    [out:json][timeout:10];
    (
      node["amenity"="hospital"](around:{radius},{lat},{lon});
      node["amenity"="clinic"](around:{radius},{lat},{lon});
      node["healthcare"="hospital"](around:{radius},{lat},{lon});
    );
    out body;
    """,
    'mall': """
    [out:json][timeout:10];
    (
      node["shop"="mall"](around:{radius},{lat},{lon});
      way["shop"="mall"](around:{radius},{lat},{lon});
      node["amenity"="marketplace"](around:{radius},{lat},{lon});
    );
    out body;
    """,
    'park': """
    [out:json][timeout:10];
    (
      node["leisure"="park"](around:{radius},{lat},{lon});
      way["leisure"="park"](around:{radius},{lat},{lon});
      node["leisure"="garden"](around:{radius},{lat},{lon});
    );
    out body;
    """,
    'airport': """
    [out:json][timeout:10];
    (
      node["aeroway"="aerodrome"](around:{radius},{lat},{lon});
      way["aeroway"="aerodrome"](around:{radius},{lat},{lon});
    );
    out body;
    """,
    'restaurant': """
    [out:json][timeout:10];
    (
      node["amenity"="restaurant"](around:{radius},{lat},{lon});
      node["amenity"="fast_food"](around:{radius},{lat},{lon});
      node["amenity"="cafe"](around:{radius},{lat},{lon});
    );
    out body;
    """,
    'bank': """
    [out:json][timeout:10];
    (
      node["amenity"="bank"](around:{radius},{lat},{lon});
      node["amenity"="atm"](around:{radius},{lat},{lon});
    );
    out body;
    """,
    'gym': """
    [out:json][timeout:10];
    (
      node["leisure"="fitness_centre"](around:{radius},{lat},{lon});
      node["leisure"="sports_centre"](around:{radius},{lat},{lon});
    );
    out body;
    """
}


def query_overpass_api(query: str) -> Optional[Dict]:
    """
    Query Overpass API
    
    Args:
        query: Overpass QL query string
        
    Returns:
        dict: API response or None if failed
    """
    try:
        response = requests.post(
            OVERPASS_API_URL,
            data={'data': query},
            timeout=OVERPASS_TIMEOUT
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Overpass API error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"Overpass API exception: {e}")
        return None


def find_nearby_amenities(
    latitude: float,
    longitude: float,
    amenity_type: str,
    radius_km: float = NEARBY_THRESHOLD_KM
) -> List[Dict]:
    """
    Find nearby amenities of a specific type
    
    Args:
        latitude: Property latitude
        longitude: Property longitude
        amenity_type: Type of amenity to search for
        radius_km: Search radius in kilometers
        
    Returns:
        list: List of nearby amenities with details
    """
    if amenity_type not in OVERPASS_QUERIES:
        return []
    
    # Convert radius to meters for Overpass API
    radius_meters = int(radius_km * 1000)
    
    # Format query
    query = OVERPASS_QUERIES[amenity_type].format(
        radius=radius_meters,
        lat=latitude,
        lon=longitude
    )
    
    # Query API
    response = query_overpass_api(query)
    
    if not response or 'elements' not in response:
        return []
    
    # Extract amenities with distance calculation
    amenities = []
    property_location = (latitude, longitude)
    
    for element in response['elements']:
        if 'lat' in element and 'lon' in element:
            amenity_location = (element['lat'], element['lon'])
            distance_km = geodesic(property_location, amenity_location).kilometers
            
            amenity_info = {
                'name': element.get('tags', {}).get('name', 'Unnamed'),
                'type': amenity_type,
                'latitude': element['lat'],
                'longitude': element['lon'],
                'distance_km': round(distance_km, 2),
                'tags': element.get('tags', {})
            }
            amenities.append(amenity_info)
    
    # Sort by distance
    amenities.sort(key=lambda x: x['distance_km'])
    
    return amenities


def detect_amenity_keywords(text: str) -> List[str]:
    """
    Detect amenity-related keywords in text
    
    Args:
        text: Property description or title
        
    Returns:
        list: List of detected amenity types
    """
    text_lower = text.lower()
    detected = []
    
    for amenity_type, keywords in AMENITY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                detected.append(amenity_type)
                break  # Only add once per type
    
    return detected


def verify_amenity_claims(
    title: str,
    description: str,
    latitude: float,
    longitude: float
) -> Tuple[float, str, Dict]:
    """
    Verify amenity claims in property listing
    
    Args:
        title: Property title
        description: Property description
        latitude: Property latitude
        longitude: Property longitude
        
    Returns:
        tuple: (fraud_score, explanation, details)
            - fraud_score (float): 0.0 to 1.0
            - explanation (str): Human-readable explanation
            - details (dict): Detailed verification results
    """
    # Combine title and description
    full_text = f"{title} {description}"
    
    # Detect claimed amenities
    claimed_amenities = detect_amenity_keywords(full_text)
    
    if not claimed_amenities:
        # No amenity claims to verify
        return 0.0, "No specific amenity claims detected in the listing.", {}
    
    # Verify each claimed amenity
    verification_results = {}
    total_claims = len(claimed_amenities)
    verified_claims = 0
    false_claims = 0
    
    for amenity_type in claimed_amenities:
        # Find nearby amenities
        nearby = find_nearby_amenities(latitude, longitude, amenity_type, NEARBY_THRESHOLD_KM)
        
        if nearby:
            # Claim verified
            nearest = nearby[0]
            verification_results[amenity_type] = {
                'verified': True,
                'nearest_name': nearest['name'],
                'nearest_distance_km': nearest['distance_km'],
                'total_found': len(nearby),
                'is_very_close': nearest['distance_km'] <= VERY_CLOSE_THRESHOLD_KM
            }
            verified_claims += 1
        else:
            # Claim not verified
            verification_results[amenity_type] = {
                'verified': False,
                'nearest_name': None,
                'nearest_distance_km': None,
                'total_found': 0,
                'is_very_close': False
            }
            false_claims += 1
    
    # Calculate fraud score
    if total_claims == 0:
        fraud_score = 0.0
    else:
        # Higher fraud score if more claims are false
        fraud_score = false_claims / total_claims
        
        # Boost fraud score if ALL claims are false
        if false_claims == total_claims:
            fraud_score = min(fraud_score + 0.2, 1.0)
    
    # Generate explanation
    if fraud_score < 0.3:
        explanation = (
            f"✅ AMENITY CLAIMS VERIFIED: The listing mentions {total_claims} amenity/amenities, "
            f"and {verified_claims} were verified using real-world data."
        )
    elif fraud_score < 0.6:
        explanation = (
            f"⚠️ PARTIAL VERIFICATION: The listing mentions {total_claims} amenity/amenities, "
            f"but only {verified_claims} could be verified. {false_claims} claim(s) could not be confirmed."
        )
    else:
        explanation = (
            f"🚨 FALSE CLAIMS DETECTED: The listing mentions {total_claims} amenity/amenities, "
            f"but {false_claims} claim(s) could not be verified. This suggests misleading information."
        )
    
    # Add detailed results
    explanation += "\n\nDetailed verification:"
    for amenity_type, result in verification_results.items():
        if result['verified']:
            explanation += (
                f"\n✅ {amenity_type.replace('_', ' ').title()}: "
                f"Verified - Nearest is '{result['nearest_name']}' "
                f"at {result['nearest_distance_km']} km "
                f"({result['total_found']} found within 2 km)"
            )
        else:
            explanation += (
                f"\n❌ {amenity_type.replace('_', ' ').title()}: "
                f"NOT VERIFIED - No {amenity_type.replace('_', ' ')} found within 2 km radius"
            )
    
    details = {
        'total_claims': total_claims,
        'verified_claims': verified_claims,
        'false_claims': false_claims,
        'verification_results': verification_results
    }
    
    return fraud_score, explanation, details


def get_nearby_amenities_summary(
    latitude: float,
    longitude: float,
    radius_km: float = 1.0
) -> Dict:
    """
    Get summary of all nearby amenities (for general information)
    
    Args:
        latitude: Property latitude
        longitude: Property longitude
        radius_km: Search radius in kilometers
        
    Returns:
        dict: Summary of nearby amenities
    """
    summary = {}
    
    for amenity_type in ['metro', 'school', 'hospital', 'mall', 'park']:
        nearby = find_nearby_amenities(latitude, longitude, amenity_type, radius_km)
        summary[amenity_type] = {
            'count': len(nearby),
            'nearest': nearby[0] if nearby else None
        }
    
    return summary


def get_amenity_verification_status() -> Dict:
    """
    Get status of amenity verification service
    
    Returns:
        dict: Service status
    """
    return {
        'service': 'amenity_verification',
        'status': 'operational',
        'api': 'Overpass API (OpenStreetMap)',
        'supported_amenities': list(AMENITY_KEYWORDS.keys()),
        'nearby_threshold_km': NEARBY_THRESHOLD_KM,
        'rate_limits': 'Fair use policy'
    }
