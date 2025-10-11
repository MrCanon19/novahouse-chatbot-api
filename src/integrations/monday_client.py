"""
Monday.com API Client
"""
import os
import requests
from typing import Dict, Optional

class MondayClient:
    """Client do komunikacji z Monday.com API"""
    
    def __init__(self):
        self.api_key = os.getenv('MONDAY_API_KEY', '')
        self.api_url = 'https://api.monday.com/v2'
        self.board_id = os.getenv('MONDAY_BOARD_ID', '')
    
    def _make_request(self, query: str, variables: Optional[Dict] = None) -> Dict:
        """Wykonaj request do Monday.com API"""
        headers = {
            'Authorization': self.api_key,
            'Content-Type': 'application/json'
        }
        
        data = {
            'query': query
        }
        
        if variables:
            data['variables'] = variables
        
        try:
            response = requests.post(
                self.api_url,
                json=data,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"Monday.com API error: {e}")
            return {'errors': [str(e)]}
    
    def create_lead_item(self, lead_data: Dict) -> Optional[str]:
        """Utwórz nowy item w Monday.com z danych leadu"""
        if not self.api_key or not self.board_id:
            print("Monday.com credentials not configured")
            return None
        
        # GraphQL mutation do utworzenia itemu
        mutation = """
        mutation ($boardId: ID!, $itemName: String!, $columnValues: JSON!) {
            create_item (
                board_id: $boardId,
                item_name: $itemName,
                column_values: $columnValues
            ) {
                id
            }
        }
        """
        
        # Przygotuj dane
        item_name = lead_data.get('name', 'New Lead')
        column_values = {
            'email': lead_data.get('email', ''),
            'phone': lead_data.get('phone', ''),
            'status': {'label': 'New'},
            'text': lead_data.get('message', '')
        }
        
        variables = {
            'boardId': self.board_id,
            'itemName': item_name,
            'columnValues': str(column_values).replace("'", '"')
        }
        
        result = self._make_request(mutation, variables)
        
        if 'errors' in result:
            print(f"Error creating Monday item: {result['errors']}")
            return None
        
        if 'data' in result and 'create_item' in result['data']:
            item_id = result['data']['create_item']['id']
            print(f"✅ Created Monday.com item: {item_id}")
            return item_id
        
        return None
    
    def update_lead_status(self, item_id: str, status: str) -> bool:
        """Zaktualizuj status leadu w Monday.com"""
        mutation = """
        mutation ($boardId: ID!, $itemId: ID!, $columnValues: JSON!) {
            change_multiple_column_values (
                board_id: $boardId,
                item_id: $itemId,
                column_values: $columnValues
            ) {
                id
            }
        }
        """
        
        column_values = {
            'status': {'label': status}
        }
        
        variables = {
            'boardId': self.board_id,
            'itemId': item_id,
            'columnValues': str(column_values).replace("'", '"')
        }
        
        result = self._make_request(mutation, variables)
        return 'errors' not in result
    
    def test_connection(self) -> bool:
        """Testuj połączenie z Monday.com"""
        if not self.api_key:
            return False
        
        query = """
        query {
            me {
                id
                name
            }
        }
        """
        
        result = self._make_request(query)
        return 'errors' not in result and 'data' in result