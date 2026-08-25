from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ===== ডাটা স্টোর =====
products = [
    {"id": 1, "name": "Potato", "name_bn": "আলু", "name_hi": "आलू", 
     "price": 30, "mrp": 40, "unit": "KG", "stock": 100, "discount": 25,
     "image": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=300&h=300&fit=crop",
     "category": "Vegetables", "active": True, "description": "Fresh farm potatoes"},
    {"id": 2, "name": "Tomato", "name_bn": "টমেটো", "name_hi": "टमाटर",
     "price": 40, "mrp": 55, "unit": "KG", "stock": 80, "discount": 27,
     "image": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=300&h=300&fit=crop",
     "category": "Vegetables", "active": True, "description": "Fresh red tomatoes"},
    {"id": 3, "name": "Cauliflower", "name_bn": "ফুলকপি", "name_hi": "फूलगोभी",
     "price": 50, "mrp": 65, "unit": "Piece", "stock": 40, "discount": 23,
     "image": "https://images.unsplash.com/photo-1568585100875-6dd3721b43ed?w=300&h=300&fit=crop",
     "category": "Vegetables", "active": True, "description": "Fresh cauliflower"},
    {"id": 4, "name": "Spinach", "name_bn": "পালং শাক", "name_hi": "पालक",
     "price": 20, "mrp": 30, "unit": "Bundle", "stock": 60, "discount": 33,
     "image": "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=300&h=300&fit=crop",
     "category": "Leafy", "active": True, "description": "Fresh green spinach"},
    {"id": 5, "name": "Onion", "name_bn": "পেঁয়াজ", "name_hi": "प्याज",
     "price": 35, "mrp": 45, "unit": "KG", "stock": 150, "discount": 22,
     "image": "https://images.unsplash.com/photo-1508747703725-719777637510?w=300&h=300&fit=crop",
     "category": "Vegetables", "active": True, "description": "Fresh onions"},
    {"id": 6, "name": "Garlic", "name_bn": "রসুন", "name_hi": "लहसुन",
     "price": 120, "mrp": 150, "unit": "KG", "stock": 30, "discount": 20,
     "image": "https://images.unsplash.com/photo-1541808814-4544cb5342c7?w=300&h=300&fit=crop",
     "category": "Vegetables", "active": True, "description": "Fresh garlic"},
    {"id": 7, "name": "Carrot", "name_bn": "গাজর", "name_hi": "गाजर",
     "price": 45, "mrp": 60, "unit": "KG", "stock": 55, "discount": 25,
     "image": "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=300&h=300&fit=crop",
     "category": "Roots", "active": True, "description": "Fresh carrots"},
    {"id": 8, "name": "Brinjal", "name_bn": "বেগুন", "name_hi": "बैंगन",
     "price": 40, "mrp": 55, "unit": "KG", "stock": 45, "discount": 27,
     "image": "https://images.unsplash.com/photo-1552074284-5e88ef1aef18?w=300&h=300&fit=crop",
     "category": "Vegetables", "active": True, "description": "Fresh brinjals"}
]

orders = []
order_counter = 1

# ===== API রাউট =====
@app.route('/')
def home():
    return jsonify({'message': '🌿 Vegetable Shop API', 'status': 'running', 'version': '2.0.0'})

@app.route('/api/products')
def get_products():
    return jsonify(products)

@app.route('/api/products/active')
def get_active_products():
    active = [p for p in products if p.get('active', True)]
    return jsonify(active)

