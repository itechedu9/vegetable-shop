from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# ডাটাবেস ছাড়া ইন-মেমরি ডাটা
products = []

@app.route('/')
def home():
    return jsonify({'message': '🌿 API is running!', 'status': 'ok'})

@app.route('/api/products')
def get_products():
    return jsonify(products)

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    new_id = len(products) + 1
    products.append({
        'id': new_id,
        'name': data.get('name', ''),
        'price': float(data.get('price', 0)),
        'stock': int(data.get('stock', 0))
    })
    return jsonify({'success': True})

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    products = [p for p in products if p['id'] != product_id]
    return jsonify({'success': True})

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    for p in products:
        if p['id'] == product_id:
            p['name'] = data.get('name', p['name'])
            p['price'] = float(data.get('price', p['price']))
            p['stock'] = int(data.get('stock', p['stock']))
            return jsonify({'success': True})
    return jsonify({'error': 'Not found'}), 404

@app.route('/admin')
def admin():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🌿 Admin</title>
        <style>
            body { font-family: Arial; background: #f0f4f8; padding: 20px; max-width: 800px; margin: auto; }
            .card { background: white; padding: 20px; border-radius: 12px; margin-bottom: 10px; }
            input { padding: 8px; margin: 4px; border: 2px solid #ddd; border-radius: 8px; }
            button { padding: 8px 16px; background: #4CAF50; color: white; border: none; border-radius: 8px; cursor: pointer; }
            table { width: 100%; border-collapse: collapse; margin-top: 10px; }
            th, td { padding: 8px; border-bottom: 1px solid #ddd; text-align: left; }
            .btn-danger { background: #e74c3c; }
            .btn-edit { background: #2196F3; }
        </style>
    </head>
    <body>
        <h1>🌿 Admin Panel</h1>
        <div class="card"><h3>➕ Add Product</h3>
        <input id="name" placeholder="Product Name">
        <input id="price" placeholder="Price" type="number">
        <input id="stock" placeholder="Stock" type="number">
        <button onclick="addProduct()">Add</button></div>
        <div class="card"><h3>📦 Products</h3>
        <table><thead><tr><th>Name</th><th>Price</th><th>Stock</th><th>Actions</th></tr></thead><tbody id="productList"></tbody></table></div>
        <script>
        const API = window.location.origin;
        function loadProducts() {
            fetch(API + '/api/products').then(r=>r.json()).then(data => {
                document.getElementById('productList').innerHTML = data.map(p =>
                    `<tr><td>${p.name}</td><td>₹${p.price}</td><td>${p.stock}</td>
                    <td><button class="btn-edit" onclick="editProduct(${p.id})">✏️</button>
                    <button class="btn-danger" onclick="deleteProduct(${p.id})">🗑️</button></td></tr>`
                ).join('');
            });
        }
        function addProduct() {
            const name = document.getElementById('name').value;
            const price = parseFloat(document.getElementById('price').value) || 0;
            const stock = parseInt(document.getElementById('stock').value) || 0;
            fetch(API + '/api/products', {method:'POST', headers:{'Content-Type':'application/json'},
                body:JSON.stringify({name, price, stock})}).then(() => loadProducts());
        }
        function deleteProduct(id) {
            if(!confirm('Delete?')) return;
            fetch(API + '/api/products/' + id, {method:'DELETE'}).then(() => loadProducts());
        }
        function editProduct(id) {
            const name = prompt('New name:'); if(!name) return;
            const price = parseFloat(prompt('New price:')) || 0;
            const stock = parseInt(prompt('New stock:')) || 0;
            fetch(API + '/api/products/' + id, {method:'PUT', headers:{'Content-Type':'application/json'},
                body:JSON.stringify({name, price, stock})}).then(() => loadProducts());
        }
        loadProducts();
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)