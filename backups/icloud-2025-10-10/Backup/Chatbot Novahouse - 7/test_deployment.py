#!/usr/bin/env python3
"""
Szybki test wdrożenia aplikacji NovaHouse Chatbot
"""
import requests
import json

BASE_URL = "https://glass-core-467907-e9.ey.r.appspot.com"

def test_endpoint(endpoint, method="GET", data=None):
    """Test pojedynczego endpointu"""
    url = f"{BASE_URL}{endpoint}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        print(f"✅ {endpoint}: {response.status_code}")
        if response.status_code == 200:
            try:
                result = response.json()
                if 'status' in result:
                    print(f"   Status: {result['status']}")
                if 'database' in result:
                    print(f"   Database: {result['database']}")
            except:
                print(f"   Response: {response.text[:100]}...")
        else:
            print(f"   Error: {response.text[:100]}...")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ {endpoint}: ERROR - {str(e)}")
        return False

def main():
    print("🚀 Testowanie wdrożenia NovaHouse Chatbot...")
    print(f"Base URL: {BASE_URL}")
    print("-" * 50)
    
    # Test endpointów
    endpoints = [
        "/api/health",
        "/_ah/health", 
        "/api/ready",
        "/",
    ]
    
    results = []
    for endpoint in endpoints:
        results.append(test_endpoint(endpoint))
    
    print("-" * 50)
    success_count = sum(results)
    print(f"📊 Wyniki: {success_count}/{len(results)} endpointów działa")
    
    if success_count > 0:
        print("🎉 Aplikacja działa!")
        # Test chatbota
        print("\n🤖 Test chatbota...")
        test_data = {
            "message": "Cześć",
            "session_id": "test-session"
        }
        test_endpoint("/api/chatbot/chat", "POST", test_data)
    else:
        print("❌ Aplikacja nie działa - wszystkie endpointy zwracają błędy")

if __name__ == "__main__":
    main()

