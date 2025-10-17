"""
Monday.com API Client
Handles all interactions with Monday.com boards
"""

import os
import requests
import json
from typing import Dict, Optional, List


class MondayClient:
    """Client for Monday.com GraphQL API"""
    
    def __init__(self):
        self.api_key = os.getenv('MONDAY_API_KEY')
        self.board_id = os.getenv('MONDAY_BOARD_ID')
        self.api_url = 'https://api.monday.com/v2'
        
        if not self.api_key:
            print("WARNING: MONDAY_API_KEY not found in environment variables")
        if not self.board_id:
            print("WARNING: MONDAY_BOARD_ID not found in environment variables")
    
    def _make_request(self, query: str, variables: Optional[Dict] = None) -> Dict:
        """Make a GraphQL request to Monday.com API"""
        
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
            print(f"Monday.com API Error: {e}")
            return {'errors': [str(e)]}
    
    def create_lead_item(self, lead_data: Dict) -> Optional[str]:
        """Create a new item on Monday.com board"""
        
        if not self.api_key or not self.board_id:
            print("Monday.com not configured, skipping lead creation")
            return None
        
        item_name = lead_data.get('name', 'Nowy Lead')
        
        column_values = {}
        
        if lead_data.get('email'):
            column_values['email'] = {'email': lead_data['email'], 'text': lead_data['email']}
        
        if lead_data.get('phone'):
            column_values['phone'] = lead_data['phone']
        
        if lead_data.get('message'):
            column_values['text'] = lead_data['message']
        
        mutation = """
        mutation ($boardId: ID!, $itemName: String!, $columnValues: JSON!) {
            create_item (
                board_id: $boardId,
                item_name: $itemName,
                column_values: $columnValues
            ) {
                id
                name
            }
        }
        """
        
        variables = {
            'boardId': int(self.board_id),
            'itemName': item_name,
            'columnValues': json.dumps(column_values)
        }
        
        result = self._make_request(mutation, variables)
        
        if 'errors' in result:
            print(f"Failed to create Monday.com item: {result['errors']}")
            return None
        
        if 'data' in result and 'create_item' in result['data']:
            item_id = result['data']['create_item']['id']
            print(f"Created Monday.com item: {item_id}")
            return item_id
        
        return None
    
    def test_connection(self) -> bool:
        """Test connection to Monday.com API"""
        
        if not self.api_key:
            return False
        
        query = """
        query {
            me {
                id
                name
                email
            }
        }
        """
        
        result = self._make_request(query)
        
        if 'errors' in result:
            print(f"Monday.com connection failed: {result['errors']}")
            return False
        
        if 'data' in result and 'me' in result['data']:
            user = result['data']['me']
            print(f"Monday.com connected as: {user.get('name')} ({user.get('email')})")
            return True
        
        return False
