"""
Test scenarios for chatbot conversations
20 different test cases as different clients
"""

TEST_SCENARIOS = [
    {
        "id": 1,
        "name": "Klient zainteresowany pakietem Express",
        "messages": [
            "Dzień dobry",
            "Chcę wycenę na mieszkanie 50m²",
            "Jaki jest najtańszy pakiet?",
            "Ile to będzie kosztować?",
            "Kiedy można zacząć?"
        ],
        "expected_context": {
            "square_meters": 50,
            "package": "Express"
        }
    },
    {
        "id": 2,
        "name": "Klient z budżetem 200k",
        "messages": [
            "Mam budżet 200 tysięcy złotych",
            "Co mogę za to dostać?",
            "Mieszkanie ma 65m²",
            "Jaki pakiet polecacie?"
        ],
        "expected_context": {
            "budget": 200000,
            "square_meters": 65
        }
    },
    {
        "id": 3,
        "name": "Klient z mieszkaniem 50m²",
        "messages": [
            "Mam mieszkanie 50m²",
            "Chcę wycenę",
            "Jaki pakiet będzie najlepszy?",
            "Jestem z Warszawy"
        ],
        "expected_context": {
            "square_meters": 50,
            "city": "Warszawa"
        }
    },
    {
        "id": 4,
        "name": "Klient z Warszawy",
        "messages": [
            "Jestem z Warszawy",
            "Chcę wykończyć mieszkanie",
            "Mam 70m²",
            "Budżet około 150 tysięcy"
        ],
        "expected_context": {
            "city": "Warszawa",
            "square_meters": 70,
            "budget": 150000
        }
    },
    {
        "id": 5,
        "name": "Klient z Wrocławia",
        "messages": [
            "Dzień dobry, jestem z Wrocławia",
            "Mam mieszkanie 60m²",
            "Chcę pakiet Comfort",
            "Ile to będzie kosztować?"
        ],
        "expected_context": {
            "city": "Wrocław",
            "square_meters": 60,
            "package": "Comfort"
        }
    },
    {
        "id": 6,
        "name": "Klient z Trójmiasta",
        "messages": [
            "Jestem z Gdańska",
            "Mam mieszkanie 80m²",
            "Chcę pakiet Premium",
            "Kiedy można zacząć?"
        ],
        "expected_context": {
            "city": "Gdańsk",
            "square_meters": 80,
            "package": "Premium"
        }
    },
    {
        "id": 7,
        "name": "Klient z małego miasta",
        "messages": [
            "Jestem z Radomska",
            "Mam mieszkanie 45m²",
            "Czy działacie w moim mieście?",
            "Chcę wycenę"
        ],
        "expected_context": {
            "city": "Radomsko",
            "square_meters": 45
        }
    },
    {
        "id": 8,
        "name": "Klient z literówkami",
        "messages": [
            "Dzien dobry",
            "Mam mieszkanie 55m2",
            "Jestem z warszawy",
            "Chce pakiet komfort"
        ],
        "expected_context": {
            "square_meters": 55,
            "city": "Warszawa",
            "package": "Comfort"
        }
    },
    {
        "id": 9,
        "name": "Klient używający emotikon",
        "messages": [
            "Dzień dobry! 😊",
            "Mam mieszkanie 50m²",
            "Chcę wycenę 😃",
            "Jestem z Wrocławia 🏠"
        ],
        "expected_context": {
            "square_meters": 50,
            "city": "Wrocław"
        }
    },
    {
        "id": 10,
        "name": "Klient mieszający języki",
        "messages": [
            "Hello, chcę wycenę",
            "Mam apartment 60m²",
            "Jestem z Warsaw",
            "Ile to będzie cost?"
        ],
        "expected_context": {
            "square_meters": 60,
            "city": "Warszawa"
        }
    },
    {
        "id": 11,
        "name": "Klient zmieniający decyzję",
        "messages": [
            "Chcę pakiet Express",
            "A może jednak Comfort?",
            "Albo Premium?",
            "Który będzie najlepszy dla 70m²?"
        ],
        "expected_context": {
            "square_meters": 70
        }
    },
    {
        "id": 12,
        "name": "Klient podający sprzeczne dane",
        "messages": [
            "Mam mieszkanie 50m²",
            "A właściwie 60m²",
            "Albo 55m²",
            "Nie jestem pewien"
        ],
        "expected_context": {
            "square_meters": 55  # Ostatnia podana wartość
        }
    },
    {
        "id": 13,
        "name": "Klient bez podawania danych",
        "messages": [
            "Dzień dobry",
            "Chcę wycenę",
            "Ile to kosztuje?",
            "Kiedy można zacząć?"
        ],
        "expected_context": {}
    },
    {
        "id": 14,
        "name": "Klient pytający o gwarancję",
        "messages": [
            "Jaka jest gwarancja?",
            "Na ile lat?",
            "Co obejmuje?",
            "Mam mieszkanie 65m²"
        ],
        "expected_context": {
            "square_meters": 65
        }
    },
    {
        "id": 15,
        "name": "Klient pytający o czas realizacji",
        "messages": [
            "Ile trwa wykończenie?",
            "Dla pakietu Comfort",
            "Mieszkanie 55m²",
            "Kiedy można zacząć?"
        ],
        "expected_context": {
            "square_meters": 55,
            "package": "Comfort"
        }
    },
    {
        "id": 16,
        "name": "Klient pytający o materiały",
        "messages": [
            "Jakie materiały są w pakiecie?",
            "Czy są wliczone w cenę?",
            "Mam mieszkanie 60m²",
            "Pakiet Premium"
        ],
        "expected_context": {
            "square_meters": 60,
            "package": "Premium"
        }
    },
    {
        "id": 17,
        "name": "Klient chcący umówić spotkanie",
        "messages": [
            "Chcę umówić spotkanie",
            "Mam mieszkanie 70m²",
            "Jestem z Warszawy",
            "Kiedy możemy się spotkać?"
        ],
        "expected_context": {
            "square_meters": 70,
            "city": "Warszawa"
        }
    },
    {
        "id": 18,
        "name": "Klient pytający o konkurencję",
        "messages": [
            "Czym różnicie się od konkurencji?",
            "Dlaczego wybrać was?",
            "Mam mieszkanie 50m²"
        ],
        "expected_context": {
            "square_meters": 50
        }
    },
    {
        "id": 19,
        "name": "Klient z negatywnym feedbackiem",
        "messages": [
            "Słyszałem złe opinie",
            "Czy to prawda?",
            "Chcę wycenę na 60m²"
        ],
        "expected_context": {
            "square_meters": 60
        }
    },
    {
        "id": 20,
        "name": "Klient z bardzo długą rozmową",
        "messages": [
            "Dzień dobry",
            "Mam mieszkanie 55m²",
            "Jestem z Wrocławia",
            "Budżet 200 tysięcy",
            "Chcę pakiet Comfort",
            "Ile to będzie kosztować?",
            "Kiedy można zacząć?",
            "Jaka jest gwarancja?",
            "Co obejmuje pakiet?",
            "Czy materiały są wliczone?",
            "Ile trwa realizacja?",
            "Czy można zmienić coś w trakcie?",
            "Jak wygląda proces?",
            "Czy jest projekt?",
            "Chcę umówić spotkanie"
        ],
        "expected_context": {
            "square_meters": 55,
            "city": "Wrocław",
            "budget": 200000,
            "package": "Comfort"
        }
    }
]

def run_test_scenario(scenario_id: int):
    """
    Run a test scenario and return results
    
    Args:
        scenario_id: ID of scenario (1-20)
    
    Returns:
        dict with test results
    """
    scenario = next((s for s in TEST_SCENARIOS if s["id"] == scenario_id), None)
    if not scenario:
        return {"error": f"Scenario {scenario_id} not found"}
    
    # This would be called from actual test runner
    # For now, return scenario structure
    return {
        "scenario": scenario,
        "status": "ready_to_test"
    }

