#!/usr/bin/env python3
"""
Test integracji z monday.com
"""
import requests
import json
import os

MONDAY_API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjU2MTI0OTM2MiwiYWFpIjoxMSwidWlkIjo2NzA0MDY5NCwiaWFkIjoiMjAyNS0wOS0xMlQwNjo1ODoxOC4yNzVaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MjU4NDk4NzEsInJnbiI6ImV1YzEifQ.Z-5M7pm_QZa1YBQ4a5caSg6XZlM4X1_fTcnF5JmQJyw"
MONDAY_API_URL = "https://api.monday.com/v2/"

def test_monday_connection():
    """Test połączenia z monday.com API"""
    headers = {
        "Authorization": MONDAY_API_KEY,
        "Content-Type": "application/json"
    }
    
    query = """
    query {
      me {
        name
        email
      }
      boards(limit: 5) {
        id
        name
        groups {
          id
          title
        }
      }
    }
    """
    
    try:
        response = requests.post(MONDAY_API_URL, 
                               json={"query": query}, 
                               headers=headers, 
                               timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if 'errors' in data:
                print(f"❌ Monday.com API Error: {data['errors']}")
                return False
            else:
                print("✅ Monday.com połączenie OK")
                print(f"   Użytkownik: {data['data']['me']['name']}")
                print(f"   Liczba tablic: {len(data['data']['boards'])}")
                
                # Wyświetl tablice
                for board in data['data']['boards']:
                    print(f"   📋 {board['name']} (ID: {board['id']})")
                return True
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection Error: {str(e)}")
        return False

def test_chatbot_monday_integration():
    """Test integracji chatbot -> monday.com przez API aplikacji"""
    app_url = "https://glass-core-467907-e9.ey.r.appspot.com"
    
    test_data = {
        "message": "Chcę umówić wizytę na jutro o 14:00",
        "session_id": "test-monday-integration",
        "user_info": {
            "name": "Jan Testowy",
            "phone": "123456789",
            "email": "test@example.com"
        }
    }
    
    try:
        response = requests.post(f"{app_url}/api/chatbot/chat", 
                               json=test_data, 
                               timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Chatbot odpowiedział")
            print(f"   Odpowiedź: {result.get('response', 'Brak odpowiedzi')}")
            
            # Sprawdź czy utworzono item w monday.com
            if 'monday_item_id' in result:
                print(f"   🎯 Utworzono item w Monday.com: {result['monday_item_id']}")
                return True
            else:
                print("   ⚠️  Brak informacji o utworzeniu item w Monday.com")
                return False
        else:
            print(f"❌ Chatbot Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Integration Test Error: {str(e)}")
        return False

def main():
    print("🔗 Test integracji Monday.com...")
    print("-" * 40)
    
    # Test 1: Bezpośrednie połączenie z Monday.com
    monday_ok = test_monday_connection()
    
    print("\n" + "-" * 40)
    
    # Test 2: Integracja przez chatbot (tylko jeśli aplikacja działa)
    if monday_ok:
        print("🤖 Test integracji przez chatbot...")
        integration_ok = test_chatbot_monday_integration()
        
        if integration_ok:
            print("\n🎉 Pełna integracja działa!")
        else:
            print("\n⚠️  Integracja wymaga poprawek")
    else:
        print("\n❌ Nie można testować integracji - problem z Monday.com API")

if __name__ == "__main__":
    main()

