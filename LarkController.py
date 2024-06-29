import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()


AUTH_TOKEN = os.getenv('AUTH_TOKEN')
LARK_API_URL = os.getenv('LARK_API_URL')

def send_message_to_lark(message):
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