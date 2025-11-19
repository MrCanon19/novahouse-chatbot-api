"""
NovaHouse - Baza Wiedzy o Pakietach Wykończeniowych
"""

# flake8: noqa

# Godziny pracy
BUSINESS_HOURS = {
    "monday_friday": "09:00 - 17:00",
    "saturday": "10:00 - 14:00",
    "sunday": "zamknięte",
    "timezone": "CET",
}

# Informacje kontaktowe
CONTACT_INFO = {
    "company_name": "NovaHouse Sp. z o.o.",
    "phone_main": "+48 585 004 663",
    "phone_logistics": "+48 509 929 437",
    "phone_finance": "+48 607 518 544",
    "email_main": "kontakt@novahouse.pl",
    "email_partners": "partnerzy@novahouse.pl",
    "website": "https://novahouse.pl",
    "offices": {
        "gdansk": "ul. Pałubickiego 2, budynek C2-parter, Gdańsk",
        "warszawa": "ul. Prosta 70, 5 piętro, Warszawa",
        "wroclaw": "ul. Sucha 3, Wrocław",
    },
    "registration": {
        "krs": "0000612864",
        "nip": "5833201699",
        "regon": "364323586",
        "share_capital": "100.000,00 PLN",
    },
    "social_media": {
        "instagram": "https://www.instagram.com/novahouse.pl/",
        "facebook": "https://www.facebook.com/novahousepl/",
        "youtube": "https://www.youtube.com/channel/UCotFF-zwnvI-k2A4yaF01DQ",
    },
}

# Obszary działania
COVERAGE_AREAS = {
    "primary": ["Trójmiasto (Gdańsk, Sopot, Gdynia)", "Warszawa", "Wrocław"],
    "description": ("Działamy na terenie trzech największych aglomeracji w Polsce"),
}

# Katalogi produktów
PRODUCT_CATALOGS = {
    "catalog_1": {
        "name": "Katalog 1 - Basic",
        "standard": "Basic",
        "products_count": "150 produktów",
        "packages": ["Express"],
        "availability": "od ręki",
        "description": ("Podstawowy katalog z sprawdzonymi produktami " "dostępnymi od ręki"),
    },
    "catalog_2": {
        "name": "Katalog 2 - Standard",
        "standard": "Standard",
        "products_count": "300 produktów",
        "packages": ["Express Plus"],
        "availability": "od ręki",
        "description": (
            "Rozszerzony katalog z większym wyborem kolorów, " "materiałów i personalizacji"
        ),
    },
    "catalog_3": {
        "name": "Katalog 3 - Premium",
        "standard": "Premium",
        "products_count": "450 produktów",
        "packages": ["Comfort", "Premium"],
        "availability": "na zamówienie",
        "description": ("Najwyższej jakości produkty, nowoczesne kolekcje, " "światowe marki"),
    },
}

# Liczby pokazujące skalę działalności
COMPANY_STATS = {
    "years_in_business": "od 2011 roku",
    "completed_projects": "350+",
    "satisfied_clients": "96%",
    "projects_before_deadline": "94%",
    "warranty_years": 3,  # 36 miesięcy
    "warranty_months": 36,
    "min_project_duration": "1.5 miesiąca",
    "supplier_partners": "120+",
    "material_discount": "15%",
}

