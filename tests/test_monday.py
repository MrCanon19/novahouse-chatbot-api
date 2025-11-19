import os
from src.integrations.monday_client import MondayClient

print("Testing Monday.com integration...")
api_key = os.getenv("MONDAY_API_KEY")
if api_key:
    print(f"API Key: {api_key[:20]}...")
else:
    print("API Key: Not configured")
print(f"Board ID: {os.getenv('MONDAY_BOARD_ID')}")
print()

client = MondayClient()
print("Testing connection...")
result = client.test_connection()

if result:
    print("\nSUCCESS! Monday.com is connected!")
    print("\nTesting lead creation...")
    item_id = client.create_lead_item(
        {
            "name": "Test Lead from API",
            "email": "test@novahouse.pl",
            "phone": "+48123456789",
            "message": "Test integration message",
        }
    )
    if item_id:
        print(f"\nLead created successfully! Item ID: {item_id}")
    else:
        print("\nFailed to create lead")
else:
    print("\nFAILED! Could not connect to Monday.com")
