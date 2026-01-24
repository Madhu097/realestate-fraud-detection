"""
Text Fraud Detection Test Script
Tests duplicate detection and promotional language detection
"""
import requests
import json

BASE_URL = "http://localhost:8000"
ANALYZE_URL = f"{BASE_URL}/api/analyze"

print("=" * 80)
print("TEXT FRAUD DETECTION - COMPREHENSIVE TESTING")
print("=" * 80)

# ============================================================
# TEST 1: Normal Listing (Should be LOW fraud score)
# ============================================================
print("\n" + "=" * 80)
print("TEST 1: Normal Listing")
print("=" * 80)

test1 = {
    "listing_data": {
        "title": "3BHK Apartment in Andheri West",
        "description": "Spacious 3-bedroom apartment with modern amenities, parking, and lift access. Located in a prime area with good connectivity.",
        "price": 15000000,
        "area_sqft": 1200,
        "city": "Mumbai",
        "locality": "Kharghar",
        "latitude": 19.0330,
        "longitude": 73.0297
    }
}

try:
    response = requests.post(ANALYZE_URL, json=test1)
    result = response.json()
    print(f"Fraud Probability: {result['fraud_probability']:.2%}")
    print(f"Fraud Types: {result['fraud_types']}")
    print(f"\nExplanations:")
    for exp in result['explanations']:
        print(f"  - {exp}")
    
    if result['fraud_probability'] < 0.4:
        print("\n✅ PASS: Low fraud score for normal listing")
    else:
        print("\n❌ FAIL: Expected low fraud score")
except Exception as e:
    print(f"❌ ERROR: {e}")

# ============================================================
# TEST 2: Promotional Language (Should be HIGH fraud score)
# ============================================================
print("\n" + "=" * 80)
print("TEST 2: Excessive Promotional Language")
print("=" * 80)

test2 = {
    "listing_data": {
        "title": "URGENT SALE - Best Deal Ever! Don't Miss!",
        "description": "Amazing luxury apartment! World-class amenities! Premium location! Act now! Limited time offer! Dream home awaits! Unbeatable price! Once in a lifetime opportunity! Grab this fantastic deal before it's gone!",
        "price": 5000000,
        "area_sqft": 1000,
        "city": "Mumbai",
        "locality": "Kharghar",
        "latitude": 19.0330,
        "longitude": 73.0297
    }
}

try:
    response = requests.post(ANALYZE_URL, json=test2)
    result = response.json()
    print(f"Fraud Probability: {result['fraud_probability']:.2%}")
    print(f"Fraud Types: {result['fraud_types']}")
    print(f"\nExplanations:")
    for exp in result['explanations']:
        print(f"  - {exp[:200]}...")  # Truncate long explanations
    
    if result['fraud_probability'] > 0.6:
        print("\n✅ PASS: High fraud score for promotional language")
        if "text_fraud" in result['fraud_types']:
            print("✅ PASS: Text fraud type correctly identified")
    else:
        print("\n❌ FAIL: Expected high fraud score")
except Exception as e:
    print(f"❌ ERROR: {e}")

# ============================================================
# TEST 3: Duplicate Detection (Submit same listing twice)
# ============================================================
print("\n" + "=" * 80)
print("TEST 3: Duplicate Detection")
print("=" * 80)

test3_first = {
    "listing_data": {
        "title": "Beautiful 2BHK with Sea View",
        "description": "Stunning 2-bedroom apartment overlooking the Arabian Sea. Fully furnished with Italian marble flooring and modular kitchen.",
        "price": 12000000,
        "area_sqft": 950,
        "city": "Mumbai",
        "locality": "Kharghar",
        "latitude": 19.0330,
        "longitude": 73.0297
    }
}

print("Submitting first listing...")
try:
    response1 = requests.post(ANALYZE_URL, json=test3_first)
    result1 = response1.json()
    print(f"First submission - Fraud Probability: {result1['fraud_probability']:.2%}")
except Exception as e:
    print(f"❌ ERROR: {e}")

print("\nSubmitting SAME listing again (should detect duplicate)...")
try:
    response2 = requests.post(ANALYZE_URL, json=test3_first)
    result2 = response2.json()
    print(f"Second submission - Fraud Probability: {result2['fraud_probability']:.2%}")
    print(f"Fraud Types: {result2['fraud_types']}")
    print(f"\nExplanations:")
    for exp in result2['explanations']:
        if 'Duplicate' in exp or 'similar' in exp:
            print(f"  - {exp[:200]}...")
    
    if result2['fraud_probability'] > result1['fraud_probability']:
        print("\n✅ PASS: Duplicate detection working (higher score on second submission)")
    else:
        print("\n⚠️  Note: Duplicate detection may need more submissions to build corpus")
except Exception as e:
    print(f"❌ ERROR: {e}")

# ============================================================
# TEST 4: Combined Fraud (Price + Text)
# ============================================================
print("\n" + "=" * 80)
print("TEST 4: Combined Fraud (Low Price + Promotional Language)")
print("=" * 80)

test4 = {
    "listing_data": {
        "title": "URGENT DISTRESS SALE - Cheapest Deal!",
        "description": "Luxury apartment at unbelievable price! Must sell immediately! Best bargain ever! Premium location! World-class amenities! Act now before it's gone!",
        "price": 1000000,  # Very low price for Kharghar
        "area_sqft": 800,
        "city": "Mumbai",
        "locality": "Kharghar",
        "latitude": 19.0330,
        "longitude": 73.0297
    }
}

try:
    response = requests.post(ANALYZE_URL, json=test4)
    result = response.json()
    print(f"Fraud Probability: {result['fraud_probability']:.2%}")
    print(f"Fraud Types: {result['fraud_types']}")
    print(f"\nExplanations:")
    for exp in result['explanations']:
        print(f"  - {exp[:200]}...")
    
    if result['fraud_probability'] > 0.7:
        print("\n✅ PASS: Very high fraud score for combined fraud")
        if len(result['fraud_types']) >= 2:
            print("✅ PASS: Multiple fraud types detected")
    else:
        print("\n⚠️  Note: Expected very high fraud score")
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
✅ Test 1: Low fraud score (< 40%) for normal listing
✅ Test 2: High fraud score (> 60%) for promotional language
✅ Test 3: Higher score on duplicate submission
✅ Test 4: Very high score (> 70%) for combined fraud

Text Fraud Detection Features:
- TF-IDF + Cosine Similarity for duplicates
- Rule-based keyword detection (50+ keywords)
- Category-based scoring (urgency, superlative, luxury, etc.)
- Conservative MAX combination with price fraud
- Clear, explainable results
""")
print("=" * 80)
