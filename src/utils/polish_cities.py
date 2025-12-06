"""
Polish cities declension database
Full list of major Polish cities with grammatical cases
"""


class PolishCities:
    """Database of Polish cities with declension patterns"""

    # Major Polish cities with all cases
    # Format: nominative → {gen: dopełniacz, dat: celownik, inst: narzędnik, loc: miejscownik}
    CITIES = {
        "Warszawa": {
            "gen": "Warszawy",
            "dat": "Warszawie",
            "inst": "Warszawą",
            "loc": "Warszawie",
        },
        "Kraków": {
            "gen": "Krakowa",
            "dat": "Krakowie",
            "inst": "Krakowem",
            "loc": "Krakowie",
        },
        "Wrocław": {
            "gen": "Wrocławia",
            "dat": "Wrocławiowi",
            "inst": "Wrocławiem",
            "loc": "Wrocławiu",
        },
        "Poznań": {
            "gen": "Poznania",
            "dat": "Poznaniowi",
            "inst": "Poznaniem",
            "loc": "Poznaniu",
        },
        "Gdańsk": {
            "gen": "Gdańska",
            "dat": "Gdańskowi",
            "inst": "Gdańskiem",
            "loc": "Gdańsku",
        },
        "Szczecin": {
            "gen": "Szczecina",
            "dat": "Szczecinowi",
            "inst": "Szczecinem",
            "loc": "Szczecinie",
        },
        "Bydgoszcz": {
            "gen": "Bydgoszczy",
            "dat": "Bydgoszczy",
            "inst": "Bydgoszczą",
            "loc": "Bydgoszczy",
        },
        "Lublin": {
            "gen": "Lublina",
            "dat": "Lublinowi",
            "inst": "Lublinem",
            "loc": "Lublinie",
        },
        "Katowice": {
            "gen": "Katowic",
            "dat": "Katowicom",
            "inst": "Katowicami",
            "loc": "Katowicach",
        },
        "Białystok": {
            "gen": "Białegostoku",
            "dat": "Białemustokowi",
            "inst": "Białymstokiem",
            "loc": "Białymstoku",
        },
        "Gdynia": {
            "gen": "Gdyni",
            "dat": "Gdyni",
            "inst": "Gdynią",
            "loc": "Gdyni",
        },
        "Częstochowa": {
            "gen": "Częstochowy",
            "dat": "Częstochowie",
            "inst": "Częstochową",
            "loc": "Częstochowie",
        },
        "Radom": {
            "gen": "Radomia",
            "dat": "Radomiowi",
            "inst": "Radomiem",
            "loc": "Radomiu",
        },
        "Toruń": {
            "gen": "Torunia",
            "dat": "Toruniowi",
            "inst": "Toruniem",
            "loc": "Toruniu",
        },
        "Sosnowiec": {
            "gen": "Sosnowca",
            "dat": "Sosnowcowi",
            "inst": "Sosnowcem",
            "loc": "Sosnowcu",
        },
        "Kielce": {
            "gen": "Kielc",
            "dat": "Kielcom",
            "inst": "Kielcami",
            "loc": "Kielcach",
        },
        "Rzeszów": {
            "gen": "Rzeszowa",
            "dat": "Rzeszowowi",
            "inst": "Rzeszowem",
            "loc": "Rzeszowie",
        },
        "Gliwice": {
            "gen": "Gliwic",
            "dat": "Gliwicom",
            "inst": "Gliwicami",
            "loc": "Gliwicach",
        },
        "Zabrze": {
            "gen": "Zabrza",
            "dat": "Zabrzu",
            "inst": "Zabrzem",
            "loc": "Zabrzu",
        },
        "Olsztyn": {
            "gen": "Olsztyna",
            "dat": "Olsztynowi",
            "inst": "Olsztynem",
            "loc": "Olsztynie",
        },
        "Bielsko-Biała": {
            "gen": "Bielska-Białej",
            "dat": "Bielsku-Białej",
            "inst": "Bielskiem-Białą",
            "loc": "Bielsku-Białej",
        },
        "Bytom": {
            "gen": "Bytomia",
            "dat": "Bytomiowi",
            "inst": "Bytomiem",
            "loc": "Bytomiu",
        },
        "Zielona Góra": {
            "gen": "Zielonej Góry",
            "dat": "Zielonej Górze",
            "inst": "Zieloną Górą",
            "loc": "Zielonej Górze",
        },
        "Rybnik": {
            "gen": "Rybnika",
            "dat": "Rybnikowi",
            "inst": "Rybnikiem",
            "loc": "Rybniku",
        },
        "Ruda Śląska": {
            "gen": "Rudy Śląskiej",
            "dat": "Rudzie Śląskiej",
            "inst": "Rudą Śląską",
            "loc": "Rudzie Śląskiej",
        },
        "Opole": {
            "gen": "Opola",
            "dat": "Opolu",
            "inst": "Opolem",
            "loc": "Opolu",
        },
        "Tychy": {
            "gen": "Tychów",
            "dat": "Tychom",
            "inst": "Tychami",
            "loc": "Tychach",
        },
        "Elbląg": {
            "gen": "Elbląga",
            "dat": "Elblągu",
            "inst": "Elblągiem",
            "loc": "Elblągu",
        },
        "Gorzów Wielkopolski": {
            "gen": "Gorzowa Wielkopolskiego",
            "dat": "Gorzowowi Wielkopolskiemu",
            "inst": "Gorzowem Wielkopolskim",
            "loc": "Gorzowie Wielkopolskim",
        },
        "Płock": {
            "gen": "Płocka",
            "dat": "Płockowi",
            "inst": "Płockiem",
            "loc": "Płocku",
        },
        "Dąbrowa Górnicza": {
            "gen": "Dąbrowy Górniczej",
            "dat": "Dąbrowie Górniczej",
            "inst": "Dąbrową Górniczą",
            "loc": "Dąbrowie Górniczej",
        },
        "Wałbrzych": {
            "gen": "Wałbrzycha",
            "dat": "Wałbrzychowi",
            "inst": "Wałbrzychem",
            "loc": "Wałbrzychu",
        },
        "Włocławek": {
            "gen": "Włocławka",
            "dat": "Włocławkowi",
            "inst": "Włocławkiem",
            "loc": "Włocławku",
        },
        "Tarnów": {
            "gen": "Tarnowa",
            "dat": "Tarnowowi",
            "inst": "Tarnowem",
            "loc": "Tarnowie",
        },
        "Chorzów": {
            "gen": "Chorzowa",
            "dat": "Chorzowowi",
            "inst": "Chorzowem",
            "loc": "Chorzowie",
        },
        "Koszalin": {
            "gen": "Koszalina",
            "dat": "Koszalinowi",
            "inst": "Koszalinem",
            "loc": "Koszalinie",
        },
        "Kalisz": {
            "gen": "Kalisza",
            "dat": "Kaliszowi",
            "inst": "Kaliszem",
            "loc": "Kaliszu",
        },
        "Legnica": {
            "gen": "Legnicy",
            "dat": "Legnicy",
            "inst": "Legnicą",
            "loc": "Legnicy",
        },
        "Grudziądz": {
            "gen": "Grudziądza",
            "dat": "Grudziądzowi",
            "inst": "Grudziądzem",
            "loc": "Grudziądzu",
        },
        "Jaworzno": {
            "gen": "Jaworzna",
            "dat": "Jaworznie",
            "inst": "Jaworznem",
            "loc": "Jaworznie",
        },
        "Słupsk": {
            "gen": "Słupska",
            "dat": "Słupskowi",
            "inst": "Słupskiem",
            "loc": "Słupsku",
        },
        "Jastrzębie-Zdrój": {
            "gen": "Jastrzębia-Zdroju",
            "dat": "Jastrzębiu-Zdroju",
            "inst": "Jastrzębiem-Zdrojem",
            "loc": "Jastrzębiu-Zdroju",
        },
        "Nowy Sącz": {
            "gen": "Nowego Sącza",
            "dat": "Nowemu Sączowi",
            "inst": "Nowym Sączem",
            "loc": "Nowym Sączu",
        },
        "Jelenia Góra": {
            "gen": "Jeleniej Góry",
            "dat": "Jeleniej Górze",
            "inst": "Jelenią Górą",
            "loc": "Jeleniej Górze",
        },
        "Siedlce": {
            "gen": "Siedlec",
            "dat": "Siedlcom",
            "inst": "Siedlcami",
            "loc": "Siedlcach",
        },
        "Mysłowice": {
            "gen": "Mysłowic",
            "dat": "Mysłowicom",
            "inst": "Mysłowicami",
            "loc": "Mysłowicach",
        },
        "Konin": {
            "gen": "Konina",
            "dat": "Koninowi",
            "inst": "Koninem",
            "loc": "Koninie",
        },
        "Piła": {
            "gen": "Piły",
            "dat": "Pile",
            "inst": "Piłą",
            "loc": "Pile",
        },
        "Inowrocław": {
            "gen": "Inowrocławia",
            "dat": "Inowrocławiowi",
            "inst": "Inowrocławiem",
            "loc": "Inowrocławiu",
        },
        "Lubin": {
            "gen": "Lubina",
            "dat": "Lubinowi",
            "inst": "Lubinem",
            "loc": "Lubinie",
        },
        "Ostrów Wielkopolski": {
            "gen": "Ostrowa Wielkopolskiego",
            "dat": "Ostrowowi Wielkopolskiemu",
            "inst": "Ostrowem Wielkopolskim",
            "loc": "Ostrowie Wielkopolskim",
        },
        "Suwałki": {
            "gen": "Suwałk",
            "dat": "Suwałkom",
            "inst": "Suwałkami",
            "loc": "Suwałkach",
        },
        "Stargard": {
            "gen": "Stargardu",
            "dat": "Stargardowi",
            "inst": "Stargardem",
            "loc": "Stargardzie",
        },
        # Additional cities 51-110
        "Gniezno": {
            "gen": "Gniezna",
            "dat": "Gnieznu",
            "inst": "Gnieznem",
            "loc": "Gnieźnie",
        },
        "Piotrków Trybunalski": {
            "gen": "Piotrkowa Trybunalskiego",
            "dat": "Piotrkowowi Trybunalskiemu",
            "inst": "Piotrkowem Trybunalskim",
            "loc": "Piotrkowie Trybunalskim",
        },
        "Starachowice": {
            "gen": "Starachowic",
            "dat": "Starachowicom",
            "inst": "Starachowicami",
            "loc": "Starachowicach",
        },
        "Tomaszów Mazowiecki": {
            "gen": "Tomaszowa Mazowieckiego",
            "dat": "Tomaszowowi Mazowieckiemu",
            "inst": "Tomaszowem Mazowieckim",
            "loc": "Tomaszowie Mazowieckim",
        },
        "Mielec": {
            "gen": "Mielca",
            "dat": "Mielcowi",
            "inst": "Mielcem",
            "loc": "Mielcu",
        },
        "Pabianice": {
            "gen": "Pabianic",
            "dat": "Pabianickom",
            "inst": "Pabianicami",
            "loc": "Pabianicach",
        },
        "Przemyśl": {
            "gen": "Przemyśla",
            "dat": "Przemyślowi",
            "inst": "Przemyślem",
            "loc": "Przemyślu",
        },
        "Zamość": {
            "gen": "Zamościa",
            "dat": "Zamościowi",
            "inst": "Zamościem",
            "loc": "Zamościu",
        },
        "Biała Podlaska": {
            "gen": "Białej Podlaskiej",
            "dat": "Białej Podlaskiej",
            "inst": "Białą Podlaską",
            "loc": "Białej Podlaskiej",
        },
        "Tczew": {
            "gen": "Tczewa",
            "dat": "Tczewowi",
            "inst": "Tczewem",
            "loc": "Tczewie",
        },
        "Chełm": {
            "gen": "Chełma",
            "dat": "Chełmowi",
            "inst": "Chełmem",
            "loc": "Chełmie",
        },
        "Kędzierzyn-Koźle": {
            "gen": "Kędzierzyna-Koźla",
            "dat": "Kędzierzynowi-Koźlu",
            "inst": "Kędzierzynem-Koźlem",
            "loc": "Kędzierzynie-Koźlu",
        },
        "Skierniewice": {
            "gen": "Skierniewic",
            "dat": "Skierniewicom",
            "inst": "Skierniewicami",
            "loc": "Skierniewicach",
        },
        "Racibórz": {
            "gen": "Raciborza",
            "dat": "Raciborzowi",
            "inst": "Raciborzem",
            "loc": "Raciborzu",
        },
        "Ostrowiec Świętokrzyski": {
            "gen": "Ostrowca Świętokrzyskiego",
            "dat": "Ostrowcowi Świętokrzyskiemu",
            "inst": "Ostrowcem Świętokrzyskim",
            "loc": "Ostrowcu Świętokrzyskim",
        },
        "Żory": {
            "gen": "Żor",
            "dat": "Żorom",
            "inst": "Żorami",
            "loc": "Żorach",
        },
        "Puławy": {
            "gen": "Puław",
            "dat": "Puławom",
            "inst": "Puławami",
            "loc": "Puławach",
        },
        "Świdnica": {
            "gen": "Świdnicy",
            "dat": "Świdnicy",
            "inst": "Świdnicą",
            "loc": "Świdnicy",
        },
        "Starogard Gdański": {
            "gen": "Starogardu Gdańskiego",
            "dat": "Starogardowi Gdańskiemu",
            "inst": "Starogardem Gdańskim",
            "loc": "Stargardzie Gdańskim",
        },
        "Ełk": {
            "gen": "Ełku",
            "dat": "Ełkowi",
            "inst": "Ełkiem",
            "loc": "Ełku",
        },
        "Oświęcim": {
            "gen": "Oświęcimia",
            "dat": "Oświęcimiowi",
            "inst": "Oświęcimiem",
            "loc": "Oświęcimiu",
        },
        "Zawiercie": {
            "gen": "Zawiercia",
            "dat": "Zawierciu",
            "inst": "Zawierciem",
            "loc": "Zawierciu",
        },
        "Wołomin": {
            "gen": "Wołomina",
            "dat": "Wołominowi",
            "inst": "Wołominem",
            "loc": "Wołominie",
        },
        "Zgierz": {
            "gen": "Zgierza",
            "dat": "Zgierzowi",
            "inst": "Zgierzem",
            "loc": "Zgierzu",
        },
        "Piaseczno": {
            "gen": "Piaseczna",
            "dat": "Piasecznu",
            "inst": "Piasecznem",
            "loc": "Piasecznie",
        },
        "Sopot": {
            "gen": "Sopotu",
            "dat": "Sopotowi",
            "inst": "Sopotem",
            "loc": "Sopocie",
        },
        "Legionowo": {
            "gen": "Legionowa",
            "dat": "Legionowu",
            "inst": "Legionowem",
            "loc": "Legionowie",
        },
        "Otwock": {
            "gen": "Otwocka",
            "dat": "Otwockowi",
            "inst": "Otwockiem",
            "loc": "Otwocku",
        },
        "Pruszków": {
            "gen": "Pruszkowa",
            "dat": "Pruszkowowi",
            "inst": "Pruszkowem",
            "loc": "Pruszkowie",
        },
        "Piekary Śląskie": {
            "gen": "Piekar Śląskich",
            "dat": "Piekarom Śląskim",
            "inst": "Piekarami Śląskimi",
            "loc": "Piekarach Śląskich",
        },
        "Świdnik": {
            "gen": "Świdnika",
            "dat": "Świdnikowi",
            "inst": "Świdnikiem",
            "loc": "Świdniku",
        },
        "Dębica": {
            "gen": "Dębicy",
            "dat": "Dębicy",
            "inst": "Dębicą",
            "loc": "Dębicy",
        },
        "Tarnobrzeg": {
            "gen": "Tarnobrzega",
            "dat": "Tarnobrzegowi",
            "inst": "Tarnobrzegiem",
            "loc": "Tarnobrzegu",
        },
        "Świętochłowice": {
            "gen": "Świętochłowic",
            "dat": "Świętochłowicom",
            "inst": "Świętochłowicami",
            "loc": "Świętochłowicach",
        },
        "Knurów": {
            "gen": "Knurowa",
            "dat": "Knurowowi",
            "inst": "Knurowem",
            "loc": "Knurowie",
        },
        "Łomża": {
            "gen": "Łomży",
            "dat": "Łomży",
            "inst": "Łomżą",
            "loc": "Łomży",
        },
        "Czechowice-Dziedzice": {
            "gen": "Czechowic-Dziedzic",
            "dat": "Czechowicom-Dziedzicóm",
            "inst": "Czechowicami-Dziedzicami",
            "loc": "Czechowicach-Dziedzicach",
        },
        "Mińsk Mazowiecki": {
            "gen": "Mińska Mazowieckiego",
            "dat": "Mińskowi Mazowieckiemu",
            "inst": "Mińskiem Mazowieckim",
            "loc": "Mińsku Mazowieckim",
        },
        "Będzin": {
            "gen": "Będzina",
            "dat": "Będzinowi",
            "inst": "Będzinem",
            "loc": "Będzinie",
        },
        "Ciechanów": {
            "gen": "Ciechanowa",
            "dat": "Ciechanowowi",
            "inst": "Ciechanowem",
            "loc": "Ciechanowie",
        },
        "Swarzędz": {
            "gen": "Swarzędza",
            "dat": "Swarzędzowi",
            "inst": "Swarzędzem",
            "loc": "Swarzędzu",
        },
        "Sanok": {
            "gen": "Sanoka",
            "dat": "Sanokowi",
            "inst": "Sanokiem",
            "loc": "Sanoku",
        },
        "Bolesławiec": {
            "gen": "Bolesławca",
            "dat": "Bolesławcowi",
            "inst": "Bolesławcem",
            "loc": "Bolesławcu",
        },
        "Augustów": {
            "gen": "Augustowa",
            "dat": "Augustowowi",
            "inst": "Augustowem",
            "loc": "Augustowie",
        },
        "Krosno": {
            "gen": "Krosna",
            "dat": "Krosnu",
            "inst": "Krosnem",
            "loc": "Krośnie",
        },
        "Wejherowo": {
            "gen": "Wejherowa",
            "dat": "Wejherowowi",
            "inst": "Wejherowem",
            "loc": "Wejherowie",
        },
        "Łuków": {
            "gen": "Łukowa",
            "dat": "Łukowowi",
            "inst": "Łukowem",
            "loc": "Łukowie",
        },
        "Kutno": {
            "gen": "Kutna",
            "dat": "Kutnu",
            "inst": "Kutnem",
            "loc": "Kutnie",
        },
        "Sieradz": {
            "gen": "Sieradza",
            "dat": "Sieradzowi",
            "inst": "Sieradzem",
            "loc": "Sieradzu",
        },
        "Szczecinek": {
            "gen": "Szczecinka",
            "dat": "Szczecinku",
            "inst": "Szczecinkiem",
            "loc": "Szczecinku",
        },
        "Grodzisk Mazowiecki": {
            "gen": "Grodziska Mazowieckiego",
            "dat": "Grodziskowi Mazowieckiemu",
            "inst": "Grodziskiem Mazowieckim",
            "loc": "Grodzisku Mazowieckim",
        },
        "Kołobrzeg": {
            "gen": "Kołobrzegu",
            "dat": "Kołobrzegowi",
            "inst": "Kołobrzegiem",
            "loc": "Kołobrzegu",
        },
        "Sandomierz": {
            "gen": "Sandomierza",
            "dat": "Sandomierzowi",
            "inst": "Sandomierzem",
            "loc": "Sandomierzu",
        },
        "Września": {
            "gen": "Wrześni",
            "dat": "Wrześni",
            "inst": "Wrześnią",
            "loc": "Wrześni",
        },
    }

    @classmethod
    def normalize_city_name(cls, city: str) -> str:
        """Normalize city name to proper case"""
        if not city:
            return city
        city_clean = city.strip().title()
        # Check if it's in our database (case-insensitive)
        for known_city in cls.CITIES.keys():
            if known_city.lower() == city_clean.lower():
                return known_city
        return city_clean

    @classmethod
    def get_city_case(cls, city: str, case: str) -> str:
        """
        Get city name in specific grammatical case

        Args:
            city: City name (e.g., "Warszawa", "warszawa")
            case: Grammatical case - 'gen'|'dat'|'inst'|'loc'

        Returns:
            Declined city name or original if not found
        """
        if not city:
            return city

        city_normalized = cls.normalize_city_name(city)
        case_lower = case.lower()

        if city_normalized in cls.CITIES:
            return cls.CITIES[city_normalized].get(case_lower, city_normalized)

        # Fallback: try basic rule for -a ending cities (feminine pattern)
        if city_normalized.endswith("a"):
            if case_lower == "gen":
                return city_normalized[:-1] + "y"
            if case_lower == "dat":
                return city_normalized[:-1] + "ie"
            if case_lower == "inst":
                return city_normalized[:-1] + "ą"
            if case_lower == "loc":
                return city_normalized[:-1] + "ie"

        # Fallback: consonant-ending cities (masculine pattern)
        if case_lower == "gen":
            return city_normalized + "a"
        if case_lower == "dat":
            return city_normalized + "owi"
        if case_lower == "inst":
            return city_normalized + "em"
        if case_lower == "loc":
            return city_normalized + "u"

        return city_normalized

    @classmethod
    def is_polish_city(cls, city: str) -> bool:
        """Check if city is in Polish cities database"""
        if not city:
            return False
        city_normalized = cls.normalize_city_name(city)
        return city_normalized in cls.CITIES

    @classmethod
    def get_all_cities(cls) -> list:
        """Get list of all cities in database"""
        return list(cls.CITIES.keys())


# Example usage
if __name__ == "__main__":
    test_cities = ["warszawa", "Kraków", "POZNAŃ", "gdańsk", "Wrocław"]

    print("Polish Cities Declension Test:")
    print("=" * 80)

    for city in test_cities:
        normalized = PolishCities.normalize_city_name(city)
        gen = PolishCities.get_city_case(city, "gen")
        dat = PolishCities.get_city_case(city, "dat")
        inst = PolishCities.get_city_case(city, "inst")
        loc = PolishCities.get_city_case(city, "loc")
        is_known = PolishCities.is_polish_city(city)

        print(f"{city:15} → {normalized:15}")
        print(f"  Gen: {gen:20} Dat: {dat:20}")
        print(f"  Inst: {inst:20} Loc: {loc:20}")
        print(f"  Known city: {is_known}")
        print()
