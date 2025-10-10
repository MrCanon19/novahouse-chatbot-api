"""
NovaHouse Professional Expert System
Profesjonalny, ciepły i kompetentny asystent bez wzmianek o stażu
"""

class NovaHouseProfessionalExpert:
    """Profesjonalny ekspert NovaHouse - kompetentny, ciepły, pomocny"""
    
    def __init__(self):
        self.knowledge = self._load_professional_knowledge()
    
    def _load_professional_knowledge(self):
        return {
            "pakiety_profesjonalne": {
                "waniliowy": {
                    "nazwa": "Pakiet Waniliowy",
                    "cena_za_m2": "1200-1500 zł/m²",
                    "opis": "Solidny standard dla osób ceniących sprawdzone rozwiązania. Wszystko będzie działać przez lata.",
                    "materialy_konkretne": {
                        "podłogi": "Panele laminowane 8mm (Kronotex, Egger) - wytrzymałe i łatwe w utrzymaniu",
                        "ściany": "Farba lateksowa Dulux/Tikkurila - można myć, nie żółknie",
                        "łazienka": "Płytki ceramiczne 30x60cm, armatura Koło/Cersanit - sprawdzone marki",
                        "kuchnia": "Blat laminowany, fronty MDF lakierowane - praktyczne i trwałe"
                    },
                    "czas_realny": "4-5 tygodni dla 50m²",
                    "dla_kogo": "Osoby z ograniczonym budżetem, które nie chcą rezygnować z jakości",
                    "zalety": "Nie oszczędzamy na instalacjach - to podstawa. Estetyka prosta ale ponadczasowa."
                },
                
                "pomarańczowy": {
                    "nazwa": "Pakiet Pomarańczowy", 
                    "cena_za_m2": "1800-2200 zł/m²",
                    "opis": "Doskonały kompromis między jakością a ceną. Widoczna różnica w standardzie bez przepłacania.",
                    "materialy_konkretne": {
                        "podłogi": "Parkiet 3-warstwowy (Barlinek, Tarkett) lub LVT premium - ciepło i elegancja",
                        "ściany": "Farby premium z akcentami (kamień dekoracyjny, tapeta strukturalna)",
                        "łazienka": "Płytki 60x120cm, armatura Hansgrohe/Grohe - design i funkcjonalność",
                        "kuchnia": "Blat kwarcowy, fronty lakierowane wysokim połyskiem - efektowny wygląd"
                    },
                    "czas_realny": "6-7 tygodni dla 70m²",
                    "dla_kogo": "Rodziny ceniące komfort i estetykę, osoby szukające optymalnego rozwiązania",
                    "zalety": "Inwestujemy w detale - listwy, ościeżnice, oświetlenie LED. Różnica widoczna od pierwszego wejrzenia."
                },
                
                "cynamonowy": {
                    "nazwa": "Pakiet Cynamonowy",
                    "cena_za_m2": "2500-3000 zł/m²", 
                    "opis": "Premium bez przesady. Materiały najwyższej jakości dla wymagających klientów.",
                    "materialy_konkretne": {
                        "podłogi": "Parkiet dębowy 15mm (Boen, Kährs) lub płytki wielkoformatowe Porcelanosa",
                        "ściany": "Tynki dekoracyjne, farby mineralne, okładziny drewniane",
                        "łazienka": "Płytki naturalne/techniczne, armatura Villeroy&Boch - elegancja na lata",
                        "kuchnia": "Blat z konglomeratu, fronty fornirowane - naturalne piękno"
                    },
                    "czas_realny": "8-10 tygodni dla 90m²",
                    "dla_kogo": "Klienci ceniący unikalne rozwiązania i najwyższą jakość",
                    "zalety": "Każdy detal przemyślany. Instalacje w najwyższym standardzie. Inwestycja na dekady."
                },
                
                "szafranowy": {
                    "nazwa": "Pakiet Szafranowy",
                    "cena_za_m2": "3500-4500 zł/m²",
                    "opis": "Absolutny szczyt możliwości. Materiały i wykonanie na najwyższym poziomie.",
                    "materialy_konkretne": {
                        "podłogi": "Parkiet egzotyczny (Merbau, Wenge) lub płytki marmurowe Carrara",
                        "ściany": "Tynki weneckie, okładziny kamienne, tapety designerskie",
                        "łazienka": "Naturalne kamienie, armatura Dornbracht/Axor - prawdziwa sztuka",
                        "kuchnia": "Blaty z naturalnego kamienia, fronty z litego drewna - unikatowe rozwiązania"
                    },
                    "czas_realny": "10-14 tygodni dla 120m²",
                    "dla_kogo": "Klienci bez kompromisów, apartamenty i domy premium",
                    "zalety": "Perfekcja w każdym detalu. Rzemiosło na najwyższym poziomie."
                }
            },
            
            "profesjonalne_porady": {
                "wybor_pakietu": {
                    "budżet_do_100k": "Pakiet Waniliowy - solidne fundamenty dla Twojego domu",
                    "budżet_100_200k": "Pakiet Pomarańczowy - optymalne rozwiązanie dla większości klientów", 
                    "budżet_200_300k": "Pakiet Cynamonowy - inwestycja w długoterminową satysfakcję",
                    "budżet_powyżej_300k": "Pakiet Szafranowy - realizacja marzeń bez kompromisów",
                    "zasada": "Zawsze lepiej wybrać mniejszy metraż w wyższym standardzie"
                },
                
                "harmonogram_profesjonalny": {
                    "przygotowanie": "1-2 tygodnie (pozwolenia, dostawy, koordynacja)",
                    "rozbiórka": "2-3 dni (w zależności od zakresu)",
                    "instalacje": "1-2 tygodnie (elektryka, hydraulika, ogrzewanie)",
                    "tynki_wylewki": "1 tydzień + 2 tygodnie na wyschnięcie",
                    "wykończenia": "2-4 tygodnie (zależnie od wybranego pakietu)",
                    "finalizacja": "2-3 dni (sprzątanie i odbiór)",
                    "uwaga": "Zawsze planujemy 15-20% dodatkowego czasu na nieprzewidziane sytuacje"
                },
                
                "najlepsze_praktyki": {
                    "instalacje": "Nigdy nie oszczędzamy na przewodach i rurach - to fundament każdego dobrego remontu",
                    "materiały": "Lepiej wybrać mniej płytek ale wysokiej jakości niż dużo tanich",
                    "wentylacja": "W łazience bez okna wentylacja mechaniczna to konieczność, nie opcja",
                    "kolory": "Maksymalnie 3 kolory w pomieszczeniu - więcej wprowadza chaos",
                    "trendy": "Klasyczne rozwiązania nigdy nie wychodzą z mody"
                },
                
                "profesjonalne_wskazówki": {
                    "najlepszy_czas": "Jesień i zima to optymalne pory - ekipy mają więcej czasu, ceny są korzystniejsze",
                    "materiały": "Zawsze zamawiamy 10-15% więcej materiałów - zabezpieczenie przed niedoborami",
                    "ekipy": "Doświadczona ekipa to podstawa sukcesu - nie warto oszczędzać na fachowcach",
                    "kontrola": "Regularne wizyty co 2-3 dni pozwalają szybko reagować na ewentualne problemy",
                    "płatności": "Standardem branżowym jest zaliczka do 30% wartości kontraktu"
                }
            },
            
            "konkretne_kalkulacje": {
                "koszty_realne": {
                    "50m2_waniliowy": "60-75 tys. zł (materiały, robocizna, nadzór)",
                    "70m2_pomarańczowy": "126-154 tys. zł (kompleksowe wykończenie)", 
                    "90m2_cynamonowy": "225-270 tys. zł (premium standard)",
                    "120m2_szafranowy": "420-540 tys. zł (najwyższa jakość)",
                    "uwaga": "Ceny zawierają wszystkie materiały, robociznę i nadzór. Meble i AGD to osobna kategoria."
                },
                
                "czas_realizacji": {
                    "mieszkanie_40m2": "4-5 tygodni",
                    "mieszkanie_70m2": "6-8 tygodni",
                    "mieszkanie_100m2": "8-12 tygodni",
                    "dom_150m2": "12-16 tygodni",
                    "czynniki": "Czas zależy od pakietu, dostępności materiałów i warunków lokalnych"
                },
                
                "zakres_standardowy": {
                    "zawsze_w_cenie": [
                        "Projekt wykonawczy i wizualizacje",
                        "Wszystkie materiały wykończeniowe zgodnie z pakietem", 
                        "Profesjonalna robocizna i nadzór",
                        "Transport i logistyka materiałów",
                        "Sprzątanie końcowe",
                        "Gwarancja 24 miesiące na wykonane prace"
                    ],
                    "dodatkowo_płatne": [
                        "Meble i sprzęt AGD",
                        "Projektowanie wnętrz (opcjonalna usługa)",
                        "Dodatkowe instalacje (klimatyzacja, systemy smart home)",
                        "Modyfikacje w trakcie realizacji",
                        "Magazynowanie mebli podczas prac"
                    ]
                }
            },
            
            "specyfika_regionalna": {
                "warszawa": {
                    "korekta_cenowa": "+15-20% (koszty logistyki i dostępności ekip)",
                    "czas_dodatkowy": "+1-2 tygodnie (ograniczenia komunikacyjne)",
                    "uwagi": "Wymagane pozwolenia wspólnoty, ograniczone godziny pracy"
                },
                "kraków": {
                    "korekta_cenowa": "+10-15%",
                    "czas_dodatkowy": "standardowy",
                    "uwagi": "Stare kamienice wymagają specjalistycznego podejścia"
                },
                "gdańsk": {
                    "korekta_cenowa": "+5-10%", 
                    "czas_dodatkowy": "standardowy",
                    "uwagi": "Szczególna uwaga na wentylację ze względu na wilgotność"
                },
                "mniejsze_miasta": {
                    "korekta_cenowa": "-10-15%",
                    "czas_dodatkowy": "+1 tydzień (dojazdy specjalistów)",
                    "uwagi": "Może być ograniczona dostępność niektórych materiałów premium"
                }
            }
        }
    
    def get_professional_answer(self, query: str, intent: str = None) -> str:
        """Profesjonalna odpowiedź eksperta NovaHouse"""
        
        query_lower = query.lower()
        
        # Konkretne pytania o koszty
        if any(word in query_lower for word in ['ile kosztuje', 'jaka cena', 'koszt', 'budżet']):
            return self._answer_about_costs_professional(query_lower)
        
        # Pytania o czas realizacji
        elif any(word in query_lower for word in ['jak długo', 'ile czasu', 'kiedy', 'termin']):
            return self._answer_about_time_professional(query_lower)
        
        # Pytania o pakiety
        elif any(word in query_lower for word in ['pakiet', 'standard', 'jakość', 'różnica']):
            return self._answer_about_packages_professional(query_lower)
        
        # Pytania o materiały
        elif any(word in query_lower for word in ['materiał', 'płytki', 'podłogi', 'farba']):
            return self._answer_about_materials_professional(query_lower)
        
        # Prośby o porady
        elif any(word in query_lower for word in ['co polecasz', 'który lepszy', 'rada', 'doradź']):
            return self._give_professional_advice(query_lower)
        
        # Pytania o lokalizację
        elif any(city in query_lower for city in ['warszawa', 'kraków', 'gdańsk', 'poznań']):
            return self._answer_about_location_professional(query_lower)
        
        else:
            return self._general_professional_response()
    
    def _answer_about_costs_professional(self, query: str) -> str:
        """Profesjonalne odpowiedzi o kosztach"""
        
        if any(size in query for size in ['50', 'małe', 'kawalerka']):
            return """💰 **Koszt wykończenia 50m² - szczegółowa kalkulacja:**

🟡 **Pakiet Waniliowy:** 60-75 tys. zł (1200-1500 zł/m²)
Solidne fundamenty dla Twojego domu - sprawdzone rozwiązania

🟠 **Pakiet Pomarańczowy:** 90-110 tys. zł (1800-2200 zł/m²)  
Optymalne rozwiązanie - widoczna różnica w jakości

🟤 **Pakiet Cynamonowy:** 125-150 tys. zł (2500-3000 zł/m²)
Materiały premium - inwestycja na dekady

**Rekomendacja:** Dla mieszkania 50m² szczególnie polecam Pakiet Pomarańczowy - doskonały stosunek jakości do ceny.

**W cenie zawarte:** materiały, robocizna, nadzór, gwarancja 24 miesiące
**Dodatkowo:** meble, AGD, ewentualne modyfikacje

Chętnie przygotujemy szczegółową wycenę dostosowaną do Twoich potrzeb."""
        
        elif any(size in query for size in ['70', 'średnie', 'dwupokojowe']):
            return """💰 **Koszt wykończenia 70m² - profesjonalna kalkulacja:**

🟡 **Pakiet Waniliowy:** 84-105 tys. zł 
Sprawdzone rozwiązania w atrakcyjnej cenie

🟠 **Pakiet Pomarańczowy:** 126-154 tys. zł
**← Najczęściej wybierany dla tej wielkości**

🟤 **Pakiet Cynamonowy:** 175-210 tys. zł
Dla klientów ceniących najwyższą jakość

**Profesjonalna rada:** 70m² to idealna wielkość dla Pakietu Pomarańczowego. Materiały premium bez przepłacania, efekt który zachwyci na lata.

**Praktyczna wskazówka:** Lepiej zainwestować w mniejszy metraż w wyższym standardzie niż większy w podstawowym.

Podaj swoje preferencje, a przygotujemy spersonalizowaną ofertę."""
        
        else:
            return """💰 **Profesjonalna kalkulacja kosztów wykończenia:**

**Stawki za metr kwadratowy:**
🟡 Waniliowy: 1200-1500 zł/m² - solidne podstawy
🟠 Pomarańczowy: 1800-2200 zł/m² - optymalne rozwiązanie  
🟤 Cynamonowy: 2500-3000 zł/m² - premium standard
🟫 Szafranowy: 3500-4500 zł/m² - najwyższa jakość

**Przykładowe kalkulacje:**
• 50m² Pomarańczowy: około 100 tys. zł
• 70m² Cynamonowy: około 200 tys. zł
• 90m² Szafranowy: około 360 tys. zł

**Korekty regionalne:**
Warszawa +20%, Kraków +15%, mniejsze miasta -15%

**Zasada:** Inwestycja w jakość zawsze się zwraca.

Podaj metraż i lokalizację - przygotujemy precyzyjną kalkulację."""
    
    def _answer_about_time_professional(self, query: str) -> str:
        """Profesjonalne informacje o czasie realizacji"""
        
        return """⏰ **Profesjonalny harmonogram realizacji:**

**Standardowe czasy wykonania:**
• **Małe mieszkanie (40-50m²):** 4-6 tygodni
• **Średnie mieszkanie (60-80m²):** 6-8 tygodni  
• **Duże mieszkanie (90-120m²):** 8-12 tygodni
• **Dom (150m²+):** 12-16 tygodni

**Szczegółowe etapy (przykład 70m²):**
1. **Przygotowanie:** 1-2 tygodnie (pozwolenia, dostawy)
2. **Prace rozbiórkowe:** 2-3 dni
3. **Instalacje:** 1-2 tygodnie (elektryka, hydraulika)
4. **Tynki i wylewki:** 1 tydzień + 2 tygodnie schnięcia
5. **Wykończenia:** 2-4 tygodnie (zależnie od pakietu)
6. **Finalizacja:** 2-3 dni (sprzątanie, odbiór)

**Profesjonalne podejście:** Zawsze planujemy 15-20% dodatkowego czasu na nieprzewidziane sytuacje.

**Optymalne terminy:** Jesień i zima - ekipy mają więcej czasu, lepsze warunki cenowe.

Chcesz poznać szczegółowy harmonogram dla swojego projektu?"""
    
    def _answer_about_packages_professional(self, query: str) -> str:
        """Profesjonalne informacje o pakietach"""
        
        if 'waniliowy' in query or 'podstawowy' in query:
            return """🟡 **Pakiet Waniliowy - profesjonalna analiza:**

**Dla kogo:** Osoby z ograniczonym budżetem, które nie chcą rezygnować z jakości
**Charakterystyka:** Solidne fundamenty dla Twojego domu - wszystko będzie działać przez lata.

**Konkretne materiały:**
• **Podłogi:** Panele Kronotex/Egger 8mm - wytrzymałe, łatwe w utrzymaniu
• **Ściany:** Farba Dulux/Tikkurila - można myć, nie żółknie  
• **Łazienka:** Płytki 30x60cm, armatura Koło - sprawdzone marki
• **Kuchnia:** Blat laminowany, fronty MDF - praktyczne rozwiązania

**Kluczowa zasada:** Nie oszczędzamy na instalacjach - to podstawa każdego dobrego remontu.

**Inwestycja:** 1200-1500 zł/m²
**Czas realizacji:** 4-5 tygodni dla 50m²

**Rekomendacja:** Idealny wybór dla pierwszego mieszkania lub przy ograniczonym budżecie."""
        
        elif 'pomarańczowy' in query:
            return """🟠 **Pakiet Pomarańczowy - najczęściej wybierany:**

**Dla kogo:** Rodziny ceniące komfort i estetykę, osoby szukające optymalnego rozwiązania
**Charakterystyka:** Doskonały kompromis między jakością a ceną - widoczna różnica bez przepłacania.

**Konkretne materiały:**
• **Podłogi:** Parkiet 3-warstwowy Barlinek/Tarkett - ciepło i elegancja
• **Ściany:** Farby premium z akcentami (kamień, tapeta strukturalna)
• **Łazienka:** Płytki 60x120cm, armatura Hansgrohe - design i funkcjonalność  
• **Kuchnia:** Blat kwarcowy, fronty lakierowane - efektowny wygląd

**Przewaga:** Inwestujemy w detale - listwy, ościeżnice, LED. Różnica widoczna od pierwszego wejrzenia.

**Inwestycja:** 1800-2200 zł/m²
**Czas realizacji:** 6-7 tygodni dla 70m²

**Profesjonalna ocena:** Najlepszy stosunek jakości do ceny w naszej ofercie."""
        
        else:
            return """🏠 **Profesjonalny przegląd pakietów NovaHouse:**

🟡 **Waniliowy (1200-1500 zł/m²)**
Solidne podstawy - sprawdzone rozwiązania w atrakcyjnej cenie

🟠 **Pomarańczowy (1800-2200 zł/m²)**  
**← Najczęściej wybierany** - optymalne rozwiązanie dla większości klientów

🟤 **Cynamonowy (2500-3000 zł/m²)**
Premium standard - materiały najwyższej jakości

🟫 **Szafranowy (3500-4500 zł/m²)**
Absolutny szczyt - realizacja marzeń bez kompromisów

**Profesjonalne rekomendacje:**
• Budżet do 100k → Waniliowy
• Budżet 100-200k → Pomarańczowy ⭐
• Budżet 200-300k → Cynamonowy  
• Budżet 300k+ → Szafranowy

**Złota zasada:** Lepiej mniejszy metraż w wyższym standardzie.

O którym pakiecie chciałbyś dowiedzieć się więcej?"""
    
    def _answer_about_materials_professional(self, query: str) -> str:
        """Profesjonalne informacje o materiałach"""
        
        return """🔨 **Profesjonalny przegląd materiałów:**

**PODŁOGI - sprawdzone rozwiązania:**
• **Panele:** Kronotex, Egger (min. 8mm) - 60-120 zł/m²
• **Parkiet 3-warstwowy:** Barlinek, Tarkett - 150-300 zł/m²  
• **LVT premium:** Moduleo, Tarkett - 100-200 zł/m²

**ŚCIANY - trwałe wykończenia:**
• **Farby:** Dulux, Tikkurila, Beckers - 25-60 zł/l
• **Tynki dekoracyjne:** San Marco, Oikos - 80-200 zł/m²

**ŁAZIENKA - funkcjonalność i estetyka:**
• **Płytki podstawowe:** Cersanit, Opoczno - 30-80 zł/m²
• **Płytki premium:** Tubądzin, Paradyż - 100-300 zł/m²
• **Armatura:** Koło (niezawodność), Hansgrohe (design)

**KUCHNIA - serce domu:**
• **Blat laminowany:** 150-300 zł/mb - praktyczne rozwiązanie
• **Blat kwarcowy:** 800-1500 zł/mb - elegancja i trwałość
• **Blat z konglomeratu:** 1200-2500 zł/mb - najwyższa jakość

**Profesjonalna zasada:** Wybieramy materiały o optymalnym stosunku jakości do ceny.

Masz pytania o konkretne materiały? Chętnie doradzę."""
    
    def _give_professional_advice(self, query: str) -> str:
        """Profesjonalne porady"""
        
        return """💡 **Profesjonalne porady NovaHouse:**

**WYBÓR PAKIETU - dopasowany do potrzeb:**
• **Ograniczony budżet** → Waniliowy (solidne podstawy)
• **Szukasz optymalnego rozwiązania** → Pomarańczowy (najczęściej wybierany)
• **Cenisz najwyższą jakość** → Cynamonowy/Szafranowy

**NAJWAŻNIEJSZE ZASADY:**
✅ **Nie oszczędzaj na instalacjach** - to fundament każdego remontu
✅ **Wybieraj sprawdzone materiały** - lepiej mniej ale wysokiej jakości
✅ **Zaplanuj wentylację** - szczególnie w łazience bez okna
✅ **Ogranicz kolory** - maksymalnie 3 w pomieszczeniu
✅ **Postaw na klasykę** - trendy przechodzą, dobry design zostaje

**PROFESJONALNE WSKAZÓWKI:**
🎯 **Najlepszy czas:** jesień/zima (korzystniejsze warunki)
🎯 **Zamów materiały z zapasem** - 10-15% więcej
🎯 **Wybierz doświadczoną ekipę** - to podstawa sukcesu
🎯 **Kontroluj regularnie** - wizyty co 2-3 dni
🎯 **Płać etapami** - maksymalnie 30% zaliczki

**ZŁOTA ZASADA:** Lepiej mniejszy metraż w wyższym standardzie niż większy w podstawowym.

Masz konkretne pytanie? Chętnie pomogę w podjęciu najlepszej decyzji."""
    
    def _answer_about_location_professional(self, query: str) -> str:
        """Profesjonalne informacje o specyfice lokalnej"""
        
        if 'warszawa' in query:
            return """🏙️ **Specyfika realizacji w Warszawie:**

**Korekty cenowe:** +15-20% do standardowych stawek
**Czas realizacji:** +1-2 tygodnie (logistyka miejska)

**Przykładowe kalkulacje:**
• 50m² Pomarańczowy: około 120 tys. zł
• 70m² Cynamonowy: około 240 tys. zł

**Specyficzne wymagania:**
• Pozwolenia wspólnoty mieszkaniowej
• Ograniczone godziny pracy (8-18, sobota do 15)
• Wyzwania parkingowe dla ekip
• Wyższe koszty transportu materiałów

**Przewagi stolicy:**
• Najlepsza dostępność materiałów premium
• Szeroki wybór specjalistycznych ekip
• Szybkie dostawy

**Profesjonalna rada:** Planuj +20% budżetu i +2 tygodnie czasu na specyfikę warszawską.

Chcesz poznać szczegóły dla konkretnej lokalizacji?"""
        
        else:
            return """🗺️ **Specyfika regionalna - profesjonalne podejście:**

**Korekty cenowe według regionów:**
• **Warszawa:** +20% (logistyka miejska)
• **Kraków:** +15% (stare budownictwo)
• **Gdańsk:** +10% (wilgotność)
• **Poznań/Wrocław:** +5-10%
• **Mniejsze miasta:** -10-15% (niższe koszty)

**Uniwersalne zasady:**
• Duże miasta = wyższe koszty, lepsza dostępność
• Małe miasta = niższe ceny, ograniczona dostępność specjalistów
• Stare budynki = dodatkowe wyzwania techniczne
• Nowe osiedla = standardowa realizacja

**Profesjonalne podejście:** Dostosowujemy metodę pracy do lokalnych warunków, zachowując najwyższe standardy jakości.

Gdzie planujesz realizację? Przygotujemy szczegółowe informacje."""
    
    def _general_professional_response(self) -> str:
        """Ogólna profesjonalna odpowiedź"""
        
        return """🏠 **Witaj w NovaHouse - Twoim partnerze w wykończeniach wnętrz**

Jestem tutaj, aby pomóc Ci w realizacji marzeń o idealnym domu. Oferuję konkretne odpowiedzi i profesjonalne doradztwo.

**Mogę pomóc Ci z:**
💰 **Precyzyjną kalkulacją kosztów** - bez ukrytych opłat
⏰ **Realistycznym harmonogramem** - opartym na doświadczeniu  
🔨 **Wyborem optymalnych materiałów** - jakość w dobrej cenie
📋 **Profesjonalnymi poradami** - jak uniknąć typowych błędów
🏠 **Doborem idealnego pakietu** - dopasowanego do Twoich potrzeb

**Przykłady konkretnych pytań:**
• "Ile kosztuje wykończenie 70m² w Krakowie?"
• "Który pakiet dla rodziny z budżetem 150k?"
• "Jak długo trwa remont 50m² w Cynamonowym?"
• "Parkiet czy panele - co lepsze?"

**Nie pytaj ogólnie - pytaj konkretnie!**
Zamiast "Jaki macie cennik?" napisz "Ile będzie kosztować moje 65m² w Pomarańczowym?"

**Napisz konkretnie - odpowiem profesjonalnie i pomocnie.**"""

# Globalna instancja profesjonalnego eksperta
professional_expert = NovaHouseProfessionalExpert()
