from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Sample products
products = [
    {"id": 1, "name": "Potato", "price": 30, "unit": "KG", "stock": 100, "category": "Vegetables", "active": True},
    {"id": 2, "name": "Tomato", "price": 40, "unit": "KG", "stock": 80, "category": "Vegetables", "active": True},
    {"id": 3, "name": "Onion", "price": 35, "unit": "KG", "stock": 150, "category": "Vegetables", "active": True},
    {"id": 4, "name": "Rice", "price": 60, "unit": "KG", "stock": 200, "category": "Grocery", "active": True},
]

orders = []
order_counter = 1

@app.route('/')
def home():
    return jsonify({'message': '🌿 Vegetable Shop API', 'status': 'running', 'version': '3.0.0'})

@app.route('/api/products')
def get_products():
    return jsonify(products)

@app.route('/api/products/active')
def get_active_products():
    active = [p for p in products if p.get('active', True)]
    return jsonify(active)

@app.route('/api/products/low-stock')
def get_low_stock():
    low = [p for p in products if p.get('stock', 0) < 20]
    return jsonify(low)

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    new_id = max([p['id'] for p in products]) + 1 if products else 1
    product = {
        'id': new_id,
        'name': data.get('name'),
        'price': float(data.get('price', 0)),
        'unit': data.get('unit', 'KG'),
        'stock': int(data.get('stock', 0)),
        'category': data.get('category', 'Vegetables'),
        'active': data.get('active', True)
    }
    products.append(product)
    return jsonify({'success': True, 'product': product})

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({'error': 'Not found'}), 404
    product.update({
        'name': data.get('name', product['name']),
        'price': float(data.get('price', product['price'])),
        'stock': int(data.get('stock', product['stock'])),
        'active': data.get('active', product.get('active', True))
    })
    return jsonify({'success': True, 'product': product})

@app.route('/api/products/<int:product_id>/stock', methods=['PUT'])
def update_stock(product_id):
    data = request.json
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({'error': 'Not found'}), 404
    product['stock'] = int(data.get('stock', product['stock']))
    return jsonify({'success': True, 'product': product})

@app.route('/api/products/<int:product_id>/toggle', methods=['PUT'])
def toggle_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({'error': 'Not found'}), 404
    product['active'] = not product.get('active', True)
    return jsonify({'success': True, 'product': product})

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    products = [p for p in products if p['id'] != product_id]
    return jsonify({'success': True})

@app.route('/api/orders')
def get_orders():
    return jsonify(orders)

@app.route('/api/orders/stats')
def get_stats():
    total = len(orders)
    new = len([o for o in orders if o['status'] == 'NEW'])
    total_sales = sum([o.get('total', 0) for o in orders if o['status'] != 'CANCELLED'])
    return jsonify({'total_orders': total, 'new_orders': new, 'total_sales': total_sales})

