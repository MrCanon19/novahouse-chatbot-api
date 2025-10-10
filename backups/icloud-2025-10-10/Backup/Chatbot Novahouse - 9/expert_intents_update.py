#!/usr/bin/env python3
"""
Aktualizacja intencji na eksperckiej poziomie
40 lat doświadczenia w rozpoznawaniu potrzeb klientów
"""

import psycopg2
import json

# Konfiguracja bazy danych
DB_CONFIG = {
    'host': '35.205.83.191',
    'database': 'chatbot_db',
    'user': 'chatbot_user',
    'password': 'NovaHouse2024SecurePass',
    'port': 5432
}

def update_expert_intents():
    """Aktualizacja intencji na poziomie eksperta"""
    
    expert_intents = [
        {
            "name": "wycena_konkretna",
            "training_phrases": [
                "ile kosztuje wykończenie 50m2",
                "koszt remontu 70 metrów",
                "cena za metr kwadratowy",
                "ile będzie kosztować moje mieszkanie",
                "jaki budżet na remont",
                "ile potrzebuję pieniędzy",
                "koszt wykończenia mieszkania",
                "ile kosztuje pakiet waniliowy",
                "ile kosztuje pakiet pomarańczowy",
                "ile kosztuje pakiet cynamonowy",
                "ile kosztuje pakiet szafranowy",
                "cena za m2",
                "koszt remontu",
                "budżet na wykończenie",
                "ile wydać na remont",
                "kalkulacja kosztów",
                "wycena mieszkania",
                "ile kosztuje remont łazienki",
                "ile kosztuje remont kuchni",
                "koszt wykończenia pod klucz"
            ],
            "response_templates": [
                "Podaj mi metraż mieszkania i preferowany pakiet, a dam Ci konkretną kalkulację kosztów z 40-letnim doświadczeniem."
            ]
        },
        
        {
            "name": "czas_realizacji_konkretny", 
            "training_phrases": [
                "jak długo trwa remont",
                "ile czasu zajmuje wykończenie",
                "kiedy będzie gotowe",
                "harmonogram prac",
                "terminy realizacji",
                "jak szybko zrobicie",
                "deadline remontu",
                "czas wykończenia mieszkania",
                "ile tygodni trwa remont",
                "kiedy mogę się wprowadzić",
                "harmonogram wykończenia",
                "etapy realizacji",
                "jak długo trwa remont 50m2",
                "jak długo trwa remont 70m2",
                "czas remontu łazienki",
                "czas remontu kuchni",
                "szybki remont",
                "ekspresowe wykończenie",
                "pilny termin",
                "jak najszybciej"
            ],
            "response_templates": [
                "Podaj metraż i pakiet, a dam Ci realny harmonogram z uwzględnieniem wszystkich etapów i możliwych opóźnień."
            ]
        },
        
        {
            "name": "porady_eksperckie",
            "training_phrases": [
                "co polecasz",
                "który pakiet wybrać", 
                "co jest lepsze",
                "jaka jest różnica",
                "co doradzasz",
                "które rozwiązanie",
                "co warto wybrać",
                "najlepszy pakiet",
                "co się opłaca",
                "mądra rada",
                "eksperckia opinia",
                "profesjonalna rada",
                "co byś wybrał",
                "twoja rekomendacja",
                "najlepszy stosunek jakości do ceny",
                "co jest warte swojej ceny",
                "na czym nie oszczędzać",
                "gdzie można zaoszczędzić",
                "najczęstsze błędy",
                "czego unikać",
                "sekrety branży",
                "praktyczne porady",
                "co warto wiedzieć",
                "insider tips"
            ],
            "response_templates": [
                "Z 40-letnim doświadczeniem mogę doradzić konkretnie. Powiedz mi o swoim budżecie, metrażu i oczekiwaniach."
            ]
        },
        
        {
            "name": "materialy_konkretne",
            "training_phrases": [
                "jakie materiały używacie",
                "jakość materiałów",
                "marki materiałów",
                "rodzaje podłóg",
                "typy płytek",
                "farby do ścian",
                "armatura łazienkowa",
                "blaty kuchenne",
                "panele podłogowe",
                "parkiet czy panele",
                "płytki czy panele",
                "laminat czy parkiet",
                "jakie płytki w łazience",
                "jaka farba na ściany",
                "jaki blat do kuchni",
                "materiały w pakiecie waniliowym",
                "materiały w pakiecie pomarańczowym",
                "materiały w pakiecie cynamonowym",
                "materiały premium",
                "najlepsze materiały",
                "trwałe materiały",
                "ekologiczne materiały",
                "antyalergiczne materiały"
            ],
            "response_templates": [
                "Opowiem Ci konkretnie o materiałach - marki, ceny, zalety i wady. Bez marketingowych bzdur."
            ]
        },
        
        {
            "name": "lokalizacja_specyfika",
            "training_phrases": [
                "remont w Warszawie",
                "wykończenie w Krakowie", 
                "remont w Gdańsku",
                "czy robicie w Poznaniu",
                "czy robicie w Wrocławiu",
                "czy robicie w Łodzi",
                "remont w małym mieście",
                "koszty w Warszawie",
                "ceny w Krakowie",
                "czy dojedzecie do",
                "obsługujecie region",
                "gdzie działacie",
                "zasięg działania",
                "dojazd do klienta",
                "koszty dojazdu",
                "dodatkowe koszty lokalizacji",
                "specyfika regionalna",
                "lokalne przepisy",
                "pozwolenia w Warszawie",
                "ograniczenia w kamienicy",
                "remont w bloku",
                "remont w domu"
            ],
            "response_templates": [
                "Każda lokalizacja ma swoją specyfikę. Powiedz gdzie planujesz remont - dam konkretne informacje o kosztach i ograniczeniach."
            ]
        },
        
        {
            "name": "problemy_praktyczne",
            "training_phrases": [
                "co może pójść nie tak",
                "najczęstsze problemy",
                "jak uniknąć błędów",
                "na co uważać",
                "pułapki w remoncie",
                "czego się spodziewać",
                "możliwe komplikacje",
                "dodatkowe koszty",
                "nieprzewidziane wydatki",
                "opóźnienia w remoncie",
                "problemy z ekipą",
                "problemy z materiałami",
                "jak kontrolować postęp",
                "jak sprawdzać jakość",
                "odbiór prac",
                "reklamacje",
                "gwarancja",
                "co robić gdy coś nie gra",
                "jak się zabezpieczyć",
                "umowa na remont",
                "płatności za remont"
            ],
            "response_templates": [
                "40 lat w branży nauczyło mnie wszystkich pułapek. Opowiem Ci jak ich uniknąć i na co uważać."
            ]
        },
        
        {
            "name": "porownanie_pakietow",
            "training_phrases": [
                "różnica między pakietami",
                "waniliowy vs pomarańczowy",
                "pomarańczowy vs cynamonowy", 
                "który pakiet lepszy",
                "porównanie standardów",
                "co się zmienia między pakietami",
                "czy warto dopłacić",
                "różnica w jakości",
                "różnica w materiałach",
                "różnica w cenie",
                "upgrade pakietu",
                "downgrade pakietu",
                "co zyskuję płacąc więcej",
                "czy podstawowy wystarczy",
                "czy premium się opłaca",
                "najlepszy stosunek jakości do ceny",
                "średni pakiet",
                "złoty środek",
                "kompromis jakość cena"
            ],
            "response_templates": [
                "Pokażę Ci konkretne różnice między pakietami - materiały, efekt końcowy, opłacalność. Bez ściemy."
            ]
        },
        
        {
            "name": "budżet_optymalizacja",
            "training_phrases": [
                "jak zaoszczędzić na remoncie",
                "gdzie można ciąć koszty",
                "na czym nie oszczędzać",
                "optymalizacja budżetu",
                "maksimum za minimum",
                "mam ograniczony budżet",
                "jak tanio zrobić remont",
                "gdzie szukać oszczędności",
                "co jest najważniejsze",
                "priorytety w remoncie",
                "etapowanie remontu",
                "remont w ratach",
                "co zrobić najpierw",
                "co można odłożyć",
                "podstawowe wykończenie",
                "minimum do zamieszkania",
                "remont pod wynajem",
                "remont na sprzedaż",
                "inwestycyjne wykończenie"
            ],
            "response_templates": [
                "Pokażę Ci jak mądrze wydać każdą złotówkę. 40 lat doświadczenia w optymalizacji budżetów."
            ]
        }
    ]
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("🔄 Aktualizacja intencji eksperckich...")
        
        for intent in expert_intents:
            # Sprawdź czy intencja już istnieje
            cursor.execute("SELECT id FROM intents WHERE name = %s", (intent["name"],))
            existing = cursor.fetchone()
            
            training_phrases_json = json.dumps(intent["training_phrases"], ensure_ascii=False)
            response_templates_json = json.dumps(intent["response_templates"], ensure_ascii=False)
            
            if existing:
                # Aktualizuj istniejącą
                cursor.execute("""
                    UPDATE intents 
                    SET training_phrases = %s, response_templates = %s 
                    WHERE name = %s
                """, (training_phrases_json, response_templates_json, intent["name"]))
                print(f"✅ Zaktualizowano: {intent['name']}")
            else:
                # Dodaj nową
                cursor.execute("""
                    INSERT INTO intents (name, training_phrases, response_templates) 
                    VALUES (%s, %s, %s)
                """, (intent["name"], training_phrases_json, response_templates_json))
                print(f"➕ Dodano: {intent['name']}")
        
        conn.commit()
        conn.close()
        
        print("\n🎯 Intencje eksperckie zaktualizowane!")
        print("Bot jest teraz mądrzejszy i bardziej trafny.")
        
    except Exception as e:
        print(f"❌ Błąd: {e}")

if __name__ == "__main__":
    update_expert_intents()
