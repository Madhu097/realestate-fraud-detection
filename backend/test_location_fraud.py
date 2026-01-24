"""
Location Fraud Detection Test Script
Tests geospatial fraud detection using Haversine distance
"""
import requests
import json

BASE_URL = "http://localhost:8000"
ANALYZE_URL = f"{BASE_URL}/api/analyze"

print("=" * 80)
print("LOCATION FRAUD DETECTION - COMPREHENSIVE TESTING")
print("=" * 80)

# ============================================================
# TEST 1: Accurate Location (Should be LOW fraud score)
# ============================================================
print("\n" + "=" * 80)
print("TEST 1: Accurate Location (Kharghar)")
print("=" * 80)

test1 = {
    "listing_data": {
        "title": "2BHK Apartment in Kharghar",
        "description": "Well-maintained apartment with good amenities",
        "price": 5000000,
        "area_sqft": 800,
        "city": "Mumbai",
        "locality": "Kharghar",
        "latitude": 19.0330,  # Exact center coordinates
        "longitude": 73.0297
    }
}

try:
    response = requests.post(ANALYZE_URL, json=test1)
    result = response.json()
    print(f"Fraud Probability: {result['fraud_probability']:.2%}")
    print(f"Fraud Types: {result['fraud_types']}")
    print(f"\nLocation Explanation:")
    for exp in result['explanations']:
        if '[Location]' in exp:
            print(f"  {exp}")
    
    if result['fraud_probability'] < 0.4:
        print("\n✅ PASS: Low fraud score for accurate location")
    else:
        print("\n⚠️  Note: Expected low fraud score")
except Exception as e:
    print(f"❌ ERROR: {e}")

# ============================================================
# TEST 2: Suspicious Distance (1.5-3 km away)
# ============================================================
print("\n" + "=" * 80)
print("TEST 2: Suspicious Distance (~2 km from Kharghar center)")
print("=" * 80)

test2 = {
    "listing_data": {
        "title": "3BHK Apartment in Kharghar",
        "description": "Spacious apartment",
        "price": 5200000,
        "area_sqft": 1000,
        "city": "Mumbai",
        "locality": "Kharghar",
        "latitude": 19.0500,  # ~2 km away from center
        "longitude": 73.0100
    }
}

try:
    response = requests.post(ANALYZE_URL, json=test2)
    result = response.json()
    print(f"Fraud Probability: {result['fraud_probability']:.2%}")
    print(f"Fraud Types: {result['fraud_types']}")
    print(f"\nLocation Explanation:")
    for exp in result['explanations']:
        if '[Location]' in exp:
            print(f"  {exp[:300]}...")
    
    if 0.3 < result['fraud_probability'] < 0.7:
        print("\n✅ PASS: Moderate fraud score for suspicious distance")
except Exception as e:
    print(f"❌ ERROR: {e}")

# ============================================================
# TEST 3: High Risk Distance (> 3 km away)
# ============================================================
print("\n" + "=" * 80)
print("TEST 3: High Risk Distance (~5 km from Kharghar center)")
print("=" * 80)

test3 = {
    "listing_data": {
        "title": "Luxury Apartment in Kharghar",
        "description": "Premium property",
        "price": 5000000,
        "area_sqft": 900,
        "city": "Mumbai",
        "locality": "Kharghar",
        "latitude": 19.0700,  # ~5 km away from center
        "longitude": 73.0700
    }
}

try:
    response = requests.post(ANALYZE_URL, json=test3)
    result = response.json()
    print(f"Fraud Probability: {result['fraud_probability']:.2%}")
    print(f"Fraud Types: {result['fraud_types']}")
    print(f"\nLocation Explanation:")
    for exp in result['explanations']:
        if '[Location]' in exp:
            print(f"  {exp[:300]}...")
    
    if result['fraud_probability'] > 0.6:
        print("\n✅ PASS: High fraud score for large distance")
        if "location_fraud" in result['fraud_types']:
            print("✅ PASS: Location fraud type correctly identified")
except Exception as e:
    print(f"❌ ERROR: {e}")

