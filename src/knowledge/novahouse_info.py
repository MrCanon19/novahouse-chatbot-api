"""
NovaHouse - Baza Wiedzy o Pakietach Wykończeniowych
"""

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
    "jak_dlugo_trwa": "Standardowo wykończenie mieszkania 50-60m2 trwa od 6 do 12 tygodni, w zależności od wybranego pakietu i zakresu prac.",
    "czy_wlaczone_materialy": "Tak, nasze pakiety są kompleksowe i zawierają zarówno robociznę jak i wszystkie niezbędne materiały.",
    "mozna_dostosowac": "Oczywiście! Wszystkie pakiety są elastyczne. Możesz wymienić materiały, dodać dodatkowe elementy lub zmienić zakres prac.",
    "gwarancja": "Tak, udzielamy 2-letniej gwarancji na wykonane prace oraz zgodnie z gwarancją producenta na materiały.",
    "platnosc": "Płatność realizowana jest etapami - zaliczka 30%, kolejne transze po zakończeniu poszczególnych etapów prac, końcowe 10% po odbiorze."
}

COMPANY_INFO = """
NovaHouse to firma specjalizująca się w kompleksowym wykończeniu mieszkań i domów.
Oferujemy trzy pakiety wykończeniowe: Standard, Premium i Luxury.

Nasze atuty:
- Kompleksowa obsługa od A do Z
- Doświadczony zespół fachowców
- Materiały najwyższej jakości
- Terminowość i rzetelność
- 2 lata gwarancji na wykonane prace
- Elastyczne formy płatności

Kontakt:
Email: kontakt@novahouse.pl
Telefon: +48 123 456 789
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
