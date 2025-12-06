"""
Tests for Polish declension system (names, surnames, cities)
"""

from src.utils.polish_cities import PolishCities
from src.utils.polish_declension import PolishDeclension


class TestPolishDeclension:
    """Test Polish name declension"""

    def test_male_name_vocative(self):
        """Test Polish male names in vocative case"""
        assert PolishDeclension.decline_name_vocative("Marcin") == "Marcinie"
        assert PolishDeclension.decline_name_vocative("Paweł") == "Pawle"
        assert PolishDeclension.decline_name_vocative("Piotr") == "Piotrze"
        assert PolishDeclension.decline_name_vocative("Jan") == "Janie"

    def test_female_name_vocative(self):
        """Test Polish female names in vocative case"""
        assert PolishDeclension.decline_name_vocative("Maria") == "Mario"
        assert PolishDeclension.decline_name_vocative("Anna") == "Anno"
        assert PolishDeclension.decline_name_vocative("Katarzyna") == "Katarzyno"
        assert PolishDeclension.decline_name_vocative("Zofia") == "Zofio"

    def test_foreign_name_unchanged(self):
        """Test foreign names are not declined"""
        assert PolishDeclension.decline_name_vocative("Alex") == "Alex"
        assert PolishDeclension.decline_name_vocative("John") == "John"
        assert PolishDeclension.decline_name_vocative("Michael") == "Michael"
        assert PolishDeclension.decline_name_vocative("Emma") == "Emma"

    def test_full_name_vocative(self):
        """Test full name declension (first name only)"""
        assert PolishDeclension.decline_full_name("Marcin Kowalski") == "Marcinie Kowalski"
        assert PolishDeclension.decline_full_name("Maria Nowak") == "Mario Nowak"
        assert PolishDeclension.decline_full_name("Alex Smith") == "Alex Smith"

    def test_surname_declension_male(self):
        """Test Polish male surname declension"""
        # -ski ending
        assert PolishDeclension.decline_surname_case("Kowalski", "male", "gen") == "Kowalskiego"
        assert PolishDeclension.decline_surname_case("Kowalski", "male", "dat") == "Kowalskiemu"
        assert PolishDeclension.decline_surname_case("Kowalski", "male", "inst") == "Kowalskim"

        # Consonant ending
        assert PolishDeclension.decline_surname_case("Nowak", "male", "gen") == "Nowaka"
        assert PolishDeclension.decline_surname_case("Nowak", "male", "dat") == "Nowakowi"
        assert PolishDeclension.decline_surname_case("Nowak", "male", "inst") == "Nowakem"

    def test_surname_declension_female(self):
        """Test Polish female surname declension"""
        # -ska ending
        assert PolishDeclension.decline_surname_case("Kowalska", "female", "gen") == "Kowalskiej"
        assert PolishDeclension.decline_surname_case("Kowalska", "female", "dat") == "Kowalskiej"
        assert PolishDeclension.decline_surname_case("Kowalska", "female", "inst") == "Kowalską"

    def test_full_name_all_cases(self):
        """Test all grammatical cases for full name"""
        cases_male = PolishDeclension.decline_full_name_cases("Marcin Kowalski", "male")
        assert "voc" in cases_male
        assert "gen" in cases_male
        assert "dat" in cases_male
        assert "inst" in cases_male
        assert "Marcinie" in cases_male["voc"]
        assert "Kowalskiego" in cases_male["gen"]

        cases_female = PolishDeclension.decline_full_name_cases("Maria Nowak", "female")
        assert "Mario" in cases_female["voc"]

    def test_is_polish_name(self):
        """Test Polish name detection"""
        assert PolishDeclension.is_polish_name("Marcin") is True
        assert PolishDeclension.is_polish_name("Maria") is True
        assert PolishDeclension.is_polish_name("Alex") is False
        assert PolishDeclension.is_polish_name("John") is False

    def test_detect_gender(self):
        """Test gender detection from first name"""
        assert PolishDeclension.detect_gender("Marcin") == "male"
        assert PolishDeclension.detect_gender("Maria") == "female"
        assert PolishDeclension.detect_gender("Paweł") == "male"
        assert PolishDeclension.detect_gender("Katarzyna") == "female"
        assert PolishDeclension.detect_gender("Alex") == "unknown"


