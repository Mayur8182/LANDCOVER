"""
Simple script to test the API endpoints
"""
import requests
import json

BASE_URL = "http://localhost:5000/api"

def test_health():
    """Test health check endpoint"""
    print("Testing health check...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")

def test_search_location():
    """Test location search"""
    print("Testing location search...")
    data = {"location": "Delhi, India"}
    response = requests.post(f"{BASE_URL}/search-location", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_fetch_imagery():
    """Test imagery fetching"""
    print("Testing imagery fetch...")
    data = {
        "bounds": {
            "north": 28.7,
            "south": 28.5,
            "east": 77.3,
            "west": 77.1
        },
        "start_date": "2023-01-01",
        "end_date": "2023-03-31"
    }
    response = requests.post(f"{BASE_URL}/fetch-imagery", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")

def test_complete_workflow():
    """Test complete workflow"""
    print("Testing complete workflow...")
    print("This may take several minutes...\n")
    
    data = {
        "bounds": {
            "north": 28.65,
            "south": 28.55,
            "east": 77.25,
            "west": 77.15
        },
        "start_date": "2023-01-01",
        "end_date": "2023-03-31",
        "model_type": "random_forest"
    }
    
    response = requests.post(f"{BASE_URL}/process-complete", json=data)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("Success!")
        print(f"Accuracy: {result['classification']['metrics']['accuracy']:.2%}")
        print(f"Output file: {result['classification']['classification']['output_path']}")
    else:
        print(f"Error: {response.json()}")

if __name__ == "__main__":
    print("=" * 50)
    print("API Testing Script")
    print("=" * 50 + "\n")
    
    try:
        test_health()
        test_search_location()
        
        # Uncomment to test imagery fetching (requires GEE authentication)
        # test_fetch_imagery()
        
        # Uncomment to test complete workflow (takes several minutes)
        # test_complete_workflow()
        
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to server.")
        print("Make sure the backend is running on http://localhost:5000")
    except Exception as e:
        print(f"Error: {e}")