PACKAGES = {
    "express": {
        "name": "Pakiet Express",
        "price_per_sqm": "od 999 zł/m²",
        "catalog_number": "Katalog 1 (Basic)",
        "design_time": "do 10 dni",
        "execution_time": "6-8 tygodni",
        "product_availability": "od ręki",
        "standard": "Basic",
        "product_choices": "150 produktów",
        "product_changes_limit": "2 produkty",
        "outside_catalog_products": "nie",
        "meetings_with_designer": "1",
        "description": (
            "Dla tych, którzy chcą szybko zamieszkać lub wynająć "
            "i cenią wygodę bez zbędnych formalności. Idealny dla "
            "inwestorów i osób szukających sprawdzonych, prostych "
            "rozwiązań."
        ),
        "features": [
            "Projekt wykonawczy + moodboard",
            "Zaufana i sprawdzona ekipa wykończeniowa",
            "Rabat 15% na wszystkie materiały",
            "Materiały budowlane (farby, kleje, fugi itp)",
            "Aranżacja wnętrza z projektantem",
            "Lista zakupowa + zestawienie produktów - moodboard",
            "Koordynacja prac i zamówień",
            "Odbiór lokalu przez inspektora budowlanego + Raport z oględzin",
            "Usługa wykończenia (malowanie, montaż drzwi, położenie podłogi, łazienka kompleksowo)",
            "Gwarancja na usługi: 3 lata",
        ],
        "bathroom": (
            "płytki do wysokości 210 cm, WC podwieszane, umywalka "
            "z szafką podwieszaną, wanna lub kabina z brodzikiem, "
            "lustro wklejane do 1m², oświetlenie 1 punkt, "
            "płytki 30x60cm i 60x60cm, baterie nadtynkowe"
        ),
        "floors": "panele laminowane, listwy",
        "doors": "skrzydła drzwiowe przylgowe, ościeżnice, klamki",
        "walls": "malowanie ścian na wybrany kolor",
        "lighting": "Dobór oświetlenia",
        "ideal_for": ("Inwestorzy i osoby szukające szybkich, " "sprawdzonych rozwiązań"),
        "personalization_before_contract": "nie",
        "visualization": "nie",
    },
    "express_plus": {
        "name": "Pakiet Express Plus",
        "price_per_sqm": "od 1199 zł/m²",
        "catalog_number": "Katalog 2 (Standard)",
        "design_time": "do 20 dni",
        "execution_time": "6-8 tygodni",
        "product_availability": "od ręki",
        "standard": "Standard",
        "product_choices": "300 produktów",
        "product_changes_limit": "3 produkty",
        "outside_catalog_products": "1 produkt od ręki",
        "meetings_with_designer": "2",
        "description": (
            "Dla osób, które chcą więcej – więcej kolorów, "
            "materiałów i personalizacji. Świetny wybór dla rodzin "
            "oraz tych, którzy lubią mieć wpływ na wygląd swojego "
            "wnętrza."
        ),
        "features": [
            "Projekt wykonawczy + moodboard",
            "Zaufana i sprawdzona ekipa wykończeniowa",
            "Rabat 15% na wszystkie materiały",
            "Materiały budowlane (farby, kleje, fugi itp)",
            "Aranżacja wnętrza z projektantem",
            "Lista zakupowa + zestawienie produktów - moodboard",
            "Koordynacja prac i zamówień",
            "Odbiór lokalu przez inspektora budowlanego + Raport z oględzin",
            (
                "Usługa wykończenia (malowanie, montaż drzwi, "
                "położenie podłogi, łazienka kompleksowo)"
            ),
            "Gwarancja na usługi: 3 lata",
        ],
        "bathroom": (
            "płytki do wysokości 270 cm + płytki dekoracyjne, "
            "WC podwieszane, umywalka, lustro wklejane do 1,5 m², "
            "wanna lub kabina z brodzikiem lub typu walk-in, "
            "oświetlenie 2 punkty, płytki 60x60cm, 60x120cm, "
            "baterie nadtynkowe"
        ),
        "floors": "panele laminowane lub winylowe, listwy",
        "doors": ("skrzydła drzwiowe przylgowe lub bezprzylgowe, " "ościeżnice, klamki"),
        "walls": "malowanie ścian na wybrany kolor",
        "lighting": "Dobór oświetlenia",
        "ideal_for": ("Rodziny i osoby, które chcą mieć wpływ na wygląd " "swojego wnętrza"),
        "personalization_before_contract": "nie",
        "visualization": "nie",
    },
    "comfort": {
        "name": "Pakiet Comfort / Szafran",
        "price_per_sqm": "od 1499 zł/m²",
        "catalog_number": "Katalog 3 (Premium)",
        "design_time": "do 4 tygodni",
        "execution_time": "8-12 tygodni",
        "product_availability": "na zamówienie",
        "standard": "Premium",
        "product_choices": "450 produktów",
        "product_changes_limit": "5 produktów",
        "outside_catalog_products": "3 produkty",
        "meetings_with_designer": "3",
        "description": (
            "Dla wymagających, którzy oczekują wysokiej jakości, "
            "nowoczesnych kolekcji i większej swobody w wyborze. "
            "Doskonały dla osób szukających wyjątkowego designu "
            "i indywidualnego podejścia."
        ),
        "features": [
            "Projekt wykonawczy + moodboard",
            "Personalizacja przed podpisaniem umowy",
            "Wizualizacja wnętrza: łazienka, kuchnia",
            "Zaufana i sprawdzona ekipa wykończeniowa",
            "Rabat 15% na wszystkie materiały",
            "Materiały budowlane (farby, kleje, fugi itp)",
            "Aranżacja wnętrza z projektantem",
            "Lista zakupowa + zestawienie produktów - moodboard",
            "Koordynacja prac i zamówień",
            "Odbiór lokalu przez inspektora budowlanego + Raport z oględzin",
            "Usługa wykończenia (malowanie, montaż drzwi, położenie podłogi, łazienka kompleksowo)",
            "Gwarancja na usługi: 3 lata",
        ],
        "bathroom": (
            "płytki do wysokości 270 cm + dekor + mozaika, "
            "lustro wklejane do 2 m² , umywalka, WC podwieszane, "
            "wanna lub kabina z brodzikiem konglomeratowym "
            "lub typu walk-in, oświetlenie 3 punkty, "
            "płytki 60x60cm, 80x80cm, 60x120cm, baterie podtynkowe"
        ),
        "floors": "panele laminowane, winylowe, deska barlinecka, listwy",
        "doors": ("skrzydła drzwiowe bezprzylgowe lub ukryte, " "ościeżnice, klamki"),
        "walls": "malowanie ścian na wybrany kolor",
        "lighting": "Dobór oświetlenia",
        "ideal_for": (
            "Osoby wymagające, szukające wyjątkowego designu " "i indywidualnego podejścia"
        ),
        "personalization_before_contract": "tak",
        "visualization": "łazienka, kuchnia",
    },
    "premium": {
        "name": "Pakiet Premium / Pomarańczowy / Cynamonowy",
        "price_per_sqm": "od 1999 zł/m²",
        "catalog_number": "Katalog Premium (Exclusive)",
        "design_time": "do 6 tygodni",
        "execution_time": "10-16 tygodni",
        "product_availability": "na zamówienie",
        "standard": "Exclusive",
        "product_choices": "600 produktów",
        "product_changes_limit": "7 produktów",
        "outside_catalog_products": "5 produktów",
        "meetings_with_designer": "4",
        "description": (
            "Najwyższy standard dla najbardziej wymagających. "
            "Luksusowe materiały, światowe marki i rozbudowana "
            "personalizacja. Idealny dla tych, którzy chcą stworzyć "
            "niepowtarzalne, prestiżowe wnętrze."
        ),
        "features": [
            "Projekt wykonawczy + moodboard",
            "Personalizacja przed podpisaniem umowy",
            "Wizualizacja wnętrza: łazienka, salon, kuchnia, hol",
            "Zaufana i sprawdzona ekipa wykończeniowa",
            "Rabat 15% na wszystkie materiały",
            "Materiały budowlane (farby, kleje, fugi itp)",
            "Aranżacja wnętrza z projektantem",
            "Lista zakupowa + zestawienie produktów - moodboard",
            "Koordynacja prac i zamówień",
            "Odbiór lokalu przez inspektora budowlanego + Raport z oględzin",
            (
                "Usługa wykończenia (malowanie, montaż drzwi, "
                "położenie podłogi, łazienka kompleksowo)"
            ),
            "Gwarancja na usługi: 3 lata",
        ],
        "bathroom": (
            "płytki do wysokości 270 cm + dekor + mozaika, "
            "lustro wklejane do 2 m² lub wieszane premium, umywalka, "
            "WC podwieszane, wanna wolnostojąca lub kabina "
            "z brodzikiem konglomeratowym lub typu walk-in, "
            "oświetlenie 4 punkty, 80x80cm, 60x120cm, 120x120cm, "
            "baterie podtynkowe"
        ),
        "floors": "podłoga drewniana, listwy",
        "doors": ("skrzydła drzwiowe bezprzylgowe lub ukryte " "lub przesuwane lub drewniane"),
        "walls": "malowanie ścian na wybrany kolor",
        "lighting": "Dobór oświetlenia",
        "ideal_for": (
            "Najbardziej wymagający klienci szukający prestiżowego, " "niepowtarzalnego wnętrza"
        ),
        "personalization_before_contract": "tak",
        "visualization": "łazienka, salon, kuchnia, hol",
        "catalog_status": "W TRAKCIE BUDOWY",
    },
    "individual": {
        "name": "Projekt Indywidualny",
        "price_per_sqm": "1700-5000 zł/m²",
        "catalog_number": "Bez ograniczeń katalogowych",
        "design_time": "6-10 tygodni",
        "execution_time": "indywidualnie dostosowany",
        "product_availability": "z całego rynku",
        "standard": "Premium + Indywidualny",
        "product_choices": "Bez ograniczeń - cały rynek",
        "product_changes_limit": "nieograniczone",
        "outside_catalog_products": "nieograniczone",
        "meetings_with_designer": "więcej niż 5",
        "description": ("Pełna personalizacja 1:1, najwyższa jakość " "bez kompromisów"),
        "features": [
            "Kompletny układ funkcjonalny dopasowany do Twojego życia",
            (
                "Pełna dokumentacja wykonawcza (elektryka, hydraulika, "
                "ściany, podłogi, drzwi, łazienki)"
            ),
            "Pełne wizualizacje 3D: łazienka, salon z kuchnią, hol, sypialnie",
            ("Indywidualny dobór materiałów - bez ograniczeń " "katalogowych, z całego rynku"),
            "Materiały w dowolnym przedziale cenowym - do premium",
            "Listy zakupowe i gotowe zestawienia produktów",
            "Stały kontakt i konsultacje z architektem (więcej godzin)",
            "Możliwość wyboru materiałów premium z Polski i Europy",
            "Architekt pracuje tylko dla Ciebie 1:1",
            "Brak ograniczeń katalogowych",
        ],
        "ideal_for": (
            "Klienci szukający całkowicie unikalnego wnętrza " "stworzonego specjalnie dla nich"
        ),
        "visualization": "Pełne wizualizacje 3D całego mieszkania",
        "bathroom": "Dowolne materiały i rozwiązania",
        "doors": "Dowolne według projektu",
    },
}