class TestPolishCities:
    """Test Polish cities database and declension"""

    def test_normalize_city_name(self):
        """Test city name normalization"""
        assert PolishCities.normalize_city_name("warszawa") == "Warszawa"
        assert PolishCities.normalize_city_name("KRAKÓW") == "Kraków"
        assert PolishCities.normalize_city_name("Poznań") == "Poznań"

    def test_city_genitive(self):
        """Test city names in genitive case (dopełniacz)"""
        assert PolishCities.get_city_case("Warszawa", "gen") == "Warszawy"
        assert PolishCities.get_city_case("Kraków", "gen") == "Krakowa"
        assert PolishCities.get_city_case("Poznań", "gen") == "Poznania"

    def test_city_dative(self):
        """Test city names in dative case (celownik)"""
        assert PolishCities.get_city_case("Warszawa", "dat") == "Warszawie"
        assert PolishCities.get_city_case("Kraków", "dat") == "Krakowie"
        assert PolishCities.get_city_case("Wrocław", "dat") == "Wrocławiowi"

    def test_city_instrumental(self):
        """Test city names in instrumental case (narzędnik)"""
        assert PolishCities.get_city_case("Warszawa", "inst") == "Warszawą"
        assert PolishCities.get_city_case("Kraków", "inst") == "Krakowem"
        assert PolishCities.get_city_case("Gdańsk", "inst") == "Gdańskiem"

    def test_city_locative(self):
        """Test city names in locative case (miejscownik)"""
        assert PolishCities.get_city_case("Warszawa", "loc") == "Warszawie"
        assert PolishCities.get_city_case("Poznań", "loc") == "Poznaniu"
        assert PolishCities.get_city_case("Wrocław", "loc") == "Wrocławiu"

    def test_is_polish_city(self):
        """Test city recognition"""
        assert PolishCities.is_polish_city("Warszawa") is True
        assert PolishCities.is_polish_city("warszawa") is True
        assert PolishCities.is_polish_city("Kraków") is True
        assert PolishCities.is_polish_city("Berlin") is False

    def test_unknown_city_fallback(self):
        """Test fallback for unknown cities"""
        # Should still return something (applying generic rules)
        result = PolishCities.get_city_case("Nieznane", "gen")
        assert result is not None
        assert len(result) > 0

    def test_case_insensitive_lookup(self):
        """Test case-insensitive city lookup"""
        assert PolishCities.get_city_case("WARSZAWA", "gen") == "Warszawy"
        assert PolishCities.get_city_case("warszawa", "gen") == "Warszawy"
        assert PolishCities.get_city_case("WaRsZaWa", "gen") == "Warszawy"

    def test_get_all_cities(self):
        """Test retrieving all cities"""
        cities = PolishCities.get_all_cities()
        assert len(cities) > 0
        assert "Warszawa" in cities
        assert "Kraków" in cities
        assert "Poznań" in cities


class TestDeclensionIntegration:
    """Integration tests for declension in conversational context"""

    def test_greeting_with_polish_name(self):
        """Test greeting message with Polish name"""
        name = "Marcin"
        vocative = PolishDeclension.decline_name_vocative(name)
        greeting = f"Cześć {vocative}!"
        assert greeting == "Cześć Marcinie!"

    def test_greeting_with_foreign_name(self):
        """Test greeting message with foreign name"""
        name = "Alex"
        vocative = PolishDeclension.decline_name_vocative(name)
        greeting = f"Cześć {vocative}!"
        assert greeting == "Cześć Alex!"

    def test_city_in_sentence_genitive(self):
        """Test city usage in sentence (genitive)"""
        city = "Warszawa"
        city_gen = PolishCities.get_city_case(city, "gen")
        sentence = f"Projekty z {city_gen}"
        assert sentence == "Projekty z Warszawy"

    def test_city_in_sentence_locative(self):
        """Test city usage in sentence (locative - w + miejscownik)"""
        city = "Kraków"
        city_loc = PolishCities.get_city_case(city, "loc")
        sentence = f"Mieszkam w {city_loc}"
        assert sentence == "Mieszkam w Krakowie"

    def test_full_name_genitive_usage(self):
        """Test full name in genitive case"""
        cases = PolishDeclension.decline_full_name_cases("Marcin Kowalski", "male")
        sentence = f"Projekt {cases['gen']}"
        assert "Kowalskiego" in sentence

    def test_mixed_polish_foreign_names(self):
        """Test handling mixed Polish and foreign names"""
        polish_name = "Marcin"
        foreign_name = "Alex"

        assert PolishDeclension.is_polish_name(polish_name) is True
        assert PolishDeclension.is_polish_name(foreign_name) is False

        voc_polish = PolishDeclension.decline_name_vocative(polish_name)
        voc_foreign = PolishDeclension.decline_name_vocative(foreign_name)

        assert voc_polish == "Marcinie"
        assert voc_foreign == "Alex"