@app.route('/api/products/<int:product_id>')
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    return jsonify(product) if product else (jsonify({'error': 'Not found'}), 404)

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    new_id = max([p['id'] for p in products]) + 1 if products else 1
    product = {
        'id': new_id,
        'name': data.get('name'),
        'name_bn': data.get('name_bn', ''),
        'name_hi': data.get('name_hi', ''),
        'price': float(data.get('price', 0)),
        'mrp': float(data.get('mrp', data.get('price', 0))),
        'unit': data.get('unit', 'KG'),
        'stock': int(data.get('stock', 0)),
        'discount': float(data.get('discount', 0)),
        'image': data.get('image', ''),
        'category': data.get('category', 'Vegetables'),
        'active': data.get('active', True),
        'description': data.get('description', '')
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
        'name_bn': data.get('name_bn', product.get('name_bn', '')),
        'name_hi': data.get('name_hi', product.get('name_hi', '')),
        'price': float(data.get('price', product['price'])),
        'mrp': float(data.get('mrp', product.get('mrp', product['price']))),
        'unit': data.get('unit', product['unit']),
        'stock': int(data.get('stock', product['stock'])),
        'discount': float(data.get('discount', product.get('discount', 0))),
        'image': data.get('image', product['image']),
        'category': data.get('category', product['category']),
        'active': data.get('active', product.get('active', True)),
        'description': data.get('description', product.get('description', ''))
    })
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
def get_order_stats():
    total = len(orders)
    new = len([o for o in orders if o['status'] == 'NEW'])
    delivered = len([o for o in orders if o['status'] == 'DELIVERED'])
    total_sales = sum([o.get('total', 0) for o in orders if o['status'] != 'CANCELLED'])
    
    # Item wise order count
    item_stats = {}
    for order in orders:
        for item in order.get('items', []):
            name = item.get('name', 'Unknown')
            if name not in item_stats:
                item_stats[name] = {'count': 0, 'total_qty': 0, 'total_revenue': 0}
            item_stats[name]['count'] += 1
            item_stats[name]['total_qty'] += item.get('quantity', 0)
            item_stats[name]['total_revenue'] += item.get('price', 0) * item.get('quantity', 0)
    
    return jsonify({
        'total_orders': total,
        'new_orders': new,
        'delivered_orders': delivered,
        'total_sales': total_sales,
        'item_stats': item_stats
    })

