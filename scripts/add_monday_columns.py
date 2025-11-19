#!/usr/bin/env python3
"""
Script to add required columns to Monday.com board for A/B Testing & Competitive Intelligence features.
"""


import requests

# Configuration
MONDAY_API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjU2MTI0OTM2MiwiYWFpIjoxMSwidWlkIjo2NzA0MDY5NCwiaWFkIjoiMjAyNS0wOS0xMlQwNjo1ODoxOC4yNzVaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MjU4NDk4NzEsInJnbiI6ImV1YzEifQ.Z-5M7pm_QZa1YBQ4a5caSg6XZlM4X1_fTcnF5JmQJyw"
BOARD_ID = "2145240699"
API_URL = "https://api.monday.com/v2"

headers = {"Authorization": MONDAY_API_TOKEN, "Content-Type": "application/json"}


def create_column(board_id, column_title, column_type, column_id=None):
    """Create a new column in Monday.com board"""

    # Generate column_id from title if not provided
    if not column_id:
        column_id = column_title.lower().replace(" ", "_")

    query = """
    mutation ($boardId: ID!, $title: String!, $columnType: ColumnType!, $columnId: String!) {
      create_column (
        board_id: $boardId,
        title: $title,
        column_type: $columnType,
        id: $columnId
      ) {
        id
        title
        type
      }
    }
    """

    variables = {
        "boardId": board_id,
        "title": column_title,
        "columnType": column_type,
        "columnId": column_id,
    }

    response = requests.post(
        API_URL, headers=headers, json={"query": query, "variables": variables}
    )

    return response.json()


def get_board_columns(board_id):
    """Get existing columns from the board"""

    query = """
    query ($boardId: ID!) {
      boards (ids: [$boardId]) {
        columns {
          id
          title
          type
        }
      }
    }
    """

    variables = {"boardId": board_id}

    response = requests.post(
        API_URL, headers=headers, json={"query": query, "variables": variables}
    )

    return response.json()


def main():
    print("🔍 Checking existing columns in Monday.com board...")

    # Get existing columns
    result = get_board_columns(BOARD_ID)
    if "data" in result and result["data"]["boards"]:
        existing_columns = result["data"]["boards"][0]["columns"]
        existing_column_ids = [col["id"] for col in existing_columns]
        print(f"✅ Found {len(existing_columns)} existing columns")
        print(f"Existing column IDs: {existing_column_ids}")
    else:
        print(f"❌ Error fetching board columns: {result}")
        return

    # Define columns to add
    columns_to_add = [
        {"id": "lead_score", "title": "Lead Score", "type": "numbers"},
        {"id": "competitor_mentioned", "title": "Competitor Mentioned", "type": "text"},
        {"id": "next_action", "title": "Next Action", "type": "text"},
    ]

    print("\n🚀 Adding new columns to Monday.com board...")

    for column in columns_to_add:
        if column["id"] in existing_column_ids:
            print(f"⏭️  Column '{column['title']}' already exists, skipping...")
            continue

        print(f"\n📝 Creating column: {column['title']} (type: {column['type']})")
        result = create_column(BOARD_ID, column["title"], column["type"], column["id"])

        if "data" in result and result["data"]["create_column"]:
            created_column = result["data"]["create_column"]
            print(
                f"✅ Successfully created column: {created_column['title']} (ID: {created_column['id']})"
            )
        else:
            print(f"❌ Error creating column '{column['title']}': {result}")
            if "errors" in result:
                for error in result["errors"]:
                    print(f"   Error: {error.get('message', 'Unknown error')}")

    print("\n" + "=" * 60)
    print("✅ Column setup complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Verify columns in Monday.com board: https://monday.com/boards/2145240699")
    print("2. Test chatbot → Monday.com integration")
    print("3. Check that lead_score, competitor_mentioned, and next_action are populated")


if __name__ == "__main__":
    main()
