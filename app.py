from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import os
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# ===== ডাটাবেস সিমুলেশন (ইন-মেমরি) =====
products = []
orders = []
suppliers = []
shops = []
order_counter = 1

# ===== স্যাম্পল ডাটা =====
def init_data():
    global products, suppliers, shops
    shops = [
        {"id": "shop1", "name": "Main Shop", "address": "Falakata, WB", "phone": "9876543210"},
        {"id": "shop2", "name": "Branch 1", "address": "Jateswar, WB", "phone": "9876543211"}
    ]
    suppliers = [
        {"id": "sup1", "name": "Green Farms", "phone": "9876543212", "address": "Siliguri"},
        {"id": "sup2", "name": "Fresh Supply Co.", "phone": "9876543213", "address": "Jalpaiguri"}
    ]
    products = [
        {"id": 1, "name": "Potato", "name_bn": "আলু", "category": "Vegetables", "sub_category": "Roots",
         "price": 30, "mrp": 40, "unit": "KG", "stock": 100, "min_stock": 20, "discount": 25,
         "image": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=200&h=200&fit=crop",
         "shop_id": "shop1", "supplier_id": "sup1", "active": True},
        {"id": 2, "name": "Tomato", "name_bn": "টমেটো", "category": "Vegetables", "sub_category": "Fruits",
         "price": 40, "mrp": 55, "unit": "KG", "stock": 80, "min_stock": 15, "discount": 27,
         "image": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=200&h=200&fit=crop",
         "shop_id": "shop1", "supplier_id": "sup1", "active": True},
        {"id": 3, "name": "Rice", "name_bn": "চাল", "category": "Grocery", "sub_category": "Grains",
         "price": 60, "mrp": 70, "unit": "KG", "stock": 200, "min_stock": 50, "discount": 10,
         "image": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=200&h=200&fit=crop",
         "shop_id": "shop1", "supplier_id": "sup2", "active": True},
        {"id": 4, "name": "Sugar", "name_bn": "চিনি", "category": "Grocery", "sub_category": "Essentials",
         "price": 45, "mrp": 55, "unit": "KG", "stock": 150, "min_stock": 30, "discount": 15,
         "image": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=200&h=200&fit=crop",
         "shop_id": "shop1", "supplier_id": "sup2", "active": True},
        {"id": 5, "name": "Onion", "name_bn": "পেঁয়াজ", "category": "Vegetables", "sub_category": "Roots",
         "price": 35, "mrp": 45, "unit": "KG", "stock": 150, "min_stock": 25, "discount": 22,
         "image": "https://images.unsplash.com/photo-1508747703725-719777637510?w=200&h=200&fit=crop",
         "shop_id": "shop1", "supplier_id": "sup1", "active": True},
        {"id": 6, "name": "Garlic", "name_bn": "রসুন", "category": "Vegetables", "sub_category": "Roots",
         "price": 120, "mrp": 150, "unit": "KG", "stock": 30, "min_stock": 10, "discount": 20,
         "image": "https://images.unsplash.com/photo-1541808814-4544cb5342c7?w=200&h=200&fit=crop",
         "shop_id": "shop1", "supplier_id": "sup1", "active": True}
    ]

init_data()

# ===== API রাউট =====
@app.route('/')
def home():
    return jsonify({'message': '🌿 Vegetable & Grocery Shop API', 'status': 'running', 'version': '3.0'})

# ---------- প্রোডাক্ট ----------
@app.route('/api/products')
def get_products():
    return jsonify(products)

@app.route('/api/products/active')
def get_active_products():
    return jsonify([p for p in products if p.get('active', True)])

@app.route('/api/products/shop/<shop_id>')
def get_products_by_shop(shop_id):
    return jsonify([p for p in products if p.get('shop_id') == shop_id and p.get('active', True)])

@app.route('/api/products/category/<category>')
def get_products_by_category(category):
    return jsonify([p for p in products if p.get('category') == category and p.get('active', True)])

