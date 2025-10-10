#!/usr/bin/env python3
"""
Rozbudowa systemu intencji NovaHouse chatbot
Dodanie nowych intencji i encji dla lepszej obsługi klientów
"""

import sys
import os
import psycopg2

# Dodaj ścieżkę do projektu
sys.path.insert(0, '/home/ubuntu/CZATNR3/novahouse_chatbot_gcp_deployment/novahouse_chatbot_api')

# Konfiguracja bazy danych
DB_CONFIG = {
    'host': '35.205.83.191',
    'database': 'chatbot_db',
    'user': 'chatbot_user',
    'password': 'NovaHouse2024SecurePass'
}

def add_enhanced_intents():
    """Dodanie rozbudowanych intencji"""
    
    enhanced_intents = [
        # Istniejące intencje (już są w bazie)
        # {'name': 'powitanie', 'examples': ['cześć', 'dzień dobry', 'witaj', 'hej', 'siema']},
        # {'name': 'umowienie_spotkania', 'examples': ['umów spotkanie', 'chcę się spotkać', 'spotkanie z konsultantem']},
        # {'name': 'umowienie_konsultacji', 'examples': ['konsultacja', 'chcę konsultację', 'potrzebuję porady']},
        # {'name': 'zapytanie_o_pakiety', 'examples': ['jakie pakiety', 'pakiety wykończeniowe', 'oferta pakietów']},
        
        # Nowe rozbudowane intencje
        {'name': 'wycena_kosztow', 'examples': [
            'ile kosztuje', 'jaka cena', 'koszt wykończenia', 'wycena', 'cennik', 
            'ile płacę', 'koszt za metr', 'cena pakietu', 'budżet', 'ile wydać'
        ]},
        
        {'name': 'harmonogram_realizacji', 'examples': [
            'jak długo trwa', 'czas realizacji', 'kiedy będzie gotowe', 'harmonogram', 
            'terminy', 'ile czasu', 'jak szybko', 'deadline', 'kiedy skończycie'
        ]},
        
        {'name': 'materialy_i_standardy', 'examples': [
            'jakie materiały', 'standardy wykończenia', 'jakość materiałów', 'co zawiera pakiet',
            'specyfikacja', 'rodzaje materiałów', 'klasy materiałów', 'producenci'
        ]},
        
        {'name': 'proces_realizacji', 'examples': [
            'jak przebiega realizacja', 'etapy prac', 'proces wykończenia', 'jak to działa',
            'kolejność prac', 'fazy realizacji', 'co po co', 'procedura'
        ]},
        
        {'name': 'gwarancja_i_serwis', 'examples': [
            'gwarancja', 'serwis', 'reklamacje', 'naprawa', 'co jeśli coś się zepsuje',
            'odpowiedzialność', 'ubezpieczenie', 'ochrona', 'wsparcie'
        ]},
        
        {'name': 'personalizacja_pakietu', 'examples': [
            'mogę zmienić', 'dostosowanie', 'personalizacja', 'modyfikacja pakietu',
            'inne kolory', 'zamienić materiał', 'własne pomysły', 'indywidualne'
        ]},
        
        {'name': 'porownanie_pakietow', 'examples': [
            'różnice między pakietami', 'porównanie', 'co lepsze', 'który pakiet wybrać',
            'comfort vs express', 'różnica w cenie', 'co więcej zawiera'
        ]},
        
        {'name': 'dokumenty_i_pozwolenia', 'examples': [
            'dokumenty', 'pozwolenia', 'formalności', 'papiery', 'zgłoszenia',
            'urząd', 'prawne', 'administracja', 'procedury'
        ]},
        
        {'name': 'finansowanie_i_platnosci', 'examples': [
            'raty', 'finansowanie', 'kredyt', 'płatności', 'jak płacić',
            'rozłożenie kosztów', 'leasing', 'bank', 'zaliczka'
        ]},
        
        {'name': 'referencje_i_portfolio', 'examples': [
            'wasze realizacje', 'portfolio', 'referencje', 'przykłady prac',
            'zdjęcia', 'wcześniejsze projekty', 'opinie klientów'
        ]},
        
        {'name': 'kontakt_i_lokalizacja', 'examples': [
            'gdzie jesteście', 'adres', 'kontakt', 'telefon', 'email',
            'showroom', 'biuro', 'jak dojechać', 'godziny otwarcia'
        ]},
        
        {'name': 'domy_pasywne', 'examples': [
            'domy pasywne', 'energooszczędne', 'ekologiczne', 'pasywny dom',
            'niskie zużycie energii', 'certyfikat pasywny', 'standard pasywny'
        ]},
        
        {'name': 'podziekowanie_pozegnanie', 'examples': [
            'dziękuję', 'dzięki', 'miłego dnia', 'do widzenia', 'pa pa',
            'pozdrawiam', 'na razie', 'żegnaj', 'koniec'
        ]}
    ]
    
    return enhanced_intents

