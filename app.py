from flask import Flask, request, jsonify
import hmac
import hashlib
import json
import requests
import os
import threading
from pyngrok import ngrok
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
PORT = 3000
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
LARK_API_URL = os.getenv('LARK_API_URL')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')


def verify_signature(req):
    signature = req.headers.get('X-Hub-Signature')
    if not signature:
        print('Missing signature')
        return False

    payload = request.get_data()
    hmac_obj = hmac.new(VERIFY_TOKEN.encode('utf-8'), payload, hashlib.sha1)
    digest = 'sha1=' + hmac_obj.hexdigest()

    return hmac.compare_digest(signature, digest)

@app.before_request
def verify_request():
    if request.method == 'POST' and not verify_signature(request):
        return 'Invalid signature', 400

@app.route('/', methods=['GET'])
def home():
    return 'Server is running.', 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print('Request Body:', data) 
    if not data:
        return 'Invalid JSON payload', 400

    process_event(request.headers.get('X-GitHub-Event'), data)
    return '', 204

def process_event(event, data):
    message = ''
    if event == 'push':
        branch = data['ref'].split('/').pop()  # Extract branch name from ref
        commits = '\n'.join([f"- {commit['message']} by {commit['author']['name']}" for commit in data['commits']])
        message = f"New push to {data['repository']['name']} on branch {branch} by {data['pusher']['name']}:\n{commits}"
    elif event == 'pull_request':
        source_branch = data['pull_request']['head']['ref']
        target_branch = data['pull_request']['base']['ref']
        message = f"New pull request #{data['number']} in {data['repository']['name']} from {source_branch} to {target_branch}."
    else:
        message = f"New event: {event}"
    
    print('Message to send to Lark:', message)
    send_message_to_lark(message)

def send_message_to_lark(message):
    payload = {
        'msg_type': 'text',
        'content': json.dumps({
            'text': message,
        }),
        'receive_id': 'oc_7161a7463ab72be5e6ee11ae1bde7306',  # Replace with actual receive_id
    }

    headers = {
        'Authorization': f'Bearer {AUTH_TOKEN}',
        'Content-Type': 'application/json',
    }

    params = {
        'receive_id_type': 'chat_id',  # Specify the correct type of receive_id
    }

    try:
        print('Message sent to Lark:', response.json())
        response = requests.post(LARK_API_URL, json=payload, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx, 5xx)
        
    except requests.exceptions.RequestException as error:
        print('Failed to send message to Lark:', error)
        # Optionally, log more details about the error for troubleshooting


def expose_flask_app():
    # Start ngrok tunnel to expose Flask app
    public_url = ngrok.connect(PORT)
    print(f"Public URL: {public_url}")

if __name__ == '__main__':
    # Start ngrok tunnel in a separate thread
    tunnel_thread = threading.Thread(target=expose_flask_app)
    tunnel_thread.start()
    
    # Start the Flask server
    app.run(port=PORT)
