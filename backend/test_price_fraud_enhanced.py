"""
Enhanced Price Fraud Testing - All Edge Cases
Tests all required scenarios for examiner demonstration
"""
import requests
import json

BASE_URL = "http://localhost:8000"
ANALYZE_URL = f"{BASE_URL}/api/analyze"

def print_test_result(test_name, result):
    """Pretty print test results"""
    print(f"\n{'='*80}")
    print(f"TEST: {test_name}")
    print(f"{'='*80}")
    print(f"Status Code: {result.get('status_code', 'N/A')}")
    print(f"Fraud Probability: {result.get('fraud_probability', 0):.2%}")
    print(f"Fraud Types: {result.get('fraud_types', [])}")
    print(f"\nExplanation:")
    for exp in result.get('explanations', []):
        print(f"  {exp}")
    print(f"{'='*80}")

# Test data based on Kharghar locality (mean ~5.2M, range 4.5M-6.7M)

print("\n" + "🧪 PRICE FRAUD DETECTION - COMPREHENSIVE TESTING" + "\n")

# ============================================================
# TEST 1: Normal Price (LOW fraud score expected)
# ============================================================
test1 = {
    "listing_data": {
        "title": "1 BHK Apartment in Kharghar",
        "description": "Well-maintained apartment with modern amenities",
        "price": 5000000,  # Normal price for Kharghar
        "area_sqft": 650,
        "city": "Mumbai",
        "locality": "Kharghar",
        "latitude": 19.0330,
        "longitude": 73.0297
    }
}

try:
    response = requests.post(ANALYZE_URL, json=test1)
    result = response.json()
    result['status_code'] = response.status_code
    print_test_result("Normal Price (Should be LOW fraud score)", result)
    
    if result['fraud_probability'] < 0.3:
        print("✅ PASS: Low fraud score for normal price")
    else:
        print("❌ FAIL: Expected low fraud score")
except Exception as e:
    print(f"❌ ERROR: {e}")

# ============================================================
# TEST 2: Very Low Price (HIGH fraud score expected)
# ============================================================
test2 = {
    "listing_data": {
        "title": "URGENT SALE - 1 BHK Apartment",
        "description": "Must sell immediately! Price negotiable!",
        "price": 1000000,  # 80% below average - very suspicious
        "area_sqft": 650,
        "city": "Mumbai",
        "locality": "Kharghar",
        "latitude": 19.0330,
        "longitude": 73.0297
    }
}

try:
    response = requests.post(ANALYZE_URL, json=test2)
    result = response.json()
    result['status_code'] = response.status_code
    print_test_result("Very Low Price (Should be HIGH fraud score)", result)
    
    if result['fraud_probability'] > 0.6:
        print("✅ PASS: High fraud score for suspiciously low price")
        if "price_manipulation" in result['fraud_types']:
            print("✅ PASS: Fraud type correctly identified")
    else:
        print("❌ FAIL: Expected high fraud score")
except Exception as e:
    print(f"❌ ERROR: {e}")

# ============================================================
# TEST 3: Very High Price (MEDIUM fraud score expected)
# ============================================================
test3 = {
    "listing_data": {
        "title": "Luxury 1 BHK Apartment",
        "description": "Premium property with exclusive amenities",
        "price": 15000000,  # 3x average - suspicious but not extreme
        "area_sqft": 650,
        "city": "Mumbai",
        "locality": "Kharghar",
        "latitude": 19.0330,
        "longitude": 73.0297
    }
}

try:
    response = requests.post(ANALYZE_URL, json=test3)
    result = response.json()
    result['status_code'] = response.status_code
    print_test_result("Very High Price (Should be MEDIUM fraud score)", result)
    
    if 0.3 < result['fraud_probability'] < 0.9:
        print("✅ PASS: Medium fraud score for high price")
    else:
        print("⚠️  WARNING: Expected medium fraud score")
except Exception as e:
    print(f"❌ ERROR: {e}")

# ============================================================
# TEST 4: Unknown Locality (LOW score + limitation explanation)
# ============================================================
test4 = {
    "listing_data": {
        "title": "2 BHK Apartment",
        "description": "Beautiful property in new area",
        "price": 5000000,
        "area_sqft": 800,
        "city": "Mumbai",
        "locality": "NonExistentPlace12345XYZ",
        "latitude": 19.0330,
        "longitude": 73.0297
    }
}

try:
    response = requests.post(ANALYZE_URL, json=test4)
    result = response.json()
    result['status_code'] = response.status_code
    print_test_result("Unknown Locality (Should show limitation)", result)
    
    if result['fraud_probability'] == 0.0:
        print("✅ PASS: Low fraud score for unknown locality")
    
    if "Insufficient comparable listings" in str(result['explanations']):
        print("✅ PASS: Correct limitation explanation")
    else:
        print("❌ FAIL: Expected insufficient data message")
except Exception as e:
    print(f"❌ ERROR: {e}")

# ============================================================
# TEST 5: Extreme Low Price (Should trigger IQR detection)
# ============================================================
test5 = {
    "listing_data": {
        "title": "DISTRESS SALE - 1 BHK",
        "description": "Immediate sale required!",
        "price": 500000,  # Extremely low - 90% below average
        "area_sqft": 650,
        "city": "Mumbai",
        "locality": "Kharghar",
        "latitude": 19.0330,
        "longitude": 73.0297
    }
}

try:
    response = requests.post(ANALYZE_URL, json=test5)
    result = response.json()
    result['status_code'] = response.status_code
    print_test_result("Extreme Low Price (Should trigger IQR bounds)", result)
    
    if result['fraud_probability'] > 0.8:
        print("✅ PASS: Very high fraud score for extreme price")
    
    if "normal range" in str(result['explanations']).lower():
        print("✅ PASS: IQR bounds mentioned in explanation")
except Exception as e:
    print(f"❌ ERROR: {e}")

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "="*80)
print("📊 TEST SUMMARY")
print("="*80)
print("""
Expected Results:
✅ Test 1 (Normal): Low fraud score (< 30%)
✅ Test 2 (Very Low): High fraud score (> 60%) + fraud type
✅ Test 3 (Very High): Medium fraud score (30-90%)
✅ Test 4 (Unknown): Low score (0%) + limitation message
✅ Test 5 (Extreme): Very high score (> 80%) + IQR bounds

All tests demonstrate:
- Z-Score + IQR combination
- Proper edge case handling
- Examiner-approved explanations
- Statistical robustness
""")
print("="*80)
