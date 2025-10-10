#!/usr/bin/env python3
"""
Skrypt do dodania podstawowych intencji i encji do bazy danych chatbota NovaHouse
"""

import requests
import json
import sys

# URL aplikacji
BASE_URL = "https://20250915t180541-dot-glass-core-467907-e9.ey.r.appspot.com"

# Definicje intencji
INTENTS = [
    {
        "name": "powitanie",
        "training_phrases": [
            "cześć", "hej", "witaj", "dzień dobry", "siema", "hello", "hi",
            "witam", "dzień dobry", "dobry wieczór", "miło cię poznać"
        ],
        "response_templates": [
            "Cześć! 👋 Witaj w NovaHouse! Jestem Twoim asystentem i pomogę Ci w wyborze pakietu wykończeniowego, uzyskaniu informacji o cenach, umówieniu spotkania z konsultantem i odpowiedzi na pytania o nasze usługi. Jak mogę Ci pomóc?"
        ]
    },
    {
        "name": "pozegnanie", 
        "training_phrases": [
            "pa", "do widzenia", "żegnaj", "miłego dnia", "dziękuję", "dzięki",
            "to wszystko", "koniec", "bye", "goodbye", "see you"
        ],
        "response_templates": [
            "Dziękujemy za rozmowę! Jeśli masz jeszcze jakieś pytania, zapraszamy ponownie. Do zobaczenia! 👋"
        ]
    },
    {
        "name": "zapytanie_o_pakiety",
        "training_phrases": [
            "pakiety wykończeniowe", "jakie pakiety", "rodzaje pakietów", "oferta pakietów",
            "pakiet comfort", "pakiet express", "standardy wykończenia", "co oferujecie",
            "pakiety", "wykończenia", "standardy", "opcje wykończenia"
        ],
        "response_templates": [
            "🏠 **Nasze pakiety wykończeniowe NovaHouse:** 🟡 **Pakiet Comfort** - podstawowy standard (do 40m², 4-6 tygodni) 🟠 **Pakiet Express Plus + Z2** - premium (do 90m², 6-10 tygodni) **Każdy pakiet zawiera:** • Kompleksowe wykończenie mieszkania • Wysokiej jakości materiały • Profesjonalne wykonanie • Pełną gwarancję • Możliwość personalizacji **O którym pakiecie chciałbyś dowiedzieć się więcej?** Napisz \"Comfort\" lub \"Express Plus\" dla szczegółów!"
        ]
    },
    {
        "name": "pytanie_o_ceny",
        "training_phrases": [
            "ile kosztuje", "ceny", "cennik", "koszt", "wycena", "ile płacę",
            "cena pakietu", "koszt wykończenia", "ile za pakiet", "budżet",
            "proszę o wycenę", "koszt realizacji"
        ],
        "response_templates": [
            "Ceny naszych pakietów zależą od metrażu i wybranego standardu wykończenia. Przygotujemy dla Ciebie indywidualną wycenę. Czy chciałbyś umówić się na bezpłatną konsultację, podczas której przedstawimy dokładną ofertę?"
        ]
    },
    {
        "name": "umowienie_konsultacji",
        "training_phrases": [
            "umów konsultację", "chcę się umówić", "spotkanie", "konsultacja",
            "umówić spotkanie", "wizyta", "prezentacja", "doradztwo",
            "chcę spotkanie", "umów wizytę", "konsultant", "doradca"
        ],
        "response_templates": [
            "Świetnie! Chętnie umówimy się na spotkanie, aby omówić Twoje potrzeby. Możesz wybrać: 📞 **Konsultację telefoniczną** - szybko i wygodnie 🏢 **Spotkanie w naszym biurze** - pełna prezentacja materiałów 🏡 **Wizytę w Twoim domu/mieszkaniu** - szczegółowa wycena i doradztwo Podaj proszę swój numer telefonu, a my skontaktujemy się z Tobą w ciągu 24 godzin."
        ]
    },
    {
        "name": "umowienie_spotkania",
        "training_phrases": [
            "umów spotkanie", "spotkanie z konsultantem", "chcę się spotkać",
            "wizyta konsultanta", "prezentacja materiałów", "spotkanie w biurze",
            "wizyta w domu", "konsultacja domowa", "umówić wizytę"
        ],
        "response_templates": [
            "📅 **Konsultacje NovaHouse:** **🎯 Rodzaje konsultacji:** • **Konsultacja z projektantem** - planowanie wnętrza • **Wycena** - kalkulacja kosztów • **Prezentacja materiałów** - wybór standardu **📍 Formy spotkań:** • **Stacjonarne** - w naszym showroomie • **Online** - wygodnie z domu • **W showroomie** - z prezentacją materiałów **📞 Rezerwacja:** • Przez Booksy (system rezerwacji) • Bezpośredni kontakt z zespołem • Formularz na stronie **💰 Pierwsza konsultacja BEZPŁATNA!** Podaj swój numer telefonu, a skontaktujemy się z Tobą."
        ]
    },
    {
        "name": "pytanie_o_kontakt",
        "training_phrases": [
            "kontakt", "telefon", "adres", "gdzie jesteście", "jak się skontaktować",
            "numer telefonu", "email", "strona internetowa", "lokalizacja",
            "biuro", "siedziba", "godziny otwarcia"
        ],
        "response_templates": [
            "📞 **Kontakt z NovaHouse:** 🏢 **Biuro:** ul. Przykładowa 123, Gdańsk 📱 **Telefon:** +48 123 456 789 📧 **Email:** kontakt@novahouse.pl 🌐 **Strona:** www.novahouse.pl **Godziny otwarcia:** Pon. - Pt.: 9:00 - 17:00 Sobota: 10:00 - 14:00 Niedziela: Zamknięte Czy mogę jeszcze w czymś pomóc?"
        ]
    },
    {
        "name": "pytanie_o_materialy",
        "training_phrases": [
            "materiały", "jakie materiały", "jakość materiałów", "marki materiałów",
            "farby", "płytki", "armatura", "oświetlenie", "specyfikacja",
            "co używacie", "producenci", "standardy materiałów"
        ],
        "response_templates": [
            "Używamy tylko wysokiej jakości materiałów od sprawdzonych dostawców: 🔨 **Materiały budowlane:** Renomowane marki europejskie 🎨 **Farby i tynki:** Dulux, Caparol, Beckers 🚿 **Armatura łazienkowa:** Grohe, Hansgrohe, Roca 💡 **Oświetlenie:** Philips, Osram, Ledvance W każdym pakiecie znajdziesz szczegółową specyfikację materiałów. Czy chcesz poznać szczegóły dla konkretnego pakietu?"
        ]
    },
    {
        "name": "pytanie_o_czas_realizacji",
        "training_phrases": [
            "ile trwa", "czas realizacji", "jak długo", "harmonogram", "terminy",
            "kiedy skończycie", "czas wykończenia", "etapy realizacji",
            "jak długo trwa wykończenie", "terminy realizacji"
        ],
        "response_templates": [
            "Czas realizacji zależy od zakresu prac i metrażu: ⏱️ **Mieszkanie do 50m²:** 4-6 tygodni ⏱️ **Mieszkanie 50-80m²:** 6-8 tygodni ⏱️ **Mieszkanie powyżej 80m²:** 8-12 tygodni **Etapy realizacji:** 1. Projekt i planowanie (1 tydzień) 2. Praca przygotowawcza (1-2 dni) 3. Instalacje (1-2 tygodnie) 4. Wykończenia (2-4 tygodnie) 5. Odbiór i sprzątanie (1-2 dni) Podaj metraż swojego mieszkania, a określimy dokładny harmonogram!"
        ]
    }
]

