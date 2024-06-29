from flask import Flask, request
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

PORT = 3000
VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')

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
    if request.method == 'POST' and not verify_signature(request) and request.path == '/webhook':
        return 'Invalid signature', 400

@app.route('/', methods=['GET'])
def home():
    return 'Server is running.', 200

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return 'Invalid JSON payload', 400

    middleware.process_event(request.headers.get('X-GitHub-Event'), data)
    return '', 204

@app.route('/sendMessageTolark', methods=['POST'])
def sendMessageToLark():
    message = request.json.get('message')
    print('Message to send to Lark:', message)
    if not message:
        return 'Invalid message', 400

    lark.send_message_to_lark(message)
    return '', 204

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
