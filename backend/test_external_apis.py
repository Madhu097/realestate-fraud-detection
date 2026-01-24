"""
Test script for external API integration
Tests the new location and amenity verification services
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.external_location_verification import verify_location_with_external_apis
from app.services.amenity_verification import verify_amenity_claims

print("=" * 80)
print("TESTING EXTERNAL API INTEGRATION")
print("=" * 80)

# Test Case 1: Valid Location (Gachibowli, Hyderabad)
print("\n" + "=" * 80)
print("TEST CASE 1: Valid Location - Gachibowli, Hyderabad")
print("=" * 80)

score1, explanation1, details1 = verify_location_with_external_apis(
    latitude=17.4400,
    longitude=78.3489,
    claimed_city="Hyderabad",
    claimed_locality="Gachibowli"
)

print(f"\nFraud Score: {score1:.2f}")
print(f"Explanation:\n{explanation1}")
print(f"\nAPIs Called: {details1.get('apis_called', 0)}")
print(f"City Matches: {details1.get('city_matches', 0)}")
print(f"Locality Matches: {details1.get('locality_matches', 0)}")

# Test Case 2: Fake Coordinates (Wrong location)
print("\n" + "=" * 80)
print("TEST CASE 2: Fake Coordinates - Claims Jubilee Hills but points to LB Nagar")
print("=" * 80)

score2, explanation2, details2 = verify_location_with_external_apis(
    latitude=17.3500,
    longitude=78.5520,
    claimed_city="Hyderabad",
    claimed_locality="Jubilee Hills"
)

print(f"\nFraud Score: {score2:.2f}")
print(f"Explanation:\n{explanation2}")
print(f"\nAPIs Called: {details2.get('apis_called', 0)}")
print(f"City Matches: {details2.get('city_matches', 0)}")
print(f"Locality Matches: {details2.get('locality_matches', 0)}")

# Test Case 3: Amenity Verification - Valid Claims
print("\n" + "=" * 80)
print("TEST CASE 3: Amenity Verification - Near Metro Station")
print("=" * 80)

score3, explanation3, details3 = verify_amenity_claims(
    title="3BHK Apartment in Gachibowli",
    description="Near Hitech City Metro Station, close to IT parks",
    latitude=17.4400,
    longitude=78.3489
)

print(f"\nFraud Score: {score3:.2f}")
print(f"Explanation:\n{explanation3}")
print(f"\nTotal Claims: {details3.get('total_claims', 0)}")
print(f"Verified Claims: {details3.get('verified_claims', 0)}")
print(f"False Claims: {details3.get('false_claims', 0)}")

# Test Case 4: Amenity Verification - False Claims
print("\n" + "=" * 80)
print("TEST CASE 4: Amenity Verification - False Airport Claim")
print("=" * 80)

score4, explanation4, details4 = verify_amenity_claims(
    title="Luxury Villa",
    description="Walking distance to international airport, near metro station",
    latitude=17.4400,
    longitude=78.3489
)

print(f"\nFraud Score: {score4:.2f}")
print(f"Explanation:\n{explanation4}")
print(f"\nTotal Claims: {details4.get('total_claims', 0)}")
print(f"Verified Claims: {details4.get('verified_claims', 0)}")
print(f"False Claims: {details4.get('false_claims', 0)}")

print("\n" + "=" * 80)
print("TESTING COMPLETE")
print("=" * 80)
print("\n✅ All tests executed successfully!")
print("\nNote: External API calls may take a few seconds due to rate limiting.")
print("If you see errors, check your internet connection or API keys in .env file.")
