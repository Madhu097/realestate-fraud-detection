"""
Comprehensive API Test Script
Tests all endpoints and CORS configuration
"""
import requests
import json
from colorama import init, Fore, Style

# Initialize colorama for colored output
init(autoreset=True)

# API Configuration
API_BASE_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:5173"

def print_header(text):
    """Print a formatted header"""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}{text.center(60)}")
    print(f"{Fore.CYAN}{'='*60}\n")

def print_success(text):
    """Print success message"""
    print(f"{Fore.GREEN}✅ {text}")

def print_error(text):
    """Print error message"""
    print(f"{Fore.RED}❌ {text}")

def print_info(text):
    """Print info message"""
    print(f"{Fore.YELLOW}ℹ️  {text}")

def test_endpoint(method, url, data=None, headers=None):
    """Test an API endpoint"""
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, timeout=5)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=5)
        else:
            print_error(f"Unsupported method: {method}")
            return None
        
        print_success(f"{method} {url}")
        print_info(f"Status Code: {response.status_code}")
        print_info(f"Response: {json.dumps(response.json(), indent=2)}")
        
        # Check CORS headers
        if 'Access-Control-Allow-Origin' in response.headers:
            print_success(f"CORS Header Present: {response.headers['Access-Control-Allow-Origin']}")
        else:
            print_error("CORS Header Missing!")
        
        return response
    
    except requests.exceptions.ConnectionError:
        print_error(f"Connection failed to {url}")
        print_error("Make sure the backend server is running!")
        return None
    except requests.exceptions.Timeout:
        print_error(f"Request timeout for {url}")
        return None
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return None

def test_cors_preflight(url):
    """Test CORS preflight request"""
    print_header("Testing CORS Preflight")
    headers = {
        'Origin': FRONTEND_URL,
        'Access-Control-Request-Method': 'POST',
        'Access-Control-Request-Headers': 'Content-Type',
    }
    
    try:
        response = requests.options(url, headers=headers, timeout=5)
        print_success(f"OPTIONS {url}")
        print_info(f"Status Code: {response.status_code}")
        
        cors_headers = {
            'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
            'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
            'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers'),
            'Access-Control-Allow-Credentials': response.headers.get('Access-Control-Allow-Credentials'),
        }
        
        print_info(f"CORS Headers: {json.dumps(cors_headers, indent=2)}")
        
        if cors_headers['Access-Control-Allow-Origin']:
            print_success("CORS is properly configured!")
        else:
            print_error("CORS configuration issue detected!")
        
        return response
    
    except Exception as e:
        print_error(f"CORS Preflight Error: {str(e)}")
        return None

def main():
    """Run all tests"""
    print_header("Truth in Listings - API Test Suite")
    
    # Test 1: Health Check
    print_header("Test 1: Health Check Endpoint")
    test_endpoint("GET", f"{API_BASE_URL}/")
    
    # Test 2: Detailed Health Check
    print_header("Test 2: Detailed Health Check")
    test_endpoint("GET", f"{API_BASE_URL}/health")
    
    # Test 3: Analysis Status
    print_header("Test 3: Analysis Status")
    test_endpoint("GET", f"{API_BASE_URL}/api/analyze/status")
    
    # Test 4: Analyze Listing
    print_header("Test 4: Analyze Listing Endpoint")
    test_data = {
        "listing_id": "test123",
        "listing_url": "https://example.com/listing/test123",
        "listing_data": {
            "title": "Test Listing",
            "price": 1000,
            "description": "This is a test listing"
        }
    }
    test_endpoint("POST", f"{API_BASE_URL}/api/analyze", data=test_data)
    
    # Test 5: CORS Preflight
    test_cors_preflight(f"{API_BASE_URL}/api/analyze")
    
    # Test 6: Test with Origin Header
    print_header("Test 6: Request with Origin Header")
    headers = {'Origin': FRONTEND_URL}
    test_endpoint("GET", f"{API_BASE_URL}/", headers=headers)
    
    print_header("All Tests Completed!")
    print_info("If all tests passed, your API is working correctly!")
    print_info(f"Frontend URL: {FRONTEND_URL}")
    print_info(f"Backend URL: {API_BASE_URL}")
    print_info(f"API Docs: {API_BASE_URL}/docs")

if __name__ == "__main__":
    main()