# Definicje encji
ENTITIES = [
    {
        "name": "pakiet_wykonczeniowy",
        "values": [
            "comfort", "waniliowy", "pomarańczowy", "cynamonowy", "szafranowy",
            "express plus", "express", "podstawowy", "premium", "standard"
        ]
    },
    {
        "name": "metraz_lokalu", 
        "values": [
            "30m2", "40m2", "50m2", "60m2", "70m2", "80m2", "90m2", "100m2",
            "30 m2", "40 m2", "50 m2", "60 m2", "70 m2", "80 m2", "90 m2", "100 m2",
            "30 metrów", "40 metrów", "50 metrów", "60 metrów", "70 metrów", "80 metrów"
        ]
    },
    {
        "name": "numer_telefonu",
        "values": [
            "123456789", "123 456 789", "+48 123 456 789", "48123456789",
            "500123456", "600123456", "700123456", "800123456", "900123456"
        ]
    },
    {
        "name": "typ_konsultacji",
        "values": [
            "telefoniczna", "online", "w biurze", "w domu", "stacjonarna",
            "domowa", "prezentacja materiałów", "wycena", "projektowanie"
        ]
    },
    {
        "name": "rodzaj_pomieszczenia",
        "values": [
            "mieszkanie", "dom", "biuro", "lokal", "kawalerka", "studio",
            "dwupokojowe", "trzypokojowe", "czteropokojowe", "penthouse"
        ]
    }
]

