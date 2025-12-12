"""
Polish Name Declension Helper
Automatically declines Polish first names to vocative case (wołacz)
"""


class PolishDeclension:
    """Helper for Polish name declension"""

    # Common Polish male first names - vocative case mapping
    MALE_NAMES = {
        "Adam": "Adamie",
        "Adrian": "Adrianie",
        "Andrzej": "Andrzeju",
        "Arkadiusz": "Arkadiuszu",
        "Bartosz": "Bartoszu",
        "Bogdan": "Bogdanie",
        "Bolesław": "Bolesławie",
        "Damian": "Damianie",
        "Daniel": "Danielu",
        "Dariusz": "Dariuszu",
        "Dawid": "Dawidzie",
        "Dominik": "Dominiku",
        "Emil": "Emilu",
        "Ernest": "Erneście",
        "Filip": "Filipie",
        "Franciszek": "Franciszku",
        "Grzegorz": "Grzegorzu",
        "Henryk": "Henryku",
        "Hubert": "Hubercie",
        "Ignacy": "Ignacy",
        "Igor": "Igorze",
        "Jacek": "Jacku",
        "Jakub": "Jakubie",
        "Jan": "Janie",
        "Janusz": "Januszu",
        "Jarosław": "Jarosławie",
        "Jerzy": "Jerzy",
        "Józef": "Józefie",
        "Kacper": "Kacprze",
        "Kamil": "Kamilu",
        "Karol": "Karolu",
        "Konrad": "Konradzie",
        "Krystian": "Krystianie",
        "Krzysztof": "Krzysztofie",
        "Leszek": "Leszku",
        "Łukasz": "Łukaszu",
        "Maciej": "Macieju",
        "Maksymilian": "Maksymilianie",
        "Marcin": "Marcinie",
        "Marek": "Marku",
        "Mariusz": "Mariuszu",
        "Mateusz": "Mateuszu",
        "Michał": "Michale",
        "Mieczysław": "Mieczysławie",
        "Mikołaj": "Mikołaju",
        "Mirosław": "Mirosławie",
        "Patryk": "Patryku",
        "Paweł": "Pawle",
        "Piotr": "Piotrze",
        "Przemysław": "Przemysławie",
        "Radosław": "Radosławie",
        "Rafał": "Rafale",
        "Robert": "Robercie",
        "Roman": "Romanie",
        "Sebastian": "Sebastianie",
        "Sławomir": "Sławomirze",
        "Stanisław": "Stanisławie",
        "Stefan": "Stefanie",
        "Szymon": "Szymonie",
        "Tadeusz": "Tadeuszu",
        "Tomasz": "Tomaszu",
        "Waldemar": "Waldemarze",
        "Wiesław": "Wiesławie",
        "Witold": "Witoldzie",
        "Władysław": "Władysławie",
        "Wojciech": "Wojciechu",
        "Zbigniew": "Zbigniewie",
        "Zdzisław": "Zdzisławie",
    }

    # Common Polish female first names - vocative case mapping
    FEMALE_NAMES = {
        "Agata": "Agato",
        "Agnieszka": "Agnieszko",
        "Aleksandra": "Aleksandro",
        "Alicja": "Alicjo",
        "Amelia": "Amelio",
        "Angelika": "Angeliko",
        "Anna": "Anno",
        "Antonina": "Antonino",
        "Barbara": "Barbaro",
        "Beata": "Beato",
        "Bogna": "Bogno",
        "Cecylia": "Cecylio",
        "Dagmara": "Dagmaro",
        "Danuta": "Danuto",
        "Dominika": "Dominiko",
        "Dorota": "Doroto",
        "Edyta": "Edyto",
        "Eliza": "Elizo",
        "Elżbieta": "Elżbieto",
        "Emilia": "Emilio",
        "Ewa": "Ewo",
        "Gabriela": "Gabrielo",
        "Grażyna": "Grażyno",
        "Halina": "Halino",
        "Hanna": "Hanno",
        "Helena": "Heleno",
        "Ilona": "Ilono",
        "Irena": "Ireno",
        "Iwona": "Iwono",
        "Izabela": "Izabelo",
        "Jadwiga": "Jadwigo",
        "Joanna": "Joanno",
        "Jolanta": "Jolanto",
        "Julia": "Julio",
        "Justyna": "Justyno",
        "Kamila": "Kamilo",
        "Karina": "Karino",
        "Karolina": "Karolino",
        "Katarzyna": "Katarzyno",
        "Kinga": "Kingo",
        "Klara": "Klaro",
        "Kornelia": "Kornelio",
        "Krystyna": "Krystyno",
        "Laura": "Lauro",
        "Lena": "Leno",
        "Liliana": "Liliano",
        "Lucyna": "Lucyno",
        "Magdalena": "Magdaleno",
        "Maja": "Majo",
        "Małgorzata": "Małgorzato",
        "Marianna": "Marianno",
        "Maria": "Mario",
        "Marlena": "Marleno",
        "Marta": "Marto",
        "Martyna": "Martyno",
        "Matylda": "Matyldo",
        "Monika": "Moniko",
        "Natalia": "Natalio",
        "Nikola": "Nikolo",
        "Nina": "Nino",
        "Olga": "Olgo",
        "Oliwia": "Oliwio",
        "Patrycja": "Patrycjo",
        "Paula": "Paulo",
        "Paulina": "Paulino",
        "Renata": "Renato",
        "Roma": "Romo",
        "Róża": "Różo",
        "Sandra": "Sandro",
        "Sara": "Saro",
        "Sylwia": "Sylwio",
        "Teresa": "Tereso",
        "Urszula": "Urszulo",
        "Wanda": "Wando",
        "Weronika": "Weroniko",
        "Wiktoria": "Wiktorio",
        "Zofia": "Zofio",
        "Zuzanna": "Zuzanno",
    }

    # Foreign names - do NOT decline
    FOREIGN_NAMES = {
        "Alex",
        "Alexander",
        "Andrew",
        "Anthony",
        "Benjamin",
        "Charles",
        "Christopher",
        "David",
        "Edward",
        "George",
        "Henry",
        "Jack",
        "James",
        "John",
        "Joseph",
        "Mark",
        "Matthew",
        "Michael",
        "Nicholas",
        "Patrick",
        "Paul",
        "Peter",
        "Richard",
        "Robert",
        "Samuel",
        "Stephen",
        "Thomas",
        "William",
        "Alice",
        "Amanda",
        "Angela",
        "Barbara",
        "Betty",
        "Carol",
        "Catherine",
        "Deborah",
        "Dorothy",
        "Elizabeth",
        "Emily",
        "Emma",
        "Helen",
        "Jennifer",
        "Jessica",
        "Karen",
        "Laura",
        "Linda",
        "Lisa",
        "Margaret",
        "Mary",
        "Nancy",
        "Patricia",
        "Ruth",
        "Sandra",
        "Sarah",
        "Susan",
        # Additional international names
        "Kevin",
        "Brian",
        "Daniel",
        "Eric",
        "Jason",
        "Justin",
        "Ryan",
        "Sean",
        "Timothy",
        "Brandon",
        "Christian",
        "Dylan",
        "Ethan",
        "Gabriel",
        "Isaac",
        "Jacob",
        "Joshua",
        "Nathan",
        "Oliver",
        "Sebastian",
        "Tyler",
        "Zachary",
        "Hannah",
        "Olivia",
        "Sophia",
        "Isabella",
        "Mia",
        "Charlotte",
        "Amelia",
        "Harper",
        "Evelyn",
        "Abigail",
        "Emily",
        "Madison",
        "Ella",
        "Scarlett",
        "Grace",
        "Chloe",
        "Victoria",
        "Riley",
        "Aria",
        "Lily",
        "Aubrey",
        "Zoe",
    }

    @classmethod
    def decline_foreign_name_vocative(cls, name: str) -> str:
        """
        Decline foreign name to vocative case (wołacz) - zgodnie z polskimi zasadami językowymi
        
        Zasady polskiej odmiany obcojęzycznych imion:
        - Imiona męskie kończące się na spółgłoskę: dodajemy -ie lub -u
        - Imiona żeńskie kończące się na -a: zmieniamy na -o
        - Imiona żeńskie kończące się na -e: dodajemy -o
        
        Args:
            name: Foreign first name (e.g., "Alex", "Michael", "Sarah", "Robert", "David")
        
        Returns:
            Declined name in vocative case (e.g., "Alexie", "Michaelu", "Saro", "Robercie", "Davidzie")
        """
        if not name:
            return name
        
        name_title = name.strip().title()
        name_lower = name_title.lower()
        
        # === IMIONA ŻEŃSKIE (najpierw sprawdzamy -a, -e, -i, -y) ===
        # WAŻNE: Sprawdzamy najpierw specjalne przypadki kończące się na -ah (np. "Sarah")
        # Imiona kończące się na -ah → -o (np. "Sarah" → "Saro")
        if name_lower.endswith("ah"):
            return name_title[:-2] + "o"  # "Sarah" → "Saro"
        
        # Imiona kończące się na -a → -o (np. "Emma" → "Emo")
        if name_lower.endswith("a"):
            # Specjalne przypadki: -ia → -io (np. "Victoria" → "Victorio", "Olivia" → "Olivio")
            if name_lower.endswith("ia") and len(name_lower) > 3:
                return name_title[:-2] + "io"
            # Dla -ya → -yo
            if name_lower.endswith("ya"):
                return name_title[:-2] + "yo"
            # Standardowe -a → -o
            return name_title[:-1] + "o"
        
        # Imiona kończące się na -e → -o lub bez zmian (np. "Alice" → "Alice" lub "Aliceo")
        if name_lower.endswith("e"):
            # Dla krótkich imion (do 5 liter) często bez zmian, dla dłuższych -o
            if len(name_lower) <= 5:
                return name_title  # "Alice" → "Alice"
            else:
                return name_title + "o"  # "Grace" → "Graceo"
        
        # Imiona kończące się na -i → bez zmian (np. "Lily" → "Lily")
        if name_lower.endswith("i"):
            return name_title
        
        # Imiona kończące się na -y → bez zmian (np. "Mary" → "Mary")
        if name_lower.endswith("y"):
            return name_title
        
        # === IMIONA MĘSKIE (kończące się na spółgłoskę) ===
        # WAŻNE: Sprawdzamy TYLKO jeśli NIE kończy się na samogłoskę (już obsłużone wyżej)
        if name_lower[-1] not in "aeiouy":
            # Zasada 1: Imiona kończące się na -t, -d, -r, -l, -n → dodajemy -ie
            # Przykłady: "Robert" → "Robercie", "David" → "Davidzie", "Michael" → "Michaelu" (ale "Michael" kończy się na -l, więc "Michaelu" jest poprawne)
            # WAŻNE: "Michael" w polskim to "Michaelu" (nie "Michaelie"), ale "Robert" to "Robercie"
            
            # Sprawdź końcówki w kolejności od najdłuższych
            # Imiona kończące się na -el, -al, -il → -elu, -alu, -ilu (np. "Michael" → "Michaelu", "Daniel" → "Danielu")
            if name_lower.endswith(("el", "al", "il")):
                return name_title + "u"
            
            # Imiona kończące się na -er, -ar, -ir → -erze, -arze, -irze (np. "Peter" → "Peterze", "Alexander" → "Alexanderze")
            if name_lower.endswith(("er", "ar", "ir")):
                # Dla krótkich imion (do 5 liter) często -u, dla dłuższych -ie
                if len(name_lower) <= 5:
                    return name_title + "u"
                else:
                    return name_title[:-2] + "erze" if name_lower.endswith("er") else name_title[:-2] + "arze" if name_lower.endswith("ar") else name_title[:-2] + "irze"
            
            # Imiona kończące się na -t, -d → -cie, -dzie (np. "Robert" → "Robercie", "David" → "Davidzie")
            if name_lower.endswith("t"):
                return name_title[:-1] + "cie"  # "Robert" → "Robercie"
            if name_lower.endswith("d"):
                return name_title[:-1] + "dzie"  # "David" → "Davidzie"
            
            # Imiona kończące się na -x → -xie (np. "Alex" → "Alexie")
            if name_lower.endswith("x"):
                return name_title + "ie"  # "Alex" → "Alexie"
            
            # Imiona kończące się na -s → -sie (np. "Thomas" → "Thomasie", "James" → "Jamesie")
            if name_lower.endswith("s"):
                # Sprawdź czy kończy się na -mas, -las, -nas, -ras (np. "Thomas" → "Thomasie")
                if name_lower.endswith(("mas", "las", "nas", "ras", "mes", "les", "nes", "res")):
                    return name_title + "ie"  # "Thomas" → "Thomasie", "James" → "Jamesie"
                # Dla innych -s → -sie
                return name_title + "ie"
            
            # Imiona kończące się na -m → -mie (np. "William" → "Williamie")
            if name_lower.endswith("m"):
                # Sprawdź czy kończy się na -iam, -lam, -mam, -ram (np. "William" → "Williamie")
                if name_lower.endswith(("iam", "lam", "mam", "ram", "em", "im", "om", "um")):
                    return name_title + "ie"  # "William" → "Williamie"
                # Dla innych -m → -mie
                return name_title + "ie"
            
            # Imiona kończące się na -r, -l, -n (ale nie -er, -el, -ar, -al) → -rze, -le, -nie lub -u
            if name_lower.endswith("r") and not name_lower.endswith(("er", "ar", "ir")):
                return name_title + "ze"  # "Peter" → "Peterze" (ale już obsłużone wyżej)
            if name_lower.endswith("l") and not name_lower.endswith(("el", "al", "il")):
                return name_title + "e"  # "Paul" → "Paule"
            if name_lower.endswith("n"):
                return name_title + "ie"  # "John" → "Johnie"
            
            # Imiona kończące się na -k, -g, -h → -ku, -gu, -hu (np. "Mark" → "Marku")
            if name_lower.endswith(("k", "g", "h")):
                return name_title + "u"
            
            # Imiona kończące się na -p, -b, -f, -v, -w, -z, -c → -u
            if name_lower.endswith(("p", "b", "f", "v", "w", "z", "c")):
                return name_title + "u"
            
            # Fallback: inne spółgłoski → -u
            return name_title + "u"
        
        # Default: return as-is (niektóre obcojęzyczne imiona nie odmieniają się)
        return name_title

    @classmethod
    def decline_name_vocative(cls, name: str) -> str:
        """
        Decline Polish or foreign first name to vocative case (wołacz)

        Args:
            name: First name (e.g., "Jan", "Maria", "Alex", "Michael")

        Returns:
            Declined name in vocative case (e.g., "Janie", "Mario", "Alexie", "Michaelu")
        """
        if not name:
            return name

        name_title = name.strip().title()

        # Check if it's a foreign name - decline it with simplified rules
        if name_title in cls.FOREIGN_NAMES:
            return cls.decline_foreign_name_vocative(name_title)

        # Check male names
        if name_title in cls.MALE_NAMES:
            return cls.MALE_NAMES[name_title]

        # Check female names
        if name_title in cls.FEMALE_NAMES:
            return cls.FEMALE_NAMES[name_title]

        # Fallback: try to detect if it's foreign by pattern
        # If it doesn't match Polish patterns, try foreign declension
        name_lower = name_title.lower()
        polish_endings = ["ski", "ska", "cki", "cka", "dzki", "dzka", "ak", "ek", "ik", "uk", "czyk", "iak"]
        is_likely_polish = any(name_lower.endswith(ending) for ending in polish_endings)
        
        if not is_likely_polish and name_title not in cls.MALE_NAMES and name_title not in cls.FEMALE_NAMES:
            # Try foreign declension as fallback
            return cls.decline_foreign_name_vocative(name_title)

        # Fallback: return original name if not found
        return name_title

    @classmethod
    def decline_full_name(cls, full_name: str) -> str:
        """
        Decline full name (first name + last name) to vocative case

        Args:
            full_name: Full name (e.g., "Jan Kowalski", "Maria Nowak")

        Returns:
            Declined name (e.g., "Janie Kowalski", "Mario Nowak")
        """
        if not full_name:
            return full_name

        parts = full_name.strip().split()

        if len(parts) == 0:
            return full_name

        # Decline only first name, keep last name as-is for vocative
        # (Polish surnames in vocative case are usually the same as nominative)
        first_name = cls.decline_name_vocative(parts[0])

        if len(parts) == 1:
            return first_name
        else:
            return f"{first_name} {' '.join(parts[1:])}"

    # --- Surname declension (common patterns) ---
    @staticmethod
    def _decline_surname_male(surname: str, case: str) -> str:
        s = surname.strip()
        lower = s.lower()

        # Common adjectival surnames
        adj_pairs = [
            ("ski", {"gen": "skiego", "dat": "skiemu", "inst": "skim"}),
            ("cki", {"gen": "ckiego", "dat": "ckiemu", "inst": "ckim"}),
            ("dzki", {"gen": "dzkiego", "dat": "dzkiemu", "inst": "dzkim"}),
            ("owski", {"gen": "owskiego", "dat": "owskiemu", "inst": "owskim"}),
            ("ewski", {"gen": "ewskiego", "dat": "ewskiemu", "inst": "ewskim"}),
        ]
        for suf, forms in adj_pairs:
            if lower.endswith(suf):
                base = s[: -len(suf)]
                return base + forms[case]

        # Check specific consonant-ending surnames BEFORE generic consonant fallback
        # -czyk endings (e.g., "Paczyk", "Maczyk")
        if lower.endswith("czyk"):
            if case == "gen":
                return s + "a"  # Paczyka
            if case == "dat":
                return s + "owi"  # Paczykowi
            if case == "inst":
                return s + "iem"  # Paczykiem
            if case == "loc":
                return s + "u"  # Paczyku

        # -iak endings (e.g., "Nowiak", "Kowaliak")
        if lower.endswith("iak"):
            if case == "gen":
                return s + "a"  # Nowiaka
            if case == "dat":
                return s + "owi"  # Nowiakowi
            if case == "inst":
                return s + "iem"  # Nowiakiem
            if case == "loc":
                return s + "u"  # Nowiaku

        # -uk endings (e.g., "Kowaluk", "Nowuk", "Bruduk")
        if lower.endswith("uk"):
            if case == "gen":
                return s + "a"  # Kowaluka
            if case == "dat":
                return s + "owi"  # Kowalukowi
            if case == "inst":
                return s + "iem"  # Kowalukiem
            if case == "loc":
                return s + "u"  # Kowaluku

        # Additional common masculine surname endings
        # -icz / -owicz (e.g., "Kowalewicz", "Nowakowicz")
        if lower.endswith("icz") or lower.endswith("owicz"):
            if case == "gen":
                return s + "a"  # Kowalewicza
            if case == "dat":
                return s + "owi"  # Kowalewiczowi
            if case == "inst":
                return s + "em"  # Kowalewiczem
            if case == "loc":
                return s + "u"  # Kowalewiczu

        # Consonant-ending masculine surnames (e.g., "Nowak", "Kowal")
        if lower[-1] not in "aeiouyąęó":
            if case == "gen":
                return s + "a"  # Nowaka
            if case == "dat":
                return s + "owi"  # Nowakowi
            if case == "inst":
                return s + "em"  # Nowakiem
            if case == "loc":
                return s + "u"  # Nowaku

        # Vowel-ending fallback (rare)
        if case == "gen":
            return s + "a"
        if case == "dat":
            return s + "owi"
        if case == "inst":
            return s + "em"
        if case == "loc":
            return s + "u"
        return s

    @staticmethod
    def _decline_surname_female(surname: str, case: str) -> str:
        s = surname.strip()
        lower = s.lower()

        # Common adjectival feminine surnames
        adj_pairs = [
            ("ska", {"gen": "skiej", "dat": "skiej", "inst": "ską", "loc": "skiej"}),
            ("cka", {"gen": "ckiej", "dat": "ckiej", "inst": "cką", "loc": "ckiej"}),
            ("dzka", {"gen": "dzkiej", "dat": "dzkiej", "inst": "dzką", "loc": "dzkiej"}),
            ("owska", {"gen": "owskiej", "dat": "owskiej", "inst": "owską", "loc": "owskiej"}),
            ("ewska", {"gen": "ewskiej", "dat": "ewskiej", "inst": "ewską", "loc": "ewskiej"}),
        ]
        for suf, forms in adj_pairs:
            if lower.endswith(suf):
                base = s[: -len(suf)]
                return base + forms[case]

        # Extended feminine endings: -czyk → -czyk-owa (female form)
        # e.g., "Paczyk" (male) → "Paczyková" (female) → decline to "Paczyková"
        if lower.endswith("czyk") or lower.endswith("iak") or lower.endswith("uk"):
            # For female form, these typically add -owa or stay unchanged with -a ending
            # Most common: Paczyk (m) → Paczyk-owa (f), but often just Paczyk in modern Polish
            if case == "gen":
                return s + "a"  # Paczyka
            if case == "dat":
                return s + "owi"  # Paczykowi (or unchanged if using base form)
            if case == "inst":
                return s + "ą"  # Paczyką
            if case == "loc":
                return s + "u"  # Paczyku

        # Feminine surnames ending with -a (e.g., "Nowakowa" – seldom used, or first names used as surnames)
        if lower.endswith("a"):
            if case == "gen":
                # Maria → Marii pattern (approximation for surname-like forms)
                if s.endswith("ia"):
                    return s[:-2] + "ii"
                return s[:-1] + "y"
            if case == "dat":
                return s[:-1] + "ie"
            if case == "inst":
                return s[:-1] + "ą"
            if case == "loc":
                return s[:-1] + "ie"  # Marii, Anny → Marii, Annie

        # Non-adjectival feminine surnames often stay unchanged except instrumental with -ą
        if case == "gen":
            return s  # e.g., "Nowak" (female) often unchanged in genitive with name context
        if case == "dat":
            return s
        if case == "inst":
            return s + "ą"
        if case == "loc":
            return s + "u" if s[-1] not in "aeiouyąęó" else s  # Nowak → Nowaku, Anna → Annie
        return s

    @classmethod
    def decline_surname_case(cls, surname: str, gender: str, case: str) -> str:
        """
        Decline surname to case: gen (dopełniacz), dat (celownik), inst (narzędnik), loc (miejscownik)

        gender: 'male' | 'female'
        case: 'gen' | 'dat' | 'inst' | 'loc'
        """
        if not surname:
            return surname
        case = case.lower()
        gender = gender.lower()
        if gender == "male":
            return cls._decline_surname_male(surname, case)
        return cls._decline_surname_female(surname, case)

    @classmethod
    def decline_full_name_cases(cls, full_name: str, gender: str) -> dict:
        """
        Return common cases for full name (first name vocative + surname cases)
        { 'voc': 'Janie', 'gen': 'Jana Kowalskiego', 'dat': 'Janowi Kowalskiemu', 'inst': 'Janem Kowalskim' }
        """
        if not full_name:
            return {}
        parts = full_name.strip().split()
        if len(parts) == 0:
            return {}
        first = parts[0]
        last = " ".join(parts[1:]) if len(parts) > 1 else ""

        voc_first = cls.decline_name_vocative(first)

        if last:
            gen_last = cls.decline_surname_case(last, gender, "gen")
            dat_last = cls.decline_surname_case(last, gender, "dat")
            inst_last = cls.decline_surname_case(last, gender, "inst")
            loc_last = cls.decline_surname_case(last, gender, "loc")
        else:
            gen_last = dat_last = inst_last = loc_last = ""

        # First name simple cases (approximation)
        gen_first = (
            first + "a"
            if gender == "male"
            else (first[:-1] + "y" if first.endswith("a") else first)
        )
        dat_first = (
            (first + "owi")
            if gender == "male"
            else (first[:-1] + "ie" if first.endswith("a") else first)
        )
        inst_first = (
            (first + "em")
            if gender == "male"
            else (first[:-1] + "ą" if first.endswith("a") else first)
        )

        # First name locative (miejscownik) - approximation
        loc_first = (
            (first + "u")
            if gender == "male" and first[-1] not in "aeiouyąęó"
            else (first[:-1] + "ie" if first.endswith("a") else first)
        )
        
        return {
            "voc": voc_first if not last else f"{voc_first} {last}",
            "gen": (gen_first if not last else f"{gen_first} {gen_last}").strip(),
            "dat": (dat_first if not last else f"{dat_first} {dat_last}").strip(),
            "inst": (inst_first if not last else f"{inst_first} {inst_last}").strip(),
            "loc": (loc_first if not last else f"{loc_first} {loc_last}").strip(),
        }

    @classmethod
    def is_polish_name(cls, name: str) -> bool:
        """Check if name is Polish (not foreign)"""
        if not name:
            return False

        name_title = name.strip().title()

        if name_title in cls.FOREIGN_NAMES:
            return False

        if name_title in cls.MALE_NAMES or name_title in cls.FEMALE_NAMES:
            return True

        # Check common Polish name patterns
        polish_endings = [
            "ski",
            "ska",
            "cki",
            "cka",
            "dzki",
            "dzka",
            "owski",
            "owska",
            "ewski",
            "ewska",
            "ak",
            "ek",
            "ik",
            "uk",
            "czyk",
            "iak",
            "owicz",
            "ewicz",
            "icz",
        ]

        name_lower = name.lower()
        return any(name_lower.endswith(ending) for ending in polish_endings)

    @classmethod
    def detect_gender(cls, first_name: str) -> str:
        """
        Detect gender from first name

        Returns:
            'male' | 'female' | 'unknown'
        """
        if not first_name:
            return "unknown"

        name_title = first_name.strip().title()

        if name_title in cls.MALE_NAMES:
            return "male"
        if name_title in cls.FEMALE_NAMES:
            return "female"

        # Heuristic: Polish female names typically end with -a
        if name_title.endswith("a") and name_title not in cls.FOREIGN_NAMES:
            return "female"

        # Heuristic: most consonant-ending Polish names are male
        if name_title[-1] not in "aeiouyąęó" and name_title not in cls.FOREIGN_NAMES:
            return "male"

        return "unknown"


# Example usage
if __name__ == "__main__":
    # Test cases
    test_names = [
        "Jan Kowalski",
        "Maria Nowak",
        "Anna Wiśniewska",
        "Piotr",
        "Agnieszka",
        "Alex Smith",
        "John Johnson",
        "Michael",
    ]

    print("Polish Name Declension Test:")
    print("=" * 60)

    for name in test_names:
        declined = PolishDeclension.decline_full_name(name)
        is_polish = PolishDeclension.is_polish_name(name.split()[0])
        print(f"{name:20} → {declined:20} (Polish: {is_polish})")
