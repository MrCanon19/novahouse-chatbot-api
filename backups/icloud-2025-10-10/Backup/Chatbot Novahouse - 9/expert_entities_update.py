#!/usr/bin/env python3
"""
Aktualizacja encji na eksperckiej poziomie
Inteligentne wyciąganie informacji z wypowiedzi klientów
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

def update_expert_entities():
    """Aktualizacja encji na poziomie eksperta"""
    
    expert_entities = [
        {
            "name": "metraz_mieszkania",
            "entity_type": "pattern",
            "values": [
                {"value": "30m2", "synonyms": ["30 m2", "30m²", "30 metrów", "trzydzieści metrów", "30 mkw"]},
                {"value": "40m2", "synonyms": ["40 m2", "40m²", "40 metrów", "czterdzieści metrów", "40 mkw"]},
                {"value": "50m2", "synonyms": ["50 m2", "50m²", "50 metrów", "pięćdziesiąt metrów", "50 mkw"]},
                {"value": "60m2", "synonyms": ["60 m2", "60m²", "60 metrów", "sześćdziesiąt metrów", "60 mkw"]},
                {"value": "70m2", "synonyms": ["70 m2", "70m²", "70 metrów", "siedemdziesiąt metrów", "70 mkw"]},
                {"value": "80m2", "synonyms": ["80 m2", "80m²", "80 metrów", "osiemdziesiąt metrów", "80 mkw"]},
                {"value": "90m2", "synonyms": ["90 m2", "90m²", "90 metrów", "dziewięćdziesiąt metrów", "90 mkw"]},
                {"value": "100m2", "synonyms": ["100 m2", "100m²", "100 metrów", "sto metrów", "100 mkw"]},
                {"value": "120m2", "synonyms": ["120 m2", "120m²", "120 metrów", "sto dwadzieścia metrów", "120 mkw"]},
                {"value": "małe_mieszkanie", "synonyms": ["małe mieszkanie", "kawalerka", "garsoniera", "studio", "mały metraż"]},
                {"value": "średnie_mieszkanie", "synonyms": ["średnie mieszkanie", "dwupokojowe", "trzypokojowe", "normalny metraż"]},
                {"value": "duże_mieszkanie", "synonyms": ["duże mieszkanie", "czteropokojowe", "pięciopokojowe", "duży metraż"]},
                {"value": "dom", "synonyms": ["dom", "domek", "budynek", "willa", "rezydencja"]}
            ]
        },
        
        {
            "name": "budżet_klienta",
            "entity_type": "pattern", 
            "values": [
                {"value": "50k", "synonyms": ["50 tysięcy", "50000", "50 tys", "pięćdziesiąt tysięcy"]},
                {"value": "75k", "synonyms": ["75 tysięcy", "75000", "75 tys", "siedemdziesiąt pięć tysięcy"]},
                {"value": "100k", "synonyms": ["100 tysięcy", "100000", "100 tys", "sto tysięcy"]},
                {"value": "150k", "synonyms": ["150 tysięcy", "150000", "150 tys", "sto pięćdziesiąt tysięcy"]},
                {"value": "200k", "synonyms": ["200 tysięcy", "200000", "200 tys", "dwieście tysięcy"]},
                {"value": "250k", "synonyms": ["250 tysięcy", "250000", "250 tys", "dwieście pięćdziesiąt tysięcy"]},
                {"value": "300k", "synonyms": ["300 tysięcy", "300000", "300 tys", "trzysta tysięcy"]},
                {"value": "400k", "synonyms": ["400 tysięcy", "400000", "400 tys", "czterysta tysięcy"]},
                {"value": "500k", "synonyms": ["500 tysięcy", "500000", "500 tys", "pięćset tysięcy"]},
                {"value": "ograniczony", "synonyms": ["ograniczony budżet", "mały budżet", "niewiele pieniędzy", "tanio", "oszczędnie"]},
                {"value": "średni", "synonyms": ["średni budżet", "normalny budżet", "rozsądnie", "w miarę"]},
                {"value": "wysoki", "synonyms": ["duży budżet", "bez ograniczeń", "premium", "najlepsze", "nie oszczędzam"]},
                {"value": "nieograniczony", "synonyms": ["nieograniczony budżet", "pieniądze nie grają roli", "najdroższe", "luksus"]}
            ]
        },
        
        {
            "name": "typ_pakietu",
            "entity_type": "list",
            "values": [
                {"value": "waniliowy", "synonyms": ["waniliowy", "podstawowy", "standard", "tani", "ekonomiczny", "budżetowy"]},
                {"value": "pomarańczowy", "synonyms": ["pomarańczowy", "średni", "złoty środek", "optymalny", "dobry stosunek jakości do ceny"]},
                {"value": "cynamonowy", "synonyms": ["cynamonowy", "premium", "wysoki standard", "drogi", "luksusowy"]},
                {"value": "szafranowy", "synonyms": ["szafranowy", "najwyższy", "top", "absolutny premium", "bez kompromisów"]},
                {"value": "comfort", "synonyms": ["comfort", "komfort", "wygodny"]},
                {"value": "express", "synonyms": ["express", "express plus", "szybki", "ekspresowy"]}
            ]
        },
        
        {
            "name": "lokalizacja_miasta",
            "entity_type": "list",
            "values": [
                {"value": "warszawa", "synonyms": ["Warszawa", "warszawie", "stolicy", "Mazowieckie"]},
                {"value": "kraków", "synonyms": ["Kraków", "krakowie", "Krakow", "Małopolskie"]},
                {"value": "gdańsk", "synonyms": ["Gdańsk", "gdansku", "Gdansk", "Pomorskie", "Trójmiasto"]},
                {"value": "poznań", "synonyms": ["Poznań", "poznaniu", "Poznan", "Wielkopolskie"]},
                {"value": "wrocław", "synonyms": ["Wrocław", "wroclawiu", "Wroclaw", "Dolnośląskie"]},
                {"value": "łódź", "synonyms": ["Łódź", "lodzi", "Lodz", "Łódzkie"]},
                {"value": "katowice", "synonyms": ["Katowice", "katowicach", "Śląskie", "Silesia"]},
                {"value": "szczecin", "synonyms": ["Szczecin", "szczecinie", "Zachodniopomorskie"]},
                {"value": "bydgoszcz", "synonyms": ["Bydgoszcz", "bydgoszczy", "Kujawsko-Pomorskie"]},
                {"value": "lublin", "synonyms": ["Lublin", "lublinie", "Lubelskie"]},
                {"value": "małe_miasto", "synonyms": ["małe miasto", "miasteczko", "prowincja", "na wsi", "poza miastem"]},
                {"value": "przedmieścia", "synonyms": ["przedmieścia", "peryferie", "obrzeża", "pod miastem"]}
            ]
        },
        
        {
            "name": "typ_mieszkania",
            "entity_type": "list",
            "values": [
                {"value": "kawalerka", "synonyms": ["kawalerka", "garsoniera", "studio", "jednopokojowe"]},
                {"value": "dwupokojowe", "synonyms": ["dwupokojowe", "2 pokoje", "dwa pokoje", "M2"]},
                {"value": "trzypokojowe", "synonyms": ["trzypokojowe", "3 pokoje", "trzy pokoje", "M3"]},
                {"value": "czteropokojowe", "synonyms": ["czteropokojowe", "4 pokoje", "cztery pokoje", "M4"]},
                {"value": "pięciopokojowe", "synonyms": ["pięciopokojowe", "5 pokoi", "pięć pokoi", "M5"]},
                {"value": "apartament", "synonyms": ["apartament", "penthouse", "loft", "duże mieszkanie"]},
                {"value": "dom", "synonyms": ["dom", "domek", "willa", "rezydencja", "budynek"]},
                {"value": "kamienica", "synonyms": ["kamienica", "stary budynek", "przedwojenne", "zabytkowe"]},
                {"value": "blok", "synonyms": ["blok", "blokowisko", "osiedle", "PRL", "wielkiej płyty"]},
                {"value": "nowe_budownictwo", "synonyms": ["nowe budownictwo", "nowy budynek", "deweloperskie", "od dewelopera"]}
            ]
        },
        
        {
            "name": "priorytet_czasowy",
            "entity_type": "list",
            "values": [
                {"value": "pilne", "synonyms": ["pilne", "szybko", "jak najszybciej", "natychmiast", "ekspresowo"]},
                {"value": "standardowe", "synonyms": ["standardowo", "normalnie", "w miarę szybko", "bez pośpiechu"]},
                {"value": "elastyczne", "synonyms": ["elastycznie", "nie spieszy mi się", "kiedy będzie czas", "bez presji"]},
                {"value": "konkretny_termin", "synonyms": ["do końca roku", "do wakacji", "przed świętami", "konkretny termin"]}
            ]
        },
        
        {
            "name": "zakres_prac",
            "entity_type": "list", 
            "values": [
                {"value": "kompleksowe", "synonyms": ["kompleksowe", "wszystko", "pod klucz", "całe mieszkanie", "full remont"]},
                {"value": "łazienka", "synonyms": ["łazienka", "łazienkę", "toaleta", "WC", "sanitariaty"]},
                {"value": "kuchnia", "synonyms": ["kuchnia", "kuchnię", "aneks kuchenny", "kitchenette"]},
                {"value": "salon", "synonyms": ["salon", "pokój dzienny", "living room", "główny pokój"]},
                {"value": "sypialnia", "synonyms": ["sypialnia", "sypialnię", "pokój do spania", "bedroom"]},
                {"value": "pokoje", "synonyms": ["pokoje", "wszystkie pokoje", "pomieszczenia mieszkalne"]},
                {"value": "podłogi", "synonyms": ["podłogi", "posadzki", "wykładziny", "parkiet", "panele"]},
                {"value": "ściany", "synonyms": ["ściany", "malowanie", "tynki", "tapety", "okładziny"]},
                {"value": "instalacje", "synonyms": ["instalacje", "elektryka", "hydraulika", "woda", "prąd"]}
            ]
        },
        
        {
            "name": "stan_mieszkania",
            "entity_type": "list",
            "values": [
                {"value": "surowy", "synonyms": ["surowy", "stan surowy", "beton", "bez wykończeń", "od dewelopera"]},
                {"value": "do_remontu", "synonyms": ["do remontu", "stare", "zniszczone", "wymaga remontu", "PRL"]},
                {"value": "częściowo_wykończone", "synonyms": ["częściowo wykończone", "w trakcie", "niedokończone"]},
                {"value": "do_odświeżenia", "synonyms": ["do odświeżenia", "kosmetyczny remont", "lekki lifting"]},
                {"value": "dobre", "synonyms": ["w dobrym stanie", "niewiele do roboty", "tylko detale"]}
            ]
        }
    ]
    
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("🔄 Aktualizacja encji eksperckich...")
        
        for entity in expert_entities:
            # Sprawdź czy encja już istnieje
            cursor.execute("SELECT id FROM entities WHERE name = %s", (entity["name"],))
            existing = cursor.fetchone()
            
            values_json = json.dumps(entity["values"], ensure_ascii=False)
            
            if existing:
                # Aktualizuj istniejącą
                cursor.execute("""
                    UPDATE entities 
                    SET values = %s 
                    WHERE name = %s
                """, (values_json, entity["name"]))
                print(f"✅ Zaktualizowano: {entity['name']}")
            else:
                # Dodaj nową
                cursor.execute("""
                    INSERT INTO entities (name, values) 
                    VALUES (%s, %s)
                """, (entity["name"], values_json))
                print(f"➕ Dodano: {entity['name']}")
        
        conn.commit()
        conn.close()
        
        print("\n🎯 Encje eksperckie zaktualizowane!")
        print("Bot teraz wyciąga konkretne informacje z wypowiedzi klientów.")
        
    except Exception as e:
        print(f"❌ Błąd: {e}")

if __name__ == "__main__":
    update_expert_entities()
