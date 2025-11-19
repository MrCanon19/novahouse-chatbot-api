#!/usr/bin/env python3
"""
Script to clean all leads (items) from Monday.com board for testing purposes.
WARNING: This will delete ALL items from the board!
"""


import requests

# Configuration
MONDAY_API_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjU2MTI0OTM2MiwiYWFpIjoxMSwidWlkIjo2NzA0MDY5NCwiaWFkIjoiMjAyNS0wOS0xMlQwNjo1ODoxOC4yNzVaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MjU4NDk4NzEsInJnbiI6ImV1YzEifQ.Z-5M7pm_QZa1YBQ4a5caSg6XZlM4X1_fTcnF5JmQJyw"
BOARD_ID = "2145240699"
API_URL = "https://api.monday.com/v2"

headers = {"Authorization": MONDAY_API_TOKEN, "Content-Type": "application/json"}


def get_all_items(board_id):
    """Get all items from the board"""

    query = """
    query ($boardId: ID!) {
      boards (ids: [$boardId]) {
        items_page (limit: 500) {
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


def delete_item(item_id):
    """Delete a single item"""

    query = """
    mutation ($itemId: ID!) {
      delete_item (item_id: $itemId) {
        id
      }
    }
    """

    variables = {"itemId": item_id}

    response = requests.post(
        API_URL, headers=headers, json={"query": query, "variables": variables}
    )

    return response.json()


def verify_board_structure(board_id):
    """Verify that required columns exist"""

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
    print("🔍 Verifying Monday.com board structure...")

    # Verify board structure
    result = verify_board_structure(BOARD_ID)
    if "data" in result and result["data"]["boards"]:
        columns = result["data"]["boards"][0]["columns"]
        column_titles = [col["title"] for col in columns]

        print(f"✅ Board has {len(columns)} columns:")
        for col in columns:
            print(f"   - {col['title']} (ID: {col['id']}, Type: {col['type']})")

        # Check for required columns
        required_columns = ["Lead Score", "Competitor Mentioned", "Next Action"]
        missing_columns = [col for col in required_columns if col not in column_titles]

        if missing_columns:
            print(f"\n⚠️  WARNING: Missing required columns: {missing_columns}")
            print("Run scripts/add_monday_columns.py first!")
        else:
            print(f"\n✅ All required columns present: {required_columns}")
    else:
        print(f"❌ Error fetching board structure: {result}")
        return

    print("\n" + "=" * 60)
    print("🗑️  Getting all leads from Monday.com board...")
    print("=" * 60)

    # Get all items
    result = get_all_items(BOARD_ID)
    if "data" in result and result["data"]["boards"]:
        items = result["data"]["boards"][0]["items_page"]["items"]

        if not items:
            print("✅ Board is already empty - no leads to delete")
            return

        print(f"\n⚠️  Found {len(items)} leads to delete:")
        for item in items[:10]:  # Show first 10
            print(f"   - {item['name']} (ID: {item['id']})")
        if len(items) > 10:
            print(f"   ... and {len(items) - 10} more")

        # Confirm deletion
        print(f"\n⚠️  WARNING: This will DELETE ALL {len(items)} leads from the board!")
        confirmation = input("Type 'DELETE' to confirm: ")

        if confirmation != "DELETE":
            print("❌ Deletion cancelled")
            return

        # Delete all items
        print(f"\n🗑️  Deleting {len(items)} leads...")
        deleted_count = 0
        error_count = 0

        for item in items:
            result = delete_item(item["id"])
            if "data" in result and result["data"]["delete_item"]:
                deleted_count += 1
                print(f"✅ Deleted: {item['name']} ({deleted_count}/{len(items)})")
            else:
                error_count += 1
                print(f"❌ Error deleting {item['name']}: {result}")

        print("\n" + "=" * 60)
        print(f"✅ Deletion complete!")
        print(f"   Deleted: {deleted_count}")
        print(f"   Errors: {error_count}")
        print("=" * 60)

    else:
        print(f"❌ Error fetching items: {result}")


if __name__ == "__main__":
    main()
