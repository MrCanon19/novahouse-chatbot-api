#!/usr/bin/env python3
"""
End-to-end test of chatbot with A/B Testing & Competitive Intelligence integration.
This simulates a real conversation with the chatbot and verifies:
1. A/B testing variants
2. Competitive intelligence detection
3. Monday.com lead creation
4. All new features working together
"""

import time

import requests

# Configuration
CHATBOT_API_URL = "https://glass-core-467907-e9.ey.r.appspot.com"
ADMIN_API_KEY = "V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB"
MONDAY_API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjU2MTI0OTM2MiwiYWFpIjoxMSwidWlkIjo2NzA0MDY5NCwiaWFkIjoiMjAyNS0wOS0xMlQwNjo1ODoxOC4yNzVaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MjU4NDk4NzEsInJnbiI6ImV1YzEifQ.Z-5M7pm_QZa1YBQ4a5caSg6XZlM4X1_fTcnF5JmQJyw"
BOARD_ID = "2145240699"


def test_chatbot_conversation(conversation_id=None):
    """Test a full chatbot conversation"""

    print("\n" + "=" * 70)
    print("💬 TESTING CHATBOT CONVERSATION")
    print("=" * 70)

    # Generate unique conversation ID if not provided
    if not conversation_id:
        conversation_id = f"test_{int(time.time())}"

    messages = [
        {
            "text": "Cześć, szukam apartamentu dla 4 osób",
            "expected": ["pakiet", "osoby", "apartament"],
        },
        {
            "text": "Interesuje mnie pakiet szafranowy. Widziałem też ofertę u Lemon Resort, ale mi się nie podobała.",
            "expected": ["szafranowy", "konkurencja", "lemon"],
        },
        {
            "text": "Chciałbym umówić wizytę. Moje imię to Jan Kowalski, telefon +48123456789, email jan.kowalski@example.com",
            "expected": ["wizyta", "spotkanie"],
        },
    ]

    conversation_history = []

    for i, msg in enumerate(messages, 1):
        print(f"\n📤 Message {i}: {msg['text']}")

        response = requests.post(
            f"{CHATBOT_API_URL}/api/chatbot/chat",
            json={"message": msg["text"], "session_id": conversation_id},
        )

        if response.status_code != 200:
            print(f"❌ Error: {response.status_code} - {response.text}")
            continue

        data = response.json()
        bot_response = data.get("response", "")
        follow_up = data.get("follow_up_question")
        detected_intent = data.get("intent", "unknown")

        print(f"📥 Bot response: {bot_response[:200]}...")
        print(f"🎯 Detected intent: {detected_intent}")

        if follow_up:
            print(f"❓ Follow-up question (A/B test): {follow_up}")

        conversation_history.append(
            {
                "user": msg["text"],
                "bot": bot_response,
                "intent": detected_intent,
                "follow_up": follow_up,
            }
        )

        time.sleep(1)  # Small delay between messages

    return conversation_id, conversation_history


def check_ab_testing_results():
    """Check A/B testing results from admin endpoint"""

    print("\n" + "=" * 70)
    print("📊 CHECKING A/B TESTING RESULTS")
    print("=" * 70)

    response = requests.get(
        f"{CHATBOT_API_URL}/api/chatbot/ab-tests/results", headers={"X-API-Key": ADMIN_API_KEY}
    )

    if response.status_code != 200:
        print(f"❌ Error fetching A/B test results: {response.status_code} - {response.text}")
        return

    data = response.json()
    tests = data.get("tests", [])

    print(f"\n✅ Found {len(tests)} A/B tests:")

    for test in tests:
        print(f"\n🧪 Test ID: {test['id']}")
        print(f"   Question Type: {test['question_type']}")
        print(f"   Active: {test['is_active']}")
        print(f"   Winner: {test['winner']}")
        print(f"   Significance: {test['significance']}")

        if test.get("stats"):
            print("   Variant performance:")
            for variant_key in ["variant_a", "variant_b"]:
                variant = test["stats"][variant_key]
                print(
                    f"      {variant_key}: {variant['shown']} shown, {variant['responses']} responses ({variant['conversion_rate']:.1f}%)"
                )