@app.route('/api/order', methods=['POST'])
def create_order():
    global order_counter
    data = request.json
    
    # Reduce stock
    for item in data.get('items', []):
        product = next((p for p in products if p['name'].lower() == item['name'].lower()), None)
        if product:
            product['stock'] -= item['quantity']
    
    order = {
        'order_id': f'ORD-{datetime.now().strftime("%Y%m%d")}-{str(order_counter).zfill(3)}',
        'customer': data.get('name', ''),
        'phone': data.get('phone', ''),
        'address': data.get('address', ''),
        'items': data.get('items', []),
        'total': float(data.get('total', 0)),
        'status': 'NEW',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    orders.append(order)
    order_counter += 1
    return jsonify({'success': True, 'order': order})

@app.route('/api/order/status', methods=['PUT'])
def update_status():
    data = request.json
    for order in orders:
        if order['order_id'] == data.get('order_id'):
            order['status'] = data.get('status')
            return jsonify({'success': True, 'order': order})
    return jsonify({'success': False}), 404

@app.route('/admin')
def admin_dashboard():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🌿 Admin</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: Arial, sans-serif; background: #f0f4f8; padding: 16px; }
            .header { background: #2E7D32; color: white; padding: 16px; border-radius: 12px; margin-bottom: 16px; }
            .stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 16px; }
            .stat-card { background: white; padding: 14px; border-radius: 12px; text-align: center; }
            .stat-card .number { font-size: 24px; font-weight: 700; color: #2E7D32; }
            .section { background: white; border-radius: 12px; padding: 16px; margin-bottom: 12px; }
            .order-item { border-bottom: 1px solid #eee; padding: 8px 0; }
            .btn { padding: 6px 12px; border: none; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; margin: 2px; }
            .btn-primary { background: #4CAF50; color: white; }
            .btn-danger { background: #e74c3c; color: white; }
            .btn-info { background: #2196F3; color: white; }
            .form-group { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin-bottom: 10px; }
            .form-group input { padding: 8px; border: 2px solid #ddd; border-radius: 8px; }
            @media (max-width: 600px) {
                .stats { grid-template-columns: repeat(2, 1fr); }
            }
        </style>
    </head>
    <body>
        <div class="header"><h1>🌿 Admin Dashboard</h1><button onclick="loadAll()" style="background:white;color:#2E7D32;padding:6px 16px;border:none;border-radius:8px;cursor:pointer;">🔄 Refresh</button></div>
        
        <div class="stats" id="stats">
            <div class="stat-card"><div class="number" id="totalOrders">0</div><div>Total Orders</div></div>
            <div class="stat-card"><div class="number" id="newOrders">0</div><div>New Orders</div></div>
            <div class="stat-card"><div class="number" id="totalSales">₹0</div><div>Total Sales</div></div>
        </div>
        
        <div class="section">
            <h3>📋 Orders</h3>
            <div id="ordersList"></div>
        </div>
        
        <div class="section">
            <h3>➕ Add Product</h3>
            <div class="form-group">
                <input id="pName" placeholder="Name" />
                <input id="pPrice" placeholder="Price" type="number" />
                <input id="pStock" placeholder="Stock" type="number" />
                <input id="pUnit" placeholder="Unit (KG/Piece)" />
                <button class="btn btn-primary" onclick="addProduct()">Add Product</button>
            </div>
        </div>
        
        <div class="section">
            <h3>🥬 Products</h3>
            <div id="productList"></div>
        </div>
        
        <script>
            function loadAll() {
                loadStats();
                loadOrders();
                loadProducts();
            }
            
            function loadStats() {
                fetch('/api/orders/stats').then(r=>r.json()).then(d => {
                    document.getElementById('totalOrders').textContent = d.total_orders || 0;
                    document.getElementById('newOrders').textContent = d.new_orders || 0;
                    document.getElementById('totalSales').textContent = '₹' + (d.total_sales || 0);
                });
            }
            
            function loadOrders() {
                fetch('/api/orders').then(r=>r.json()).then(d => {
                    const list = document.getElementById('ordersList');
                    if (d.length === 0) { list.innerHTML = '<p>No orders yet</p>'; return; }
                    list.innerHTML = d.map(o => `
                        <div class="order-item">
                            <b>#${o.order_id}</b> | ${o.customer} | ₹${o.total} 
                            <span style="background:#fff3e0;padding:2px 10px;border-radius:12px;font-size:12px;">${o.status}</span>
                            ${o.status === 'NEW' ? `<button class="btn btn-info" onclick="updateStatus('${o.order_id}','CONFIRMED')">Confirm</button>` : ''}
                            ${o.status === 'CONFIRMED' ? `<button class="btn btn-primary" onclick="updateStatus('${o.order_id}','DELIVERED')">Deliver</button>` : ''}
                            ${o.status !== 'DELIVERED' && o.status !== 'CANCELLED' ? `<button class="btn btn-danger" onclick="updateStatus('${o.order_id}','CANCELLED')">Cancel</button>` : ''}
                        </div>
                    `).join('');
                });
            }
            
            function loadProducts() {
                fetch('/api/products').then(r=>r.json()).then(d => {
                    const list = document.getElementById('productList');
                    if (d.length === 0) { list.innerHTML = '<p>No products</p>'; return; }
                    list.innerHTML = d.map(p => `
                        <div style="border-bottom:1px solid #eee;padding:6px 0;display:flex;justify-content:space-between;flex-wrap:wrap;">
                            <span><b>${p.name}</b> | ₹${p.price} | Stock: ${p.stock}</span>
                            <span>
                                <button class="btn btn-info" onclick="toggleProduct(${p.id})">${p.active !== false ? '🔴' : '🟢'}</button>
                                <button class="btn btn-danger" onclick="deleteProduct(${p.id})">🗑️</button>
                            </span>
                        </div>
                    `).join('');
                });
            }
            
            function updateStatus(orderId, status) {
                fetch('/api/order/status', {
                    method: 'PUT',
                    headers: {'Content-Type':'application/json'},
                    body: JSON.stringify({order_id: orderId, status: status})
                }).then(() => loadAll());
            }
            
            function addProduct() {
                fetch('/api/products', {
                    method: 'POST',
                    headers: {'Content-Type':'application/json'},
                    body: JSON.stringify({
                        name: document.getElementById('pName').value,
                        price: parseFloat(document.getElementById('pPrice').value) || 0,
                        stock: parseInt(document.getElementById('pStock').value) || 0,
                        unit: document.getElementById('pUnit').value || 'KG'
                    })
                }).then(() => { 
                    ['pName','pPrice','pStock','pUnit'].forEach(id => document.getElementById(id).value = '');
                    loadAll(); 
                });
            }
            
            function toggleProduct(id) {
                fetch(`/api/products/${id}/toggle`, {method: 'PUT'}).then(() => loadProducts());
            }
            
            function deleteProduct(id) {
                if (!confirm('Delete this product?')) return;
                fetch(`/api/products/${id}`, {method: 'DELETE'}).then(() => loadProducts());
            }
            
            loadAll();
            setInterval(loadAll, 30000);
        </script>
    </body>
    </html>
    '''
    return html

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
