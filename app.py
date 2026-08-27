from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({'message': '🌿 API is working!', 'status': 'ok'})

@app.route('/api/products')
def products():
    return jsonify([
        {'id': 1, 'name': 'Potato', 'price': 30, 'stock': 100},
        {'id': 2, 'name': 'Tomato', 'price': 40, 'stock': 80}
    ])

@app.route('/api/orders')
def orders():
    return jsonify([])

@app.route('/admin')
def admin():
    return '<h1>🌿 Admin Panel</h1><p>API is running!</p>'

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
