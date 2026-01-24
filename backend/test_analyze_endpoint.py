"""
Test script for the /api/analyze endpoint
Tests the dummy fraud detection logic
"""
import requests
import json

# API endpoint
BASE_URL = "http://localhost:8000"
ANALYZE_ENDPOINT = f"{BASE_URL}/api/analyze"

# Test data using the frozen schema
test_listing = {
    "listing_data": {
        "title": "Spacious 3BHK Apartment in Prime Location",
        "description": "Beautiful 3BHK apartment with modern amenities, parking, and great view",
        "price": 5000000,
        "area_sqft": 1500,
        "city": "Mumbai",
        "locality": "Andheri West",
        "latitude": 19.1334,
        "longitude": 72.8291
    }
}

def test_analyze_endpoint():
    """Test the /api/analyze endpoint with valid data"""
    print("=" * 60)
    print("Testing /api/analyze endpoint")
    print("=" * 60)
    
    try:
        print("\n📤 Sending request to:", ANALYZE_ENDPOINT)
        print("\n📋 Request payload:")
        print(json.dumps(test_listing, indent=2))
        
        response = requests.post(ANALYZE_ENDPOINT, json=test_listing)
        
        print(f"\n📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS!")
            print("\n📥 Response data:")
            result = response.json()
            print(json.dumps(result, indent=2))
            
            # Validate response structure
            print("\n🔍 Validating response structure...")
            assert "fraud_probability" in result, "Missing fraud_probability"
            assert "fraud_types" in result, "Missing fraud_types"
            assert "explanations" in result, "Missing explanations"
            
            assert isinstance(result["fraud_probability"], (int, float)), "fraud_probability must be a number"
            assert isinstance(result["fraud_types"], list), "fraud_types must be a list"
            assert isinstance(result["explanations"], list), "explanations must be a list"
            
            assert 0.0 <= result["fraud_probability"] <= 1.0, "fraud_probability must be between 0 and 1"
            
            print("✅ Response structure is valid!")
            
            # Check dummy values
            print("\n🎭 Checking dummy values...")
            assert result["fraud_probability"] == 0.0, "Expected fraud_probability to be 0.0"
            assert result["fraud_types"] == [], "Expected fraud_types to be empty"
            assert result["explanations"] == [], "Expected explanations to be empty"
            print("✅ Dummy values are correct!")
            
        else:
            print(f"❌ FAILED with status {response.status_code}")
            print("Response:", response.text)
            
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: Could not connect to backend")
        print("Make sure the backend server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")


def test_missing_data():
    """Test the endpoint with missing listing_data"""
    print("\n" + "=" * 60)
    print("Testing /api/analyze with missing data")
    print("=" * 60)
    
    try:
        print("\n📤 Sending request with empty payload...")
        response = requests.post(ANALYZE_ENDPOINT, json={})
        
        print(f"\n📊 Response Status: {response.status_code}")
        
        if response.status_code == 400:
            print("✅ Correctly rejected invalid request!")
            print("Response:", response.json())
        else:
            print(f"⚠️ Expected 400, got {response.status_code}")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")


if __name__ == "__main__":
    print("\n🚀 Starting API Tests\n")
    test_analyze_endpoint()
    test_missing_data()
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
