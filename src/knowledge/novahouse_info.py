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
    "address": "Trójmiasto, Warszawa, Wrocław",
    "nip": "Dostępna na wniosek",
    "social_media": {
        "instagram": "https://www.instagram.com/novahouse.pl/",
        "facebook": "https://www.facebook.com/novahousepl/",
        "youtube": "https://www.youtube.com/channel/UCotFF-zwnvI-k2A4yaF01DQ"
    }
}

# Obszary działania
COVERAGE_AREAS = {
    "primary": ["Trójmiasto (Gdańsk, Sopot, Gdynia)", "Warszawa", "Wrocław"],
    "description": "Działamy na terenie trzech największych aglomeracji w Polsce"
}

# Liczby pokazujące skalę działalności
COMPANY_STATS = {
    "completed_projects": "30+",
    "satisfied_clients": "95%",
    "projects_before_deadline": "94%",
    "warranty_years": 3,  # 36 miesięcy
    "min_project_duration": "1.5 miesiąca"
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
    "jak_dlugo_trwa": "Realizacja już od 1,5 miesiąca! Wykończenie mieszkania 50-60m² trwa zwykle od 6 tygodni, w zależności od pakietu i zakresu prac. 94% naszych projektów kończymy przed terminem!",
    "czy_wlaczone_materialy": "Tak, nasze pakiety zawierają zarówno robociznę jak i wszystkie materiały potrzebne do realizacji prac. Otrzymasz też personalizowaną listę zakupów dopasowaną do Twoich preferencji.",
    "mozna_dostosowac": "Zdecydowanie! Wszystkie pakiety są w pełni elastyczne. Każdy z naszych pakietów oraz elementy kosztorysu możesz modyfikować zgodnie z Twoimi potrzebami. Możesz wymienić materiały, dodać dodatkowe usługi lub zmienić zakres prac.",
    "gwarancja": "Udzielamy 36-miesięcznej (3-letniej) gwarancji od momentu odbioru na wykonane prace. To jeden z najdłuższych okresów gwarancji na rynku! Na materiały obowiązuje gwarancja producenta.",
    "platnosc": "Płatności realizujemy etapowo: zaliczka przy podpisaniu umowy, kolejne transze po ukończeniu poszczególnych etapów, końcowa płatność po odbiorze prac. Oferujemy przejrzyste wyceny dostosowane do Twojego budżetu.",
    "ile_kosztuje": "Ceny zaczynają się od 949 zł/m² (pakiet Standard) do 1990 zł/m² (pakiet Luxury). Wycena indywidualna jest bezpłatna. Oferujemy cennik dodatkowych prac - wszystko jasno, uczciwie, bez zaskoczeń.",
    "produkty": "Współpracujemy z najlepszymi producentami: Laufen, Geberit, Kaldewei, Hansgrohe, Grohe, Roca, Tubadzin, Paradyż, Mapei, Quick-Step, Deante, Ferro, Cersanit i wiele innych. W zależności od pakietu oferujemy różne opcje — od standardowych do luksusowych marek.",
    "etapy": "Współpraca przebiega w 4 etapach: 1) Wybór pakietu lub projektu indywidualnego + wycena, 2) Projektowanie z projektantem (zdalne lub w biurze) + 2-3 propozycje układów funkcjonalnych, 3) Wykończenie pod klucz + nadzór (zajmujemy się wszystkim!), 4) Finalizacja i odbiór lokalu (mieszkanie czyste i gotowe do zamieszkania).",
    "czy_potrzebny_projekt": "Dla pełnego zakresu prac rekomendujemy projekt indywidualny. Spotkanie aranżacyjne może być zdalne lub w naszym biurze. Przygotujemy 2-3 propozycje układów funkcjonalnych, precyzyjną listę zakupów i projekt wykonawczy.",
    "smart_home": "Smart home jest dostępna w pakiecie Premium i Luxury. Możesz wybrać automatykę oświetlenia, temperatury lub bezpieczeństwa.",
    "terminowosc": "Terminowość to nasz standard i obietnica! Każdy etap prac realizujemy zgodnie z ustalonym harmonogramem. 94% naszych zleceń oddajemy przed terminem. Dzięki sprawdzonemu systemowi zarządzania projektami masz pewność realizacji na czas.",
    "ekipy": "Współpracujemy wyłącznie ze sprawdzonymi ekipami wykończeniowymi, które znamy od lat i z którymi zrealizowaliśmy dziesiątki udanych projektów. To fachowcy, którym ufamy - rzetelni, terminowi i dbający o detale.",
    "zakres_uslug": "Oferujemy kompleksową usługę pod klucz: projekt i koncepcja, zakupy i logistyka, koordynacja i nadzór, prace wykończeniowe, zabudowy stolarskie (kuchnie, szafy, meble na wymiar), ostateczne dopracowanie i sprzątanie.",
    "co_obejmuje_usluga": "Zajmujemy się WSZYSTKIM: od projektu przez zakupy materiałów, koordynację prac, prace wykończeniowe, zabudowy stolarskie, aż po finalne sprzątanie. Ty cieszysz się gotowym wnętrzem!",
    "zabudowy_stolarskie": "Tworzymy zabudowy stolarskie na wymiar: kompleksowo - od projektu przez produkcję do montażu. Korzystamy z najwyższej jakości materiałów dla trwałości i funkcjonalności. Oferujemy przejrzyste wyceny dostosowane do Twojego budżetu.",
    "gdzie_dzialamy": "Działamy na terenie Trójmiasta (Gdańsk, Sopot, Gdynia), Warszawy oraz Wrocławia.",
    "cennik_dodatkowy": "Mamy oficjalny cennik dodatkowych prac - wszystko jasno, uczciwie, bez zaskoczeń. Każda dodatkowa usługa ma swój jasno określony koszt zapisany czarno na białym. Zero niedomówień.",
    "po_odbiorze": "Po zakończeniu prac Twoje mieszkanie będzie idealnie czyste i gotowe do natychmiastowego zamieszkania. Dodatkowo zapewniamy 36-miesięczną gwarancję od momentu odbioru.",
}

