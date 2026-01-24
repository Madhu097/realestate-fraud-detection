"""
Quick test script to verify API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("Testing GET / (health check)...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_detailed_health():
    """Test the detailed health endpoint"""
    print("Testing GET /health...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_analyze_status():
    """Test the analyze status endpoint"""
    print("Testing GET /api/analyze/status...")
    response = requests.get(f"{BASE_URL}/api/analyze/status")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

def test_analyze_endpoint():
    """Test the analyze endpoint"""
    print("Testing POST /api/analyze...")
    payload = {
        "listing_id": "TEST123",
        "listing_url": "https://example.com/listing/TEST123",
        "listing_data": {
            "title": "Test Listing",
            "price": 1500,
            "description": "This is a test listing"
        }
    }
    response = requests.post(f"{BASE_URL}/api/analyze", json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()

if __name__ == "__main__":
    print("=" * 60)
    print("Truth in Listings - API Test Suite")
    print("=" * 60)
    print()
    
    try:
        test_health_check()
        test_detailed_health()
        test_analyze_status()
        test_analyze_endpoint()
        print("✅ All tests completed successfully!")
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API.")
        print("Make sure the server is running with: uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
