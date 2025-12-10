from difflib import SequenceMatcher
from typing import Optional

from src.knowledge.novahouse_info import (
    FAQ,
    PRODUCT_PARTNERS,
    TEAM_INFO,
    WHY_CHOOSE_US,
    get_client_reviews_summary,
    get_package_description,
    get_portfolio_list,
    get_process_overview,
)
from src.models.chatbot import db
from src.models.faq_learning import LearnedFAQ


class FaqService:
    def __init__(self):
        # Inicjalizacja wzorców FAQ w bardziej uporządkowany sposób
        self._initialize_faq_patterns()

    def _initialize_faq_patterns(self):
        """Strukturyzuje wzorce FAQ dla łatwiejszego zarządzania."""
        self.faq_patterns = {
            "roznice_miedzy_pakietami": (
                [
                    "pakiet",
                    "express",
                    "comfort",
                    "premium",
                    "indywidualny",
                    "różnice między",
                    "jaki pakiet",
                ],
                0.50,
            ),
            "jak_dlugo_trwa": (
                [
                    "jak długo",
                    "ile trwa",
                    "czas realizacji",
                    "termin",
                    "ile czasu",
                    "czas wykończenia",
                ],
                0.65,
            ),
            "czy_wlaczone_materialy": (
                ["materiały", "cena obejmuje", "co zawiera", "co dostanę", "co jest w cenie"],
                0.60,
            ),
            "mozna_dostosowac": (
                ["dostosować", "zmienić", "modyfikacja", "elastyczny", "zmiana", "personalizacja"],
                0.60,
            ),
            "gwarancja": (["gwarancja", "rękojmia", "reklamacja", "jak długa gwarancja"], 0.70),
            "dodatkowe_oplaty": (
                [
                    "dodatkowe koszty",
                    "dodatkowe opłaty",
                    "ukryte koszty",
                    "niespodzianki",
                    "dopłaty",
                ],
                0.65,
            ),
            "ile_kosztuje": (
                ["płatność", "zapłata", "koszt", "ile kosztuje", "cena", "wycena", "budżet"],
                0.55,
            ),
            "produkty": (["produkt", "materiały", "wyposażenie", "urządzenia"], 0.55),
            "proces": (
                ["etap", "proces", "przebieg", "jak działacie", "jak to wygląda", "workflow"],
                0.60,
            ),
            "czy_potrzebny_projekt": (["projekt", "potrzebny", "czy", "konieczny"], 0.60),
            "smart_home": (["smart", "automatyka", "inteligentny dom", "automatyzacja"], 0.70),
            "terminowosc": (
                ["terminowo", "na czas", "dotrzymanie", "opóźnienie", "spóźnienie"],
                0.70,
            ),
            "ekipy": (["ekipa", "ekipy", "fachowcy", "wykonawcy", "pracownicy"], 0.70),
            "zakres_uslug": (["zakres", "co robicie", "czym się zajmujecie", "usługi"], 0.70),
            "zabudowy_stolarskie": (
                ["stolars", "zabudow", "meble", "kuchnia na wymiar", "szafa"],
                0.70,
            ),
            "cennik_dodatkowy": (
                ["cennik", "dodatkow", "extra", "niespodzianki", "ukryte koszty"],
                0.70,
            ),
            "po_odbiorze": (["po odbiorze", "po skończeniu", "gotowe", "zakończeni"], 0.70),
            "portfolio": (
                ["realizacj", "portfolio", "przykład", "zdjęcia", "fotki", "referencje"],
                0.70,
            ),
            "opinie": (["opini", "recenzj", "rekomendacj", "co mówią", "feedback"], 0.70),
            "partnerzy": (["partner", "producent", "marka", "firmy"], 0.70),
            "dlaczego_my": (
                ["dlaczego", "czemu wy", "jakie macie przewagi", "co was wyróżnia"],
                0.70,
            ),
            "zespol": (["zespół", "team", "pracownicy", "kto", "agnieszka"], 0.70),
        }
        # Dodaj też obsługę konkretnych pakietów
        for pkg in ["premium", "standard", "luxury"]:
            self.faq_patterns[f"pakiet_{pkg}"] = ([pkg], 0.9)

        self.cities_dict = {
            "poznań": ["poznań", "poznaniu", "poznania"],
            "leszno": ["leszno", "lesznie"],
            "konin": ["konin", "koninie"],
            "piła": ["piła", "pile"],
            "szczecin": ["szczecin", "szczecinie", "szczecina"],
            "świnoujście": ["świnoujście", "świnoujściu"],
            "zielona góra": ["zielona góra", "zielonej góry"],
            "gorzów": ["gorzów", "gorzowie"],
            "gorzów wielkopolski": ["gorzów", "gorzowie"],
            "żagań": ["żagań", "żaganiu"],
            "wrocław": ["wrocław", "wrocławiu", "wrocławia"],
            "wałbrzych": ["wałbrzych", "wałbrzychu"],
            "jelenia góra": ["jelenia góra", "jeleniej góry"],
            "legnica": ["legnica", "legnicy"],
            "opole": ["opole", "opolu"],
            "nysa": ["nysa", "nysie"],
            "bydgoszcz": ["bydgoszcz", "bydgoszczy"],
            "toruń": ["toruń", "toruniu"],
            "włocławek": ["włocławek", "włocławku"],
            "grudziądz": ["grudziądz", "grudziądzu"],
            "łódź": ["łódź", "łodzi"],
            "kalisz": ["kalisz", "kaliszu"],
            "sieradz": ["sieradz", "sieradzu"],
            "piotrków trybunalski": ["piotrków", "piotrkowie"],
            "warszawa": ["warszawa", "warszawie", "warszawy", "warszawą"],
            "radom": ["radom", "radomiu"],
            "ostrołęka": ["ostrołęka"],
            "siedlce": ["siedlce", "siedlcach"],
            "radzymin": ["radzymin", "radzyminie"],
            "olsztyn": ["olsztyn", "olsztynie"],
            "elbląg": ["elbląg", "elblągu"],
            "białystok": ["białystok", "białymstoku"],
            "łomża": ["łomża", "łomży"],
            "suwałki": ["suwałki", "suwałkach"],
            "lublin": ["lublin", "lublinie"],
            "chełm": ["chełm", "chełmie"],
            "biała podlaska": ["biała podlaska", "białej podlaskiej"],
            "zamość": ["zamość", "zamościu"],
            "rzeszów": ["rzeszów", "rzeszowie"],
            "krosno": ["krosno", "krosnach"],
            "sanok": ["sanok", "sanoku"],
            "mielec": ["mielec", "mielcu"],
            "kielce": ["kielce", "kielcach"],
            "busko-zdrój": ["busko-zdrój", "busku-zdroju"],
            "częstochowa": ["częstochowa", "częstochowie"],
            "radomsko": ["radomsko", "radomsku"],
            "katowice": ["katowice", "katowicach"],
            "kraków": ["kraków", "krakowie", "krakowa"],
            "gliwice": ["gliwice", "gliwicach"],
            "zabrze": ["zabrze", "zabrzu"],
            "bytom": ["bytom", "bytomiu"],
            "ruda śląska": ["ruda śląska", "rudzie śląskiej"],
            "myślowice": ["myślowice"],
            "sosnowiec": ["sosnowiec", "sosnowcu"],
            "dąbrowa górnicza": ["dąbrowa", "dabrowa gornicza"],
            "chorzów": ["chorzów", "chorzowie"],
            "tychy": ["tychy", "tychach"],
            "tarnowskie góry": ["tarnowskie góry"],
            "gdańsk": ["gdańsk", "gdańsku", "gdańskiej"],
            "gdynia": ["gdynia", "gdyni"],
            "sopot": ["sopot", "sopocie"],
            "wejherowo": ["wejherowo", "wejherowie"],
            "tczew": ["tczew", "tczewie"],
        }

        self.show_packages_keywords = [
            "jakie macie pakiety",
            "jakie pakiety",
            "co oferujesz",
            "jakie oferujesz",
            "pokaż pakiety",
            "pokaz pakiety",
            "opowiedz o pakietach",
            "chcę poznać pakiety",
        ]
        self.short_confirmations = [
            "tak",
            "chcę",
            "tak chcę",
            "chce",
            "tak chce",
            "pokaz",
            "pokaż",
            "opowiedz",
            "tak pokaz",
            "tak pokaż",
            "jasne",
            "ok",
            "dobra",
        ]
        self.greetings = ["cześć", "dzień dobry", "witam", "hej", "hello", "siema", "elo", "co tam"]
        self.introduction_keywords = ["jestem", "nazywam się", "mam na imię", "to ja"]

    def _similarity(self, a, b):
        """Oblicza podobieństwo między dwoma ciągami znaków (0-1)."""
        return SequenceMatcher(None, a, b).ratio()

    def check_faq(self, message: str) -> Optional[str]:
        """Sprawdza, czy wiadomość pasuje do któregokolwiek ze wzorców FAQ."""
        message_lower = message.lower()

        # 1. Sprawdzenie wzorców z fuzzy matchingiem
        best_match_key = None
        best_score = 0.0
        for key, (keywords, threshold) in self.faq_patterns.items():
            for keyword in keywords:
                if keyword in message_lower:  # Szybka ścieżka
                    best_match_key = key
                    best_score = 1.0
                    break
                score = self._similarity(keyword, message_lower)
                if score > threshold and score > best_score:
                    best_score = score
                    best_match_key = key
            if best_score == 1.0:
                break

        if best_match_key:
            return self._get_faq_response(best_match_key)

        # 2. Sprawdzenie miast
        mentioned_city = self._check_cities(message_lower)
        if mentioned_city or any(
            word in message_lower
            for word in [
                "gdzie",
                "lokalizacja",
                "obszar",
                "region",
                "miasto",
                "mieszkam",
                "jestem z",
            ]
        ):
            city_name = mentioned_city if mentioned_city else "Polsce"
            return f"✅ Super! {city_name} to jeden z naszych głównych rynków. Świetnie tam pracujemy!\n\n🏠 Czy to mieszkanie czy dom? Ile metrów kwadratowych?"

        # 3. Sprawdzenie intencji pokazania pakietów
        if self._wants_packages(message_lower):
            return self._get_packages_overview()

        # 4. Sprawdzenie powitań
        if self._is_greeting(message_lower):
            return f"Cześć! 👋 Jestem asystentem NovaHouse.\n\n📊 ... projektów | ... zadowolonych | ... przed terminem\n\nPomagam w wyborze idealnego pakietu wykończeniowego. Z jakiego jesteś miasta i co planujesz — mieszkanie czy dom?"

        return None

    def _get_faq_response(self, key: str) -> Optional[str]:
        """Pobiera odpowiedź na podstawie klucza FAQ."""
        if key.startswith("pakiet_"):
            pkg_name = key.split("_")[1]
            return get_package_description(pkg_name)

        # Mapowanie kluczy na specjalne funkcje
        special_handlers = {
            "proces": get_process_overview,
            "portfolio": get_portfolio_list,
            "opinie": get_client_reviews_summary,
            "dlaczego_my": lambda: f"💎 DLACZEGO NOVAHOUSE?\n\n"
            + "\n".join([f"✅ {k.title()}: {v}" for k, v in WHY_CHOOSE_US.items()]),
            "zespol": lambda: f"👥 NASZ ZESPÓŁ:\n\n{TEAM_INFO['wiceprezes']['name']} - {TEAM_INFO['wiceprezes']['position']}\n\"{TEAM_INFO['wiceprezes']['quote']}\"\n\n...",
            "partnerzy": lambda: f"🤝 Współpracujemy z najlepszymi producentami:\n\n{', '.join(PRODUCT_PARTNERS)}\n\nTo gwarancja jakości materiałów i trwałości wykończenia!",
            "zakres_uslug": lambda: "Zajmujemy się kompleksowym wykończeniem wnętrz pod klucz... Chcesz poznać szczegóły?",
        }

        if key in special_handlers:
            return special_handlers[key]()

        return FAQ.get(key)

    def _check_cities(self, message_lower: str) -> Optional[str]:
        """Sprawdza wzmianki o miastach."""
        for city, variations in self.cities_dict.items():
            if any(variant in message_lower for variant in variations):
                return city.title()
        return None

    def _wants_packages(self, message_lower: str) -> bool:
        """Sprawdza, czy użytkownik chce zobaczyć pakiety."""
        is_direct_question = any(
            keyword in message_lower for keyword in self.show_packages_keywords
        )
        is_short_confirmation = len(message_lower.split()) <= 3 and any(
            word == message_lower.strip() or word in message_lower
            for word in self.short_confirmations
        )
        return is_direct_question or is_short_confirmation

    def _get_packages_overview(self) -> str:
        """Zwraca ogólny opis pakietów."""
        return (
            "📦 NASZE PAKIETY:\n\n"
            "1️⃣ **EXPRESS** - Szybkie, proste wykończenie\n"
            "2️⃣ **COMFORT** - Standardowe, najchętniej wybierane\n"
            "3️⃣ **PREMIUM** - Podniesiona jakość i materiały\n"
            "4️⃣ **LUXURY** - Luksusowe rozwiązania i design\n"
            "5️⃣ **INDYWIDUALNY** - Projekt dostosowany do Twoich potrzeb\n\n"
            "💡 Każdy pakiet można dostosować do Twojego budżetu i preferencji.\n\n"
            "O który pakiet chciałbyś dowiedzieć się więcej?"
        )

    def _is_greeting(self, message_lower: str) -> bool:
        """Sprawdza, czy wiadomość jest powitaniem (i niczym więcej)."""
        has_greeting = any(greeting in message_lower for greeting in self.greetings)
        has_introduction = any(keyword in message_lower for keyword in self.introduction_keywords)
        return has_greeting and not has_introduction

    def check_learned_faq(self, message: str) -> Optional[str]:
        """Sprawdza, czy wiadomość pasuje do nauczonych wzorców FAQ."""
        try:
            message_lower = message.lower()
            learned_faqs = LearnedFAQ.query.filter_by(is_active=True).all()

            for faq in learned_faqs:
                keywords = faq.question_pattern.lower().split()
                if any(keyword in message_lower for keyword in keywords):
                    faq.usage_count += 1
                    db.session.commit()
                    return faq.answer
            return None
        except Exception as e:
            print(f"[Learned FAQ] Error: {e}")
            # W przypadku błędu bazy danych nie przerywamy działania
            return None


# Globalna instancja serwisu dla łatwego dostępu
faq_service = FaqService()