COMPANY_INFO = """
NovaHouse to profesjonalna firma specjalizująca się w kompleksowym wykończeniu wnętrz pod klucz.

📊 O NAS:
Tworzymy wnętrza, które są gotowe do zamieszkania. Od projektu po efekt końcowy – zajmujemy się wszystkim, abyś nie musiał się o nic martwić. Działamy na terenie Trójmiasta (Gdańsk, Sopot, Gdynia), Warszawy oraz Wrocławia.

� NASZE WYNIKI:
• 30+ zrealizowanych projektów
• 95% zadowolonych klientów
• 94% zleceń oddanych przed terminem
• 36 miesięcy gwarancji
• Realizacja od 1,5 miesiąca

✨ DLACZEGO MY?

🎯 Terminowość to nasza obietnica
Terminowość to nasz standard. Z nami nie musisz martwić się o opóźnienia czy niedotrzymane terminy. Każdy etap prac realizujemy zgodnie z ustalonym harmonogramem. Dzięki sprawdzonemu systemowi zarządzania projektami oraz zgranemu zespołowi specjalistów masz pewność, że wszystko zostanie wykonane na czas.

👷 Zaufane ekipy wykończeniowe
Współpracujemy wyłącznie ze sprawdzonymi ekipami, które znamy od lat i z którymi zrealizowaliśmy dziesiątki udanych projektów. To fachowcy, którym ufamy na każdym etapie prac – za ich rzetelność, terminowość i dbałość o detale.

💰 Cennik dodatkowych prac – jasno, uczciwie, bez zaskoczeń
U nas nie ma miejsca na domysły. Każda dodatkowa usługa ma swój jasno określony koszt – zapisany w oficjalnym cenniku. Dzięki temu wiesz dokładnie, za co płacisz i możesz podejmować decyzje z pełnym spokojem. Zero niedomówień. Wszystko czarno na białym.

⚡ Zespół, który działa za Ciebie – szybciej, sprawniej
Naszym celem jest nie tylko dotrzymanie terminu, ale realizacja prac przed czasem. Każdy projekt to współpraca całego zespołu – od projektanta po logistyka – który przejmuje za Ciebie wszystkie obowiązki. Na bieżąco otrzymujesz raporty z postępu prac i zdjęcia, więc masz pełną kontrolę bez wychodzenia z domu.

🔧 CO ROBIMY:
✔ Projekt i koncepcja – Tworzymy dopracowany projekt dopasowany do Twoich potrzeb
✔ Zakupy i logistyka – Organizujemy wszystkie materiały i elementy wyposażenia
✔ Koordynacja i nadzór – Kontrolujemy harmonogram, jakość wykonania i postęp prac
✔ Prace wykończeniowe – Kompleksowe remonty, montaż podłóg, drzwi, malowanie
✔ Zabudowy stolarskie – Kuchnie, szafy, meble na wymiar – idealnie dopasowane
✔ Ostateczne dopracowanie – Sprzątanie i przygotowanie wnętrza do użytkowania

📞 KONTAKT:
Telefon: +48 585 004 663
Email: kontakt@novahouse.pl
Strona: https://novahouse.pl
Instagram: @novahouse.pl
Facebook: /novahousepl
YouTube: NovaHouse

🕐 GODZINY PRACY:
Poniedziałek - Piątek: 09:00 - 17:00
Sobota: 10:00 - 14:00
Niedziela: zamknięte

💰 CENY ORIENTACYJNIE:
Wykończenie od 949 zł/m² do 1990 zł/m² (w zależności od pakietu i zakresu prac).
Realizacja już od 1,5 miesiąca – bez zbędnej zwłoki, z jasnym harmonogramem prac.

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
        "question": "Jaki jest typ Twojej nieruchomości?",
        "type": "choice",
        "options": ["Mieszkanie", "Dom", "Apartamentowiec", "Powierzchnia komercyjna"],
        "weight": 8,
        "data_field": "property_type",
        "scoring": {
            "Mieszkanie": {"points": 5, "package": "standard"},
            "Dom": {"points": 10, "package": "premium"},
            "Apartamentowiec": {"points": 8, "package": "premium"},
            "Powierzchnia komercyjna": {"points": 12, "package": "luxury"}
        }
    },
    {
        "id": 6,
        "question": "Jaki styl wnętrz Ciebie przyciąga?",
        "type": "choice",
        "options": ["Minimalistyczny", "Nowoczesny", "Klasyczny", "Industrial", "Skandynawski"],
        "weight": 7,
        "data_field": "interior_style",
        "scoring": {
            "Minimalistyczny": {"points": 8, "package": "premium"},
            "Nowoczesny": {"points": 10, "package": "premium"},
            "Klasyczny": {"points": 6, "package": "standard"},
            "Industrial": {"points": 10, "package": "premium"},
            "Skandynawski": {"points": 9, "package": "premium"}
        }
    },
    {
        "id": 7,
        "question": "Czy chcesz integrację smart home?",
        "type": "boolean",
        "weight": 12,
        "scoring": {
            "tak": {"points": 15, "package": "luxury"},
            "nie": {"points": 5, "package": "standard"}
        }
    },
    {
        "id": 8,
        "question": "Czy jesteś zainteresowany konsultacją z naszym designerem?",
        "type": "boolean",
        "weight": 5,
        "scoring": {
            "tak": {"points": 10, "package": "premium"},
            "nie": {"points": 3, "package": "standard"}
        }
    }
]

# Partnerzy produktowi
PRODUCT_PARTNERS = [
    "Laufen", "Geberit", "Kaldewei", "Erkado", "Tubadzin", "Hansgrohe", 
    "DRE", "Roca", "Elita", "Porta", "Paradyż", "Mapei", "KFA", 
    "Quick-Step", "Deante", "Ferro", "Cersanit"
]

# Proces realizacji krok po kroku
PROCESS_STEPS = {
    "krok_1": {
        "title": "Wybór pakietu lub projektu indywidualnego",
        "description": "Oferujemy cztery różnorodne pakiety wykończeniowe lub możliwość stworzenia projektu dostosowanego do Twoich potrzeb. Po otrzymaniu informacji o metrażu skontaktujemy się, aby umówić się na spotkanie, na którym przygotujemy szczegółową wycenę zgodnie z Twoimi preferencjami i wymaganiami.",
        "duration": "1 spotkanie",
        "deliverables": ["Szczegółowa wycena", "Dobór pakietu", "Ustalenie zakresu prac"]
    },
    "krok_2": {
        "title": "Projektowanie z Projektantem",
        "description": "Spotkanie aranżacyjne dopasujemy do Twojej wygody – może odbyć się zdalnie lub w naszym biurze. Każdy z naszych pakietów oraz elementy kosztorysu są w pełni elastyczne, co daje Ci swobodę modyfikacji zgodnie z Twoimi potrzebami. Przygotujemy dla Ciebie 2-3 propozycje układów funkcjonalnych do wyboru, na podstawie których stworzymy precyzyjną listę zakupów oraz projekt wykonawczy.",
        "duration": "1-2 tygodnie",
        "deliverables": ["2-3 propozycje układów funkcjonalnych", "Precyzyjna lista zakupów", "Projekt wykonawczy"]
    },
    "krok_3": {
        "title": "Usługa wykończenia pod klucz + Nadzór",
        "description": "Z naszą usługą wykończeniową i nadzorem możesz cieszyć się spokojem i zająć się swoimi sprawami – Projektant zajmie się wszystkim za Ciebie! Od zarządzania całym przebiegiem prac, przez organizację zamówień i montaż zabudów stolarskich, aż po finalną kontrolę jakości. Dzięki temu masz pewność, że efekt końcowy będzie zgodny z Twoimi oczekiwaniami.",
        "duration": "Od 1,5 miesiąca",
        "deliverables": ["Raporty z postępu prac", "Zdjęcia na bieżąco", "Pełna koordynacja"]
    },
    "krok_4": {
        "title": "Finalizacja zlecenia i odbiór lokalu",
        "description": "Po zakończeniu prac Twoje mieszkanie będzie idealnie czyste i gotowe do natychmiastowego zamieszkania. Dodatkowo, zapewniamy Ci 36-miesięczną gwarancję od momentu odbioru, co daje Ci pełen komfort i poczucie bezpieczeństwa.",
        "duration": "1 dzień",
        "deliverables": ["Czyste mieszkanie gotowe do zamieszkania", "36-miesięczna gwarancja", "Dokumentacja odbiorcza"]
    }
}

# Portfolio - przykładowe realizacje
PORTFOLIO = {
    "realizacja_1": {
        "title": "Mieszkanie – 100 m²",
        "type": "Projekt indywidualny",
        "location": "Nie określono",
        "url": "https://novahouse.pl/realizacje/mieszkanie-100-m2-projekt-indywidualny/"
    },
    "realizacja_2": {
        "title": "Mieszkanie – 3 pokoje 60m²",
        "type": "Projekt indywidualny",
        "location": "Sopot, ul. Okrzei",
        "url": "https://novahouse.pl/realizacje/sopot-okrzei/"
    },
    "realizacja_3": {
        "title": "Dom – 6 pokoi 165m²",
        "type": "Projekt indywidualny",
        "location": "Małkowo",
        "url": "https://novahouse.pl/realizacje/malkowo-dom/"
    },
    "realizacja_4": {
        "title": "Dom – 6 pokoi 150m²",
        "type": "Projekt indywidualny",
        "location": "Nie określono",
        "url": "https://novahouse.pl/realizacje/dom-150-m2/"
    }
}

# Blog i materiały edukacyjne
BLOG_ARTICLES = [
    {
        "title": "Architekt Wnętrz – Kim Jest i Dlaczego Warto Zatrudnić Profesjonalistę?",
        "url": "https://novahouse.pl/architekt-wnetrz-kim-jest-i-dlaczego-warto-zatrudnic-profesjonaliste/"
    },
    {
        "title": "Kuchnia modułowa czy na wymiar? Kompleksowy przewodnik",
        "url": "https://novahouse.pl/kuchnia-modulowa-czy-na-wymiar-kompleksowy-przewodnik-dla-osob-urzadzajacych-wymarzona-kuchnie/"
    },
    {
        "title": "Aranżacja wnętrz z NovaHouse – Twój styl w każdym detalu",
        "url": "https://novahouse.pl/aranzacja-wnetrz-z-novahouse-twoj-styl-w-kazdym-detalu/"
    },
    {
        "title": "Gotowe mieszkania z NovaHouse – oszczędź czas i zamieszkaj od zaraz",
        "url": "https://novahouse.pl/gotowe-mieszkania-nowoczesne-rozwiazania-dla-twojego-komfortu/"
    },
    {
        "title": "Planowanie Remontu Domu – Kluczowe Kwestie do Rozważenia",
        "url": "https://novahouse.pl/planowanie-remontu-domu-kluczowe-kwestie-do-rozwazenia/"
    },
    {
        "title": "Projektant wnętrz – Jakiego wybrać?",
        "url": "https://novahouse.pl/projektant-wnetrz-jakiego-wybrac/"
    }
]

# Zespół
TEAM_INFO = {
    "wiceprezes": {
        "name": "Agnieszka Kubiak",
        "position": "Wiceprezes",
        "quote": "Wiem, jak wiele decyzji trzeba podjąć podczas urządzania mieszkania – dlatego postanowiliśmy ułatwić Ci ten proces. Przygotowaliśmy dla Ciebie starannie wyselekcjonowane katalogi produktów. To nie jest przypadkowy zbiór – to efekt wieloletniej współpracy z naszymi klientami.",
        "responsibility": "Nadzór nad projektami i wsparcie klientów"
    },
    "projektanci": {
        "count": "Zespół doświadczonych projektantów",
        "role": "Projektowanie wnętrz, dobór materiałów, koordynacja z klientem",
        "note": "Każdy klient ma przypisanego dedykowanego projektanta"
    }
}

# Opinie klientów z Google
CLIENT_REVIEWS = [
    {
        "author": "Alex Szymczak",
        "rating": 5,
        "time": "4 tygodnie temu",
        "text": "Skorzystałem z usługi wykończenia pod klucz. Kontakt jest z jedną osobą, wyznaczoną projektantką, która projektuje i koordynuje prace. Mieszkanie było..."
    },
    {
        "author": "Magda Nowak",
        "rating": 5,
        "time": "4 tygodnie temu",
        "text": "Wiele czynników sprawiło że zdecydowaliśmy się na Novahouse. Wywiązali się wzorowo z umowy. Jakość zabudowy stolarskiej bardzo dobra, gładzie i..."
    },
    {
        "author": "Krzysztof Skutnik",
        "rating": 5,
        "time": "4 tygodnie temu",
        "text": "Wykonywaliśmy wykończenie mieszkania wraz z NovaHouse. Otrzymaliśmy sporo praktycznych rozwiązań już na etapie projektowania. Z odrobiną cierpliwości i współpracy udało..."
    },
    {
        "author": "Joanna Drewek",
        "rating": 5,
        "time": "tydzień temu",
        "text": "Jestem zadowolona z projektów zaproponowanych przez projektanta pana Michała. Wykazał się profesjonalizmem i, co bardzo ważne, cierpliwością przy ustalaniu różnych..."
    },
    {
        "author": "Beata Werner",
        "rating": 5,
        "time": "3 tygodnie temu",
        "text": "Firma NovaHouse bardzo dobrze zaprojektowała moje nowe mieszkanie, wszystkie meble a także pomogła stworzyć w moim domu styl prowansalski. Bardzo..."
    }
]

# USP - Unique Selling Points
WHY_CHOOSE_US = {
    "kompleksowo": "Kompleksowo – od projektu, przez produkcję, aż po montaż. Nie musisz koordynować pracy różnych ekip – wszystko załatwiamy za Ciebie.",
    "gwarancja": "Gwarancja jakości i trwałości: Korzystamy z najwyższej jakości materiałów, dzięki czemu nasze zabudowy są funkcjonalne i trwałe przez lata.",
    "budzet": "Pełna kontrola nad budżetem: Oferujemy przejrzyste wyceny, dostosowane do budżetu, który planujesz przeznaczyć. Dzięki temu dokładnie wiesz, za co płacisz.",
    "terminowosc": "94% projektów oddanych przed terminem - to nasza obietnica i standard pracy.",
    "ekipy": "Sprawdzone ekipy wykończeniowe znane od lat - rzetelne, terminowe, dbające o każdy detal.",
    "raporty": "Raporty i zdjęcia na bieżąco - pełna kontrola bez wychodzenia z domu.",
    "sprzatanie": "Mieszkanie gotowe do zamieszkania - idealna czystość po zakończeniu prac."
}

# Materiały i katalogi
MATERIALS_INFO = """
Przygotowaliśmy dla Ciebie starannie wyselekcjonowane katalogi produktów. To nie jest przypadkowy zbiór – to efekt wieloletniej współpracy z naszymi klientami.