FAQ = {
    # Czas realizacji
    "jak_dlugo_trwa_calosc": "W przypadku pakietów Express i Express Plus: zazwyczaj od 7 do 10 tygodni – w zależności od pakietu, zakresu i metrażu. W przypadku pakietów Comfort i Premium: zazwyczaj od 12 do 18 tygodni – w zależności od pakietu, zakresu i metrażu. W przypadku projektu indywidualnego: zazwyczaj od 14 do 20 tygodni – w zależności od zakresu i metrażu. Projekt + realizacja to całość, którą prowadzimy od A do Z.",
    "kiedy_rozpoczecie_projektowanie": "Najczęściej w ciągu 1–2 tygodni od podpisania umowy – w tym czasie finalizujemy umowę i dobieramy odpowiedniego projektanta do Twoich potrzeb.",
    "jak_dlugo_trwa_projektowanie": "Standardowo: pakiet Express 1–2 tygodnie. Wyższe pakiety Comfort i Premium to 4-6 tygodni. Przy projektach indywidualnych może być dłużej 6-10 tygodni w zależności od metrażu, bo wszystko dopasowujemy pod Ciebie.",
    "ile_trwa_wykończenie": "W pakietach bazowych Express i Express Plus wykończenie trwa 6–8 tygodni. Przy większych metrażach lub nietypowych rozwiązaniach czas może się wydłużyć.",
    "kiedy_rozpoczecie_realizacje": "Najczęściej w ciągu 1–2 tygodni od zakończenia projektu – w tym czasie finalizujemy projekt, kosztorys i zamawiamy materiały.",
    # Proces
    "czy_musze_byc_obecny": "Nie 🙂. Nasz zespół prowadzi całość, a Ty dostajesz regularne raporty i zdjęcia. Możesz być w stałym kontakcie z Koordynatorem projektu.",
    "pomoc_z_odbiorem_dewelopera": "Tak, pomagamy w odbiorze technicznym i doradzamy przy zgłoszeniach – Nasz inżynier sprawdza mieszkanie i przedstawia raport z ewentualnymi usterkami.",
    "proces_krok_po_kroku": "1. Rozmowa telefoniczna o preferencjach → 2. Spotkanie ze specjalistą ds wykończeń wnętrz → 3. Opcjonalne 2 spotkanie z projektantem → 4. Podpisanie umowy → 5. Projektowanie → 6. Zakupy i logistyka → 7. Realizacja wykończenia i nadzór → 8. Montaż zabudów stolarskich → 9. Odbiór i gwarancja.",
    "wspolpraca_zdalna": "Tak. Realizujemy projekty w – Gdańsk, Warszawa, Wrocław oraz okolice do 60 km od Centrum. Dojeżdżamy i prowadzimy zdalne konsultacje.",
    # Pakiety - zakres i różnice
    "co_zawiera_pakiet": "Wspólny zakres dla wszystkich pakietów: Odbiór lokalu od dewelopera przez inspektora budowlanego, kompleksowe prace wykonawcze (malowanie, montaż podłóg, drzwi, pełne wykończenie łazienki: płytki, armatura, prysznic/wanna, WC, lustro, oświetlenie), materiały budowlane (kleje, farby, fugi, hydroizolacja), materiały wykończeniowe (podłogi, listwy, płytki, drzwi, klamki, armatura, ceramika), koordynacja zamówień materiałów i prac, sprzątanie pobudowlane, projekt pakietowy (układ funkcjonalny, rzuty wykonawcze, moodboardy, lista zakupowa, konsultacje z projektantem). Wyższe pakiety Comfort i Premium posiadają dodatkowo wizualizacje wybranych pomieszczeń.",
    "roznice_miedzy_pakietami": "Kluczowe różnice: 1) Standard produktów (Basic, Standard, Comfort, Premium, Indywidualny), 2) Liczba produktów do wyboru (od 150 do pełnego asortymentu 7 sklepów partnerskich), 3) Zakres wizualizacji (od podstawowych do pełnych wizualizacji całego mieszkania), 4) Liczba konsultacji z projektantem (od 1 do 5 spotkań), 5) Zakres wykończenia łazienki (wysokość płytek, wielkość płytek, ilość oświetlenia, typy baterii itp.), 6) Rodzaj podłóg (od laminatów, przez winylowe do drewnianych), 7) Rodzaj drzwi (od przylgowych przez bezprzylgowe do ukrytych), 8) Czas realizacji (od 6 do 16 tygodni).",
    "projekt_indywidualny_vs_pakiet": "Projekt indywidualny to pełna personalizacja 1:1, dobór produktów z całego rynku, materiały w dowolnym przedziale cenowym po premium, wizualizacje całego mieszkania, wydłużony czas prac projektanta na konsultacje, brak ograniczeń katalogowych. Cena: 1700–5000 zł/m² + zabudowy stolarskie. W skrócie: Pakiety = szybciej i taniej. Projekt Indywidualny = najwyższa personalizacja i architekt tylko dla Ciebie.",
    "zmiana_elementow_pakietu": "Tak. W pliku masz jasno określone limity zmian: Express: 2 zmiany produktów, Express Plus: 3 zmiany, Comfort/Szafran: 5 zmian, Premium/Pomarańczowy/Cynamonowy: 7 zmian. Wszystkie zmiany rozliczane są różnicą cenową danego produktu.",
    "laczenie_pakietow": "Tak. Każdy pakiet ma określony limit zmian między katalogami (2–7 zmian). Plus: dopłata za różnice cenowe oraz możliwość wyboru produktów z poza katalogu z 7 sklepów partnerskich.",
    # Ceny i rozliczenia
    "jak_liczycie_metry": "Metraż rozliczamy zawsze uczciwie i transparentnie — po powierzchni podłogi, bo tylko ona realnie wpływa na zakres prac i koszt materiałów. Klient od początku zna dokładny koszt, bez ukrytych dopłat.",
    "cena_pakietu_meble_oswietlenie": "Oświetlenie – nie (tylko dobór oświetlenia na bazie 12 popularnych producentów), Meble – NIE (podstawowe szafki łazienkowe w pakietach Express i Express Plus), Gładzenie ścian – nie ma tego w zakresie prac, jest tylko gruntowanie + malowanie (w pakietach nie ma gładzi). Jeśli klient potrzebuje gładzi lub mebli, czy oświetlenia – możemy to zrealizować jako prace dodatkowe.",
    "kuchnie_szafy": "Tak – oferujemy kuchnie na wymiar i szafy wnękowe realizowane przez naszych sprawdzonych stolarzy. Projektujemy, koordynujemy i montujemy zabudowy tak, aby pasowały do całego wnętrza.",
    "koszt_dla_metrazu": "Ceny naszych pakietów startują już od 999 zł/m² w wersji Express. Pakiet Express Plus to od 1199 zł/m², Comfort zaczyna się od 1499 zł/m², a Premium – od 1999 zł/m². Aby przygotować precyzyjną wycenę dla Twojego mieszkania, potrzebujemy krótkiego spotkania lub przesłania rzutu lokalu — wtedy przeliczamy ofertę co do metra.",
    "koszt_projekt_indywidualny": "Projekt Indywidualny to w pełni spersonalizowana usługa, w której architekt pracuje z Tobą 1:1 i tworzy wnętrze dokładnie pod Twój styl, potrzeby i budżet. Cena: 1700–5000 zł/m² (w zależności od standardu i złożoności). W ramach projektu otrzymujesz: kompletny układ funkcjonalny, pełną dokumentację wykonawczą, pełne wizualizacje 3D (łazienka, salon z kuchnią, hol, sypialnie), indywidualny dobór materiałów z całego rynku, listy zakupowe, stały kontakt z architektem, możliwość wyboru materiałów premium z Polski i Europy.",
    "dodatkowe_oplaty": "Tak: dopłaty za zmiany produktów (różnica cenowa), prace dodatkowe poza zakresem katalogu (gładzie, przeróbki hydrauliczne, elektryczne, zabudowy GK, meble na wymiar). Wszystko pokazujemy z góry i podpisujemy przed pracami, żeby klient nie miał żadnych niespodzianek na podstawie cennika.",
    "vat": "Wykończenia mieszkań do 150 m² = 8% VAT. Wykończenia domów do 300 m² = 8% VAT. Wszystkie nasze pakiety mają już wliczony korzystny VAT 8% – klient od razu wie, ile płaci.",
    "kosztorys": "Tak – przygotowujemy dokładną specyfikację prac oraz materiałów dla konkretnego mieszkania. Nic nie jest ukryte.",
    "platnosc_transze": "Tak – umożliwiamy wygodny system rozliczeń w kilku transzach.",
    "dodatkowe_prace_rozliczenie": "Każde dodatkowe prace wyceniamy na podstawie naszego cennika pisemnie przed wykonaniem. Zero niespodzianek i pełna kontrola kosztów.",
    # Katalogi i rabaty
    "ile_katalogow": "Mamy 3 katalogi produktów: Katalog 1 (Basic) - 150 produktów dla pakietu Express, Katalog 2 (Standard) - 300 produktów dla pakietu Express Plus, Katalog 3 (Premium) - 450 produktów dla pakietów Comfort i Premium. Produkty w katalogach Basic i Standard są dostępne od ręki, produkty Premium na zamówienie.",
    "rabat_na_materialy": "Tak! Wszyscy klienci otrzymują rabat 15% na wszystkie materiały. To jeden z benefitów współpracy z NovaHouse - dzięki naszym negocjacjom z dostawcami możesz zaoszczędzić na materiałach wysokiej jakości.",
    "wymiana_produktow_miedzy_katalogami": "Tak, możesz wymieniać produkty między katalogami w ramach limitów: Express - 2 produkty, Express Plus - 3 produkty, Comfort - 5 produktów, Premium - 7 produktów. Przy wymianie obowiązuje rozliczenie różnicy cenowej. Dodatkowo możesz wybierać produkty z poza katalogu ze sklepów partnerskich (Express Plus: 1 produkt, Comfort: 3 produkty, Premium: 5 produktów) z dopłatą wynikającą z różnicy ceny.",
    # Pozostałe
    "gwarancja": "Udzielamy 36-miesięcznej (3-letniej) gwarancji od momentu odbioru na wykonane prace. To jeden z najdłuższych okresów gwarancji na rynku! Na materiały obowiązuje gwarancja producenta.",
    "produkty": "Współpracujemy z najlepszymi producentami: Laufen, Geberit, Kaldewei, Hansgrohe, Grohe, Roca, Tubadzin, Paradyż, Mapei, Quick-Step, Deante, Ferro, Cersanit i wiele innych. W zależności od pakietu oferujemy różne opcje — od standardowych do luksusowych marek.",
    "terminowosc": "Terminowość to nasz standard i obietnica! Każdy etap prac realizujemy zgodnie z ustalonym harmonogramem. 94% naszych zleceń oddajemy przed terminem. Dzięki sprawdzonemu systemowi zarządzania projektami masz pewność realizacji na czas.",
    "ekipy": "Współpracujemy wyłącznie ze sprawdzonymi ekipami wykończeniowymi, które znamy od lat i z którymi zrealizowaliśmy dziesiątki udanych projektów. To fachowcy, którym ufamy - rzetelni, terminowi i dbający o detale.",
    "gdzie_dzialamy": "Działamy na terenie Trójmiasta (Gdańsk, Sopot, Gdynia), Warszawy oraz Wrocławia oraz okolice do 60 km od Centrum. Nasze biura znajdują się: Gdańsk - ul. Pałubickiego 2 (C2-parter), Warszawa - ul. Prosta 70 (5 piętro), Wrocław - ul. Sucha 3.",
    "po_odbiorze": "Po zakończeniu prac Twoje mieszkanie będzie idealnie czyste i gotowe do natychmiastowego zamieszkania. Dodatkowo zapewniamy 36-miesięczną gwarancję od momentu odbioru.",
    # Domy pasywne
    "domy_pasywne": "Oferujemy budowę domów pasywnych w trzech podstawowych metrażach: 70m² (idealny dla pary), 85m² (dla małej rodziny) i 140m² (dla większej rodziny). Nasze domy wykorzystują nowoczesne technologie: Posytec (system izolacji), IsoBeton (energooszczędny materiał konstrukcyjny) i CLT/HBE (połączenie drewna i betonu). Domy pasywne charakteryzują się minimalnym zużyciem energii, niskimi kosztami eksploatacji i doskonałą wentylacją z odzyskiem ciepła.",
    "technologie_domy_pasywne": "W naszych domach pasywnych wykorzystujemy trzy główne technologie: 1) Posytec - zaawansowany system izolacji zapewniający doskonałą izolację termiczną, 2) IsoBeton - energooszczędny materiał konstrukcyjny o wysokich parametrach izolacyjnych, 3) CLT/HBE (Cross Laminated Timber / Holz Beton Element) - połączenie drewna i betonu zapewniające doskonałe właściwości izolacyjne i konstrukcyjne.",
    # Zabudowy stolarskie
    "zabudowy_stolarskie_szczegoly": "Oferujemy kompleksowe zabudowy stolarskie na wymiar: szafy, garderoby, dressing roomy, biblioteczki, regały, zabudowy kuchenne i łazienkowe. Proces obejmuje kompleksowe podejście od projektu, przez produkcję, aż po montaż. Korzystamy z najwyższej jakości materiałów dla trwałości i funkcjonalności. Wycena jest przygotowywana indywidualnie po zrobieniu projektu.",
    "kuchnie_na_wymiar": "Tak, wykonujemy kuchnie na wymiar. Wycena jest przygotowywana indywidualnie po zrobieniu projektu, uwzględniającego wszystkie Twoje potrzeby i preferencje. Oferujemy kompleksowe zabudowy kuchenne dopasowane do przestrzeni.",
    # Usługi dodatkowe
    "klimatyzacja": "Tak, oferujemy montaż klimatyzacji. W pakiecie Waniliowy/Express cena za jedną jednostkę zaczyna się od 7800 zł. W pozostałych pakietach wycena jest przygotowywana indywidualnie po zrobieniu projektu.",
    "schody_na_zamowienie": "Tak, wykonujemy schody na zamówienie. Wycena jest przygotowywana indywidualnie po zrobieniu projektu, uwzględniającego wszystkie potrzeby i preferencje.",
    "wizualizacje": "Oferujemy wizualizacje 3D projektowanych wnętrz, które pozwalają zobaczyć, jak będzie wyglądać gotowa przestrzeń przed rozpoczęciem prac. Wizualizacje są dostępne w pakietach Comfort (łazienka, kuchnia), Premium (łazienka, salon, kuchnia, hol) oraz w projektach indywidualnych (całe mieszkanie).",
    "nadzor_prace": "Tak, zapewniamy pełen nadzór nad pracami. Nasi Projektanci nadzorują każdy etap realizacji – dbają o zgodność z projektem, normy techniczne oraz terminowe dostawy materiałów. Dzięki temu nie musisz martwić się przepisami budowlanymi ani technicznymi szczegółami.",
    "raporty_postep": "Tak, regularnie przesyłamy raporty dotyczące postępu prac, w tym zdjęcia. Dzięki temu możesz na bieżąco śledzić postępy bez konieczności wychodzenia z domu.",
    # Informacje firmowe
    "dane_firmowe": "NovaHouse Sp. z o.o. jest zarejestrowana pod numerem KRS 0000612864, posiada NIP 5833201699 oraz REGON 364323586. Kapitał zakładowy firmy wynosi 100.000,00 PLN. Działamy od 2011 roku.",
    "kontakt_specjalistyczny": "W sprawach logistyki i zamówień można dzwonić pod numer +48 509 929 437, w kwestiach finansowych i księgowych pod numer +48 607 518 544. W sprawie współpracy z partnerami i wykonawcami: partnerzy@novahouse.pl. Główny kontakt: +48 585 004 663, kontakt@novahouse.pl.",
    "doswiadczenie_firmy": "NovaHouse działa na rynku od 2011 roku. Mamy za sobą ponad 350 zrealizowanych projektów i 96% zadowolonych klientów. Współpracujemy z ponad 120 sprawdzonymi dostawcami i wykonawcami. 94% naszych projektów oddajemy przed terminem.",
}

