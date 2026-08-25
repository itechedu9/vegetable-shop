from flask import Flask, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        'message': '🌿 Vegetable Shop API',
        'status': 'running',
        'version': '1.0.0'
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'database': 'not connected yet'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)