W katalogach znajdziesz tylko te materiały i rozwiązania, które najczęściej wybierali – sprawdzone, estetyczne i funkcjonalne. Usunęliśmy produkty egzotyczne, które nie budziły zainteresowania.

Dzięki temu oszczędzasz swój czas – eliminujemy chaos i skupiamy się na tym, co naprawdę się sprawdza. Twój wybór staje się prostszy, a efekt końcowy – przewidywalnie dobry.
"""

def get_process_overview():
    """Zwraca przegląd procesu realizacji"""
    overview = "🔧 PROCES REALIZACJI - 4 KROKI:\n\n"
    for key, step in PROCESS_STEPS.items():
        overview += f"**{step['title']}** ({step['duration']})\n"
        overview += f"{step['description']}\n\n"
    return overview

def get_portfolio_list():
    """Zwraca listę realizacji"""
    portfolio_text = "📸 NASZE REALIZACJE:\n\n"
    for key, project in PORTFOLIO.items():
        portfolio_text += f"• {project['title']} - {project['type']}\n"
        if project['location'] != "Nie określono":
            portfolio_text += f"  Lokalizacja: {project['location']}\n"
        portfolio_text += f"  Więcej: {project['url']}\n\n"
    return portfolio_text

def get_client_reviews_summary():
    """Zwraca podsumowanie opinii klientów"""
    reviews_text = "⭐ CO MÓWIĄ KLIENCI:\n\n"
    for review in CLIENT_REVIEWS[:3]:  # Top 3 reviews
        reviews_text += f"**{review['author']}** ({review['time']})\n"
        reviews_text += f"⭐⭐⭐⭐⭐ {review['text']}\n\n"
    reviews_text += "\nWięcej opinii: https://maps.google.com/?cid=15887695859047735593\n"
    return reviews_text