def add_intent(intent_data):
    """Dodaje intencję do bazy danych"""
    url = f"{BASE_URL}/api/chatbot/intents"
    
    payload = {
        "name": intent_data["name"],
        "training_phrases": json.dumps(intent_data["training_phrases"]),
        "response_templates": json.dumps(intent_data["response_templates"])
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"✅ Dodano intencję: {intent_data['name']}")
            return True
        else:
            print(f"❌ Błąd dodawania intencji {intent_data['name']}: {response.status_code}")
            print(f"   Odpowiedź: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Wyjątek przy dodawaniu intencji {intent_data['name']}: {e}")
        return False

def add_entity(entity_data):
    """Dodaje encję do bazy danych"""
    url = f"{BASE_URL}/api/chatbot/entities"
    
    payload = {
        "name": entity_data["name"],
        "values": json.dumps(entity_data["values"])
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print(f"✅ Dodano encję: {entity_data['name']}")
            return True
        else:
            print(f"❌ Błąd dodawania encji {entity_data['name']}: {response.status_code}")
            print(f"   Odpowiedź: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Wyjątek przy dodawaniu encji {entity_data['name']}: {e}")
        return False

def main():
    print("🚀 Rozpoczynam dodawanie intencji i encji do bazy danych...")
    
    # Dodawanie intencji
    print("\n📝 Dodawanie intencji...")
    intent_success = 0
    for intent in INTENTS:
        if add_intent(intent):
            intent_success += 1
    
    print(f"\n✅ Dodano {intent_success}/{len(INTENTS)} intencji")
    
    # Dodawanie encji
    print("\n🏷️ Dodawanie encji...")
    entity_success = 0
    for entity in ENTITIES:
        if add_entity(entity):
            entity_success += 1
    
    print(f"\n✅ Dodano {entity_success}/{len(ENTITIES)} encji")
    
    print(f"\n🎉 Zakończono! Intencje: {intent_success}/{len(INTENTS)}, Encje: {entity_success}/{len(ENTITIES)}")
    
    if intent_success == len(INTENTS) and entity_success == len(ENTITIES):
        print("✅ Wszystkie dane zostały pomyślnie dodane!")
        print("🔄 Chatbot powinien teraz rozpoznawać intencje i uruchamiać integrację Monday.com")
    else:
        print("⚠️ Niektóre dane nie zostały dodane. Sprawdź logi powyżej.")

if __name__ == "__main__":
    main()

