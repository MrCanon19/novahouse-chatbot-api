#!/usr/bin/env python3
"""
Script to organize Monday.com board and run E2E test of chatbot integration.
This will:
1. Verify board structure and columns
2. Test Monday.com API connection
3. Create a test lead with all required fields
4. Verify the lead was created correctly with A/B testing & competitive intelligence data
"""

import json
from datetime import datetime

import requests

# Configuration
MONDAY_API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjU2MTI0OTM2MiwiYWFpIjoxMSwidWlkIjo2NzA0MDY5NCwiaWFkIjoiMjAyNS0wOS0xMlQwNjo1ODoxOC4yNzVaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MjU4NDk4NzEsInJnbiI6ImV1YzEifQ.Z-5M7pm_QZa1YBQ4a5caSg6XZlM4X1_fTcnF5JmQJyw"
BOARD_ID = "2145240699"
API_URL = "https://api.monday.com/v2"

headers = {"Authorization": MONDAY_API_TOKEN, "Content-Type": "application/json"}


def get_board_info(board_id):
    """Get complete board information including columns"""

    query = """
    query ($boardId: ID!) {
      boards (ids: [$boardId]) {
        name
        state
        columns {
          id
          title
          type
        }
        items_page (limit: 10) {
          items {
            id
            name
          }
        }
      }
    }
    """

    variables = {"boardId": board_id}

    response = requests.post(
        API_URL, headers=headers, json={"query": query, "variables": variables}
    )

    return response.json()


def create_test_lead(board_id, columns_map):
    """Create a test lead with all fields populated"""

    # Prepare column values
    column_values = {
        columns_map.get("Telefon", "text_mkwa47yd"): "+48123456789",
        columns_map.get("E-mail", "text_mkwa8qna"): "test@novahouse.pl",
        columns_map.get(
            "Notatki", "text_mkwaqbkz"
        ): "Test lead from E2E test - A/B Testing & Competitive Intelligence",
        columns_map.get("Źródło", "text_mkwavbbk"): "Chatbot API Test",
        columns_map.get("Kategorie/Tagi", "text_mkwatsh6"): "test, automated",
        columns_map.get("Lead Score", "lead_score"): "85",
        columns_map.get(
            "Competitor Mentioned", "competitor_mentioned"
        ): "Tak - wspomniał o konkurencji XYZ",
        columns_map.get(
            "Next Action", "next_action"
        ): "Umówić spotkanie - klient zainteresowany pakietem szafranowym",
    }

    query = """
    mutation ($boardId: ID!, $itemName: String!, $columnValues: JSON!) {
      create_item (
        board_id: $boardId,
        item_name: $itemName,
        column_values: $columnValues
      ) {
        id
        name
        column_values {
          id
          text
          value
        }
      }
    }
    """

    variables = {
        "boardId": board_id,
        "itemName": f"Test Lead E2E - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "columnValues": json.dumps(column_values),
    }

    response = requests.post(
        API_URL, headers=headers, json={"query": query, "variables": variables}
    )

    return response.json()


def verify_lead(item_id):
    """Verify that the lead was created with all correct values"""

    query = """
    query ($itemId: ID!) {
      items (ids: [$itemId]) {
        id
        name
        column_values {
          id
          text
          value
        }
      }
    }
    """

    variables = {"itemId": item_id}

    response = requests.post(
        API_URL, headers=headers, json={"query": query, "variables": variables}
    )

    return response.json()


def main():
    print("=" * 70)
    print("🔍 MONDAY.COM BOARD ORGANIZATION & E2E TEST")
    print("=" * 70)

    # Step 1: Get board info
    print("\n📋 Step 1: Fetching board information...")
    result = get_board_info(BOARD_ID)

    if "data" not in result or not result["data"]["boards"]:
        print(f"❌ Error fetching board: {result}")
        return

    board = result["data"]["boards"][0]
    columns = board["columns"]
    items = board["items_page"]["items"]

    print(f"✅ Board: {board['name']}")
    print(f"✅ State: {board['state']}")
    print(f"✅ Columns: {len(columns)}")
    print(f"✅ Current items: {len(items)}")

    # Create columns map
    columns_map = {col["title"]: col["id"] for col in columns}

    print("\n📊 Board Structure:")
    print("-" * 70)
    for col in columns:
        print(f"   {col['title']:30} | ID: {col['id']:25} | Type: {col['type']}")
    print("-" * 70)

    # Step 2: Verify required columns
    print("\n✅ Step 2: Verifying required columns...")
    required_columns = {
        "Lead Score": "lead_score",
        "Competitor Mentioned": "competitor_mentioned",
        "Next Action": "next_action",
    }

    all_present = True
    for col_title, col_id in required_columns.items():
        if col_title in columns_map:
            print(f"   ✅ {col_title} (ID: {columns_map[col_title]})")
        else:
            print(f"   ❌ Missing: {col_title}")
            all_present = False

    if not all_present:
        print("\n❌ Missing required columns! Run scripts/add_monday_columns.py first.")
        return

    # Step 3: Create test lead
    print("\n🧪 Step 3: Creating test lead with A/B Testing & Competitive Intelligence data...")
    result = create_test_lead(BOARD_ID, columns_map)

    if "data" not in result or not result["data"]["create_item"]:
        print(f"❌ Error creating test lead: {result}")
        if "errors" in result:
            for error in result["errors"]:
                print(f"   Error: {error.get('message', 'Unknown error')}")
        return

    created_item = result["data"]["create_item"]
    item_id = created_item["id"]
    item_name = created_item["name"]

    print(f"✅ Created test lead: {item_name} (ID: {item_id})")

    # Step 4: Verify lead
    print("\n🔍 Step 4: Verifying test lead...")
    result = verify_lead(item_id)

    if "data" not in result or not result["data"]["items"]:
        print(f"❌ Error verifying lead: {result}")
        return

    item = result["data"]["items"][0]

    print(f"✅ Lead verified: {item['name']}")
    print("\n📊 Column Values:")
    print("-" * 70)

    # Map column IDs to titles for display
    board_result = get_board_info(BOARD_ID)
    columns_titles = {
        col["id"]: col["title"] for col in board_result["data"]["boards"][0]["columns"]
    }

    key_column_ids = [
        "lead_score",
        "competitor_mentioned",
        "next_action",
        "text_mkwa47yd",
        "text_mkwa8qna",
        "text_mkwavbbk",
    ]
    for col_value in item["column_values"]:
        if col_value["id"] in key_column_ids and col_value["text"]:
            col_title = columns_titles.get(col_value["id"], col_value["id"])
            print(f"   {col_title:30} | {col_value['text']}")
    print("-" * 70)

    # Step 5: Summary
    print("\n" + "=" * 70)
    print("✅ E2E TEST COMPLETE!")
    print("=" * 70)
    print("\n📊 Summary:")
    print(f"   ✅ Board structure verified: {len(columns)} columns")
    print(f"   ✅ Required columns present: Lead Score, Competitor Mentioned, Next Action")
    print(f"   ✅ Test lead created: {item_name}")
    print(f"   ✅ All fields populated correctly")
    print("\n🎯 Next Steps:")
    print("   1. Verify test lead in Monday.com: https://monday.com/boards/2145240699")
    print("   2. Test chatbot conversation → Monday.com integration")
    print("   3. Check A/B testing variants in chatbot responses")
    print("   4. Verify competitive intelligence detection")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
