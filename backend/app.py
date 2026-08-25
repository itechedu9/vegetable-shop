from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)

# ============ DATA STORAGE ============
# In-memory storage (will be replaced with database later)
products = [
    {
        "id": 1,
        "name": "Potato",
        "name_bn": "আলু",
        "name_hi": "आलू",
        "price": 30,
        "unit": "KG",
        "image": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=300&h=300&fit=crop",
        "category": "Vegetables",
        "stock": 100,
        "discount": 0,
        "available": True,
        "description": "Fresh farm potatoes"
    },
    {
        "id": 2,
        "name": "Tomato",
        "name_bn": "টমেটো",
        "name_hi": "टमाटर",
        "price": 40,
        "unit": "KG",
        "image": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=300&h=300&fit=crop",
        "category": "Vegetables",
        "stock": 80,
        "discount": 10,
        "available": True,
        "description": "Fresh red tomatoes"
    },
    {
        "id": 3,
        "name": "Cauliflower",
        "name_bn": "ফুলকপি",
        "name_hi": "फूलगोभी",
        "price": 50,
        "unit": "Piece",
        "image": "https://images.unsplash.com/photo-1568585100875-6dd3721b43ed?w=300&h=300&fit=crop",
        "category": "Vegetables",
        "stock": 40,
        "discount": 0,
        "available": True,
        "description": "Fresh cauliflower"
    },
    {
        "id": 4,
        "name": "Spinach",
        "name_bn": "পালং শাক",
        "name_hi": "पालक",
        "price": 20,
        "unit": "Bundle",
        "image": "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=300&h=300&fit=crop",
        "category": "Leafy",
        "stock": 60,
        "discount": 0,
        "available": True,
        "description": "Fresh green spinach"
    },
    {
        "id": 5,
        "name": "Onion",
        "name_bn": "পেঁয়াজ",
        "name_hi": "प्याज",
        "price": 35,
        "unit": "KG",
        "image": "https://images.unsplash.com/photo-1508747703725-719777637510?w=300&h=300&fit=crop",
        "category": "Vegetables",
        "stock": 150,
        "discount": 5,
        "available": True,
        "description": "Fresh onions"
    },
    {
        "id": 6,
        "name": "Garlic",
        "name_bn": "রসুন",
        "name_hi": "लहसुन",
        "price": 120,
        "unit": "KG",
        "image": "https://images.unsplash.com/photo-1541808814-4544cb5342c7?w=300&h=300&fit=crop",
        "category": "Vegetables",
        "stock": 30,
        "discount": 0,
        "available": True,
        "description": "Fresh garlic"
    },
    {
        "id": 7,
        "name": "Carrot",
        "name_bn": "গাজর",
        "name_hi": "गाजर",
        "price": 45,
        "unit": "KG",
        "image": "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=300&h=300&fit=crop",
        "category": "Roots",
        "stock": 55,
        "discount": 0,
        "available": True,
        "description": "Fresh carrots"
    },
    {
        "id": 8,
        "name": "Brinjal",
        "name_bn": "বেগুন",
        "name_hi": "बैंगन",
        "price": 40,
        "unit": "KG",
        "image": "https://images.unsplash.com/photo-1552074284-5e88ef1aef18?w=300&h=300&fit=crop",
        "category": "Vegetables",
        "stock": 45,
        "discount": 0,
        "available": True,
        "description": "Fresh brinjals"
    }
]

orders = []
order_counter = 1

# ============ API ROUTES ============

@app.route('/')
def home():
    return jsonify({
        'message': '🌿 Vegetable Shop API',
        'status': 'running',
        'version': '2.0.0'
    })

# ---------- PRODUCTS ----------
@app.route('/api/products')
def get_products():
    return jsonify(products)

