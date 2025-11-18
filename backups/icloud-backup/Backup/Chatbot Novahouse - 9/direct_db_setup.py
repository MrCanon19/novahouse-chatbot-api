#!/usr/bin/env python3
"""
Bezpośrednie dodanie intencji i encji do bazy PostgreSQL
"""

import psycopg2
import json
import sys

# Konfiguracja bazy danych
DB_CONFIG = {
    'host': '35.205.83.191',
    'database': 'chatbot_db', 
    'user': 'chatbot_user',
    'password': 'NovaHouse2024SecurePass',
    'port': 5432
}

# Intencje do dodania
INTENTS = [
    {
        "name": "powitanie",
        "training_phrases": ["cześć", "hej", "witaj", "dzień dobry", "siema", "hello", "hi", "witam"],
        "response_templates": ["Cześć! 👋 Witaj w NovaHouse! Jestem Twoim asystentem i pomogę Ci w wyborze pakietu wykończeniowego, uzyskaniu informacji o cenach, umówieniu spotkania z konsultantem i odpowiedzi na pytania o nasze usługi. Jak mogę Ci pomóc?"]
    },
    {
        "name": "umowienie_spotkania", 
        "training_phrases": ["umów spotkanie", "spotkanie z konsultantem", "chcę się spotkać", "wizyta konsultanta", "umówić wizytę", "spotkanie", "konsultacja"],
        "response_templates": ["📅 Konsultacje NovaHouse: Podaj swój numer telefonu, a skontaktujemy się z Tobą w ciągu 24 godzin."]
    },
    {
        "name": "umowienie_konsultacji",
        "training_phrases": ["umów konsultację", "chcę się umówić", "konsultacja", "doradztwo", "chcę spotkanie", "konsultant", "doradca"],
        "response_templates": ["Świetnie! Podaj proszę swój numer telefonu, a my skontaktujemy się z Tobą w ciągu 24 godzin."]
    },
    {
        "name": "zapytanie_o_pakiety",
        "training_phrases": ["pakiety wykończeniowe", "jakie pakiety", "rodzaje pakietów", "oferta pakietów", "pakiet comfort", "pakiet express", "pakiety"],
        "response_templates": ["🏠 Nasze pakiety wykończeniowe NovaHouse: 🟡 Pakiet Comfort - podstawowy standard (do 40m², 4-6 tygodni) 🟠 Pakiet Express Plus + Z2 - premium (do 90m², 6-10 tygodni)"]
    }
]

# Encje do dodania
ENTITIES = [
    {
        "name": "numer_telefonu",
        "values": ["123456789", "123 456 789", "+48 123 456 789", "500123456", "600123456", "700123456", "800123456", "900123456"]
    },
    {
        "name": "pakiet_wykonczeniowy", 
        "values": ["comfort", "express plus", "express", "podstawowy", "premium", "standard"]
    }
]

def connect_db():
    """Połączenie z bazą danych"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ Błąd połączenia z bazą: {e}")
        return None

def add_intents(conn):
    """Dodaje intencje do bazy"""
    cursor = conn.cursor()
    success = 0
    
    for intent in INTENTS:
        try:
            cursor.execute("""
                INSERT INTO intents (name, training_phrases, response_templates)
                VALUES (%s, %s, %s)
                ON CONFLICT (name) DO NOTHING
            """, (
                intent["name"],
                json.dumps(intent["training_phrases"]),
                json.dumps(intent["response_templates"])
            ))
            
            if cursor.rowcount > 0:
                print(f"✅ Dodano intencję: {intent['name']}")
                success += 1
            else:
                print(f"⚠️ Intencja już istnieje: {intent['name']}")
                
        except Exception as e:
            print(f"❌ Błąd dodawania intencji {intent['name']}: {e}")
    
    conn.commit()
    return success

def add_entities(conn):
    """Dodaje encje do bazy"""
    cursor = conn.cursor()
    success = 0
    
    for entity in ENTITIES:
        try:
            cursor.execute("""
                INSERT INTO entities (name, values)
                VALUES (%s, %s)
                ON CONFLICT (name) DO NOTHING
            """, (
                entity["name"],
                json.dumps(entity["values"])
            ))
            
            if cursor.rowcount > 0:
                print(f"✅ Dodano encję: {entity['name']}")
                success += 1
            else:
                print(f"⚠️ Encja już istnieje: {entity['name']}")
                
        except Exception as e:
            print(f"❌ Błąd dodawania encji {entity['name']}: {e}")
    
    conn.commit()
    return success

def main():
    print("🚀 Bezpośrednie dodawanie do bazy PostgreSQL...")
    
    conn = connect_db()
    if not conn:
        sys.exit(1)
    
    try:
        print("\n📝 Dodawanie intencji...")
        intent_success = add_intents(conn)
        
        print("\n🏷️ Dodawanie encji...")
        entity_success = add_entities(conn)
        
        print(f"\n🎉 Zakończono! Intencje: {intent_success}/{len(INTENTS)}, Encje: {entity_success}/{len(ENTITIES)}")
        
        if intent_success > 0 or entity_success > 0:
            print("✅ Dane zostały dodane do bazy!")
            print("🔄 Chatbot wymaga przeładowania aby załadować nowe dane")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()

