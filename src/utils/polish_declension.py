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
        "Bartosz": "Bartoszu",
        "Damian": "Damianie",
        "Daniel": "Danielu",
        "Dawid": "Dawidzie",
        "Filip": "Filipie",
        "Grzegorz": "Grzegorzu",
        "Hubert": "Hubercie",
        "Jacek": "Jacku",
        "Jakub": "Jakubie",
        "Jan": "Janie",
        "Janusz": "Januszu",
        "Jarosław": "Jarosławie",
        "Kamil": "Kamilu",
        "Karol": "Karolu",
        "Krzysztof": "Krzysztofie",
        "Łukasz": "Łukaszu",
        "Maciej": "Macieju",
        "Marcin": "Marcinie",
        "Marek": "Marku",
        "Mateusz": "Mateuszu",
        "Michał": "Michale",
        "Paweł": "Pawle",
        "Piotr": "Piotrze",
        "Radosław": "Radosławie",
        "Robert": "Robercie",
        "Sebastian": "Sebastianie",
        "Stanisław": "Stanisławie",
        "Szymon": "Szymonie",
        "Tomasz": "Tomaszu",
        "Wojciech": "Wojciechu",
        "Zbigniew": "Zbigniewie",
    }

    # Common Polish female first names - vocative case mapping
    FEMALE_NAMES = {
        "Agata": "Agato",
        "Agnieszka": "Agnieszko",
        "Aleksandra": "Aleksandro",
        "Alicja": "Alicjo",
        "Anna": "Anno",
        "Barbara": "Barbaro",
        "Beata": "Beato",
        "Dorota": "Doroto",
        "Ewa": "Ewo",
        "Iwona": "Iwono",
        "Joanna": "Joanno",
        "Justyna": "Justyno",
        "Kamila": "Kamilo",
        "Karolina": "Karolino",
        "Katarzyna": "Katarzyno",
        "Krystyna": "Krystyno",
        "Magdalena": "Magdaleno",
        "Małgorzata": "Małgorzato",
        "Maria": "Mario",
        "Marta": "Marto",
        "Monika": "Moniko",
        "Natalia": "Natalio",
        "Paulina": "Paulino",
        "Renata": "Renato",
        "Teresa": "Tereso",
        "Urszula": "Urszulo",
        "Wanda": "Wando",
        "Zofia": "Zofio",
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
        "Jennifer",
    }

    @classmethod
    def decline_name_vocative(cls, name: str) -> str:
        """
        Decline Polish first name to vocative case (wołacz)

        Args:
            name: First name (e.g., "Jan", "Maria", "Alex")

        Returns:
            Declined name in vocative case (e.g., "Janie", "Mario", "Alex")
        """
        if not name:
            return name

        name_title = name.strip().title()

        # Check if it's a foreign name - return as-is
        if name_title in cls.FOREIGN_NAMES:
            return name_title

        # Check male names
        if name_title in cls.MALE_NAMES:
            return cls.MALE_NAMES[name_title]

        # Check female names
        if name_title in cls.FEMALE_NAMES:
            return cls.FEMALE_NAMES[name_title]

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
                return s + "owi"  # Paczykowii
            if case == "inst":
                return s + "iem"  # Paczykiem

        # -iak endings (e.g., "Nowiak", "Kowaliak")
        if lower.endswith("iak"):
            if case == "gen":
                return s + "a"  # Nowiaka
            if case == "dat":
                return s + "owi"  # Nowiakowii
            if case == "inst":
                return s + "iem"  # Nowiakiem

        # -uk endings (e.g., "Kowaluk", "Nowuk", "Bruduk")
        if lower.endswith("uk"):
            if case == "gen":
                return s + "a"  # Kowaluka
            if case == "dat":
                return s + "owi"  # Kowalukowi
            if case == "inst":
                return s + "iem"  # Kowalukiem

        # Additional common masculine surname endings
        # -icz / -owicz (e.g., "Kowalewicz", "Nowakowicz")
        if lower.endswith("icz") or lower.endswith("owicz"):
            if case == "gen":
                return s + "a"  # Kowalewicza
            if case == "dat":
                return s + "owi"  # Kowalewiczowi
            if case == "inst":
                return s + "em"  # Kowalewiczem

        # Consonant-ending masculine surnames (e.g., "Nowak", "Kowal")
        if lower[-1] not in "aeiouyąęó":
            if case == "gen":
                return s + "a"  # Nowaka
            if case == "dat":
                return s + "owi"  # Nowakowi
            if case == "inst":
                return s + "em"  # Nowakiem

        # Vowel-ending fallback (rare)
        if case == "gen":
            return s + "a"
        if case == "dat":
            return s + "owi"
        if case == "inst":
            return s + "em"
        return s

    @staticmethod
    def _decline_surname_female(surname: str, case: str) -> str:
        s = surname.strip()
        lower = s.lower()

        # Common adjectival feminine surnames
        adj_pairs = [
            ("ska", {"gen": "skiej", "dat": "skiej", "inst": "ską"}),
            ("cka", {"gen": "ckiej", "dat": "ckiej", "inst": "cką"}),
            ("dzka", {"gen": "dzkiej", "dat": "dzkiej", "inst": "dzką"}),
            ("owska", {"gen": "owskiej", "dat": "owskiej", "inst": "owską"}),
            ("ewska", {"gen": "ewskiej", "dat": "ewskiej", "inst": "ewską"}),
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
                return s + "owi"  # Paczykowii (or unchanged if using base form)
            if case == "inst":
                return s + "ą"  # Paczyką

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

        # Non-adjectival feminine surnames often stay unchanged except instrumental with -ą
        if case == "gen":
            return s  # e.g., "Nowak" (female) often unchanged in genitive with name context
        if case == "dat":
            return s
        if case == "inst":
            return s + "ą"
        return s

    @classmethod
    def decline_surname_case(cls, surname: str, gender: str, case: str) -> str:
        """
        Decline surname to case: gen (dopełniacz), dat (celownik), inst (narzędnik)

        gender: 'male' | 'female'
        case: 'gen' | 'dat' | 'inst'
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
        else:
            gen_last = dat_last = inst_last = ""

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

        return {
            "voc": voc_first if not last else f"{voc_first} {last}",
            "gen": (gen_first if not last else f"{gen_first} {gen_last}").strip(),
            "dat": (dat_first if not last else f"{dat_first} {dat_last}").strip(),
            "inst": (inst_first if not last else f"{inst_first} {inst_last}").strip(),
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