COMPANY_INFO = """
NovaHouse to profesjonalna firma specjalizująca się w kompleksowym wykończeniu wnętrz pod klucz.

📊 O NAS:
NovaHouse działa na rynku od 2011 roku. Początkowo koncentrowaliśmy się na technikach home staging, a obecnie oferujemy pełen zakres usług projektowania i realizacji przestrzeni mieszkalnych i komercyjnych. Tworzymy wnętrza, które są gotowe do zamieszkania. Od projektu po efekt końcowy – zajmujemy się wszystkim, abyś nie musiał się o nic martwić. Działamy na terenie Trójmiasta (Gdańsk, Sopot, Gdynia), Warszawy oraz Wrocławia.

🎯 MISJA:
Naszą misją jest tworzenie pięknych wnętrz, realizowanych terminowo i w ustalonym budżecie, wyręczając klientów w całym procesie remontowym. Chcemy zmieniać postrzeganie firm remontowych na terminowe i solidne oraz upraszczać klientom przejście przez skomplikowany proces remontowy.

🎯 GŁÓWNE CELE:
1. Zmiana postrzegania firm remontowych na terminowe i solidne
2. Uproszczenie klientom przejścia przez skomplikowany proces remontowy poprzez załatwianie za nich każdej sprawy
3. Projektowanie pięknych wnętrz w ustalonym budżecie i realizacja prac w terminie

🏆 NASZE WYNIKI:
• Działamy od 2011 roku
• 350+ zrealizowanych projektów
• 96% zadowolonych klientów
• 94% zleceń oddanych przed terminem
• 120+ sprawdzonych dostawców i partnerów
• 36 miesięcy gwarancji
• 15% rabatu na wszystkie materiały
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

💰 CENY PAKIETÓW:
• Express: od 999 zł/m²* | Projektowanie: do 10 dni | Realizacja: 6-8 tygodni** | 150 produktów
• Express Plus: od 1199 zł/m²* | Projektowanie: do 20 dni | Realizacja: 6-8 tygodni** | 300 produktów
• Comfort/Szafran: od 1499 zł/m²* | Projektowanie: do 4 tygodni | Realizacja: 8-12 tygodni** | 450 produktów
• Premium/Pomarańczowy/Cynamonowy: od 1999 zł/m²* | Projektowanie: do 6 tygodni | Realizacja: 10-16 tygodni** | 600 produktów
• Projekt Indywidualny: 1700-5000 zł/m² | Projektowanie: 6-10 tygodni | Realizacja: indywidualna

* Podana cena dotyczy mieszkania o powierzchni 65 m² w stanie deweloperskim. Dla innych metraży ceny przeliczane są indywidualnie.
** Podany czas realizacji obowiązuje dla mieszkań o powierzchni od 20 do 90 m².

🎁 RABAT: 15% na wszystkie materiały dla każdego pakietu!
💳 Wszystkie ceny zawierają VAT 8%. Realizacja projekt + wykończenie to całość od A do Z.

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
    for feature in package["features"]:
        description += f"• {feature}\n"
    description += f"\n**Dla kogo:** {package['ideal_for']}"

    return description


def get_all_packages_summary():
    """Zwraca podsumowanie wszystkich pakietów"""
    summary = "Oferujemy 5 opcji wykończeniowych:\n\n"
    for key, package in PACKAGES.items():
        execution = package.get("execution_time", "na zapytanie")
        summary += f"**{package['name']}** ({package['price_per_sqm']}, {execution})\n"
        summary += f"{package['description']}\n"
        summary += f"Standard: {package['standard']} | Produkty: {package['product_choices']}\n\n"
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
            "71+": {"points": 15, "package": "luxury"},
        },
    },
    {
        "id": 2,
        "question": "Jaki jest Twój budżet na wykończenie (PLN)?",
        "type": "range",
        "weight": 20,
        "scoring": {
            "0-100000": {"points": 5, "package": "standard"},
            "100001-200000": {"points": 10, "package": "premium"},
            "200001+": {"points": 15, "package": "luxury"},
        },
    },
    {
        "id": 3,
        "question": "Czy zależy Ci na szybkim terminie realizacji?",
        "type": "boolean",
        "weight": 5,
        "scoring": {
            "tak": {"points": 5, "package": "standard"},
            "nie": {"points": 10, "package": "premium"},
        },
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
            "Luksusowe": {"points": 15, "package": "luxury"},
        },
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
            "Powierzchnia komercyjna": {"points": 12, "package": "luxury"},
        },
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
            "Skandynawski": {"points": 9, "package": "premium"},
        },
    },
    {
        "id": 7,
        "question": "Czy chcesz integrację smart home?",
        "type": "boolean",
        "weight": 12,
        "scoring": {
            "tak": {"points": 15, "package": "luxury"},
            "nie": {"points": 5, "package": "standard"},
        },
    },
    {
        "id": 8,
        "question": "Czy jesteś zainteresowany konsultacją z naszym designerem?",
        "type": "boolean",
        "weight": 5,
        "scoring": {
            "tak": {"points": 10, "package": "premium"},
            "nie": {"points": 3, "package": "standard"},
        },
    },
]

# Partnerzy produktowi
PRODUCT_PARTNERS = [
    "Laufen",
    "Geberit",
    "Kaldewei",
    "Erkado",
    "Tubadzin",
    "Hansgrohe",
    "DRE",
    "Roca",
    "Elita",
    "Porta",
    "Paradyż",
    "Mapei",
    "KFA",
    "Quick-Step",
    "Deante",
    "Ferro",
    "Cersanit",
]

# Proces realizacji krok po kroku
PROCESS_STEPS = {
    "krok_1": {
        "title": "Wybór pakietu lub projektu indywidualnego",
        "description": "Oferujemy cztery różnorodne pakiety wykończeniowe lub możliwość stworzenia projektu dostosowanego do Twoich potrzeb. Po otrzymaniu informacji o metrażu skontaktujemy się, aby umówić się na spotkanie, na którym przygotujemy szczegółową wycenę zgodnie z Twoimi preferencjami i wymaganiami.",
        "duration": "1 spotkanie",
        "deliverables": ["Szczegółowa wycena", "Dobór pakietu", "Ustalenie zakresu prac"],
    },
    "krok_2": {
        "title": "Projektowanie z Projektantem",
        "description": "Spotkanie aranżacyjne dopasujemy do Twojej wygody – może odbyć się zdalnie lub w naszym biurze. Każdy z naszych pakietów oraz elementy kosztorysu są w pełni elastyczne, co daje Ci swobodę modyfikacji zgodnie z Twoimi potrzebami. Przygotujemy dla Ciebie 2-3 propozycje układów funkcjonalnych do wyboru, na podstawie których stworzymy precyzyjną listę zakupów oraz projekt wykonawczy.",
        "duration": "1-2 tygodnie",
        "deliverables": [
            "2-3 propozycje układów funkcjonalnych",
            "Precyzyjna lista zakupów",
            "Projekt wykonawczy",
        ],
    },
    "krok_3": {
        "title": "Usługa wykończenia pod klucz + Nadzór",
        "description": "Z naszą usługą wykończeniową i nadzorem możesz cieszyć się spokojem i zająć się swoimi sprawami – Projektant zajmie się wszystkim za Ciebie! Od zarządzania całym przebiegiem prac, przez organizację zamówień i montaż zabudów stolarskich, aż po finalną kontrolę jakości. Dzięki temu masz pewność, że efekt końcowy będzie zgodny z Twoimi oczekiwaniami.",
        "duration": "Od 1,5 miesiąca",
        "deliverables": ["Raporty z postępu prac", "Zdjęcia na bieżąco", "Pełna koordynacja"],
    },
    "krok_4": {
        "title": "Finalizacja zlecenia i odbiór lokalu",
        "description": "Po zakończeniu prac Twoje mieszkanie będzie idealnie czyste i gotowe do natychmiastowego zamieszkania. Dodatkowo, zapewniamy Ci 36-miesięczną gwarancję od momentu odbioru, co daje Ci pełen komfort i poczucie bezpieczeństwa.",
        "duration": "1 dzień",
        "deliverables": [
            "Czyste mieszkanie gotowe do zamieszkania",
            "36-miesięczna gwarancja",
            "Dokumentacja odbiorcza",
        ],
    },
}

# Portfolio - przykładowe realizacje
PORTFOLIO = {
    "realizacja_1": {
        "title": "Mieszkanie – 100 m²",
        "type": "Projekt indywidualny",
        "location": "Nie określono",
        "url": "https://novahouse.pl/realizacje/mieszkanie-100-m2-projekt-indywidualny/",
    },
    "realizacja_2": {
        "title": "Mieszkanie – 3 pokoje 60m²",
        "type": "Projekt indywidualny",
        "location": "Sopot, ul. Okrzei",
        "url": "https://novahouse.pl/realizacje/sopot-okrzei/",
    },
    "realizacja_3": {
        "title": "Dom – 6 pokoi 165m²",
        "type": "Projekt indywidualny",
        "location": "Małkowo",
        "url": "https://novahouse.pl/realizacje/malkowo-dom/",
    },
    "realizacja_4": {
        "title": "Dom – 6 pokoi 150m²",
        "type": "Projekt indywidualny",
        "location": "Nie określono",
        "url": "https://novahouse.pl/realizacje/dom-150-m2/",
    },
}

# Blog i materiały edukacyjne
BLOG_ARTICLES = [
    {
        "title": "Architekt Wnętrz – Kim Jest i Dlaczego Warto Zatrudnić Profesjonalistę?",
        "url": "https://novahouse.pl/architekt-wnetrz-kim-jest-i-dlaczego-warto-zatrudnic-profesjonaliste/",
    },
    {
        "title": "Kuchnia modułowa czy na wymiar? Kompleksowy przewodnik",
        "url": "https://novahouse.pl/kuchnia-modulowa-czy-na-wymiar-kompleksowy-przewodnik-dla-osob-urzadzajacych-wymarzona-kuchnie/",
    },
    {
        "title": "Aranżacja wnętrz z NovaHouse – Twój styl w każdym detalu",
        "url": "https://novahouse.pl/aranzacja-wnetrz-z-novahouse-twoj-styl-w-kazdym-detalu/",
    },
    {
        "title": "Gotowe mieszkania z NovaHouse – oszczędź czas i zamieszkaj od zaraz",
        "url": "https://novahouse.pl/gotowe-mieszkania-nowoczesne-rozwiazania-dla-twojego-komfortu/",
    },
    {
        "title": "Planowanie Remontu Domu – Kluczowe Kwestie do Rozważenia",
        "url": "https://novahouse.pl/planowanie-remontu-domu-kluczowe-kwestie-do-rozwazenia/",
    },
    {
        "title": "Projektant wnętrz – Jakiego wybrać?",
        "url": "https://novahouse.pl/projektant-wnetrz-jakiego-wybrac/",
    },
]

# Zespół
TEAM_INFO = {
    "wiceprezes": {
        "name": "Agnieszka Kubiak",
        "position": "Wiceprezes",
        "quote": "Wiem, jak wiele decyzji trzeba podjąć podczas urządzania mieszkania – dlatego postanowiliśmy ułatwić Ci ten proces. Przygotowaliśmy dla Ciebie starannie wyselekcjonowane katalogi produktów. To nie jest przypadkowy zbiór – to efekt wieloletniej współpracy z naszymi klientami.",
        "responsibility": "Nadzór nad projektami i wsparcie klientów",
    },
    "projektanci": {
        "count": "Zespół doświadczonych projektantów",
        "role": "Projektowanie wnętrz, dobór materiałów, koordynacja z klientem",
        "note": "Każdy klient ma przypisanego dedykowanego projektanta",
    },
}

# Opinie klientów z Google
CLIENT_REVIEWS = [
    {
        "author": "Alex Szymczak",
        "rating": 5,
        "time": "4 tygodnie temu",
        "text": "Skorzystałem z usługi wykończenia pod klucz. Kontakt jest z jedną osobą, wyznaczoną projektantką, która projektuje i koordynuje prace. Mieszkanie było...",
    },
    {
        "author": "Magda Nowak",
        "rating": 5,
        "time": "4 tygodnie temu",
        "text": "Wiele czynników sprawiło że zdecydowaliśmy się na Novahouse. Wywiązali się wzorowo z umowy. Jakość zabudowy stolarskiej bardzo dobra, gładzie i...",
    },
    {
        "author": "Krzysztof Skutnik",
        "rating": 5,
        "time": "4 tygodnie temu",
        "text": "Wykonywaliśmy wykończenie mieszkania wraz z NovaHouse. Otrzymaliśmy sporo praktycznych rozwiązań już na etapie projektowania. Z odrobiną cierpliwości i współpracy udało...",
    },
    {
        "author": "Joanna Drewek",
        "rating": 5,
        "time": "tydzień temu",
        "text": "Jestem zadowolona z projektów zaproponowanych przez projektanta pana Michała. Wykazał się profesjonalizmem i, co bardzo ważne, cierpliwością przy ustalaniu różnych...",
    },
    {
        "author": "Beata Werner",
        "rating": 5,
        "time": "3 tygodnie temu",
        "text": "Firma NovaHouse bardzo dobrze zaprojektowała moje nowe mieszkanie, wszystkie meble a także pomogła stworzyć w moim domu styl prowansalski. Bardzo...",
    },
]

# USP - Unique Selling Points
WHY_CHOOSE_US = {
    "kompleksowo": "Kompleksowo – od projektu, przez produkcję, aż po montaż. Nie musisz koordynować pracy różnych ekip – wszystko załatwiamy za Ciebie.",
    "gwarancja": "Gwarancja jakości i trwałości: Korzystamy z najwyższej jakości materiałów, dzięki czemu nasze zabudowy są funkcjonalne i trwałe przez lata.",
    "budzet": "Pełna kontrola nad budżetem: Oferujemy przejrzyste wyceny, dostosowane do budżetu, który planujesz przeznaczyć. Dzięki temu dokładnie wiesz, za co płacisz.",
    "terminowosc": "94% projektów oddanych przed terminem - to nasza obietnica i standard pracy.",
    "ekipy": "Sprawdzone ekipy wykończeniowe znane od lat - rzetelne, terminowe, dbające o każdy detal.",
    "raporty": "Raporty i zdjęcia na bieżąco - pełna kontrola bez wychodzenia z domu.",
    "sprzatanie": "Mieszkanie gotowe do zamieszkania - idealna czystość po zakończeniu prac.",
}

# Korzyści pakietów wykończeniowych
PACKAGE_BENEFITS = {
    "title": "Nasze pakiety wykończeniowe – szybciej, prościej, przewidywalnie",
    "benefits": [
        "Szybszy – autorski proces projektowania oraz dedykowany system prac umożliwiają szybszą realizację inwestycji",
        "Przewidywalny – od początku wiesz, ile zapłacisz i kiedy skończymy",
        "Prosty – jedna osoba kontaktowa, jasne zasady współpracy i minimalne formalności",
        "Elastyczny – możliwość personalizacji produktów i modyfikacji zakresu usług",
        "Z kontrolą kosztów – stała cena pakietu oraz pełna transparentność kosztów dodatkowych dzięki szczegółowemu cennikowi usług",
        "Rabat 15% na wszystkie materiały – oszczędzasz na wysokiej jakości produktach",
    ],
}

# Materiały i katalogi
MATERIALS_INFO = """
Przygotowaliśmy dla Ciebie starannie wyselekcjonowane katalogi produktów. To nie jest przypadkowy zbiór – to efekt wieloletniej współpracy z naszymi klientami.

