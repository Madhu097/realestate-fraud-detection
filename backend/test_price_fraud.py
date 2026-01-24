"""
Test Price Fraud Detection
Tests the three required cases
"""
import requests
import json

BASE_URL = "http://localhost:8000"
ANALYZE_URL = f"{BASE_URL}/api/analyze"

# Test data based on dataset analysis
# Dataset shows Kharghar locality with prices around 4.5M - 6.7M

print("=" * 80)
print("TESTING PRICE FRAUD DETECTION")
print("=" * 80)

# TEST 1: Normal price (should get LOW score)
print("\n" + "=" * 80)
print("TEST 1: Normal Price")
print("=" * 80)

normal_listing = {
    "listing_data": {
        "title": "1 BHK Apartment in Kharghar",
        "description": "Nice apartment with modern amenities",
        "price": 5000000,  # 5M - normal for Kharghar
        "area_sqft": 650,
        "city": "Mumbai",
        "locality": "Kharghar",
        "latitude": 19.0330,
        "longitude": 73.0297
    }
}

try:
    response = requests.post(ANALYZE_URL, json=normal_listing)
    result = response.json()
    print(f"Status: {response.status_code}")
    print(f"Fraud Probability: {result['fraud_probability']:.2f}")
    print(f"Fraud Types: {result['fraud_types']}")
    print(f"Explanations: {result['explanations']}")
    
    if result['fraud_probability'] < 0.3:
        print("✅ PASS: Low fraud score for normal price")
    else:
        print("❌ FAIL: Expected low fraud score")
except Exception as e:
    print(f"❌ ERROR: {e}")

# TEST 2: Very low price (should get HIGH score)
print("\n" + "=" * 80)
print("TEST 2: Suspiciously Low Price")
print("=" * 80)

low_price_listing = {
    "listing_data": {
        "title": "1 BHK Apartment in Kharghar",
        "description": "Urgent sale! Very cheap!",
        "price": 1000000,  # 1M - way too low for Kharghar
        "area_sqft": 650,
        "city": "Mumbai",
        "locality": "Kharghar",
        "latitude": 19.0330,
        "longitude": 73.0297
    }
}

try:
    response = requests.post(ANALYZE_URL, json=low_price_listing)
    result = response.json()
    print(f"Status: {response.status_code}")
    print(f"Fraud Probability: {result['fraud_probability']:.2f}")
    print(f"Fraud Types: {result['fraud_types']}")
    print(f"Explanations: {result['explanations']}")
    
    if result['fraud_probability'] > 0.6:
        print("✅ PASS: High fraud score for suspiciously low price")
    else:
        print("❌ FAIL: Expected high fraud score")
except Exception as e:
    print(f"❌ ERROR: {e}")

# TEST 3: Unknown locality (should get explanation about insufficient data)
print("\n" + "=" * 80)
print("TEST 3: Unknown Locality")
print("=" * 80)

unknown_locality_listing = {
    "listing_data": {
        "title": "2 BHK Apartment in NonExistentPlace",
        "description": "Beautiful apartment",
        "price": 5000000,
        "area_sqft": 800,
        "city": "Mumbai",
        "locality": "NonExistentPlace12345",
        "latitude": 19.0330,
        "longitude": 73.0297
    }
}

try:
    response = requests.post(ANALYZE_URL, json=unknown_locality_listing)
    result = response.json()
    print(f"Status: {response.status_code}")
    print(f"Fraud Probability: {result['fraud_probability']:.2f}")
    print(f"Fraud Types: {result['fraud_types']}")
    print(f"Explanations: {result['explanations']}")
    
    if "Insufficient data" in str(result['explanations']):
        print("✅ PASS: Got explanation about insufficient data")
    else:
        print("❌ FAIL: Expected insufficient data message")
except Exception as e:
    print(f"❌ ERROR: {e}")

print("\n" + "=" * 80)
print("ALL TESTS COMPLETED")
print("=" * 80)
