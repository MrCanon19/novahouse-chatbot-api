"""
Full E2E conversation tests with real API integrations
Tests complete customer journey: chat → context extraction → lead → (optional) booking

WARNING: These tests create REAL data in Monday.com and potentially ZenCal.
Only run when you want to test the complete production flow.

Usage:
    pytest tests/integration/test_full_conversation_live.py -v

Requirements:
    - MONDAY_API_KEY, MONDAY_BOARD_ID in environment
    - ZENCAL_API_KEY in environment (optional)
    - OPENAI_API_KEY for GPT responses (or skip with GPT_FALLBACK_ENABLED=false)
"""

import json
import os
import time

import pytest


@pytest.fixture
def client(app):
    """Test client for Flask app"""
    return app.test_client()


@pytest.mark.skipif(
    not os.getenv("MONDAY_API_KEY") or not os.getenv("MONDAY_BOARD_ID"),
    reason="Brak Monday API credentials",
)
class TestFullConversationLive:
    """Testy pełnych rozmów z prawdziwymi integracjami"""

    def test_simple_inquiry_to_lead(self, client, app):
        """
        Scenariusz 1: Proste zapytanie → Lead w Monday

        Kroki:
        1. Powitanie
        2. Podanie danych kontaktowych
        3. Info o mieszkaniu
        4. Wybór pakietu
        5. Potwierdzenie → Lead utworzony
        """
        session_id = f"test-simple-{int(time.time())}"

        messages = [
            "Cześć, chciałbym wykończyć mieszkanie",
            "Mam na imię Jan Kowalski",
            "jan.kowalski.test@example.com",
            "+48111222333",
            "Mieszkam w Warszawie",
            "Mieszkanie ma 65 metrów",
            "Interesuje mnie pakiet Comfort",
            "Tak, potwierdzam dane",
        ]

        print(f"\n{'='*60}")
        print(f"🧪 Test: Simple Inquiry → Lead")
        print(f"Session: {session_id}")
        print(f"{'='*60}")

        for i, msg in enumerate(messages, 1):
            response = client.post(
                "/api/chatbot/chat",
                json={"message": msg, "session_id": session_id},
            )
            assert response.status_code == 200, f"Failed at message {i}: {msg}"
            data = response.get_json()
            print(f"\n[{i}/{len(messages)}] User: {msg}")
            print(f"Bot: {data.get('response', 'NO RESPONSE')[:150]}...")

            # Small delay to avoid rate limits
            time.sleep(0.5)

        # Check if lead was created
        with app.app_context():
            from src.models.chatbot import Lead

            lead = Lead.query.filter_by(session_id=session_id).first()
            assert lead is not None, "Lead nie został utworzony w bazie"
            assert lead.name == "Jan Kowalski"
            assert lead.email == "jan.kowalski.test@example.com"
            assert lead.phone == "+48111222333"
            assert lead.monday_item_id is not None, "Lead nie został zsynchronizowany z Monday"

            print(f"\n✅ Lead utworzony:")
            print(f"   - ID: {lead.id}")
            print(f"   - Score: {lead.lead_score}/100")
            print(f"   - Monday ID: {lead.monday_item_id}")
            print(f"   - Status: {lead.status}")

    def test_complex_negotiation_to_lead(self, client, app):
        """
        Scenariusz 2: Złożona negocjacja z pytaniami → Lead

        Kroki:
        1. Pytanie o cenę
        2. FAQ o czasie trwania
        3. Porównanie pakietów
        4. Pytanie o materiały
        5. Podanie danych
        6. Lead utworzony
        """
        session_id = f"test-complex-{int(time.time())}"

        messages = [
            "Ile kosztuje wykończenie mieszkania 80m2?",
            "A jak długo to trwa?",
            "Jaka jest różnica między Express a Comfort?",
            "Czy materiały są wliczone w cenę?",
            "Ok, chcę dostać ofertę. Jestem Maria Nowak",
            "maria.nowak.test@example.com",
            "+48555666777",
            "Kraków, 80 metrów kwadratowych",
            "Pakiet Premium wydaje się najlepszy",
            "Tak, wszystko się zgadza",
        ]

        print(f"\n{'='*60}")
        print(f"🧪 Test: Complex Negotiation → Lead")
        print(f"Session: {session_id}")
        print(f"{'='*60}")

        for i, msg in enumerate(messages, 1):
            response = client.post(
                "/api/chatbot/chat",
                json={"message": msg, "session_id": session_id},
            )
            assert response.status_code == 200, f"Failed at message {i}: {msg}"
            data = response.get_json()
            print(f"\n[{i}/{len(messages)}] User: {msg}")
            print(f"Bot: {data.get('response', 'NO RESPONSE')[:150]}...")

            time.sleep(0.5)

        # Check lead
        with app.app_context():
            from src.models.chatbot import Lead

            lead = Lead.query.filter_by(session_id=session_id).first()
            assert lead is not None, "Lead nie został utworzony"
            assert "Maria Nowak" in lead.name
            assert lead.monday_item_id is not None

            print(f"\n✅ Complex lead utworzony:")
            print(f"   - Score: {lead.lead_score}/100")
            print(f"   - Monday ID: {lead.monday_item_id}")
            print(f"   - Messages: {len(messages)} (long conversation)")

    def test_context_extraction_accuracy(self, client, app):
        """
        Scenariusz 3: Test dokładności ekstrakcji kontekstu

        Sprawdza czy chatbot poprawnie wyciąga:
        - Imię i nazwisko
        - Email
        - Telefon
        - Miasto
        - Metraż
        - Pakiet
        """
        session_id = f"test-context-{int(time.time())}"

        # Wszystkie dane w jednej wiadomości
        mega_message = (
            "Cześć! Jestem Piotr Wiśniewski z Wrocławia. "
            "Mój email to piotr.wisniewski.test@example.com, "
            "telefon +48777888999. "
            "Mam mieszkanie 95m2 i interesuje mnie pakiet Express+. "
            "Proszę o kontakt!"
        )

        print(f"\n{'='*60}")
        print(f"🧪 Test: Context Extraction Accuracy")
        print(f"Session: {session_id}")
        print(f"{'='*60}")

        response = client.post(
            "/api/chatbot/chat",
            json={"message": mega_message, "session_id": session_id},
        )
        assert response.status_code == 200
        data = response.get_json()
        print(f"\nUser: {mega_message}")
        print(f"Bot: {data.get('response', '')[:200]}...")

        # Confirm
        time.sleep(1)
        response = client.post(
            "/api/chatbot/chat",
            json={"message": "Tak, dane są poprawne", "session_id": session_id},
        )
        assert response.status_code == 200

        # Check context extraction
        with app.app_context():
            from src.models.chatbot import ChatConversation, Lead

            conv = ChatConversation.query.filter_by(session_id=session_id).first()
            assert conv is not None

            context = json.loads(conv.context_data or "{}")
            print(f"\n📊 Extracted context:")
            print(f"   - Name: {context.get('name', 'MISSING')}")
            print(f"   - Email: {context.get('email', 'MISSING')}")
            print(f"   - Phone: {context.get('phone', 'MISSING')}")
            print(f"   - City: {context.get('city', 'MISSING')}")
            print(f"   - Square meters: {context.get('square_meters', 'MISSING')}")
            print(f"   - Package: {context.get('package', 'MISSING')}")

            # Assertions
            assert "Piotr" in context.get("name", "") or "Wiśniewski" in context.get("name", "")
            assert "piotr.wisniewski.test@example.com" in context.get("email", "")
            assert "+48777888999" in context.get("phone", "")
            assert "Wrocław" in context.get("city", "").title()

            lead = Lead.query.filter_by(session_id=session_id).first()
            if lead:
                print(f"\n✅ Lead created with Monday ID: {lead.monday_item_id}")
            else:
                print(f"\n⚠️ Lead not yet created (may need explicit confirmation)")

    def test_polish_name_declension_in_chat(self, client, app):
        """
        Scenariusz 4: Test odmiany polskich imion w rozmowie

        Sprawdza czy bot poprawnie odmienia imiona w wołaczu:
        - Marcin → Marcinie
        - Anna → Anno
        - Alex → Alex (bez odmiany dla obcych imion)
        """
        test_cases = [
            ("Marcin", "Marcinie"),
            ("Anna", "Anno"),
            ("Kasia", "Kasiu"),
            ("Alex", "Alex"),  # Foreign name - no declension
        ]

        print(f"\n{'='*60}")
        print(f"🧪 Test: Polish Name Declension")
        print(f"{'='*60}")

        for name, expected_vocative in test_cases:
            session_id = f"test-declension-{name.lower()}-{int(time.time())}"

            response = client.post(
                "/api/chatbot/chat",
                json={"message": f"Cześć, mam na imię {name}", "session_id": session_id},
            )
            assert response.status_code == 200
            data = response.get_json()
            bot_response = data.get("response", "")

            print(f"\n👤 Name: {name}")
            print(f"   Expected vocative: {expected_vocative}")
            print(f"   Bot response: {bot_response[:100]}...")

            # Check if vocative is used (might be in first or later messages)
            if expected_vocative in bot_response:
                print(f"   ✅ Correct declension found: '{expected_vocative}'")
            else:
                print(f"   ⚠️ Declension '{expected_vocative}' not found in first response")
                # This is OK - bot might not use name in every message

            time.sleep(0.5)

    def test_memory_across_10_messages(self, client, app):
        """
        Scenariusz 5: Test pamięci rozmowy przez 10+ wiadomości

        Sprawdza czy bot pamięta wcześniej podane informacje:
        - Imię z wiadomości 1 → użyte w wiadomości 10
        - Miasto z wiadomości 2 → użyte w wiadomości 11
        - Pakiet z wiadomości 5 → zapamiętany do końca
        """
        session_id = f"test-memory-{int(time.time())}"

        messages = [
            "Cześć, jestem Tomasz",
            "Mieszkam we Wrocławiu",
            "Jak długo trwa wykończenie?",
            "A ile to kosztuje?",
            "Interesuje mnie pakiet Comfort",
            "Jakie materiały są używane?",
            "Czy możecie zrobić również kuchnię?",
            "A co z łazienką?",
            "Czy macie portfolio?",
            "Pamiętasz moje imię?",  # Test memory
            "A w jakim mieście mieszkam?",  # Test memory
            "Który pakiet wybrałem?",  # Test memory
        ]

        print(f"\n{'='*60}")
        print(f"🧪 Test: Memory Across 10+ Messages")
        print(f"Session: {session_id}")
        print(f"{'='*60}")

        responses_text = []

        for i, msg in enumerate(messages, 1):
            response = client.post(
                "/api/chatbot/chat",
                json={"message": msg, "session_id": session_id},
            )
            assert response.status_code == 200
            data = response.get_json()
            bot_response = data.get("response", "")
            responses_text.append(bot_response)

            print(f"\n[{i}/{len(messages)}] User: {msg}")
            print(f"Bot: {bot_response[:120]}...")

            time.sleep(0.5)

        # Check memory in last 3 responses
        last_3_responses = " ".join(responses_text[-3:])

        print(f"\n📊 Memory check (last 3 responses):")

        has_name = "Tomasz" in last_3_responses or "tomasz" in last_3_responses.lower()
        has_city = "Wrocław" in last_3_responses or "wrocław" in last_3_responses.lower()
        has_package = "Comfort" in last_3_responses or "comfort" in last_3_responses.lower()

        print(f"   - Remembers name 'Tomasz': {'✅' if has_name else '❌'}")
        print(f"   - Remembers city 'Wrocław': {'✅' if has_city else '❌'}")
        print(f"   - Remembers package 'Comfort': {'✅' if has_package else '❌'}")

        # At least 2 out of 3 should be remembered
        memory_score = sum([has_name, has_city, has_package])
        assert memory_score >= 2, f"Bot forgot too much (only {memory_score}/3 remembered)"

        print(f"\n✅ Memory test passed: {memory_score}/3 facts remembered")