# ============================================================
# TEST 4: Combined Fraud (Distance + Price Anomaly)
# ============================================================
print("\n" + "=" * 80)
print("TEST 4: Combined Fraud (Wrong location + Wrong price)")
print("=" * 80)

test4 = {
    "listing_data": {
        "title": "Apartment in Kharghar",
        "description": "Good property",
        "price": 10000000,  # Way above average for Kharghar (avg: 5.2M)
        "area_sqft": 800,
        "city": "Mumbai",
        "locality": "Kharghar",
        "latitude": 19.0800,  # ~6 km away
        "longitude": 73.0800
    }
}

try:
    response = requests.post(ANALYZE_URL, json=test4)
    result = response.json()
    print(f"Fraud Probability: {result['fraud_probability']:.2%}")
    print(f"Fraud Types: {result['fraud_types']}")
    print(f"\nLocation Explanation:")
    for exp in result['explanations']:
        if '[Location]' in exp:
            print(f"  {exp[:400]}...")
    
    if result['fraud_probability'] > 0.7:
        print("\n✅ PASS: Very high fraud score for combined fraud")
except Exception as e:
    print(f"❌ ERROR: {e}")

# ============================================================
# TEST 5: Unknown Locality (Edge Case)
# ============================================================
print("\n" + "=" * 80)
print("TEST 5: Unknown Locality (Edge Case)")
print("=" * 80)

test5 = {
    "listing_data": {
        "title": "Apartment in Unknown Area",
        "description": "Nice property",
        "price": 5000000,
        "area_sqft": 800,
        "city": "Mumbai",
        "locality": "UnknownLocality12345",
        "latitude": 19.0330,
        "longitude": 73.0297
    }
}

try:
    response = requests.post(ANALYZE_URL, json=test5)
    result = response.json()
    print(f"Fraud Probability: {result['fraud_probability']:.2%}")
    print(f"Fraud Types: {result['fraud_types']}")
    print(f"\nLocation Explanation:")
    for exp in result['explanations']:
        if '[Location]' in exp:
            print(f"  {exp}")
    
    if "not in our reference database" in str(result['explanations']):
        print("\n✅ PASS: Correct handling of unknown locality")
except Exception as e:
    print(f"❌ ERROR: {e}")

# ============================================================
# TEST 6: Invalid Coordinates (Edge Case)
# ============================================================
print("\n" + "=" * 80)
print("TEST 6: Invalid Coordinates (Edge Case)")
print("=" * 80)

test6 = {
    "listing_data": {
        "title": "Apartment in Kharghar",
        "description": "Good property",
        "price": 5000000,
        "area_sqft": 800,
        "city": "Mumbai",
        "locality": "Kharghar",
        "latitude": 95.0,  # Invalid (> 90)
        "longitude": 200.0  # Invalid (> 180)
    }
}

try:
    response = requests.post(ANALYZE_URL, json=test6)
    result = response.json()
    print(f"Fraud Probability: {result['fraud_probability']:.2%}")
    print(f"Fraud Types: {result['fraud_types']}")
    print(f"\nLocation Explanation:")
    for exp in result['explanations']:
        if '[Location]' in exp:
            print(f"  {exp}")
    
    if result['fraud_probability'] > 0.7:
        print("\n✅ PASS: High fraud score for invalid coordinates")
except Exception as e:
    print(f"❌ ERROR: {e}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)
print("""
Expected Results:
✅ Test 1: Low fraud score (< 40%) for accurate location
✅ Test 2: Moderate fraud score (30-70%) for suspicious distance
✅ Test 3: High fraud score (> 60%) for large distance
✅ Test 4: Very high score (> 70%) for combined fraud
✅ Test 5: Proper handling of unknown locality
✅ Test 6: High score for invalid coordinates

Location Fraud Detection Features:
- Haversine distance formula for geo-calculations
- Distance thresholds: 1.5 km (suspicious), 3 km (high risk)
- Price-location sanity check
- Reference database of 15 Mumbai localities
- Comprehensive edge case handling
- Clear, non-technical explanations
""")
print("=" * 80)
