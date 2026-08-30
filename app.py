from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import os
<<<<<<< HEAD
=======
import psycopg2
import psycopg2.extras
from datetime import datetime
>>>>>>> 3f2658ae2757f2f089ed88ad2a4175f321e228e2

app = Flask(__name__)
CORS(app)

# ডাটাবেস ছাড়া ইন-মেমরি ডাটা
products = []

<<<<<<< HEAD
=======
def get_db():
    if not DATABASE_URL:
        print("⚠️ DATABASE_URL not set!")
        return None
    try:
        return psycopg2.connect(DATABASE_URL)
    except Exception as e:
        print(f"⚠️ Connection error: {e}")
        return None

def run_query(query, params=None, fetch=False):
    conn = get_db()
    if not conn:
        return None if not fetch else []
    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute(query, params or ())
        if fetch:
            result = cur.fetchall()
            cur.close()
            conn.close()
            return result
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"⚠️ Query error: {e}")
        try:
            conn.rollback()
        except:
            pass
        return None if not fetch else []

# ===== API রাউট =====
>>>>>>> 3f2658ae2757f2f089ed88ad2a4175f321e228e2
@app.route('/')
def home():
    return jsonify({'message': '🌿 API is running!', 'status': 'ok'})

@app.route('/api/products')
def get_products():
<<<<<<< HEAD
    return jsonify(products)
=======
    data = run_query("SELECT * FROM products ORDER BY id", fetch=True)
    if data is None:
        return jsonify([])
    return jsonify([dict(row) for row in data])
>>>>>>> 3f2658ae2757f2f089ed88ad2a4175f321e228e2

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
<<<<<<< HEAD
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
=======
    try:
        run_query(
            "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)",
            (data.get('name'), float(data.get('price', 0)), int(data.get('stock', 0)))
        )
        return jsonify({'success': True, 'message': 'Product added'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        run_query("DELETE FROM products WHERE id=%s", (product_id,))
        return jsonify({'success': True, 'message': 'Product deleted'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
>>>>>>> 3f2658ae2757f2f089ed88ad2a4175f321e228e2

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
<<<<<<< HEAD
    for p in products:
        if p['id'] == product_id:
            p['name'] = data.get('name', p['name'])
            p['price'] = float(data.get('price', p['price']))
            p['stock'] = int(data.get('stock', p['stock']))
            return jsonify({'success': True})
    return jsonify({'error': 'Not found'}), 404
=======
    try:
        run_query(
            "UPDATE products SET name=%s, price=%s, stock=%s WHERE id=%s",
            (data.get('name'), float(data.get('price', 0)), int(data.get('stock', 0)), product_id)
        )
        return jsonify({'success': True, 'message': 'Product updated'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
>>>>>>> 3f2658ae2757f2f089ed88ad2a4175f321e228e2

@app.route('/admin')
def admin():
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
<<<<<<< HEAD
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
=======
        <title>🌿 Admin Panel</title>
        <style>
            body { font-family: Arial; background: #f0f4f8; padding: 20px; max-width: 800px; margin: auto; }
            .card { background: white; padding: 20px; border-radius: 12px; margin-bottom: 15px; box-shadow: 0 2px 8px rgba(0,0,0,0.05); }
            input { padding: 8px 12px; margin: 4px; border: 2px solid #ddd; border-radius: 8px; font-size: 14px; }
            button { padding: 8px 20px; background: #2E7D32; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; }
            button:hover { background: #1B5E20; }
            table { width: 100%; border-collapse: collapse; margin-top: 10px; }
            th, td { padding: 10px; border-bottom: 1px solid #eee; text-align: left; }
            .btn-danger { background: #e74c3c; }
            .btn-danger:hover { background: #c0392b; }
            .btn-edit { background: #2196F3; }
            .btn-edit:hover { background: #0b7dda; }
            .btn-sm { padding: 4px 10px; font-size: 12px; margin: 2px; }
>>>>>>> 3f2658ae2757f2f089ed88ad2a4175f321e228e2
        </style>
    </head>
    <body>
        <h1>🌿 Admin Panel</h1>
<<<<<<< HEAD
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
=======
        <div class="card">
            <h3>➕ Add Product</h3>
            <div style="display:flex; gap:8px; flex-wrap:wrap;">
                <input id="name" placeholder="Product Name" style="flex:2; min-width:150px;">
                <input id="price" placeholder="Price" type="number" style="flex:1; min-width:100px;">
                <input id="stock" placeholder="Stock" type="number" style="flex:1; min-width:100px;">
                <button onclick="addProduct()" style="flex:1; min-width:80px;">Add</button>
            </div>
        </div>
        <div class="card">
            <h3>📦 Products</h3>
            <div style="overflow-x:auto;">
                <table>
                    <thead><tr><th>Name</th><th>Price</th><th>Stock</th><th>Actions</th></tr></thead>
                    <tbody id="productList"></tbody>
                </table>
            </div>
        </div>
        <script>
            const API = window.location.origin;

            function loadProducts() {
                fetch(API + '/api/products')
                    .then(r => r.json())
                    .then(data => {
                        const list = document.getElementById('productList');
                        if (data.length === 0) {
                            list.innerHTML = '<tr><td colspan="4" style="text-align:center;color:#888;">No products yet</td></tr>';
                            return;
                        }
                        list.innerHTML = data.map(p => `
                            <tr>
                                <td><strong>${p.name}</strong></td>
                                <td>₹${parseFloat(p.price).toFixed(2)}</td>
                                <td>${p.stock}</td>
                                <td>
                                    <button class="btn-edit btn-sm" onclick="editProduct(${p.id})">✏️ Edit</button>
                                    <button class="btn-danger btn-sm" onclick="deleteProduct(${p.id})">🗑️ Delete</button>
                                </td>
                            </tr>
                        `).join('');
                    })
                    .catch(err => {
                        document.getElementById('productList').innerHTML = '<tr><td colspan="4" style="color:red;">Error loading products</td></tr>';
                    });
            }

            function addProduct() {
                const name = document.getElementById('name').value.trim();
                const price = parseFloat(document.getElementById('price').value) || 0;
                const stock = parseInt(document.getElementById('stock').value) || 0;
                if (!name) { alert('Please enter product name'); return; }
                fetch(API + '/api/products', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({name, price, stock})
                })
                .then(r => r.json())
                .then(res => {
                    if (res.success) {
                        loadProducts();
                        document.getElementById('name').value = '';
                        document.getElementById('price').value = '';
                        document.getElementById('stock').value = '';
                    } else {
                        alert('Error: ' + res.error);
                    }
                });
            }

            function deleteProduct(id) {
                if (!confirm('Delete this product?')) return;
                fetch(API + '/api/products/' + id, {method: 'DELETE'})
                    .then(() => loadProducts());
            }

            function editProduct(id) {
                const newName = prompt('Enter new name:');
                if (newName === null) return;
                const newPrice = parseFloat(prompt('Enter new price:')) || 0;
                const newStock = parseInt(prompt('Enter new stock:')) || 0;
                fetch(API + '/api/products/' + id, {
                    method: 'PUT',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({name: newName, price: newPrice, stock: newStock})
                }).then(() => loadProducts());
            }

            loadProducts();
            setInterval(loadProducts, 30000);
>>>>>>> 3f2658ae2757f2f089ed88ad2a4175f321e228e2
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