@app.route('/api/products/low-stock')
def get_low_stock():
    return jsonify([p for p in products if p.get('stock', 0) <= p.get('min_stock', 0) and p.get('active', True)])

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    new_id = max([p['id'] for p in products]) + 1 if products else 1
    product = {
        'id': new_id,
        'name': data.get('name'),
        'name_bn': data.get('name_bn', ''),
        'category': data.get('category', 'Vegetables'),
        'sub_category': data.get('sub_category', ''),
        'price': float(data.get('price', 0)),
        'mrp': float(data.get('mrp', data.get('price', 0))),
        'unit': data.get('unit', 'KG'),
        'stock': int(data.get('stock', 0)),
        'min_stock': int(data.get('min_stock', 10)),
        'discount': float(data.get('discount', 0)),
        'image': data.get('image', ''),
        'shop_id': data.get('shop_id', 'shop1'),
        'supplier_id': data.get('supplier_id', ''),
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
        'name_bn': data.get('name_bn', product.get('name_bn', '')),
        'category': data.get('category', product['category']),
        'sub_category': data.get('sub_category', product.get('sub_category', '')),
        'price': float(data.get('price', product['price'])),
        'mrp': float(data.get('mrp', product.get('mrp', product['price']))),
        'unit': data.get('unit', product['unit']),
        'stock': int(data.get('stock', product['stock'])),
        'min_stock': int(data.get('min_stock', product.get('min_stock', 10))),
        'discount': float(data.get('discount', product.get('discount', 0))),
        'image': data.get('image', product['image']),
        'shop_id': data.get('shop_id', product.get('shop_id', 'shop1')),
        'supplier_id': data.get('supplier_id', product.get('supplier_id', '')),
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

# ---------- শপ ----------
@app.route('/api/shops')
def get_shops():
    return jsonify(shops)

@app.route('/api/shops', methods=['POST'])
def add_shop():
    data = request.json
    shop = {
        'id': f"shop{len(shops)+1}",
        'name': data.get('name'),
        'address': data.get('address', ''),
        'phone': data.get('phone', '')
    }
    shops.append(shop)
    return jsonify({'success': True, 'shop': shop})

# ---------- সাপ্লায়ার ----------
@app.route('/api/suppliers')
def get_suppliers():
    return jsonify(suppliers)

@app.route('/api/suppliers', methods=['POST'])
def add_supplier():
    data = request.json
    supplier = {
        'id': f"sup{len(suppliers)+1}",
        'name': data.get('name'),
        'phone': data.get('phone', ''),
        'address': data.get('address', '')
    }
    suppliers.append(supplier)
    return jsonify({'success': True, 'supplier': supplier})

# ---------- অর্ডার ----------
@app.route('/api/orders')
def get_orders():
    return jsonify(orders)

@app.route('/api/orders/stats')
def get_stats():
    total = len(orders)
    new = len([o for o in orders if o.get('status') == 'NEW'])
    confirmed = len([o for o in orders if o.get('status') == 'CONFIRMED'])
    delivered = len([o for o in orders if o.get('status') == 'DELIVERED'])
    total_sales = sum([o.get('total', 0) for o in orders if o.get('status') != 'CANCELLED'])
    return jsonify({
        'total_orders': total, 'new_orders': new, 'confirmed_orders': confirmed,
        'delivered_orders': delivered, 'total_sales': total_sales
    })

@app.route('/api/order', methods=['POST'])
def create_order():
    global order_counter
    data = request.json
    for item in data.get('items', []):
        product = next((p for p in products if p['name'].lower() == item['name'].lower()), None)
        if product and product['stock'] < item['quantity']:
            return jsonify({'success': False, 'message': f'Insufficient stock for {item["name"]}'}), 400
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
        .btn-success { background: #27ae60; color: white; }
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
        .form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; }
        .form-grid input, .form-grid select { padding: 8px 12px; border: 2px solid #e8e8e8; border-radius: 10px; font-size: 14px; }
        .form-grid input:focus, .form-grid select:focus { border-color: #4CAF50; outline: none; }
        .table-wrap { overflow-x: auto; }
        table { width: 100%; border-collapse: collapse; font-size: 13px; }
        th { text-align: left; padding: 8px 6px; background: #e8f5e9; color: #1a472a; }
        td { padding: 8px 6px; border-bottom: 1px solid #f0f0f0; vertical-align: middle; }
        .badge { padding: 2px 10px; border-radius: 12px; font-size: 11px; font-weight: 600; }
        .badge-active { background: #e8f5e9; color: #1B5E20; }
        .badge-inactive { background: #FFEBEE; color: #B71C1C; }
        .badge-new { background: #FFF3E0; color: #E65100; }
        .badge-confirmed { background: #E3F2FD; color: #0D47A1; }
        .badge-delivered { background: #E8F5E9; color: #1B5E20; }
        .badge-cancelled { background: #FFEBEE; color: #B71C1C; }
        .stock-low { color: #e74c3c; font-weight: 700; }
        .modal { display: none; position: fixed; top:0;left:0;right:0;bottom:0; background:rgba(0,0,0,0.6); backdrop-filter:blur(8px); z-index:1000; justify-content:center; align-items:center; padding:20px; }
        .modal.active { display: flex; }
        .modal-box { background: white; max-width: 600px; width:100%; border-radius:20px; padding:24px; max-height:90vh; overflow-y:auto; }
        .modal-header { display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; }
        .modal-close { background:#f0f0f0; border:none; width:36px; height:36px; border-radius:50%; font-size:20px; cursor:pointer; }
        .modal-footer { display:flex; gap:10px; margin-top:16px; justify-content:flex-end; }
        @media (max-width:600px) { .stats { grid-template-columns:repeat(2,1fr); } .form-grid { grid-template-columns:1fr; } }
    </style>
</head>
<body>
<div class="header">
    <h1>🌿 Admin <span>Dashboard</span></h1>
    <div>
        <span id="lowStockAlert" style="background:#e74c3c;color:white;padding:4px 12px;border-radius:20px;font-size:12px;display:none;margin-right:10px;">⚠️ Low Stock!</span>
        <button class="btn btn-outline" onclick="loadAll()">🔄 Refresh</button>
    </div>
</div>

<div class="stats" id="stats">
    <div class="stat-card"><div class="number" id="totalOrders">0</div><div class="label">Total Orders</div></div>
    <div class="stat-card"><div class="number" id="newOrders">0</div><div class="label">New Orders</div></div>
    <div class="stat-card"><div class="number" id="deliveredOrders">0</div><div class="label">Delivered</div></div>
    <div class="stat-card"><div class="number" id="totalSales">₹0</div><div class="label">Total Sales</div></div>
</div>

<div class="tabs">
    <button class="tab active" onclick="showTab('orders')">📋 Orders</button>
    <button class="tab" onclick="showTab('products')">🥬 Products</button>
    <button class="tab" onclick="showTab('stock')">📦 Stock</button>
    <button class="tab" onclick="showTab('add')">➕ Add Product</button>
    <button class="tab" onclick="showTab('shops')">🏪 Shops</button>
    <button class="tab" onclick="showTab('suppliers')">🏭 Suppliers</button>
</div>

<!-- Orders -->
<div id="tab-orders" class="section"><h2>📋 Orders</h2><div id="ordersList"></div></div>

<!-- Products -->
<div id="tab-products" class="section" style="display:none;">
    <h2>🥬 Products</h2>
    <div class="table-wrap"><table><thead><tr>
        <th>Image</th><th>Name</th><th>Category</th><th>Price</th><th>MRP</th><th>Stock</th><th>Discount</th><th>Shop</th><th>Status</th><th>Actions</th>
    </tr></thead><tbody id="productList"></tbody></table></div>
</div>

<!-- Stock -->
<div id="tab-stock" class="section" style="display:none;"><h2>📦 Stock Management</h2><div id="stockList"></div></div>

<!-- Add Product -->
<div id="tab-add" class="section" style="display:none;">
    <h2>➕ Add Product</h2>
    <div style="margin-bottom:12px;">
        <label>Image URL:</label>
        <input type="text" id="pImage" placeholder="https://example.com/image.jpg" style="width:100%;padding:8px;border:2px solid #ddd;border-radius:10px;margin-top:4px;" />
    </div>
    <div class="form-grid">
        <input type="text" id="pName" placeholder="Name" />
        <input type="text" id="pNameBn" placeholder="Name (বাংলা)" />
        <select id="pCategory"><option value="Vegetables">Vegetables</option><option value="Grocery">Grocery</option><option value="Fruits">Fruits</option></select>
        <input type="text" id="pSubCategory" placeholder="Sub Category" />
        <input type="number" id="pPrice" placeholder="Price" />
        <input type="number" id="pMrp" placeholder="MRP" />
        <input type="text" id="pUnit" placeholder="Unit (KG/Piece)" />
        <input type="number" id="pStock" placeholder="Stock" />
        <input type="number" id="pMinStock" placeholder="Min Stock Alert" />
        <input type="number" id="pDiscount" placeholder="Discount %" />
        <select id="pShopId"></select>
        <select id="pSupplierId"><option value="">Select Supplier</option></select>
    </div>
    <button class="btn btn-primary" onclick="addProduct()" style="margin-top:10px;">➕ Add Product</button>
</div>

<!-- Shops -->
<div id="tab-shops" class="section" style="display:none;">
    <h2>🏪 Shop Management</h2>
    <div class="form-grid" style="margin-bottom:12px;">
        <input type="text" id="shopName" placeholder="Shop Name" />
        <input type="text" id="shopAddress" placeholder="Address" />
        <input type="text" id="shopPhone" placeholder="Phone" />
    </div>
    <button class="btn btn-primary" onclick="addShop()">➕ Add Shop</button>
    <div id="shopList" style="margin-top:12px;"></div>
</div>

<!-- Suppliers -->
<div id="tab-suppliers" class="section" style="display:none;">
    <h2>🏭 Supplier Management</h2>
    <div class="form-grid" style="margin-bottom:12px;">
        <input type="text" id="supName" placeholder="Supplier Name" />
        <input type="text" id="supPhone" placeholder="Phone" />
        <input type="text" id="supAddress" placeholder="Address" />
    </div>
    <button class="btn btn-primary" onclick="addSupplier()">➕ Add Supplier</button>
    <div id="supplierList" style="margin-top:12px;"></div>
</div>

<!-- Stock Modal -->
<div class="modal" id="stockModal">
    <div class="modal-box">
        <div class="modal-header"><h2>📦 Update Stock</h2><button class="modal-close" onclick="closeStockModal()">✕</button></div>
        <div class="modal-body">
            <p><strong id="stockProductName"></strong></p>
            <p>Current Stock: <span id="stockCurrent"></span></p>
            <div class="form-grid" style="margin-top:10px;">
                <input type="number" id="stockNew" placeholder="New Stock" />
                <input type="number" id="stockMin" placeholder="Min Stock Alert" />
            </div>
        </div>
        <div class="modal-footer">
            <button class="btn btn-danger" onclick="closeStockModal()">Cancel</button>
            <button class="btn btn-primary" onclick="saveStock()">💾 Update</button>
        </div>
    </div>
</div>

<script>
let allProducts = [], allOrders = [], allShops = [], allSuppliers = [];
let editingStockId = null;

function showTab(tab) {
    document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
    document.querySelectorAll('.section').forEach(s=>s.style.display='none');
    document.getElementById('tab-'+tab).style.display='block';
    document.querySelector(`.tab[onclick="showTab('${tab}')"]`).classList.add('active');
    if(tab==='products') loadProducts();
    if(tab==='stock') loadStock();
    if(tab==='shops') loadShops();
    if(tab==='suppliers') loadSuppliers();
}

function loadAll() {
    loadStats(); loadOrders(); loadProducts(); loadStock(); loadShops(); loadSuppliers(); checkLowStock();
}

function loadStats() {
    fetch('/api/orders/stats').then(r=>r.json()).then(d=>{
        document.getElementById('totalOrders').textContent=d.total_orders||0;
        document.getElementById('newOrders').textContent=d.new_orders||0;
        document.getElementById('deliveredOrders').textContent=d.delivered_orders||0;
        document.getElementById('totalSales').textContent='₹'+(d.total_sales||0);
    });
}

function loadOrders() {
    fetch('/api/orders').then(r=>r.json()).then(d=>{
        const list=document.getElementById('ordersList');
        if(!d.length){list.innerHTML='<p style="color:#888;">📭 No orders</p>';return;}
        list.innerHTML=d.sort((a,b)=>new Date(b.created_at)-new Date(a.created_at)).slice(0,20).map(o=>`
            <div style="border-bottom:1px solid #eee;padding:10px 0;display:flex;justify-content:space-between;flex-wrap:wrap;gap:6px;">
                <div><strong>#${o.order_id}</strong> <span class="badge badge-${o.status.toLowerCase()}">${o.status}</span> ${o.customer} | ₹${o.total}</div>
                <div>
                    ${o.status==='NEW'?`<button class="btn btn-info btn-sm" onclick="updateStatus('${o.order_id}','CONFIRMED')">Confirm</button>`:''}
                    ${o.status==='CONFIRMED'?`<button class="btn btn-success btn-sm" onclick="updateStatus('${o.order_id}','DELIVERED')">Deliver</button>`:''}
                    ${o.status!=='DELIVERED'&&o.status!=='CANCELLED'?`<button class="btn btn-danger btn-sm" onclick="updateStatus('${o.order_id}','CANCELLED')">Cancel</button>`:''}
                </div>
            </div>
        `).join('');
    });
}

function loadProducts() {
    fetch('/api/products').then(r=>r.json()).then(d=>{
        allProducts=d;
        document.getElementById('productList').innerHTML=d.map(p=>`
            <tr>
                <td><img src="${p.image||'https://via.placeholder.com/50'}" style="width:40px;height:40px;object-fit:cover;border-radius:6px;" onerror="this.src='https://via.placeholder.com/50'" /></td>
                <td>${p.name}<br><small style="color:#888;">${p.name_bn||''}</small></td>
                <td>${p.category}</td>
                <td>₹${p.price}</td>
                <td><span style="text-decoration:line-through;color:#888;">₹${p.mrp||p.price}</span></td>
                <td class="${p.stock<=p.min_stock?'stock-low':''}">${p.stock}</td>
                <td>${p.discount||0}%</td>
                <td>${p.shop_id||'-'}</td>
                <td><span class="badge ${p.active!==false?'badge-active':'badge-inactive'}">${p.active!==false?'Active':'Inactive'}</span></td>
                <td>
                    <button class="btn btn-warning btn-sm" onclick="toggleProduct(${p.id})">${p.active!==false?'🔴':'🟢'}</button>
                    <button class="btn btn-danger btn-sm" onclick="deleteProduct(${p.id})">🗑️</button>
                </td>
            </tr>
        `).join('');
    });
}

function loadStock() {
    fetch('/api/products').then(r=>r.json()).then(d=>{
        const low=d.filter(p=>p.stock<=p.min_stock&&p.active!==false);
        let html='';
        if(low.length){html+=`<div style="background:#fff3e0;padding:12px;border-radius:12px;margin-bottom:12px;border-left:4px solid #e74c3c;">
            <h3 style="color:#e74c3c;">⚠️ Low Stock (${low.length})</h3>${low.map(p=>`
                <div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #f0f0f0;">
                    <span>${p.name}</span><span style="color:#e74c3c;font-weight:700;">${p.stock} (Min:${p.min_stock})</span>
                    <button class="btn btn-primary btn-sm" onclick="openStockModal(${p.id})">Update</button>
                </div>`).join('')}</div>`;
        }
        html+=`<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px;">`;
        d.filter(p=>p.active!==false).forEach(p=>{
            const isLow=p.stock<=p.min_stock;
            html+=`<div style="background:${isLow?'#fff3e0':'#f8faf8'};padding:12px;border-radius:12px;border-left:4px solid ${isLow?'#e74c3c':'#4CAF50'};">
                <div style="font-weight:600;">${p.name}</div>
                <div>Stock: <span style="font-weight:700;color:${isLow?'#e74c3c':'#2E7D32'};">${p.stock}</span> / ${p.unit}</div>
                <div style="font-size:12px;color:#888;">Min: ${p.min_stock||10}</div>
                <button class="btn btn-primary btn-sm" onclick="openStockModal(${p.id})" style="margin-top:6px;">📦 Update</button>
            </div>`;
        });
        html+='</div>';
        document.getElementById('stockList').innerHTML=html;
    });
}

function checkLowStock() {
    fetch('/api/products/low-stock').then(r=>r.json()).then(d=>{
        const alert=document.getElementById('lowStockAlert');
        if(d.length){alert.style.display='inline-block';alert.textContent=`⚠️ ${d.length} Low Stock!`;}
        else alert.style.display='none';
    });
}

function loadShops() {
    fetch('/api/shops').then(r=>r.json()).then(d=>{
        allShops=d;
        const sel=document.getElementById('pShopId');
        sel.innerHTML=d.map(s=>`<option value="${s.id}">${s.name}</option>`).join('');
        document.getElementById('shopList').innerHTML=d.map(s=>`
            <div style="background:#f8faf8;padding:10px 14px;border-radius:10px;margin-bottom:6px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;">
                <div><strong>${s.name}</strong></div>
                <div style="color:#555;font-size:13px;">📍 ${s.address||''} | 📱 ${s.phone||''}</div>
            </div>
        `).join('');
    });
}

function loadSuppliers() {
    fetch('/api/suppliers').then(r=>r.json()).then(d=>{
        allSuppliers=d;
        const sel=document.getElementById('pSupplierId');
        sel.innerHTML=`<option value="">Select Supplier</option>`+d.map(s=>`<option value="${s.id}">${s.name}</option>`).join('');
        document.getElementById('supplierList').innerHTML=d.map(s=>`
            <div style="background:#f8faf8;padding:10px 14px;border-radius:10px;margin-bottom:6px;display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;">
                <div><strong>${s.name}</strong></div>
                <div style="color:#555;font-size:13px;">📍 ${s.address||''} | 📱 ${s.phone||''}</div>
            </div>
        `).join('');
    });
}

function openStockModal(id) {
    const p=allProducts.find(x=>x.id===id);
    if(!p)return;
    editingStockId=id;
    document.getElementById('stockProductName').textContent=p.name;
    document.getElementById('stockCurrent').textContent=p.stock;
    document.getElementById('stockNew').value=p.stock;
    document.getElementById('stockMin').value=p.min_stock||10;
    document.getElementById('stockModal').classList.add('active');
}

function closeStockModal() {
    document.getElementById('stockModal').classList.remove('active');
    editingStockId=null;
}

function saveStock() {
    if(!editingStockId)return;
    const stock=parseInt(document.getElementById('stockNew').value)||0;
    const minStock=parseInt(document.getElementById('stockMin').value)||10;
    const p=allProducts.find(x=>x.id===editingStockId);
    if(p)p.min_stock=minStock;
    fetch(`/api/products/${editingStockId}/stock`,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({stock})})
    .then(()=>{fetch(`/api/products/${editingStockId}`,{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify(p)});})
    .then(()=>{alert('✅ Stock updated!');closeStockModal();loadAll();});
}

function updateStatus(id,status){
    fetch('/api/order/status',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({order_id:id,status})})
    .then(()=>loadAll());
}

function toggleProduct(id){
    fetch(`/api/products/${id}/toggle`,{method:'PUT'}).then(()=>loadProducts());
}

function deleteProduct(id){
    if(!confirm('Delete?'))return;
    fetch(`/api/products/${id}`,{method:'DELETE'}).then(()=>loadProducts());
}

function addProduct(){
    const data={
        name:document.getElementById('pName').value,
        name_bn:document.getElementById('pNameBn').value,
        category:document.getElementById('pCategory').value,
        sub_category:document.getElementById('pSubCategory').value,
        price:parseFloat(document.getElementById('pPrice').value)||0,
        mrp:parseFloat(document.getElementById('pMrp').value)||0,
        unit:document.getElementById('pUnit').value||'KG',
        stock:parseInt(document.getElementById('pStock').value)||0,
        min_stock:parseInt(document.getElementById('pMinStock').value)||10,
        discount:parseFloat(document.getElementById('pDiscount').value)||0,
        image:document.getElementById('pImage').value||'',
        shop_id:document.getElementById('pShopId').value||'shop1',
        supplier_id:document.getElementById('pSupplierId').value||'',
        active:true
    };
    fetch('/api/products',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)})
    .then(()=>{alert('✅ Product added!');loadAll();});
}

function addShop(){
    const name=document.getElementById('shopName').value;
    if(!name){alert('Enter shop name');return;}
    fetch('/api/shops',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({
        name,address:document.getElementById('shopAddress').value,phone:document.getElementById('shopPhone').value
    })}).then(()=>{alert('✅ Shop added!');document.getElementById('shopName').value='';document.getElementById('shopAddress').value='';document.getElementById('shopPhone').value='';loadShops();});
}

function addSupplier(){
    const name=document.getElementById('supName').value;
    if(!name){alert('Enter supplier name');return;}
    fetch('/api/suppliers',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({
        name,phone:document.getElementById('supPhone').value,address:document.getElementById('supAddress').value
    })}).then(()=>{alert('✅ Supplier added!');document.getElementById('supName').value='';document.getElementById('supPhone').value='';document.getElementById('supAddress').value='';loadSuppliers();});
}

document.getElementById('stockModal').addEventListener('click',function(e){if(e.target===this)closeStockModal();});
loadAll();
setInterval(loadAll,30000);
</script>
</body>
</html>
    '''
    return html

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
