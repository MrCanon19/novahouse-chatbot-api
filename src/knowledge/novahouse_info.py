"""
NovaHouse - Baza Wiedzy o Pakietach Wykończeniowych
"""

# Godziny pracy
BUSINESS_HOURS = {
    "monday_friday": "09:00 - 17:00",
    "saturday": "10:00 - 14:00",
    "sunday": "zamknięte",
    "timezone": "CET"
}

# Informacje kontaktowe
CONTACT_INFO = {
    "phone": "+48 585 004 663",
    "email": "kontakt@novahouse.pl",
    "website": "https://novahouse.pl",
    "address": "Warszawa",
    "nip": "Dostępna na wniosek"
}

PACKAGES = {
    "standard": {
        "name": "Pakiet Standard",
        "price_range": "Dostępny cenowo",
        "description": "Podstawowe wykończenie mieszkania z materiałami dobrej jakości",
        "features": [
            "Podstawowe płytki ceramiczne",
            "Standardowe drzwi wewnętrzne",
            "Panele podłogowe klasy AC4",
            "Malowanie ścian farbą lateksową",
            "Podstawowa armatura łazienkowa",
            "Instalacje elektryczne i hydrauliczne"
        ],
        "ideal_for": "Osoby szukające solidnego wykończenia w przystępnej cenie"
    },
    "premium": {
        "name": "Pakiet Premium",
        "price_range": "Średnia półka cenowa",
        "description": "Wyższa jakość materiałów i wykończenia",
        "features": [
            "Płytki ceramiczne znanych marek",
            "Drzwi wewnętrzne premium z ukrytą ościeżnicą",
            "Panele drewniane lub kamienne",
            "Gładzie gipsowe i malowanie premium",
            "Armatura łazienkowa renomowanych producentów",
            "Smart home - podstawowa automatyka",
            "Oświetlenie LED"
        ],
        "ideal_for": "Klienci oczekujący wyższego standardu i nowoczesnych rozwiązań"
    },
    "luxury": {
        "name": "Pakiet Luxury (Indywidualny)",
        "price_range": "Premium",
        "description": "Ekskluzywne wykończenie szyte na miarę",
        "features": [
            "Materiały ekskluzywne (marmur, granit)",
            "Meble i zabudowy na wymiar",
            "Zaawansowana automatyka budynkowa",
            "Designerskie oświetlenie",
            "Armatura premium (Grohe, Hansgrohe)",
            "Indywidualny projekt wnętrz",
            "Konsultacje z architektem wnętrz"
        ],
        "ideal_for": "Klienci z wysokimi wymaganiami, szukający wyjątkowego designu"
    }
}

FAQ = {
    "jak_dlugo_trwa": "Wykończenie mieszkania 50-60m² trwa zwykle 6-12 tygodni w zależności od pakietu i zakresu prac. W naszym harmonogramie postaramy się znaleźć Ci dogodny czas.",
    "czy_wlaczone_materialy": "Tak, nasze pakiety zawierają zarówno robociznę jak i wszystkie materiały potrzebne do realizacji prac.",
    "mozna_dostosowac": "Zdecydowanie! Wszystkie pakiety są elastyczne. Możesz wymienić materiały, dodać dodatkowe usługi lub zmienić zakres prac — dostosujemy ofertę do Twoich potrzeb.",
    "gwarancja": "Udzielamy 2-letniej gwarancji na wykonane prace. Na materiały obowiązuje gwarancja producenta.",
    "platnosc": "Płatności realizujemy etapowo: zaliczka 30%, kolejne transze po ukończeniu poszczególnych etapów, końcowe 10% po odbiorze prac.",
    "ile_kosztuje": "Ceny zaczynają się od 949 zł/m² (pakiet Standard) do 1990 zł/m² (pakiet Luxury). Wycena indywidualna jest bezpłatna.",
    "produkty": "Współpracujemy z najlepszymi producentami materiałów budowlanych. W zależności od pakietu oferujemy różne opcje — od standardowych do luksusowych marek.",
    "etapy": "Współpraca z nami przebiega w kilku etapach: wstępna konsultacja, projekt, wycena, zawarcie umowy, realizacja, inspekcja, odbiór.",
    "czy_potrzebny_projekt": "Dla pełnego zakresu prac rekomendujemy projekt indywidualny. Pozwoli Ci to w pełni kontrolować budżet i wynik końcowy.",
    "smart_home": "Smart home jest dostępna w pakiecie Premium i Luxury. Możesz wybrać automatykę oświetlenia, temperatury lub bezpieczeństwa.",
}

