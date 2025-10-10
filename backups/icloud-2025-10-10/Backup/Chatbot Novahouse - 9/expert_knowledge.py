"""
NovaHouse Expert Knowledge Base
40 lat doświadczenia w wykończeniach - konkretna, praktyczna wiedza
"""

class NovaHouseExpert:
    """Ekspert z 40-letnim doświadczeniem w wykończeniach"""
    
    def __init__(self):
        self.knowledge = self._load_expert_knowledge()
    
    def _load_expert_knowledge(self):
        return {
            "pakiety_rzeczywiste": {
                "waniliowy": {
                    "nazwa": "Pakiet Waniliowy",
                    "cena_za_m2": "1200-1500 zł/m²",
                    "opis_eksperta": "Solidny standard dla osób, które chcą dobrze i tanio. Nie ma fajerwerków, ale wszystko będzie działać przez lata.",
                    "materialy_konkretne": {
                        "podłogi": "Panele laminowane 8mm (Kronotex, Egger) - wytrzymałe, łatwe w utrzymaniu",
                        "ściany": "Farba lateksowa Dulux/Tikkurila - można myć, nie żółknie",
                        "łazienka": "Płytki ceramiczne 30x60cm, armatura Koło/Cersanit - sprawdzone marki",
                        "kuchnia": "Blat laminowany, fronty MDF lakierowane - praktyczne i trwałe"
                    },
                    "czas_realny": "4-5 tygodni dla 50m² (bez opóźnień dostawców)",
                    "dla_kogo": "Młode pary, pierwsze mieszkanie, ograniczony budżet ale chcą jakość",
                    "uwagi_eksperta": "Nie oszczędzamy na instalacjach - to podstawa. Estetyka prosta ale ponadczasowa."
                },
                
                "pomarańczowy": {
                    "nazwa": "Pakiet Pomarańczowy", 
                    "cena_za_m2": "1800-2200 zł/m²",
                    "opis_eksperta": "Złoty środek - widać różnicę w jakości, ale nie przepłacasz za markę. Mój osobisty faworyt.",
                    "materialy_konkretne": {
                        "podłogi": "Parkiet 3-warstwowy (Barlinek, Tarkett) lub LVT premium - ciepło i elegancja",
                        "ściany": "Farby premium + akcenty (kamień dekoracyjny, tapeta strukturalna)",
                        "łazienka": "Płytki 60x120cm, armatura Hansgrohe/Grohe - design i funkcjonalność",
                        "kuchnia": "Blat kwarcowy, fronty lakierowane wysokim połyskiem - wow efekt"
                    },
                    "czas_realny": "6-7 tygodni dla 70m²",
                    "dla_kogo": "Rodziny z dziećmi, osoby ceniące komfort i estetykę",
                    "uwagi_eksperta": "Tu już inwestujemy w detale - listwy, ościeżnice, oświetlenie LED. Różnica widoczna gołym okiem."
                },
                
                "cynamonowy": {
                    "nazwa": "Pakiet Cynamonowy",
                    "cena_za_m2": "2500-3000 zł/m²", 
                    "opis_eksperta": "Premium bez przesady. Materiały, które znają tylko fachowcy. Jakość na dekady.",
                    "materialy_konkretne": {
                        "podłogi": "Parkiet dębowy 15mm (Boen, Kährs) lub płytki wielkoformatowe Porcelanosa",
                        "ściany": "Tynki dekoracyjne, farby mineralne, okładziny drewniane",
                        "łazienka": "Płytki naturalne/techniczne, armatura Villeroy&Boch - luksus na lata",
                        "kuchnia": "Blat z konglomeratu, fronty fornirowane - naturalne piękno"
                    },
                    "czas_realny": "8-10 tygodni dla 90m²",
                    "dla_kogo": "Wymagający klienci, inwestorzy, osoby ceniące unikalne rozwiązania",
                    "uwagi_eksperta": "Każdy detal przemyślany. Instalacje w najwyższym standardzie. To się zwraca."
                },
                
                "szafranowy": {
                    "nazwa": "Pakiet Szafranowy",
                    "cena_za_m2": "3500-4500 zł/m²",
                    "opis_eksperta": "Absolutny top. Materiały, które większość ludzi widzi tylko w magazynach. Dla perfekcjonistów.",
                    "materialy_konkretne": {
                        "podłogi": "Parkiet egzotyczny (Merbau, Wenge) lub płytki marmurowe Carrara",
                        "ściany": "Tynki weneckie, okładziny kamienne, tapety designerskie",
                        "łazienka": "Naturalne kamienie, armatura Dornbracht/Axor - sztuka użytkowa",
                        "kuchnia": "Blaty z naturalnego kamienia, fronty z litego drewna - unikat"
                    },
                    "czas_realny": "10-14 tygodni dla 120m²",
                    "dla_kogo": "Klienci bez kompromisów, apartamenty, domy premium",
                    "uwagi_eksperta": "Tu liczy się każdy milimetr. Rzemiosło na najwyższym poziomie. Efekt na całe życie."
                }
            },
            
            "praktyczne_porady": {
                "wybor_pakietu": {
                    "budżet_do_100k": "Waniliowy - solidnie i rozsądnie",
                    "budżet_100_200k": "Pomarańczowy - najlepszy stosunek jakości do ceny", 
                    "budżet_200_300k": "Cynamonowy - widoczna różnica w jakości",
                    "budżet_powyżej_300k": "Szafranowy - bez kompromisów",
                    "uwaga": "Zawsze lepiej wybrać mniejszy metraż w wyższym standardzie niż duży w niskim"
                },
                
                "harmonogram_realny": {
                    "przygotowanie": "1-2 tygodnie (pozwolenia, dostawy, koordynacja)",
                    "rozbiórka": "2-3 dni (zależy od zakresu)",
                    "instalacje": "1-2 tygodnie (elektryka, hydraulika, ogrzewanie)",
                    "tynki_wylewki": "1 tydzień + 2 tygodnie schnięcia",
                    "wykończenia": "2-4 tygodnie (zależy od pakietu)",
                    "sprzątanie_odbiór": "2-3 dni",
                    "uwaga": "Zawsze dodaj 20% czasu na nieprzewidziane - to norma w branży"
                },
                
                "częste_błędy": {
                    "oszczędzanie_na_instalacjach": "Nigdy nie oszczędzaj na przewodach i rurach - to podstawa",
                    "tanie_płytki": "Lepiej mniej płytek ale dobrych niż dużo tanich",
                    "brak_wentylacji": "W łazience bez okna wentylacja to nie opcja, to konieczność",
                    "za_dużo_kolorów": "Maksymalnie 3 kolory w pomieszczeniu - więcej to chaos",
                    "modne_trendy": "Trendy przechodzą, klasyka zostaje - myśl długoterminowo"
                },
                
                "sekrety_branży": {
                    "najlepszy_czas": "Jesień/zima - ekipy mają więcej czasu, lepsze ceny",
                    "materiały": "Kupuj materiały 10-15% więcej - zawsze coś się zepsuje/zabraknie",
                    "ekipy": "Dobra ekipa to 70% sukcesu - nie wybieraj najtańszej",
                    "kontrola": "Sprawdzaj postępy co 2-3 dni - problemy łatwiej naprawić na bieżąco",
                    "płatności": "Nigdy nie płać z góry więcej niż 30% - to standard branżowy"
                }
            },
            
            "konkretne_odpowiedzi": {
                "ile_kosztuje": {
                    "50m2_waniliowy": "60-75k zł (1200-1500 zł/m²)",
                    "70m2_pomarańczowy": "126-154k zł (1800-2200 zł/m²)", 
                    "90m2_cynamonowy": "225-270k zł (2500-3000 zł/m²)",
                    "120m2_szafranowy": "420-540k zł (3500-4500 zł/m²)",
                    "uwaga": "Ceny zawierają materiały, robociznę i nadzór. Bez mebli i AGD."
                },
                
                "jak_długo": {
                    "małe_mieszkanie_40m2": "4-5 tygodni",
                    "średnie_mieszkanie_70m2": "6-8 tygodni",
                    "duże_mieszkanie_100m2": "8-12 tygodni",
                    "dom_150m2": "12-16 tygodni",
                    "uwaga": "Czas zależy od pakietu, dostępności materiałów i pogody (jeśli dom)"
                },
                
                "co_w_cenie": {
                    "zawsze_w_cenie": [
                        "Projekt wykonawczy",
                        "Wszystkie materiały wykończeniowe", 
                        "Robocizna i nadzór",
                        "Transport materiałów",
                        "Sprzątanie końcowe",
                        "Gwarancja 2 lata"
                    ],
                    "dodatkowo_płatne": [
                        "Meble i AGD",
                        "Projektowanie wnętrz (opcjonalnie)",
                        "Dodatkowe instalacje (klimatyzacja, alarm)",
                        "Zmiany w trakcie realizacji",
                        "Przechowywanie mebli podczas remontu"
                    ]
                }
            },
            
            "lokalne_specyfiki": {
                "warszawa": {
                    "ceny": "+15-20% do standardowych (wysokie koszty logistyki)",
                    "czas": "+1-2 tygodnie (korki, ograniczenia parkowania)",
                    "uwagi": "Potrzebne pozwolenia wspólnoty, ograniczone godziny pracy"
                },
                "kraków": {
                    "ceny": "+10-15% do standardowych",
                    "czas": "standardowy",
                    "uwagi": "Stare kamienice wymagają specjalnego podejścia"
                },
                "gdańsk": {
                    "ceny": "+5-10% do standardowych", 
                    "czas": "standardowy",
                    "uwagi": "Wilgotność - szczególna uwaga na wentylację"
                },
                "mniejsze_miasta": {
                    "ceny": "-10-15% od standardowych",
                    "czas": "+1 tydzień (dojazdy ekip)",
                    "uwagi": "Ograniczona dostępność niektórych materiałów"
                }
            }
        }
    
    def get_expert_answer(self, query: str, intent: str = None) -> str:
        """Eksperckia odpowiedź na podstawie 40-letniego doświadczenia"""
        
        query_lower = query.lower()
        
        # Konkretne pytania o ceny
        if any(word in query_lower for word in ['ile kosztuje', 'jaka cena', 'koszt']):
            return self._answer_about_costs(query_lower)
        
        # Pytania o czas
        elif any(word in query_lower for word in ['jak długo', 'ile czasu', 'kiedy']):
            return self._answer_about_time(query_lower)
        
        # Pytania o pakiety
        elif any(word in query_lower for word in ['pakiet', 'standard', 'jakość']):
            return self._answer_about_packages(query_lower)
        
        # Pytania o materiały
        elif any(word in query_lower for word in ['materiał', 'płytki', 'podłogi', 'farba']):
            return self._answer_about_materials(query_lower)
        
        # Porady praktyczne
        elif any(word in query_lower for word in ['co wybrać', 'który lepszy', 'polecasz']):
            return self._give_practical_advice(query_lower)
        
        # Lokalizacja
        elif any(city in query_lower for city in ['warszawa', 'kraków', 'gdańsk', 'poznań']):
            return self._answer_about_location(query_lower)
        
        else:
            return self._general_expert_response()
    
    def _answer_about_costs(self, query: str) -> str:
        """Konkretne odpowiedzi o kosztach"""
        
        if '50' in query or 'małe' in query:
            return """💰 **Koszt wykończenia 50m² - konkretnie:**

🟡 **Waniliowy:** 60-75k zł (1200-1500 zł/m²)
- Solidnie, bez fajerwerków, będzie służyć lata

🟠 **Pomarańczowy:** 90-110k zł (1800-2200 zł/m²)  
- Złoty środek - widać różnicę, nie przepłacasz

🟤 **Cynamonowy:** 125-150k zł (2500-3000 zł/m²)
- Premium materiały, efekt na dekady

**Moja rada:** Dla 50m² polecam Pomarańczowy - najlepszy stosunek jakości do ceny.

**W cenie:** materiały, robocizna, nadzór, gwarancja 2 lata
**Dodatkowo:** meble, AGD, ewentualne zmiany w trakcie

Chcesz konkretną wycenę? Potrzebuję poznać Twoje mieszkanie."""
        
        elif '70' in query or 'średnie' in query:
            return """💰 **Koszt wykończenia 70m² - realne ceny:**

🟡 **Waniliowy:** 84-105k zł 
- Podstawa done right - sprawdzone rozwiązania

🟠 **Pomarańczowy:** 126-154k zł
- **← Mój faworyt dla tej wielkości**

🟤 **Cynamonowy:** 175-210k zł
- Jeśli budżet pozwala - widoczna różnica

**Eksperckia rada:** 70m² to idealna wielkość na Pomarańczowy. Materiały premium, ale bez przesady. Efekt wow gwarantowany.

**Sekret:** Lepiej zrobić 70m² w Pomarańczowym niż 90m² w Waniliowym.

Masz konkretny budżet? Dopasujemy pakiet do Twoich możliwości."""
        
        else:
            return """💰 **Realne koszty wykończenia (2024):**

**Za metr kwadratowy:**
🟡 Waniliowy: 1200-1500 zł/m²
🟠 Pomarańczowy: 1800-2200 zł/m²  
🟤 Cynamonowy: 2500-3000 zł/m²
🟫 Szafranowy: 3500-4500 zł/m²

**Przykłady konkretne:**
• 50m² Pomarańczowy: ~100k zł
• 70m² Cynamonowy: ~200k zł
• 90m² Szafranowy: ~360k zł

**40 lat doświadczenia mówi:** 
Nie oszczędzaj na instalacjach. Lepiej mniejszy metraż w wyższym standardzie.

**Warszawa +20%, Kraków +15%, mniejsze miasta -15%**

Podaj metraż - dam Ci konkretną kalkulację."""
    
    def _answer_about_time(self, query: str) -> str:
        """Realistyczne czasy realizacji"""
        
        return """⏰ **Realne czasy wykończenia (z 40-letnim doświadczeniem):**

**Małe mieszkanie (40-50m²):** 4-6 tygodni
**Średnie mieszkanie (60-80m²):** 6-8 tygodni  
**Duże mieszkanie (90-120m²):** 8-12 tygodni
**Dom (150m²+):** 12-16 tygodni

**Etapy (przykład 70m²):**
• Przygotowanie i dostawy: 1-2 tygodnie
• Rozbiórka: 2-3 dni
• Instalacje (prąd, woda): 1-2 tygodnie
• Tynki i wylewki: 1 tydzień + 2 tygodnie schnięcia
• Wykończenia: 2-4 tygodnie
• Sprzątanie: 2-3 dni

**Sekret branży:** Zawsze dodaj 20% czasu na nieprzewidziane. To norma.

**Najlepszy czas na remont:** Jesień/zima - ekipy mają więcej czasu, lepsze ceny.

**Twoje mieszkanie:** Podaj metraż i pakiet - dam precyzyjny harmonogram."""
    
    def _answer_about_packages(self, query: str) -> str:
        """Eksperckia analiza pakietów"""
        
        if 'waniliowy' in query or 'podstawowy' in query:
            return """🟡 **Pakiet Waniliowy - eksperckia ocena:**

**Dla kogo:** Młode pary, pierwsze mieszkanie, budżet do 100k
**Moja ocena:** Solidnie i rozsądnie - bez fajerwerków, ale wszystko będzie działać przez lata.

**Konkretne materiały:**
• Podłogi: Panele Kronotex/Egger 8mm - wytrzymałe, łatwe w utrzymaniu
• Ściany: Farba Dulux/Tikkurila - można myć, nie żółknie  
• Łazienka: Płytki 30x60cm, armatura Koło - sprawdzone marki
• Kuchnia: Blat laminowany, fronty MDF - praktyczne

**Sekret:** Nie oszczędzamy na instalacjach - to podstawa. Estetyka prosta ale ponadczasowa.

**Cena:** 1200-1500 zł/m²
**Czas:** 4-5 tygodni dla 50m²

**Moja rada:** Jeśli budżet ograniczony - śmiało. Lepiej mniejszy metraż w Waniliowym niż większy w tandetzie."""
        
        elif 'pomarańczowy' in query:
            return """🟠 **Pakiet Pomarańczowy - mój osobisty faworyt:**

**Dla kogo:** Rodziny z dziećmi, osoby ceniące komfort i estetykę
**Moja ocena:** Złoty środek - widać różnicę w jakości, ale nie przepłacasz za markę.

**Konkretne materiały:**
• Podłogi: Parkiet 3-warstwowy Barlinek/Tarkett - ciepło i elegancja
• Ściany: Farby premium + akcenty (kamień, tapeta strukturalna)
• Łazienka: Płytki 60x120cm, armatura Hansgrohe - design i funkcjonalność  
• Kuchnia: Blat kwarcowy, fronty lakierowane - wow efekt

**Sekret:** Tu już inwestujemy w detale - listwy, ościeżnice, LED. Różnica widoczna gołym okiem.

**Cena:** 1800-2200 zł/m²
**Czas:** 6-7 tygodni dla 70m²

**40 lat doświadczenia:** To najlepszy stosunek jakości do ceny. Polecam w 80% przypadków."""
        
        else:
            return """🏠 **Pakiety NovaHouse - eksperckia analiza:**

🟡 **Waniliowy (1200-1500 zł/m²)**
Solidnie i tanio. Dla pierwszego mieszkania - idealny.

🟠 **Pomarańczowy (1800-2200 zł/m²)**  
**← Mój faworyt.** Najlepszy stosunek jakości do ceny.

🟤 **Cynamonowy (2500-3000 zł/m²)**
Premium bez przesady. Materiały znane tylko fachowcom.

🟫 **Szafranowy (3500-4500 zł/m²)**
Absolutny top. Dla perfekcjonistów bez kompromisów.

**40-letnie doświadczenie mówi:**
• Budżet do 100k → Waniliowy
• Budżet 100-200k → Pomarańczowy ⭐
• Budżet 200-300k → Cynamonowy  
• Budżet 300k+ → Szafranowy

**Sekret:** Lepiej mniejszy metraż w wyższym standardzie niż duży w niskim.

O którym chcesz wiedzieć więcej?"""
    
    def _answer_about_materials(self, query: str) -> str:
        """Konkretne informacje o materiałach"""
        
        return """🔨 **Materiały - konkretnie, bez marketingu:**

**PODŁOGI:**
• Panele: Kronotex, Egger (8mm min.) - 60-120 zł/m²
• Parkiet 3-warstwowy: Barlinek, Tarkett - 150-300 zł/m²  
• LVT premium: Moduleo, Tarkett - 100-200 zł/m²

**ŚCIANY:**
• Farby: Dulux, Tikkurila, Beckers - 25-60 zł/l
• Tynki dekoracyjne: San Marco, Oikos - 80-200 zł/m²

**ŁAZIENKA:**
• Płytki podstawowe: Cersanit, Opoczno - 30-80 zł/m²
• Płytki premium: Tubądzin, Paradyż - 100-300 zł/m²
• Armatura: Koło (podstawa), Hansgrohe (premium)

**KUCHNIA:**
• Blat laminowany: 150-300 zł/mb
• Blat kwarcowy: 800-1500 zł/mb
• Blat z konglomeratu: 1200-2500 zł/mb

**Sekret branży:** Nie kupuj najtańszego, ale nie przepłacaj za markę. Stosunek jakości do ceny to klucz.

**Konkretne pytanie o materiał?** Napisz - doradzę jak fachowiec."""
    
    def _give_practical_advice(self, query: str) -> str:
        """Praktyczne porady eksperta"""
        
        return """💡 **Porady eksperta (40 lat w branży):**

**WYBÓR PAKIETU:**
• Budżet ograniczony → Waniliowy (solidnie i tanio)
• Chcesz jakość → Pomarańczowy (mój faworyt)
• Bez kompromisów → Cynamonowy/Szafranowy

**NAJCZĘSTSZE BŁĘDY:**
❌ Oszczędzanie na instalacjach - to podstawa!
❌ Tanie płytki - lepiej mniej ale dobrych
❌ Brak wentylacji w łazience bez okna
❌ Za dużo kolorów - max 3 w pomieszczeniu
❌ Gonienie za trendami - klasyka zostaje

**SEKRETY BRANŻY:**
✅ Najlepszy czas: jesień/zima (lepsze ceny)
✅ Kup materiały +15% (zawsze coś zabraknie)
✅ Dobra ekipa = 70% sukcesu
✅ Kontroluj postępy co 2-3 dni
✅ Nie płać z góry więcej niż 30%

**ZŁOTA ZASADA:** Lepiej mniejszy metraż w wyższym standardzie niż duży w niskim.

**Konkretne pytanie?** Napisz - doradzę jak ojciec."""
    
    def _answer_about_location(self, query: str) -> str:
        """Odpowiedzi uwzględniające lokalizację"""
        
        if 'warszawa' in query:
            return """🏙️ **Wykończenia w Warszawie - specyfika:**

**CENY:** +15-20% do standardowych (wysokie koszty logistyki)
**CZAS:** +1-2 tygodnie (korki, ograniczenia parkowania)

**PRZYKŁADY:**
• 50m² Pomarańczowy: ~120k zł (zamiast 100k)
• 70m² Cynamonowy: ~240k zł (zamiast 200k)

**UWAGI PRAKTYCZNE:**
• Potrzebne pozwolenia wspólnoty mieszkaniowej
• Ograniczone godziny pracy (8-18, sobota do 15)
• Problem z parkowaniem dla ekip
• Wyższe koszty transportu materiałów

**ZALETY:**
• Najlepsza dostępność materiałów premium
• Duży wybór ekip specjalistycznych
• Szybkie dostawy

**Moja rada:** Planuj +20% budżetu i +2 tygodnie czasu. Warszawa ma swoje prawa.

Konkretny adres? Mogę dokładniej oszacować koszty logistyki."""
        
        elif 'kraków' in query:
            return """🏰 **Wykończenia w Krakowie - co warto wiedzieć:**

**CENY:** +10-15% do standardowych
**CZAS:** Standardowy (może +1 tydzień w centrum)

**SPECYFIKA:**
• Stare kamienice wymagają specjalnego podejścia
• Grube mury - problemy z instalacjami
• Często zabytkowe ograniczenia
• Dobra dostępność materiałów

**PRZYKŁADY:**
• 50m² Pomarańczowy: ~110k zł
• 70m² Cynamonowy: ~220k zł

**UWAGI:**
• W Starym Mieście - konserwator zabytków
• Wąskie uliczki - problem z dostawami
• Wysokie standardy wykonania

**Moja rada:** Kraków to piękne miasto, ale stare budynki mają swoje wymagania. Planuj dokładnie."""
        
        else:
            return """🗺️ **Wykończenia w różnych lokalizacjach:**

**WARSZAWA:** +20% ceny, +2 tygodnie (logistyka)
**KRAKÓW:** +15% ceny, standardowy czas
**GDAŃSK:** +10% ceny, uwaga na wilgotność
**POZNAŃ/WROCŁAW:** +5-10% ceny
**MNIEJSZE MIASTA:** -10-15% ceny, +1 tydzień (dojazdy)

**UNIWERSALNE ZASADY:**
• Duże miasta = wyższe koszty, lepsza dostępność
• Małe miasta = niższe ceny, ograniczona dostępność
• Stare budynki = dodatkowe wyzwania
• Nowe osiedla = standardowa realizacja

**Sekret:** Lokalizacja wpływa głównie na logistykę, nie na jakość. Dobra ekipa zrobi dobrze wszędzie.

Gdzie planujesz remont? Dam konkretne wskazówki."""
    
    def _general_expert_response(self) -> str:
        """Ogólna odpowiedź eksperta"""
        
        return """👨‍🔧 **Ekspert NovaHouse - 40 lat doświadczenia:**

Jestem tu, żeby dać Ci konkretne odpowiedzi, nie marketingowe bzdury.

**Mogę pomóc z:**
💰 **Realnymi cenami** - bez ukrytych kosztów
⏰ **Prawdziwymi terminami** - z doświadczenia, nie z marzeń  
🔨 **Wyborem materiałów** - co naprawdę warto kupić
📋 **Praktycznymi poradami** - jak uniknąć błędów
🏠 **Doborem pakietu** - do Twojego budżetu i potrzeb

**Przykłady konkretnych pytań:**
• "Ile kosztuje wykończenie 70m² w Warszawie?"
• "Który pakiet dla młodej pary z budżetem 120k?"
• "Jak długo trwa remont 50m² w Cynamonowym?"
• "Co wybrać: parkiet czy panele?"

**Nie pytaj:** "Jaki macie cennik?" 
**Pytaj:** "Ile będzie kosztować moje 65m² w Pomarańczowym?"

**Napisz konkretnie - odpowiem jak fachowiec, nie jak sprzedawca.**"""

# Globalna instancja eksperta
expert = NovaHouseExpert()
