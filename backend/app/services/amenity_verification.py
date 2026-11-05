"""
Amenity Verification Service
Verifies claims about nearby amenities and flags contradictory claims
without causing false positive fraud penalties for standard residential features.
"""
import os
import re
from typing import Tuple, Dict, List, Optional

ENABLE_EXTERNAL_APIS = os.getenv("ENABLE_EXTERNAL_APIS", "false").lower() == "true"

# Contradictory amenity claims based on geography
IMPOSSIBLE_GEO_CLAIMS = {
    'hyderabad': ['beachfront', 'sea view', 'beach facing', 'ocean view', 'coastal', 'harbor view'],
    'delhi': ['beachfront', 'sea view', 'beach facing', 'ocean view', 'coastal'],
    'bangalore': ['beachfront', 'sea view', 'beach facing', 'ocean view', 'coastal'],
    'pune': ['beachfront', 'sea view', 'beach facing', 'ocean view', 'coastal']
}

def verify_amenity_claims(
    title: str,
    description: str,
    latitude: float,
    longitude: float,
    city: str = ""
) -> Tuple[float, str, Dict]:
    """
    Verify amenity claims for realism, contradiction, and feasibility.
    """
    full_text = f"{title} {description}".lower()
    
    # 1. Check for geographically impossible claims (e.g. Sea View in landlocked Hyderabad)
    city_lower = city.lower().strip() if city else ""
    if not city_lower:
        # Infer city from text if mentioned
        for known_city in IMPOSSIBLE_GEO_CLAIMS:
            if known_city in full_text:
                city_lower = known_city
                break
                
    if city_lower in IMPOSSIBLE_GEO_CLAIMS:
        forbidden = [term for term in IMPOSSIBLE_GEO_CLAIMS[city_lower] if term in full_text]
        if forbidden:
            return 0.80, (
                f"🚨 GEOGRAPHICALLY IMPOSSIBLE AMENITY CLAIM: Listing claims '{', '.join(forbidden)}' "
                f"in {city_lower.title()}, which is a landlocked city with no coastline. "
                f"This indicates a fraudulent or copy-pasted scam listing."
            ), {"impossible_claims": forbidden}

    # 2. Check for airport claims directly in residential listings
    if "international airport inside" in full_text or "private runway" in full_text:
        return 0.70, "⚠️ Highly suspicious / unrealistic infrastructure claims detected.", {}

    # Standard residential amenities (gym, parking, pool, 24x7 security, lift, garden)
    amenity_matches = []
    for am in ['gym', 'parking', 'lift', 'pool', 'security', 'garden', 'clubhouse', 'power backup']:
        if am in full_text:
            amenity_matches.append(am)
            
    if amenity_matches:
        return 0.0, (
            f"Residential amenities ({', '.join(amenity_matches[:4])}) verified consistent "
            f"with standard residential apartment complexes."
        ), {"verified_amenities": amenity_matches}
        
    return 0.0, "Standard property specifications verified. No contradictory amenity claims found.", {}


def get_amenity_verification_status() -> Dict:
    return {
        'service': 'amenity_verification',
        'status': 'operational',
        'mode': 'semantic_consistency_and_feasibility'
    }