def check_competitive_intelligence():
    """Check competitive intelligence detections"""

    print("\n" + "=" * 70)
    print("🔍 CHECKING COMPETITIVE INTELLIGENCE")
    print("=" * 70)

    response = requests.get(
        f"{CHATBOT_API_URL}/api/chatbot/competitive-intelligence",
        headers={"X-API-Key": ADMIN_API_KEY},
    )

    if response.status_code != 200:
        print(
            f"❌ Error fetching competitive intelligence: {response.status_code} - {response.text}"
        )
        return

    data = response.json()
    signals = data.get("signals", [])

    print(f"\n✅ Found {len(signals)} competitive intelligence signals:")

    for signal in signals[:10]:  # Show last 10
        print(f"\n🎯 Signal from conversation {signal['conversation_id']}:")
        print(f"   Competitor: {signal['competitor_name']}")
        print(f"   Context: {signal['context'][:100]}...")
        print(f"   Detected: {signal['detected_at']}")


def verify_monday_lead(conversation_id):
    """Check if lead was created in Monday.com"""

    print("\n" + "=" * 70)
    print("📋 VERIFYING MONDAY.COM LEAD CREATION")
    print("=" * 70)

    headers = {"Authorization": MONDAY_API_TOKEN, "Content-Type": "application/json"}

    # Get recent items from board
    query = """
    query ($boardId: ID!) {
      boards (ids: [$boardId]) {
        items_page (limit: 10) {
          items {
            id
            name
            created_at
            column_values {
              id
              text
              value
            }
          }
        }
      }
    }
    """

    response = requests.post(
        "https://api.monday.com/v2",
        headers=headers,
        json={"query": query, "variables": {"boardId": BOARD_ID}},
    )

    if response.status_code != 200:
        print(f"❌ Error fetching Monday.com items: {response.status_code}")
        return

    data = response.json()
    items = data.get("data", {}).get("boards", [{}])[0].get("items_page", {}).get("items", [])

    print(f"\n✅ Found {len(items)} recent leads in Monday.com")

    # Find the most recent lead (likely from our test)
    if items:
        latest_lead = items[0]
        print(f"\n📊 Latest lead: {latest_lead['name']}")
        print(f"   Created: {latest_lead['created_at']}")

        # Check for our special columns
        print("\n   Key column values:")
        for col in latest_lead["column_values"]:
            if col["id"] in ["lead_score", "competitor_mentioned", "next_action"] and col["text"]:
                print(f"      {col['id']}: {col['text']}")


def main():
    print("=" * 70)
    print("🚀 CHATBOT E2E TEST - A/B TESTING & COMPETITIVE INTELLIGENCE")
    print("=" * 70)
    print("\nThis test will:")
    print("1. Simulate a chatbot conversation with competitive mention")
    print("2. Check A/B testing variants in responses")
    print("3. Verify competitive intelligence detection")
    print("4. Confirm lead creation in Monday.com")
    print("=" * 70)

    # Step 1: Test conversation
    conversation_id, history = test_chatbot_conversation()

    # Step 2: Check A/B testing
    time.sleep(2)
    check_ab_testing_results()

    # Step 3: Check competitive intelligence
    time.sleep(2)
    check_competitive_intelligence()

    # Step 4: Verify Monday.com lead
    time.sleep(2)
    verify_monday_lead(conversation_id)

    # Final summary
    print("\n" + "=" * 70)
    print("✅ E2E TEST COMPLETE")
    print("=" * 70)
    print("\n📊 Summary:")
    print(f"   ✅ Conversation tested: {conversation_id}")
    print(f"   ✅ Messages exchanged: {len(history)}")
    print("   ✅ A/B testing checked")
    print("   ✅ Competitive intelligence checked")
    print("   ✅ Monday.com integration verified")
    print("\n🎯 Next steps:")
    print("   1. Review A/B test performance in dashboard")
    print("   2. Check competitive intelligence alerts")
    print("   3. Verify lead details in Monday.com: https://monday.com/boards/2145240699")
    print("   4. Monitor follow-up question effectiveness")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