def add_enhanced_entities():
    """Dodanie rozbudowanych encji"""
    
    enhanced_entities = [
        # Istniejące encje (już są w bazie)
        # {'name': 'numer_telefonu', 'patterns': [r'\d{3}[-\s]?\d{3}[-\s]?\d{3}', r'\+48\s?\d{3}[-\s]?\d{3}[-\s]?\d{3}']},
        # {'name': 'pakiet_wykonczeniowy', 'values': ['comfort', 'express', 'plus', 'szafranowy', 'pomarańczowy']},
        
        # Nowe rozbudowane encje
        {'name': 'powierzchnia_mieszkania', 'patterns': [
            r'\d+\s*m2?', r'\d+\s*metr', r'\d+\s*mkw', r'powierzchnia\s+\d+',
            r'\d+\s*m\s*kwadrat', r'mieszkanie\s+\d+\s*m'
        ]},
        
        {'name': 'typ_nieruchomosci', 'values': [
            'mieszkanie', 'dom', 'apartament', 'kawalerka', 'studio',
            'loft', 'penthouse', 'kamienica', 'szeregowiec', 'bliźniak'
        ]},
        
        {'name': 'lokalizacja', 'values': [
            'warszawa', 'kraków', 'gdańsk', 'wrocław', 'poznań', 'łódź',
            'katowice', 'lublin', 'białystok', 'szczecin', 'mazowieckie',
            'małopolskie', 'śląskie', 'dolnośląskie', 'wielkopolskie'
        ]},
        
        {'name': 'budzet_klienta', 'patterns': [
            r'\d+\s*tys', r'\d+\s*tysięcy', r'\d+\s*000', r'budżet\s+\d+',
            r'\d+\s*zł', r'do\s+\d+', r'około\s+\d+', r'maksymalnie\s+\d+'
        ]},
        
        {'name': 'termin_realizacji', 'patterns': [
            r'\d+\s*tygodni?', r'\d+\s*miesięcy?', r'do\s+\d+', r'w\s+\d+',
            r'za\s+\d+', r'przez\s+\d+', r'pilnie', r'szybko', r'natychmiast'
        ]},
        
        {'name': 'rodzaj_pomieszczenia', 'values': [
            'kuchnia', 'łazienka', 'salon', 'sypialnia', 'pokój', 'przedpokój',
            'korytarz', 'balkon', 'taras', 'garderoba', 'biuro', 'gabinet'
        ]},
        
        {'name': 'styl_wnetrza', 'values': [
            'nowoczesny', 'klasyczny', 'skandynawski', 'industrialny', 'minimalistyczny',
            'rustykalny', 'prowansalski', 'loft', 'glamour', 'boho', 'vintage'
        ]},
        
        {'name': 'email', 'patterns': [
            r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        ]},
        
        {'name': 'imie_klienta', 'patterns': [
            r'jestem\s+(\w+)', r'nazywam\s+się\s+(\w+)', r'mam\s+na\s+imię\s+(\w+)',
            r'to\s+(\w+)', r'(\w+)\s+z\s+tej\s+strony'
        ]}
    ]
    
    return enhanced_entities

def execute_database_updates():
    """Wykonanie aktualizacji bazy danych"""
    
    try:
        # Połączenie z bazą danych
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("🚀 Dodawanie rozbudowanych intencji...")
        
        # Dodanie nowych intencji
        enhanced_intents = add_enhanced_intents()
        for intent in enhanced_intents:
            # Sprawdź czy intencja już istnieje
            cursor.execute("SELECT id FROM intents WHERE name = %s", (intent['name'],))
            if cursor.fetchone() is None:
                # Konwersja examples na training_phrases (JSON)
                training_phrases = intent['examples']
                response_templates = [f"Rozumiem, że pytasz o {intent['name']}. Mogę Ci w tym pomóc!"]
                
                cursor.execute(
                    "INSERT INTO intents (name, training_phrases, response_templates) VALUES (%s, %s, %s)",
                    (intent['name'], str(training_phrases), str(response_templates))
                )
                print(f"✅ Dodano intencję: {intent['name']}")
            else:
                print(f"⚠️ Intencja już istnieje: {intent['name']}")
        
        print("🚀 Dodawanie rozbudowanych encji...")
        
        # Dodanie nowych encji
        enhanced_entities = add_enhanced_entities()
        for entity in enhanced_entities:
            # Sprawdź czy encja już istnieje
            cursor.execute("SELECT id FROM entities WHERE name = %s", (entity['name'],))
            if cursor.fetchone() is None:
                # Konwersja patterns i values na format tekstowy
                patterns = entity.get('patterns', [])
                values = entity.get('values', [])
                # Połącz patterns i values w jeden string
                entity_values = str(patterns + values)
                
                cursor.execute(
                    "INSERT INTO entities (name, values) VALUES (%s, %s)",
                    (entity['name'], entity_values)
                )
                print(f"✅ Dodano encję: {entity['name']}")
            else:
                print(f"⚠️ Encja już istnieje: {entity['name']}")
        
        # Zatwierdzenie zmian
        conn.commit()
        
        # Sprawdzenie końcowego stanu
        cursor.execute("SELECT COUNT(*) FROM intents")
        intents_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM entities")
        entities_count = cursor.fetchone()[0]
        
        print(f"\n✅ Aktualizacja zakończona pomyślnie!")
        print(f"📊 Łączna liczba intencji: {intents_count}")
        print(f"📊 Łączna liczba encji: {entities_count}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Błąd aktualizacji bazy danych: {e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()
        raise

if __name__ == "__main__":
    execute_database_updates()

