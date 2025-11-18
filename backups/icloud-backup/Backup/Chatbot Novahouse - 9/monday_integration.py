import os
import requests
from flask import current_app

MONDAY_API_URL = "https://api.monday.com/v2/"

def create_monday_item(board_id, group_id, item_name, column_values=None):
    api_key = current_app.config.get("MONDAY_API_KEY")
    if not api_key:
        raise ValueError("Missing MONDAY_API_KEY in app configuration")

    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

    query = """
    mutation createItem ($boardId: ID!, $groupId: String!, $itemName: String!, $columnValues: JSON) {
      create_item (board_id: $boardId, group_id: $groupId, item_name: $itemName, column_values: $columnValues) {
        id
      }
    }
    """

    variables = {
        "boardId": str(board_id),
        "groupId": group_id,
        "itemName": item_name,
        "columnValues": column_values
    }

    data = {
        'query': query,
        'variables': variables
    }

    response = requests.post(MONDAY_API_URL, headers=headers, json=data)
    return response.json()

def get_board_id_by_name(board_name):
    api_key = current_app.config.get("MONDAY_API_KEY")
    if not api_key:
        raise ValueError("Missing MONDAY_API_KEY in app configuration")

    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

    query = """
    query { boards (limit: 1, board_kind: public) { id name } } 
    """

    data = {
        'query': query
    }

    response = requests.post(MONDAY_API_URL, headers=headers, json=data)
    boards = response.json().get("data", {}).get("boards", [])
    for board in boards:
        if board["name"] == board_name:
            return board["id"]
    return None

def get_board_columns(board_id):
    api_key = current_app.config.get("MONDAY_API_KEY")
    if not api_key:
        raise ValueError("Missing MONDAY_API_KEY in app configuration")

    headers = {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

    query = """
    query ($boardId: Int!) { boards (ids: [$boardId]) { columns { id title type } } } 
    """

    variables = {
        "boardId": board_id
    }

    data = {
        'query': query,
        'variables': variables
    }

    response = requests.post(MONDAY_API_URL, headers=headers, json=data)
    return response.json()


