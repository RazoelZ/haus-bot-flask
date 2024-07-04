import json
import requests
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get environment variables for authentication and API URLs
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
LARK_API_URL = os.getenv('LARK_API_URL')
LARK_API_USER_DEPARTMENT = os.getenv('LARK_API_URL_GET_USER_DEPARTMENT')
AUTH_TOKEN_GET = os.getenv('AUTH_TOKEN_DEPARTMEN')

def send_message_to_lark_group(message):
    """
    Send a message to a Lark group.

    Args:
        message (str): The message to be sent to the Lark group.
    
    Returns:
        None
    """
    payload = {
        "receive_id": "oc_da933eb5b74c65d365a70b5277ac459d",  # Replace with actual receive_id
        "msg_type": "text",
        "content": json.dumps({
            "text": message,
        }),
    }

    headers = {
        'Authorization': f'Bearer {AUTH_TOKEN}',
        'Content-Type': 'application/json',
    }

    params = {
        'receive_id_type': 'chat_id',  # Specify the correct type of receive_id
    }

    try:
        response = requests.post(LARK_API_URL, json=payload, headers=headers, params=params)
        response.raise_for_status()
        print('Message sent to Lark:', response.json())
    except requests.exceptions.RequestException as error:
        print('Failed to send message to Lark:', payload)
        print('Failed to send message to Lark:', error)
        if error.response is not None:
            print('Failed to send message to Lark:', error.response.text)

def send_message_to_lark(message, receive_id):
    """
    Send a message to a specific Lark user.

    Args:
        message (str): The message to be sent.
        receive_id (str): The ID of the recipient.
    
    Returns:
        None
    """
    payload = {
        "receive_id": receive_id,  # Replace with actual receive_id
        "msg_type": "text",
        "content": json.dumps({
            "text": message,
        }),
    }

    headers = {
        'Authorization': f'Bearer {AUTH_TOKEN}',
        'Content-Type': 'application/json',
    }

    params = {
        'receive_id_type': 'user_id',  # Specify the correct type of receive_id
    }

    try:
        response = requests.post(LARK_API_URL, json=payload, headers=headers, params=params)
        response.raise_for_status()
        print('Message sent to Lark:', response.json())
    except requests.exceptions.RequestException as error:
        print('Failed to send message to Lark:', payload)
        print('Failed to send message to Lark:', error)
        if error.response is not None:
            print('Failed to send message to Lark:', error.response.text)

def get_user_id_from_department(department_id):
    """
    Retrieve user IDs from a specific department.

    Args:
        department_id (str): The ID of the department.
    
    Returns:
        list: A list of dictionaries containing user names and user IDs, or None if an error occurs.
    """
    headers = {
        'Authorization': f'Bearer {AUTH_TOKEN_GET}',
        'Content-Type': 'application/json',
    }

    params = {
        'department_id': department_id,
        'department_id_type': 'open_department_id',
        'user_id_type': 'open_id',
        'page_size': 10,
    }

    try:
        response = requests.get(LARK_API_USER_DEPARTMENT, headers=headers, params=params)
        response.raise_for_status()
        user_data = response.json()
        users = []
        for item in user_data.get('data', {}).get('items', []):
            users.append({'name': item['name'], 'user_id': item['user_id']})
        return users
    except requests.exceptions.RequestException as error:
        print('Failed to get user ID from department:', error)
        if error.response is not None:
            print('Failed to get user ID from department:', error.response.text)
        return None
