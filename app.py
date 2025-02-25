from flask import Flask, request, jsonify
from flask_cors import CORS
import hmac
import hashlib
import os
import threading
from pyngrok import ngrok
from dotenv import load_dotenv
import LarkController as lark
import Middleware as middleware

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Define the port for the Flask application
PORT = 3000

# Get the VERIFY_TOKEN from environment variables
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')

def verify_signature(req):
    """
    Verify the signature of the incoming request to ensure it is from a trusted source.

    Args:
        req: The Flask request object.

    Returns:
        bool: True if the signature is valid, False otherwise.
    """
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
    """
    Middleware to verify the request signature before processing the request.
    """
    if request.path == '/webhook' and not verify_signature(request):
        return 'Invalid signature', 400

@app.route('/', methods=['GET'])
def home():
    """
    Home route to verify the server is running.

    Returns:
        str: A confirmation message.
        int: HTTP status code.
    """
    return 'Server is running.', 200

@app.route('/webhook', methods=['POST'])
def webhook():
    """
    Webhook route to handle GitHub events.

    Returns:
        str: Empty string.
        int: HTTP status code.
    """
    data = request.json
    if not data:
        return 'Invalid JSON payload', 400

    middleware.process_event(request.headers.get('X-GitHub-Event'), data)
    return '', 204

@app.route('/sendMessageTolark', methods=['POST'])
def sendMessageToLark():
    """
    Route to send a message to Lark group.

    Returns:
        str: Empty string or error message.
        int: HTTP status code.
    """
    message = request.json.get('message')
    print('Message to send to Lark:', message)
    if not message:
        return 'Invalid message', 400

    lark.send_message_to_lark_group(message)
    return '', 204

@app.route('/sendMessageTolarkChat', methods=['POST'])
def sendMessageToLarkChat():
    """
    Route to send a message to a specific Lark chat.

    Returns:
        str: Empty string or error message.
        int: HTTP status code.
    """
    message = request.json.get('message')
    receive_id = request.json.get('receive_id')
    print('Message to send to Lark:', message)
    print('Receive ID:', receive_id)
    if not message:
        return 'Invalid message', 400

    lark.send_message_to_lark(message, receive_id)
    return '', 204

@app.route('/getUserFromDepartment', methods=['POST'])
def getUserFromDepartment():
    """
    Route to get users from a specific department.

    Returns:
        json: List of users or error message.
        int: HTTP status code.
    """
    data = request.get_json()
    department_id = data.get('department_id')
    print('Department ID:', department_id)
    if not department_id:
        return jsonify({'error': 'Invalid department_id'}), 400

    users = lark.get_user_id_from_department(department_id)
    if users is None:
        return jsonify({'error': 'Failed to retrieve users'}), 500

    return jsonify(users), 200

def expose_flask_app():
    """
    Function to expose the Flask app to the public internet using ngrok.
    """
    public_url = ngrok.connect(PORT)
    print(f"Public URL: {public_url}")

if __name__ == '__main__':
    # Start ngrok tunnel in a separate thread
    tunnel_thread = threading.Thread(target=expose_flask_app)
    tunnel_thread.start()
    
    # Start the Flask server
    app.run(port=PORT)