COMPANY_INFO = """
NovaHouse to profesjonalna firma specjalizująca się w kompleksowym wykończeniu mieszkań i domów w Warszawie.

📊 O NAS:
Oferujemy kompleksowe usługi wykończeniowe od A do Z. Nasz zespół ma wieloletnie doświadczenie w realizacji projektów dla wymagających klientów.

✨ NASZE ATUTY:
• Kompleksowa obsługa projektu od A do Z
• Doświadczony zespół fachowców
• Materiały najwyższej jakości
• Terminowość i rzetelność
• 2 lata gwarancji na wykonane prace
• Elastyczne formy płatności
• Indywidualne podejście do każdego projektu

📞 KONTAKT:
Telefon: +48 585 004 663
Email: kontakt@novahouse.pl
Strona: https://novahouse.pl

🕐 GODZINY PRACY:
Poniedziałek - Piątek: 09:00 - 17:00
Sobota: 10:00 - 14:00
Niedziela: zamknięte

💰 CENY ORIENTACYJNIE:
Wykończenie szacujemy od 949 zł/m² do 1990 zł/m² (w zależności od pakietu i zakresu prac).

Chętnie odpowiemy na wszystkie Twoje pytania. Zapraszamy do kontaktu!
"""

def get_package_description(package_name):
    """Zwraca szczegółowy opis pakietu"""
    package = PACKAGES.get(package_name.lower())
    if not package:
        return None
    
    description = f"**{package['name']}** ({package['price_range']})\n\n"
    description += f"{package['description']}\n\n"
    description += "**Co zawiera:**\n"
    for feature in package['features']:
        description += f"• {feature}\n"
    description += f"\n**Dla kogo:** {package['ideal_for']}"
    
    return description

def get_all_packages_summary():
    """Zwraca podsumowanie wszystkich pakietów"""
    summary = "Oferujemy 3 pakiety wykończeniowe:\n\n"
    for key, package in PACKAGES.items():
        summary += f"**{package['name']}** - {package['description']}\n"
    return summary

QUALIFICATION_QUESTIONS = [
    {
        "id": 1,
        "question": "Jaki jest metraż Twojego mieszkania?",
        "type": "number",
        "weight": 10,
        "scoring": {
            "0-40": {"points": 5, "package": "standard"},
            "41-70": {"points": 10, "package": "premium"},
            "71+": {"points": 15, "package": "luxury"}
        }
    },
    {
        "id": 2,
        "question": "Jaki jest Twój budżet na wykończenie (PLN)?",
        "type": "range",
        "weight": 20,
        "scoring": {
            "0-100000": {"points": 5, "package": "standard"},
            "100001-200000": {"points": 10, "package": "premium"},
            "200001+": {"points": 15, "package": "luxury"}
        }
    },
    {
        "id": 3,
        "question": "Czy zależy Ci na szybkim terminie realizacji?",
        "type": "boolean",
        "weight": 5,
        "scoring": {
            "tak": {"points": 5, "package": "standard"},
            "nie": {"points": 10, "package": "premium"}
        }
    },
    {
        "id": 4,
        "question": "Jakie materiały Cię interesują?",
        "type": "choice",
        "options": ["Podstawowe", "Średniej jakości", "Premium", "Luksusowe"],
        "weight": 15,
        "scoring": {
            "Podstawowe": {"points": 5, "package": "standard"},
            "Średniej jakości": {"points": 8, "package": "standard"},
            "Premium": {"points": 12, "package": "premium"},
            "Luksusowe": {"points": 15, "package": "luxury"}
        }
    },
    {
        "id": 5,
        "question": "Czy planujesz automatykę domową (smart home)?",
        "type": "boolean",
        "weight": 10,
        "scoring": {
            "tak": {"points": 10, "package": "premium"},
            "nie": {"points": 5, "package": "standard"}
        }
    },
    {
        "id": 6,
        "question": "Czy potrzebujesz indywidualnego projektu wnętrz?",
        "type": "boolean",
        "weight": 15,
        "scoring": {
            "tak": {"points": 15, "package": "luxury"},
            "nie": {"points": 5, "package": "standard"}
        }
    },
    {
        "id": 7,
        "question": "Jakie są Twoje priorytety?",
        "type": "choice",
        "options": ["Cena", "Jakość", "Czas realizacji", "Ekskluzywność"],
        "weight": 15,
        "scoring": {
            "Cena": {"points": 5, "package": "standard"},
            "Jakość": {"points": 10, "package": "premium"},
            "Czas realizacji": {"points": 8, "package": "standard"},
            "Ekskluzywność": {"points": 15, "package": "luxury"}
        }
    }
]