@app.route('/api/order', methods=['POST'])
def create_order():
    global order_counter
    data = request.json
    order = {
        'order_id': f'ORD-{datetime.now().strftime("%Y%m%d")}-{str(order_counter).zfill(3)}',
        'customer': data.get('name', ''),
        'phone': data.get('phone', ''),
        'address': data.get('address', ''),
        'area': data.get('area', ''),
        'landmark': data.get('landmark', ''),
        'items': data.get('items', []),
        'subtotal': float(data.get('subtotal', 0)),
        'delivery': float(data.get('delivery', 0)),
        'total': float(data.get('total', 0)),
        'status': 'NEW',
        'payment_method': data.get('payment_method', 'COD'),
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    # Reduce stock
    for item in order['items']:
        product = next((p for p in products if p['name'].lower() == item['name'].lower()), None)
        if product:
            product['stock'] -= item['quantity']
    orders.append(order)
    order_counter += 1
    return jsonify({'success': True, 'order': order})

@app.route('/api/order/status', methods=['PUT'])
def update_order_status():
    data = request.json
    for order in orders:
        if order['order_id'] == data.get('order_id'):
            order['status'] = data.get('status')
            return jsonify({'success': True, 'order': order})
    return jsonify({'success': False, 'message': 'Order not found'}), 404

# ===== অ্যাডমিন প্যানেল =====
@app.route('/admin')
def admin_dashboard():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🌿 Admin Dashboard</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { font-family: -apple-system, 'Segoe UI', Roboto, sans-serif; background: #f0f4f8; padding: 12px; }
            .header { background: linear-gradient(135deg, #1a472a, #2E7D32); color: white; padding: 16px 20px; border-radius: 16px; margin-bottom: 16px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; }
            .header h1 { font-size: 20px; }
            .header h1 span { font-size: 14px; font-weight: 400; opacity: 0.8; }
            .btn { padding: 8px 16px; border: none; border-radius: 10px; font-size: 13px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
            .btn:hover { transform: scale(0.97); }
            .btn-primary { background: #4CAF50; color: white; }
            .btn-danger { background: #e74c3c; color: white; }
            .btn-warning { background: #FF9800; color: white; }
            .btn-info { background: #2196F3; color: white; }
            .btn-outline { background: transparent; border: 2px solid white; color: white; }
            .btn-sm { padding: 4px 10px; font-size: 11px; }
            
            .stats { display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 10px; margin-bottom: 16px; }
            .stat-card { background: white; padding: 14px; border-radius: 12px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
            .stat-card .number { font-size: 26px; font-weight: 700; color: #2E7D32; }
            .stat-card .label { font-size: 12px; color: #888; }
            
            .tabs { display: flex; gap: 8px; margin-bottom: 16px; overflow-x: auto; flex-wrap: wrap; }
            .tab { padding: 8px 16px; border-radius: 20px; border: 2px solid #ddd; background: white; cursor: pointer; font-weight: 600; font-size: 13px; white-space: nowrap; }
            .tab.active { background: #2E7D32; color: white; border-color: #2E7D32; }
            
            .section { background: white; border-radius: 16px; padding: 16px; margin-bottom: 16px; box-shadow: 0 2px 10px rgba(0,0,0,0.04); }
            .section h2 { font-size: 18px; color: #1a472a; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }
            
            .product-form { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; }
            .product-form input, .product-form select, .product-form textarea { padding: 8px 12px; border: 2px solid #e8e8e8; border-radius: 10px; font-size: 14px; }
            .product-form input:focus { border-color: #4CAF50; outline: none; }
            
            .product-table { width: 100%; border-collapse: collapse; font-size: 13px; }
            .product-table th { text-align: left; padding: 8px 6px; background: #e8f5e9; color: #1a472a; }
            .product-table td { padding: 8px 6px; border-bottom: 1px solid #f0f0f0; }
            .product-table .active-badge { padding: 2px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; }
            .product-table .active-badge.active { background: #e8f5e9; color: #1B5E20; }
            .product-table .active-badge.inactive { background: #FFEBEE; color: #B71C1C; }
            
            .order-card { background: #f8faf8; padding: 12px 14px; border-radius: 12px; margin-bottom: 8px; border-left: 4px solid #FF9800; }
            .order-card.delivered { border-left-color: #4CAF50; }
            .order-card.cancelled { border-left-color: #e74c3c; }
            .order-header { display: flex; justify-content: space-between; flex-wrap: wrap; gap: 6px; }
            .order-id { font-weight: 700; color: #2E7D32; }
            .order-status { padding: 2px 12px; border-radius: 12px; font-size: 11px; font-weight: 600; }
            .status-NEW { background: #FFF3E0; color: #E65100; }
            .status-CONFIRMED { background: #E3F2FD; color: #0D47A1; }
            .status-DELIVERED { background: #E8F5E9; color: #1B5E20; }
            .status-CANCELLED { background: #FFEBEE; color: #B71C1C; }
            .order-items { font-size: 12px; color: #555; margin: 4px 0; }
            .order-actions { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 6px; }
            
            .item-stat-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 8px; }
            .item-stat-card { background: #f8faf8; padding: 10px 14px; border-radius: 10px; display: flex; justify-content: space-between; align-items: center; }
            .item-stat-card .name { font-weight: 600; }
            .item-stat-card .info { font-size: 12px; color: #666; }
            
            @media (max-width: 600px) {
                .stats { grid-template-columns: repeat(2, 1fr); }
                .product-table { font-size: 11px; }
                .product-table td, .product-table th { padding: 4px; }
                .product-form { grid-template-columns: 1fr; }
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🌿 Admin <span>Dashboard</span></h1>
            <div>
                <button class="btn btn-outline" onclick="loadAll()">🔄 Refresh</button>
            </div>
        </div>

        <!-- Stats -->
        <div class="stats" id="stats">
            <div class="stat-card"><div class="number" id="totalOrders">0</div><div class="label">Total Orders</div></div>
            <div class="stat-card"><div class="number" id="newOrders">0</div><div class="label">New Orders</div></div>
            <div class="stat-card"><div class="number" id="deliveredOrders">0</div><div class="label">Delivered</div></div>
            <div class="stat-card"><div class="number" id="totalSales">₹0</div><div class="label">Total Sales</div></div>
        </div>

        <!-- Tabs -->
        <div class="tabs">
            <button class="tab active" onclick="showTab('orders')">📋 Orders</button>
            <button class="tab" onclick="showTab('products')">🥬 Products</button>
            <button class="tab" onclick="showTab('analytics')">📊 Analytics</button>
            <button class="tab" onclick="showTab('add')">➕ Add Product</button>
        </div>

        <!-- Orders -->
        <div id="tab-orders" class="section">
            <h2>📋 Recent Orders</h2>
            <div id="ordersList"><p style="color:#888;">Loading...</p></div>
        </div>

        <!-- Products -->
        <div id="tab-products" class="section" style="display:none;">
            <h2>🥬 Product Management</h2>
            <div style="overflow-x:auto;">
                <table class="product-table" id="productTable">
                    <thead><tr><th>Image</th><th>Name</th><th>Price</th><th>MRP</th><th>Stock</th><th>Discount</th><th>Status</th><th>Actions</th></tr></thead>
                    <tbody id="productList"></tbody>
                </table>
            </div>
        </div>

        <!-- Analytics -->
        <div id="tab-analytics" class="section" style="display:none;">
            <h2>📊 Order Analytics</h2>
            <div id="analyticsContent"><p style="color:#888;">Loading...</p></div>
        </div>

        <!-- Add Product -->
        <div id="tab-add" class="section" style="display:none;">
            <h2>➕ Add New Product</h2>
            <div class="product-form" id="productForm">
                <input type="text" id="pName" placeholder="Name (English)" />
                <input type="text" id="pNameBn" placeholder="Name (বাংলা)" />
                <input type="text" id="pNameHi" placeholder="Name (हिंदी)" />
                <input type="number" id="pPrice" placeholder="Price (₹)" />
                <input type="number" id="pMrp" placeholder="MRP (₹)" />
                <input type="text" id="pUnit" placeholder="Unit (KG/Piece)" />
                <input type="number" id="pStock" placeholder="Stock" />
                <input type="number" id="pDiscount" placeholder="Discount %" />
                <input type="text" id="pImage" placeholder="Image URL" />
                <input type="text" id="pCategory" placeholder="Category" />
                <textarea id="pDesc" placeholder="Description" rows="2"></textarea>
            </div>
            <button class="btn btn-primary" onclick="addProduct()" style="margin-top:10px;">➕ Add Product</button>
        </div>

        <script>
            let allProducts = [];
            let allOrders = [];

            function showTab(tab) {
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.section').forEach(s => s.style.display = 'none');
                document.getElementById('tab-' + tab).style.display = 'block';
                document.querySelector(`.tab[onclick="showTab('${tab}')"]`).classList.add('active');
                if (tab === 'products') loadProducts();
                if (tab === 'analytics') loadAnalytics();
            }

            function loadAll() {
                loadOrders();
                loadProducts();
                loadAnalytics();
                loadStats();
            }

            function loadStats() {
                fetch('/api/orders/stats')
                    .then(r => r.json())
                    .then(data => {
                        document.getElementById('totalOrders').textContent = data.total_orders || 0;
                        document.getElementById('newOrders').textContent = data.new_orders || 0;
                        document.getElementById('deliveredOrders').textContent = data.delivered_orders || 0;
                        document.getElementById('totalSales').textContent = '₹' + (data.total_sales || 0);
                    });
            }

            function loadOrders() {
                fetch('/api/orders')
                    .then(r => r.json())
                    .then(data => {
                        allOrders = data;
                        const list = document.getElementById('ordersList');
                        if (data.length === 0) {
                            list.innerHTML = '<p style="color:#888;">📭 No orders yet</p>';
                            return;
                        }
                        data.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
                        list.innerHTML = data.slice(0, 20).map(o => `
                            <div class="order-card ${o.status.toLowerCase()}">
                                <div class="order-header">
                                    <span class="order-id">#${o.order_id}</span>
                                    <span class="order-status status-${o.status}">${o.status}</span>
                                </div>
                                <div><strong>${o.customer}</strong> | 📱 ${o.phone}</div>
                                <div>📍 ${o.address}</div>
                                <div class="order-items">${o.items.map(i => `${i.name} × ${i.quantity} ${i.unit}`).join(' | ')}</div>
                                <div style="font-weight:700;color:#2E7D32;">Total: ₹${o.total}</div>
                                <div class="order-actions">
                                    ${o.status === 'NEW' ? `<button class="btn btn-info btn-sm" onclick="updateStatus('${o.order_id}','CONFIRMED')">✅ Confirm</button>` : ''}
                                    ${o.status === 'CONFIRMED' ? `<button class="btn btn-primary btn-sm" onclick="updateStatus('${o.order_id}','DELIVERED')">✅ Deliver</button>` : ''}
                                    ${o.status !== 'DELIVERED' && o.status !== 'CANCELLED' ? `<button class="btn btn-danger btn-sm" onclick="updateStatus('${o.order_id}','CANCELLED')">❌ Cancel</button>` : ''}
                                    <button class="btn btn-info btn-sm" onclick="window.location.href='tel:${o.phone}'">📞 Call</button>
                                    <button class="btn btn-sm" style="background:#25D366;color:white;" onclick="window.open('https://wa.me/${o.phone}?text=Your%20order%20${o.order_id}')">💬 WhatsApp</button>
                                </div>
                            </div>
                        `).join('');
                    });
            }

            function loadProducts() {
                fetch('/api/products')
                    .then(r => r.json())
                    .then(data => {
                        allProducts = data;
                        const list = document.getElementById('productList');
                        list.innerHTML = data.map(p => `
                            <tr>
                                <td><img src="${p.image}" style="width:40px;height:40px;object-fit:cover;border-radius:6px;" /></td>
                                <td><strong>${p.name}</strong><br><small style="color:#888;">${p.name_bn || ''}</small></td>
                                <td>₹${p.price}</td>
                                <td><span style="text-decoration:line-through;color:#888;">₹${p.mrp || p.price}</span></td>
                                <td>${p.stock}</td>
                                <td>${p.discount || 0}%</td>
                                <td><span class="active-badge ${p.active !== false ? 'active' : 'inactive'}">${p.active !== false ? 'Active' : 'Inactive'}</span></td>
                                <td>
                                    <button class="btn btn-warning btn-sm" onclick="toggleProduct(${p.id})">${p.active !== false ? '🔴 Inactive' : '🟢 Active'}</button>
                                    <button class="btn btn-danger btn-sm" onclick="deleteProduct(${p.id})">🗑️</button>
                                </td>
                            </tr>
                        `).join('');
                    });
            }

            function loadAnalytics() {
                fetch('/api/orders/stats')
                    .then(r => r.json())
                    .then(data => {
                        const container = document.getElementById('analyticsContent');
                        const items = data.item_stats || {};
                        const keys = Object.keys(items);
                        if (keys.length === 0) {
                            container.innerHTML = '<p style="color:#888;">No orders yet to analyze</p>';
                            return;
                        }
                        let html = `<div class="item-stat-grid">`;
                        keys.forEach(name => {
                            const stat = items[name];
                            html += `
                                <div class="item-stat-card">
                                    <div>
                                        <div class="name">${name}</div>
                                        <div class="info">${stat.count} orders</div>
                                    </div>
                                    <div style="text-align:right;">
                                        <div style="font-weight:700;color:#2E7D32;">${stat.total_qty} qty</div>
                                        <div class="info">₹${stat.total_revenue}</div>
                                    </div>
                                </div>
                            `;
                        });
                        html += '</div>';
                        container.innerHTML = html;
                    });
            }

            function updateStatus(orderId, status) {
                fetch('/api/order/status', {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ order_id: orderId, status: status })
                }).then(() => loadAll());
            }

            function toggleProduct(id) {
                fetch(`/api/products/${id}/toggle`, { method: 'PUT' })
                    .then(() => loadProducts());
            }

            function deleteProduct(id) {
                if (!confirm('Delete this product?')) return;
                fetch(`/api/products/${id}`, { method: 'DELETE' })
                    .then(() => loadProducts());
            }

            function addProduct() {
                const product = {
                    name: document.getElementById('pName').value,
                    name_bn: document.getElementById('pNameBn').value,
                    name_hi: document.getElementById('pNameHi').value,
                    price: parseFloat(document.getElementById('pPrice').value) || 0,
                    mrp: parseFloat(document.getElementById('pMrp').value) || 0,
                    unit: document.getElementById('pUnit').value || 'KG',
                    stock: parseInt(document.getElementById('pStock').value) || 0,
                    discount: parseFloat(document.getElementById('pDiscount').value) || 0,
                    image: document.getElementById('pImage').value || 'https://via.placeholder.com/300',
                    category: document.getElementById('pCategory').value || 'Vegetables',
                    description: document.getElementById('pDesc').value || '',
                    active: true
                };
                fetch('/api/products', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(product)
                }).then(r => r.json()).then(data => {
                    if (data.success) {
                        alert('✅ Product added!');
                        document.querySelectorAll('#productForm input, #productForm textarea').forEach(el => el.value = '');
                        loadProducts();
                    }
                });
            }

            // Auto refresh
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