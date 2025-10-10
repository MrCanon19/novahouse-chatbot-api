#!/usr/bin/env python3
"""
Test skryptu bazy wiedzy NovaHouse
"""

import requests
import json

def test_knowledge_base():
    """Test integracji bazy wiedzy z chatbotem"""
    
    base_url = "https://glass-core-467907-e9.ey.r.appspot.com"
    
    # Test pytania o pakiety
    test_questions = [
        "Jakie pakiety wykończeniowe oferujecie?",
        "Ile kosztuje pakiet Comfort?",
        "Jak długo trwa realizacja?",
        "Czy można umówić konsultację?",
        "Jakie materiały używacie?",
        "Czy robicie domy pasywne?",
        "Jak mogę się z wami skontaktować?",
        "Czy macie showroom?",
        "Co to jest pakiet Express Plus?"
    ]
    
    print("🧠 Test bazy wiedzy NovaHouse...")
    print("=" * 50)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Pytanie: {question}")
        
        try:
            response = requests.post(
                f"{base_url}/api/chatbot/chat",
                json={
                    "message": question,
                    "session_id": f"test_session_{i}"
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Odpowiedź: {data.get('response', 'Brak odpowiedzi')[:200]}...")
                print(f"   Intent: {data.get('intent', 'unknown')}")
                print(f"   Baza wiedzy: {data.get('knowledge_base_enabled', False)}")
            else:
                print(f"❌ Błąd {response.status_code}: {response.text}")
                
        except Exception as e:
            print(f"❌ Błąd połączenia: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Test zakończony!")

if __name__ == "__main__":
    test_knowledge_base()

