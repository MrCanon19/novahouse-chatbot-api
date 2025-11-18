"""
Monday.com Lead Creator - dostosowany do nowej struktury board Chat
"""

import os
import json
import requests
from flask import current_app
from datetime import datetime

MONDAY_API_URL = "https://api.monday.com/v2/"
BOARD_ID = "2145240699"  # ID board Chat
GROUP_ID = "leady_z_chatbota"  # ID grupy "Leady z chatbota"

def create_lead_from_chat(name, phone, email, metraz, budget, message, session_id):
    """Tworzy lead w Monday.com na podstawie danych z chatbota - nowa struktura"""
    
    try:
        api_key = os.getenv('MONDAY_API_KEY')
        if not api_key:
            current_app.logger.error("Brak MONDAY_API_KEY")
            return False
        
        headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }
        
        # Przygotuj nazwę leada
        if name and phone:
            item_name = f"{name} - {phone}"
        elif phone:
            item_name = f"Lead - {phone}"
        elif email:
            item_name = f"Lead - {email}"
        else:
            item_name = f"Lead - {session_id[:8]}"
        
        # Przygotuj dane dla nowej struktury Monday.com
        column_values = {}
        
        # Status - domyślnie "Working on it" (pomarańczowy)
        column_values["status"] = {"label": "Working on it"}
        
        # Data utworzenia - dzisiejsza data
        today = datetime.now().strftime("%Y-%m-%d")
        column_values["data_utworzenia"] = {"date": today}
        
        # Telefon
        if phone:
            column_values["telefon"] = phone
        
        # Data pozyskania - dzisiejsza data
        column_values["data_pozyskania"] = {"date": today}
        
        # Dodatkowe informacje w komentarzu/update
        additional_info = []
        if email:
            additional_info.append(f"📧 Email: {email}")
        if metraz:
            additional_info.append(f"🏠 Metraż: {metraz}m²")
        if budget:
            additional_info.append(f"💰 Budżet: {budget}k zł")
        if message:
            additional_info.append(f"💬 Wiadomość: {message[:200]}")
        
        # GraphQL mutation do tworzenia elementu
        query = """
        mutation ($boardId: ID!, $groupId: String!, $itemName: String!, $columnValues: JSON) {
          create_item (board_id: $boardId, group_id: $groupId, item_name: $itemName, column_values: $columnValues) {
            id
            name
          }
        }
        """
        
        variables = {
            "boardId": BOARD_ID,
            "groupId": GROUP_ID,
            "itemName": item_name,
            "columnValues": json.dumps(column_values)
        }
        
        data = {
            'query': query,
            'variables': variables
        }
        
        current_app.logger.info(f"Wysyłanie do Monday.com: {item_name}")
        current_app.logger.debug(f"Dane: {data}")
        
        response = requests.post(MONDAY_API_URL, headers=headers, json=data)
        result = response.json()
        
        current_app.logger.info(f"Odpowiedź Monday.com: {result}")
        
        if response.status_code == 200 and 'data' in result and result['data']['create_item']:
            item_id = result['data']['create_item']['id']
            current_app.logger.info(f"Lead utworzony w Monday.com: {item_id}")
            
            # Dodaj dodatkowe informacje jako update/komentarz
            if additional_info:
                add_update_to_item(item_id, "\n".join(additional_info))
            
            return True
        else:
            current_app.logger.error(f"Błąd Monday.com: {result}")
            return False
            
    except Exception as e:
        current_app.logger.error(f"Błąd tworzenia leada w Monday.com: {e}")
        return False

def add_update_to_item(item_id, update_text):
    """Dodaje update/komentarz do elementu w Monday.com"""
    
    try:
        api_key = os.getenv('MONDAY_API_KEY')
        if not api_key:
            return False
        
        headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }
        
        query = """
        mutation ($itemId: ID!, $body: String!) {
          create_update (item_id: $itemId, body: $body) {
            id
          }
        }
        """
        
        variables = {
            "itemId": str(item_id),
            "body": update_text
        }
        
        data = {
            'query': query,
            'variables': variables
        }
        
        response = requests.post(MONDAY_API_URL, headers=headers, json=data)
        result = response.json()
        
        if response.status_code == 200 and 'data' in result:
            current_app.logger.info(f"Update dodany do leada {item_id}")
            return True
        else:
            current_app.logger.error(f"Błąd dodawania update: {result}")
            return False
            
    except Exception as e:
        current_app.logger.error(f"Błąd dodawania update: {e}")
        return False

def get_board_structure():
    """Pobiera strukturę board Chat do debugowania"""
    
    try:
        api_key = os.getenv('MONDAY_API_KEY')
        if not api_key:
            return None
        
        headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }
        
        query = """
        query ($boardId: ID!) {
          boards (ids: [$boardId]) {
            name
            columns {
              id
              title
              type
            }
            groups {
              id
              title
            }
          }
        }
        """
        
        variables = {
            "boardId": BOARD_ID
        }
        
        data = {
            'query': query,
            'variables': variables
        }
        
        response = requests.post(MONDAY_API_URL, headers=headers, json=data)
        return response.json()
        
    except Exception as e:
        current_app.logger.error(f"Błąd pobierania struktury board: {e}")
        return None

def test_monday_connection():
    """Test połączenia z Monday.com API"""
    
    try:
        api_key = os.getenv('MONDAY_API_KEY')
        if not api_key:
            return {"success": False, "error": "Brak API key"}
        
        headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }
        
        query = """
        query {
          me {
            name
            email
          }
        }
        """
        
        data = {'query': query}
        
        response = requests.post(MONDAY_API_URL, headers=headers, json=data)
        result = response.json()
        
        if response.status_code == 200 and 'data' in result:
            return {"success": True, "user": result['data']['me']}
        else:
            return {"success": False, "error": result}
            
    except Exception as e:
        return {"success": False, "error": str(e)}