@app.route('/api/products/<int:product_id>')
def get_product(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({'error': 'Product not found'}), 404

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
        'unit': data.get('unit', 'KG'),
        'image': data.get('image', ''),
        'category': data.get('category', 'Vegetables'),
        'stock': int(data.get('stock', 0)),
        'discount': float(data.get('discount', 0)),
        'available': data.get('available', True),
        'description': data.get('description', '')
    }
    products.append(product)
    return jsonify({'success': True, 'product': product})

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    product = next((p for p in products if p['id'] == product_id), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    product.update({
        'name': data.get('name', product['name']),
        'name_bn': data.get('name_bn', product.get('name_bn', '')),
        'name_hi': data.get('name_hi', product.get('name_hi', '')),
        'price': float(data.get('price', product['price'])),
        'unit': data.get('unit', product['unit']),
        'image': data.get('image', product['image']),
        'category': data.get('category', product['category']),
        'stock': int(data.get('stock', product['stock'])),
        'discount': float(data.get('discount', product.get('discount', 0))),
        'available': data.get('available', product['available']),
        'description': data.get('description', product.get('description', ''))
    })
    return jsonify({'success': True, 'product': product})

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products
    products = [p for p in products if p['id'] != product_id]
    return jsonify({'success': True})

# ---------- ORDERS ----------
@app.route('/api/orders')
def get_orders():
    return jsonify(orders)

@app.route('/api/orders/<order_id>')
def get_order(order_id):
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if order:
        return jsonify(order)
    return jsonify({'error': 'Order not found'}), 404

@app.route('/api/orders/track', methods=['POST'])
def track_order():
    data = request.json
    order_id = data.get('order_id')
    phone = data.get('phone')
    
    order = next((o for o in orders if o['order_id'] == order_id and o['phone'] == phone), None)
    if order:
        return jsonify(order)
    return jsonify({'error': 'Order not found'}), 404

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
        'payment_status': 'PENDING' if data.get('payment_method') == 'COD' else 'PAID',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Reduce stock
    for item in order['items']:
        product = next((p for p in products if p['name'].lower() == item['name'].lower()), None)
        if product:
            product['stock'] -= item['quantity']
    
    orders.append(order)
    order_counter += 1
    
    return jsonify({
        'success': True,
        'order': order,
        'message': 'Order placed successfully!'
    })

@app.route('/api/order/status', methods=['PUT'])
def update_order_status():
    data = request.json
    order_id = data.get('order_id')
    new_status = data.get('status')
    
    for order in orders:
        if order['order_id'] == order_id:
            order['status'] = new_status
            order['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            return jsonify({'success': True, 'order': order})
    
    return jsonify({'success': False, 'message': 'Order not found'}), 404

# ---------- ADMIN DASHBOARD ----------
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
            body { 
                font-family: -apple-system, 'Segoe UI', Roboto, sans-serif;
                background: #f0f4f8;
                padding: 12px;
            }
            .header {
                background: linear-gradient(135deg, #1a472a, #2E7D32);
                color: white;
                padding: 16px 20px;
                border-radius: 16px;
                margin-bottom: 16px;
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 10px;
            }
            .header h1 { font-size: 22px; }
            .header-actions { display: flex; gap: 10px; flex-wrap: wrap; }
            .btn {
                padding: 8px 16px;
                border: none;
                border-radius: 10px;
                font-size: 13px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
            }
            .btn:hover { transform: scale(0.97); }
            .btn-primary { background: #4CAF50; color: white; }
            .btn-outline { background: transparent; border: 2px solid white; color: white; }
            
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
                gap: 10px;
                margin-bottom: 16px;
            }
            .stat-card {
                background: white;
                padding: 14px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            }
            .stat-card .number { font-size: 24px; font-weight: 700; color: #2E7D32; }
            .stat-card .label { font-size: 12px; color: #888; }
            
            .tabs {
                display: flex;
                gap: 8px;
                margin-bottom: 16px;
                overflow-x: auto;
            }
            .tab {
                padding: 8px 16px;
                border-radius: 20px;
                border: 2px solid #ddd;
                background: white;
                cursor: pointer;
                font-weight: 600;
                font-size: 13px;
                white-space: nowrap;
            }
            .tab.active { background: #2E7D32; color: white; border-color: #2E7D32; }
            
            .order-card {
                background: white;
                border-radius: 14px;
                padding: 16px;
                margin-bottom: 12px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.06);
                border-left: 5px solid #FF9800;
            }
            .order-card.delivered { border-left-color: #4CAF50; }
            .order-card.cancelled { border-left-color: #e74c3c; }
            .order-card.confirmed { border-left-color: #2196F3; }
            
            .order-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                flex-wrap: wrap;
                gap: 8px;
                margin-bottom: 8px;
            }
            .order-id { font-weight: 700; color: #2E7D32; font-size: 16px; }
            .order-status {
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
            }
            .status-new { background: #FFF3E0; color: #E65100; }
            .status-confirmed { background: #E3F2FD; color: #0D47A1; }
            .status-preparing { background: #F3E5F5; color: #6A1B9A; }
            .status-out_for_delivery { background: #FFF8E1; color: #F57F17; }
            .status-delivered { background: #E8F5E9; color: #1B5E20; }
            .status-cancelled { background: #FFEBEE; color: #B71C1C; }
            
            .order-details { font-size: 14px; color: #444; margin: 4px 0; }
            .order-items {
                background: #f8faf8;
                padding: 8px 12px;
                border-radius: 8px;
                font-size: 13px;
                margin: 8px 0;
            }
            .order-actions {
                display: flex;
                gap: 8px;
                margin-top: 10px;
                flex-wrap: wrap;
            }
            .btn-confirm { background: #2196F3; color: white; }
            .btn-prepare { background: #9C27B0; color: white; }
            .btn-deliver { background: #FF9800; color: white; }
            .btn-complete { background: #4CAF50; color: white; }
            .btn-cancel { background: #e74c3c; color: white; }
            .btn-call { background: #25D366; color: white; }
            .btn-whatsapp { background: #075E54; color: white; }
            
            .product-form {
                background: white;
                padding: 20px;
                border-radius: 14px;
                margin-bottom: 16px;
            }
            .product-form h3 { margin-bottom: 12px; color: #2E7D32; }
            .form-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                gap: 10px;
            }
            .form-grid input, .form-grid select, .form-grid textarea {
                padding: 10px 12px;
                border: 2px solid #e8e8e8;
                border-radius: 10px;
                font-size: 14px;
            }
            .form-grid input:focus { border-color: #4CAF50; outline: none; }
            
            @media (max-width: 600px) {
                .stats { grid-template-columns: repeat(2, 1fr); }
                .order-actions { flex-direction: column; }
                .order-actions .btn { width: 100%; }
                .form-grid { grid-template-columns: 1fr; }
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🌿 Admin Dashboard</h1>
            <div class="header-actions">
                <button class="btn btn-outline" onclick="loadOrders()">🔄 Refresh</button>
                <button class="btn btn-primary" onclick="document.getElementById('productForm').scrollIntoView()">+ Add Product</button>
            </div>
        </div>
        
        <div class="stats" id="stats">
            <div class="stat-card"><div class="number" id="totalOrders">0</div><div class="label">Total Orders</div></div>
            <div class="stat-card"><div class="number" id="newOrders">0</div><div class="label">New Orders</div></div>
            <div class="stat-card"><div class="number" id="deliveredOrders">0</div><div class="label">Delivered</div></div>
            <div class="stat-card"><div class="number" id="totalSales">₹0</div><div class="label">Total Sales</div></div>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="filterOrders('all')">All</button>
            <button class="tab" onclick="filterOrders('NEW')">🆕 New</button>
            <button class="tab" onclick="filterOrders('CONFIRMED')">✅ Confirmed</button>
            <button class="tab" onclick="filterOrders('PREPARING')">🔪 Preparing</button>
            <button class="tab" onclick="filterOrders('OUT_FOR_DELIVERY')">🚚 Delivering</button>
            <button class="tab" onclick="filterOrders('DELIVERED')">🏠 Delivered</button>
            <button class="tab" onclick="filterOrders('CANCELLED')">❌ Cancelled</button>
        </div>
        
        <div id="ordersList"></div>
        
        <!-- Product Form -->
        <div class="product-form" id="productForm">
            <h3>➕ Add New Product</h3>
            <div class="form-grid">
                <input type="text" id="pName" placeholder="Product Name (English)" />
                <input type="text" id="pNameBn" placeholder="Name (বাংলা)" />
                <input type="text" id="pNameHi" placeholder="Name (हिंदी)" />
                <input type="number" id="pPrice" placeholder="Price (₹)" />
                <input type="text" id="pUnit" placeholder="Unit (KG/Piece)" />
                <input type="text" id="pImage" placeholder="Image URL" />
                <input type="text" id="pCategory" placeholder="Category" />
                <input type="number" id="pStock" placeholder="Stock Quantity" />
                <input type="number" id="pDiscount" placeholder="Discount %" />
                <textarea id="pDesc" placeholder="Description" rows="2"></textarea>
            </div>
            <button class="btn btn-primary" onclick="addProduct()" style="margin-top:10px;">➕ Add Product</button>
        </div>
        
        <script>
            let allOrders = [];
            let currentFilter = 'all';
            
            function loadOrders() {
                fetch('/api/orders')
                    .then(res => res.json())
                    .then(data => {
                        allOrders = data;
                        renderOrders();
                        updateStats();
                    })
                    .catch(err => {
                        document.getElementById('ordersList').innerHTML = 
                            '<p style="color:red;text-align:center;padding:20px;">⚠️ Error loading orders. Make sure backend is running.</p>';
                    });
            }
            
            function filterOrders(status) {
                currentFilter = status;
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                event.target.classList.add('active');
                renderOrders();
            }
            
            function renderOrders() {
                const list = document.getElementById('ordersList');
                let filtered = allOrders;
                if (currentFilter !== 'all') {
                    filtered = allOrders.filter(o => o.status === currentFilter);
                }
                
                if (filtered.length === 0) {
                    list.innerHTML = '<p style="text-align:center;color:#888;padding:40px;">📭 No orders found</p>';
                    return;
                }
                
                // Sort: newest first
                filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
                
                list.innerHTML = filtered.map(order => `
                    <div class="order-card ${order.status.toLowerCase()}">
                        <div class="order-header">
                            <span class="order-id">#${order.order_id}</span>
                            <span class="order-status status-${order.status.toLowerCase()}">${order.status}</span>
                        </div>
                        <div class="order-details"><strong>${order.customer}</strong> | 📱 ${order.phone}</div>
                        <div class="order-details">📍 ${order.address}</div>
                        <div class="order-items">
                            ${order.items.map(item => 
                                `${item.name} × ${item.quantity} ${item.unit} = ₹${(item.price * item.quantity).toFixed(2)}`
                            ).join(' | ')}
                        </div>
                        <div class="order-details" style="font-weight:700;color:#2E7D32;font-size:16px;">
                            Total: ₹${order.total}
                        </div>
                        <div class="order-actions">
                            ${order.status === 'NEW' ? `<button class="btn btn-confirm" onclick="updateStatus('${order.order_id}','CONFIRMED')">✅ Confirm</button>` : ''}
                            ${order.status === 'CONFIRMED' ? `<button class="btn btn-prepare" onclick="updateStatus('${order.order_id}','PREPARING')">🔪 Prepare</button>` : ''}
                            ${order.status === 'PREPARING' ? `<button class="btn btn-deliver" onclick="updateStatus('${order.order_id}','OUT_FOR_DELIVERY')">🚚 Deliver</button>` : ''}
                            ${order.status === 'OUT_FOR_DELIVERY' ? `<button class="btn btn-complete" onclick="updateStatus('${order.order_id}','DELIVERED')">✅ Complete</button>` : ''}
                            ${order.status !== 'DELIVERED' && order.status !== 'CANCELLED' ? 
                                `<button class="btn btn-cancel" onclick="updateStatus('${order.order_id}','CANCELLED')">❌ Cancel</button>` : ''}
                            <button class="btn btn-call" onclick="window.location.href='tel:${order.phone}'">📞 Call</button>
                            <button class="btn btn-whatsapp" onclick="window.open('https://wa.me/${order.phone}?text=Your%20order%20${order.order_id}%20has%20been%20updated%20to%20${order.status}','_blank')">💬 WhatsApp</button>
                        </div>
                    </div>
                `).join('');
            }
            
            function updateStats() {
                document.getElementById('totalOrders').textContent = allOrders.length;
                document.getElementById('newOrders').textContent = allOrders.filter(o => o.status === 'NEW').length;
                document.getElementById('deliveredOrders').textContent = allOrders.filter(o => o.status === 'DELIVERED').length;
                const total = allOrders.reduce((sum, o) => sum + (o.total || 0), 0);
                document.getElementById('totalSales').textContent = '₹' + total;
            }
            
            function updateStatus(orderId, status) {
                fetch('/api/order/status', {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ order_id: orderId, status: status })
                })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        loadOrders();
                    }
                })
                .catch(err => alert('Error updating status'));
            }
            
            function addProduct() {
                const product = {
                    name: document.getElementById('pName').value,
                    name_bn: document.getElementById('pNameBn').value,
                    name_hi: document.getElementById('pNameHi').value,
                    price: parseFloat(document.getElementById('pPrice').value),
                    unit: document.getElementById('pUnit').value,
                    image: document.getElementById('pImage').value || 'https://via.placeholder.com/300',
                    category: document.getElementById('pCategory').value || 'Vegetables',
                    stock: parseInt(document.getElementById('pStock').value) || 0,
                    discount: parseFloat(document.getElementById('pDiscount').value) || 0,
                    description: document.getElementById('pDesc').value,
                    available: true
                };
                
                fetch('/api/products', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(product)
                })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        alert('✅ Product added successfully!');
                        ['pName','pNameBn','pNameHi','pPrice','pUnit','pImage','pCategory','pStock','pDiscount','pDesc'].forEach(id => 
                            document.getElementById(id).value = '');
                    }
                })
                .catch(err => alert('Error adding product'));
            }
            
            // Auto refresh every 30 seconds
            loadOrders();
            setInterval(loadOrders, 30000);
        </script>
    </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)