W katalogach znajdziesz tylko te materiały i rozwiązania, które najczęściej wybierali – sprawdzone, estetyczne i funkcjonalne. Usunęliśmy produkty egzotyczne, które nie budziły zainteresowania.

Dzięki temu oszczędzasz swój czas – eliminujemy chaos i skupiamy się na tym, co naprawdę się sprawdza. Twój wybór staje się prostszy, a efekt końcowy – przewidywalnie dobry.
"""

# Domy pasywne
PASSIVE_HOUSES = {
    "description": "Domy pasywne to energooszczędne budynki, które minimalizują zużycie energii dzięki doskonałej izolacji i wykorzystaniu odnawialnych źródeł energii.",
    "available_sizes": {
        "70m2": {
            "size": "70m²",
            "ideal_for": "Para lub małe gospodarstwo domowe",
            "description": "Kompaktowy dom pasywny idealny dla pary",
        },
        "85m2": {
            "size": "85m²",
            "ideal_for": "Mała rodzina (2-3 osoby)",
            "description": "Optymalny dom pasywny dla małej rodziny",
        },
        "140m2": {
            "size": "140m²",
            "ideal_for": "Większa rodzina (4-5 osób)",
            "description": "Przestronny dom pasywny dla większej rodziny",
        },
    },
    "technologies": {
        "posytec": {
            "name": "Posytec",
            "description": "Zaawansowany system izolacji zapewniający doskonałą izolację termiczną",
        },
        "isobeton": {
            "name": "IsoBeton",
            "description": "Energooszczędny materiał konstrukcyjny o wysokich parametrach izolacyjnych",
        },
        "clt_hbe": {
            "name": "CLT/HBE",
            "description": "Cross Laminated Timber / Holz Beton Element - połączenie drewna i betonu zapewniające doskonałe właściwości izolacyjne i konstrukcyjne",
        },
    },
    "benefits": [
        "Minimalne zużycie energii do ogrzewania i chłodzenia",
        "Niższe koszty eksploatacji",
        "Doskonała wentylacja z odzyskiem ciepła",
        "Wysoki komfort użytkowania",
        "Ekologiczne i energooszczędne",
        "Doskonała izolacja termiczna i akustyczna",
    ],
}

# Zabudowy stolarskie
CARPENTRY_SERVICES = {
    "description": "Tworzymy zabudowy stolarskie na wymiar - kompleksowo od projektu przez produkcję do montażu. Korzystamy z najwyższej jakości materiałów dla trwałości i funkcjonalności.",
    "types": {
        "szafy": "Szafy na wymiar dopasowane do przestrzeni",
        "garderoby": "Garderoby i dressing roomy",
        "biblioteczki": "Biblioteczki i regały",
        "zabudowy_kuchenne": "Zabudowy kuchenne na wymiar",
        "zabudowy_lazienkowe": "Zabudowy łazienkowe",
        "inne": "Inne zabudowy na indywidualne zamówienie",
    },
    "process": [
        "Kompleksowe podejście od projektu, przez produkcję, aż po montaż",
        "Wykorzystanie materiałów wysokiej jakości",
        "Pełna kontrola nad budżetem dzięki przejrzystym wycenom",
        "Indywidualne dopasowanie do potrzeb klienta",
    ],
    "pricing": "Wycena przygotowywana indywidualnie po zrobieniu projektu",
}

# Usługi dodatkowe
ADDITIONAL_SERVICES = {
    "klimatyzacja": {
        "name": "Klimatyzacja",
        "description": "Montaż systemów klimatyzacji",
        "pricing": {
            "waniliowy": "od 7800 zł za jednostkę",
            "other": "Wycena indywidualna po projekcie",
        },
    },
    "schody": {
        "name": "Schody",
        "description": "Wykonanie schodów na zamówienie",
        "pricing": "Wycena indywidualna po projekcie",
    },
    "wizualizacje": {
        "name": "Wizualizacje 3D",
        "description": "Wizualizacje projektowanych wnętrz pozwalające zobaczyć gotową przestrzeń przed rozpoczęciem prac",
        "included_in": ["Comfort", "Premium", "Individual"],
    },
    "nadzor": {
        "name": "Pełen nadzór nad pracami",
        "description": "Projektanci nadzorują każdy etap realizacji – dbają o zgodność z projektem, normy techniczne oraz terminowe dostawy materiałów",
    },
    "raporty": {
        "name": "Raporty z postępu prac",
        "description": "Regularne przesyłanie raportów i zdjęć z postępu prac",
    },
}

# Blog i edukacja
BLOG_TOPICS = {
    "title": "Wiedza i Blog NovaHouse",
    "description": "Edukacja w zakresie projektowania i wykańczania wnętrz, praktyczne porady, inspiracje",
    "categories": [
        "Projektowanie wnętrz",
        "Wykańczanie mieszkań",
        "Wybór materiałów",
        "Porady ekspertów",
        "Realizacje krok po kroku",
    ],
    "value": [
        "Edukacja w zakresie projektowania i wykańczania wnętrz",
        "Praktyczne porady dotyczące wyboru materiałów i rozwiązań",
        "Inspiracje do własnych projektów",
        "Budowanie zaufania poprzez dzielenie się wiedzą ekspercką",
    ],
}


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
        if project["location"] != "Nie określono":
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
