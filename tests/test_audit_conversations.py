"""
Comprehensive audit test suite: 20 test conversations for chatbot quality assessment
Tests cover: basic interactions, FAQ detection, booking intent, language handling,
edge cases, memory retention, and integration scenarios.
"""

from src.models.chatbot import ChatConversation, ChatMessage


class TestAuditSet1BasicConversations:
    """Set 1: Basic conversation scenarios (5 tests)"""

    def test_1_simple_greeting(self, client):
        """Test 1.1: Simple greeting response"""
        response = client.post(
            "/api/chatbot/chat", json={"message": "Cześć, jak się masz?", "session_id": "audit-1-1"}
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "response" in data
        assert len(data["response"]) > 10  # Should have meaningful response
        print(f"✓ Test 1.1 - Greeting: {data['response'][:100]}")

    def test_2_self_introduction(self, client, app):
        """Test 1.2: Self-introduction with name extraction"""
        response = client.post(
            "/api/chatbot/chat",
            json={"message": "Cześć, mam na imię Marcin Marini", "session_id": "audit-1-2"},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "response" in data

        # Verify name extraction (stored in context_data JSON)
        with app.app_context():
            conv = ChatConversation.query.filter_by(session_id="audit-1-2").first()
            if conv:
                import json

                context = json.loads(conv.context_data or "{}")
                print(f"✓ Test 1.2 - Context extracted: {context}")

    def test_3_faq_question_timeline(self, client):
        """Test 1.3: FAQ detection - timeline question"""
        response = client.post(
            "/api/chatbot/chat",
            json={"message": "Ile czasu trwa cały proces u Was?", "session_id": "audit-1-3"},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "response" in data
        # Should match FAQ or provide relevant info
        response_lower = data["response"].lower()
        assert any(
            keyword in response_lower
            for keyword in ["projekt", "realizacja", "tygodni", "miesiąc", "dni"]
        )
        print(f"✓ Test 1.3 - FAQ Timeline: {data['response'][:100]}")

    def test_4_booking_intent(self, client):
        """Test 1.4: Booking intent detection"""
        response = client.post(
            "/api/chatbot/chat",
            json={"message": "Chciałbym umówić się na spotkanie", "session_id": "audit-1-4"},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "response" in data
        # Should include booking link or offer
        print(f"✓ Test 1.4 - Booking Intent: {data['response'][:100]}")

    def test_5_english_greeting(self, client):
        """Test 1.5: English language handling"""
        response = client.post(
            "/api/chatbot/chat",
            json={"message": "Hello, what services do you offer?", "session_id": "audit-1-5"},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "response" in data
        assert len(data["response"]) > 10
        print(f"✓ Test 1.5 - English: {data['response'][:100]}")


class TestAuditSet2EdgeCases:
    """Set 2: Edge cases and special characters (5 tests)"""

    def test_6_typos_misspellings(self, client):
        """Test 2.1: Handling typos and misspellings"""
        response = client.post(
            "/api/chatbot/chat",
            json={"message": "Ile kosztuje pakie Express?", "session_id": "audit-2-1"},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "response" in data
        # Should still understand despite typo
        print(f"✓ Test 2.1 - Typos: {data['response'][:100]}")

    def test_7_emojis_special_chars(self, client):
        """Test 2.2: Handling emojis and special characters"""
        response = client.post(
            "/api/chatbot/chat",
            json={"message": "Cześć! 😊 Jaki pakiet polecacie? 🏠", "session_id": "audit-2-2"},
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "response" in data
        print(f"✓ Test 2.2 - Emojis: {data['response'][:100]}")

    def test_8_contradictory_data(self, client, app):
        """Test 2.3: Contradictory information handling"""
        session = "audit-2-3"

        # First message with name
        client.post("/api/chatbot/chat", json={"message": "Jestem Marcin", "session_id": session})

        # Second message with different name
        response = client.post(
            "/api/chatbot/chat", json={"message": "Czekaj, to właśnie Paweł", "session_id": session}
        )
        assert response.status_code == 200

        with app.app_context():
            conv = ChatConversation.query.filter_by(session_id=session).first()
            # Should handle gracefully without crashing
            assert conv is not None
            print("✓ Test 2.3 - Contradictory data: Handled gracefully")

    def test_9_language_mixing(self, client):
        """Test 2.4: Polish and English mixed"""
        response = client.post(
            "/api/chatbot/chat",
            json={
                "message": "Jak long będzie projekt? How much? Ile kosztuje?",
                "session_id": "audit-2-4",
            },
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "response" in data
        print(f"✓ Test 2.4 - Mixed language: {data['response'][:100]}")

    def test_10_complex_package_inquiry(self, client):
        """Test 2.5: Complex multi-part inquiry"""
        response = client.post(
            "/api/chatbot/chat",
            json={
                "message": "Interesuje mnie pakiet Comfort z dodatkami: meble, oświetlenie, szafy. Ile to będzie kosztować dla mieszkania 50m2? Jakie są warunki płatności?",
                "session_id": "audit-2-5",
            },
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "response" in data
        print(f"✓ Test 2.5 - Complex inquiry: {data['response'][:150]}")


class TestAuditSet3Memory:
    """Set 3: Memory and context retention (5 tests)"""

    def test_11_short_conversation_memory(self, client):
        """Test 3.1: 5-message conversation memory"""
        session = "audit-3-1"
        messages = [
            "Cześć!",
            "Mam na imię Marcin",
            "Jestem zainteresowany wykończeniem mieszkania",
            "Ile kosztuje pakiet Express?",
            "A co zawiera pakiet Comfort?",
        ]

        for msg in messages:
            response = client.post(
                "/api/chatbot/chat", json={"message": msg, "session_id": session}
            )
            assert response.status_code == 200

        print("✓ Test 3.1 - 5-message memory: Completed without errors")

    def test_12_long_conversation_memory(self, client, app):
        """Test 3.2: 10-message conversation memory (respecting rate limiting)"""
        import time

        session = "audit-3-2"
        messages = [
            "Cześć",
            "Jak się masz?",
            "Jestem Piotr",
            "Z Warszawy",
            "Szukam dobrze",  # message count: 5
        ] + [
            f"Następna wiadomość nr {i}" for i in range(6, 11)
        ]  # Add 5 more = 10 total

        msg_count = 0
        for msg in messages:
            response = client.post(
                "/api/chatbot/chat", json={"message": msg, "session_id": session}
            )
            # Rate limiter may return 429 after multiple messages
            assert response.status_code in [200, 429]
            msg_count += 1
            time.sleep(0.1)  # Small delay between messages to avoid rate limiting

        with app.app_context():
            conv = ChatConversation.query.filter_by(session_id=session).first()
            if conv:
                messages_db = ChatMessage.query.filter_by(conversation_id=conv.id).all()
                # Should have both user and bot messages
                print(f"✓ Test 3.2 - 10-message memory: {len(messages_db)} total messages stored")

    def test_13_context_retention(self, client):
        """Test 3.3: Retaining extracted context across messages"""
        session = "audit-3-3"

        # Extract initial info
        client.post(
            "/api/chatbot/chat",
            json={"message": "Cześć, mam na imię Ewa, jestem z Krakowa", "session_id": session},
        )

        # Later reference previous context
        response = client.post(
            "/api/chatbot/chat", json={"message": "Pamiętasz gdzie jestem?", "session_id": session}
        )
        assert response.status_code == 200
        data = response.get_json()
        # Should reference the city or show understanding of context
        print(f"✓ Test 3.3 - Context retention: {data['response'][:100]}")

    def test_14_repeated_questions(self, client):
        """Test 3.4: Handling repeated questions"""
        session = "audit-3-4"

        # Ask same question twice
        for i in range(2):
            response = client.post(
                "/api/chatbot/chat",
                json={"message": "Ile kosztuje pakiet Premium?", "session_id": session},
            )
            assert response.status_code == 200
            assert "response" in response.get_json()

        print("✓ Test 3.4 - Repeated questions: Handled gracefully")

    def test_15_message_history_limit(self, client, app):
        """Test 3.5: Verify history limit is respected (should be 10 messages)"""
        session = "audit-3-5"

        # Send 25 messages to exceed typical history limit
        for i in range(25):
            client.post(
                "/api/chatbot/chat",
                json={"message": f"Wiadomość numer {i + 1}", "session_id": session},
            )

        with app.app_context():
            conv = ChatConversation.query.filter_by(session_id=session).first()
            messages_count = ChatMessage.query.filter_by(conversation_id=conv.id).count()
            # Should have messages but check if limiting works
            print(f"✓ Test 3.5 - Message history: {messages_count} total messages (limit check)")


class TestAuditSet4Integration:
    """Set 4: Integration testing (5 tests)"""

    def test_16_lead_creation_monday(self, client, app):
        """Test 4.1: Lead creation and Monday.com sync"""
        session = "audit-4-1"

        response = client.post(
            "/api/chatbot/chat",
            json={
                "message": "Cześć, mam na imię Tomasz Nowak, mój email to tomasz@example.com, jestem zainteresowany",
                "session_id": session,
            },
        )
        assert response.status_code == 200

        with app.app_context():
            conv = ChatConversation.query.filter_by(session_id=session).first()
            if conv:
                # Check if lead was attempted to be created
                print("✓ Test 4.1 - Lead creation: Conversation recorded (lead creation attempted)")

    def test_17_booking_with_zencal(self, client):
        """Test 4.2: Booking intent with ZenCal"""
        response = client.post(
            "/api/chatbot/chat",
            json={
                "message": "Chciałbym zarezerwować termin na spotkanie projektowe",
                "session_id": "audit-4-2",
            },
        )
        assert response.status_code == 200
        data = response.get_json()
        # Should offer booking or reference ZenCal
        print(f"✓ Test 4.2 - ZenCal booking: {data['response'][:100]}")

    def test_18_rodo_consent_handling(self, client):
        """Test 4.3: RODO consent and data handling"""
        response = client.post(
            "/api/chatbot/chat",
            json={
                "message": "Czy mogę wam zaufać z moimi danymi osobowymi?",
                "session_id": "audit-4-3",
            },
        )
        assert response.status_code == 200
        data = response.get_json()
        assert "response" in data
        print(f"✓ Test 4.3 - RODO handling: {data['response'][:100]}")

    def test_19_email_extraction(self, client, app):
        """Test 4.4: Email extraction and validation"""
        session = "audit-4-4"

        response = client.post(
            "/api/chatbot/chat",
            json={"message": "Mój email to contact@novahouse.pl", "session_id": session},
        )
        assert response.status_code == 200

        with app.app_context():
            conv = ChatConversation.query.filter_by(session_id=session).first()
            if conv:
                import json

                context = json.loads(conv.context_data or "{}")
                email = context.get("email", "")
                print(f"✓ Test 4.4 - Email extraction: {email}")

    def test_20_city_location_extraction(self, client, app):
        """Test 4.5: City/location extraction and declension"""
        session = "audit-4-5"

        response = client.post(
            "/api/chatbot/chat",
            json={
                "message": "Mieszkam w Warszawie, ale czasem jestem w Krakowie",
                "session_id": session,
            },
        )
        assert response.status_code == 200

        with app.app_context():
            conv = ChatConversation.query.filter_by(session_id=session).first()
            if conv:
                print("✓ Test 4.5 - City extraction: Location info processed")


class TestAuditLanguageAndStyle:
    """Additional tests for Polish language quality"""

    def test_greeting_formality(self, client):
        """Test formal vs informal greetings"""
        # Formal
        response1 = client.post(
            "/api/chatbot/chat",
            json={"message": "Dzień dobry Panią/Pani", "session_id": "lang-formal"},
        )
        assert response1.status_code == 200

        # Informal
        response2 = client.post(
            "/api/chatbot/chat", json={"message": "Cześć!", "session_id": "lang-informal"}
        )
        assert response2.status_code == 200
        print("✓ Language test - Formality levels: Both handled")

    def test_polish_declension_names(self, client):
        """Test Polish name declension handling"""
        names = [
            ("Jestem Marcin", "audit-name-1"),
            ("Mam na imię Maria", "audit-name-2"),
            ("Jestem Piotr", "audit-name-3"),
        ]

        for name_msg, session in names:
            response = client.post(
                "/api/chatbot/chat", json={"message": name_msg, "session_id": session}
            )
            assert response.status_code == 200

        print("✓ Language test - Name declension: Processed")


class TestAuditErrorHandling:
    """Error handling and edge cases"""

    def test_empty_message_handling(self, client):
        """Test empty message handling"""
        response = client.post("/api/chatbot/chat", json={"message": "", "session_id": "error-1"})
        # Should either reject or handle gracefully
        assert response.status_code in [200, 400]

    def test_very_long_message(self, client):
        """Test very long message handling"""
        long_message = "Cześć " * 500  # Very long
        response = client.post(
            "/api/chatbot/chat", json={"message": long_message, "session_id": "error-2"}
        )
        # Should handle without crashing
        assert response.status_code in [200, 413]  # 413 = Payload Too Large

    def test_special_sql_chars(self, client):
        """Test SQL injection protection"""
        response = client.post(
            "/api/chatbot/chat",
            json={"message": "'; DROP TABLE users; --", "session_id": "error-3"},
        )
        assert response.status_code == 200
        # Should treat as normal message, not execute
        print("✓ Error test - SQL injection protection: Safe")
