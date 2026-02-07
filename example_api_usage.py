"""
Example API requests for both US and UK Match.com
"""
import requests
import json

API_URL = "http://localhost:8000/automate"

def test_us_match():
    """Test US Match.com automation via API"""
    print("🇺🇸 Testing US Match.com API...")
    
    payload = {
        "email": "test_us_user@gmail.com",
        "password": "TestPassword123!",
        "name": "John",
        "region": "us"
    }
    
    response = requests.post(API_URL, json=payload)
    print(f"Response: {response.json()}")

def test_uk_match():
    """Test UK Match.com automation via API"""
    print("🇬🇧 Testing UK Match.com API...")
    
    payload = {
        "email": "test_uk_user@gmail.com",
        "password": "TestPassword123!",
        "name": "James",
        "region": "uk"
    }
    
    response = requests.post(API_URL, json=payload)
    print(f"Response: {response.json()}")

def health_check():
    """Check if API is running"""
    print("🏥 Checking API health...")
    response = requests.get("http://localhost:8000/")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    # Check if API is running
    try:
        health_check()
        print("\n" + "="*50 + "\n")
        
        # Test US
        test_us_match()
        print("\n" + "="*50 + "\n")
        
        # Test UK
        test_uk_match()
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: API is not running!")
        print("Please start the API first: python api.py")