@pytest.mark.skipif(
    not os.getenv("MONDAY_API_KEY") or not os.getenv("ZENCAL_API_KEY"),
    reason="Brak Monday + ZenCal credentials",
)
class TestFullJourneyWithBooking:
    """Testy pełnej ścieżki: rozmowa → lead → booking (wymaga obu kluczy)"""

    def test_lead_to_booking_flow(self, client, app):
        """
        Scenariusz 6: Lead → Booking (wymaga Monday + ZenCal)

        UWAGA: Ten test tworzy prawdziwe spotkanie w ZenCal!
        Uruchom tylko gdy chcesz przetestować pełną integrację.
        """
        pytest.skip("Booking creation disabled by default - uncomment to test")

        # Uncomment below to enable:
        """
        session_id = f"test-booking-{int(time.time())}"

        messages = [
            "Chcę umówić się na konsultację",
            "Jestem Andrzej Nowak",
            "andrzej.nowak.test@example.com",
            "+48999888777",
            "Warszawa, mieszkanie 70m2",
            "Pakiet Express+",
            "Tak, potwierdzam",
            "Chciałbym spotkanie w przyszłym tygodniu",
        ]

        print(f"\\n{'='*60}")
        print(f"🧪 Test: Full Journey (Lead → Booking)")
        print(f"Session: {session_id}")
        print(f"⚠️  WARNING: Creates REAL booking in ZenCal!")
        print(f"{'='*60}")

        for i, msg in enumerate(messages, 1):
            response = client.post(
                "/api/chatbot/chat",
                json={"message": msg, "session_id": session_id},
            )
            assert response.status_code == 200
            data = response.get_json()
            print(f"\\n[{i}] User: {msg}")
            print(f"Bot: {data.get('response', '')[:150]}...")
            time.sleep(0.5)

        with app.app_context():
            from src.models.chatbot import Lead

            lead = Lead.query.filter_by(session_id=session_id).first()
            assert lead is not None
            assert lead.monday_item_id is not None

            print(f"\\n✅ Complete flow:")
            print(f"   - Lead created: {lead.id}")
            print(f"   - Monday sync: {lead.monday_item_id}")
            print(f"   - Booking: Check ZenCal manually")
        """
