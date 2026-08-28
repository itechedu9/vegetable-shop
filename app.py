from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# ===== ডাটা স্টোর =====
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
         "shop_id": "shop2", "supplier_id": "sup2", "active": True}
    ]

init_data()

# ===== API রাউট =====
@app.route('/')
def home():
    return jsonify({'message': '🌿 Vegetable & Grocery Shop API', 'status': 'running', 'version': '3.0'})

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

# ===== পূর্ণাঙ্গ অ্যাডমিন প্যানেল (Flask API Connected + Image Upload) =====
@app.route('/admin')
def admin_dashboard():
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.5, user-scalable=yes">
    <title>🌿 Pro Stock & Item Manager</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Roboto, system-ui, sans-serif; }
        body { background: #f4f7fc; padding: 20px; min-height: 100vh; display: flex; justify-content: center; }
        .app { max-width: 1400px; width: 100%; background: white; border-radius: 32px; box-shadow: 0 20px 60px rgba(0,20,40,0.08); padding: 24px 28px 40px; }
        h1 { font-weight: 600; font-size: 1.9rem; color: #0a2e1f; display: flex; align-items: center; gap: 10px; margin-bottom: 8px; flex-wrap: wrap; }
        h1 i { color: #2e7d32; }
        .sub { color: #3e5a4a; margin-bottom: 24px; border-left: 6px solid #4caf50; padding-left: 18px; font-weight: 400; background: #f0f8f0; border-radius: 0 40px 40px 0; line-height: 1.6; }
        .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin: 20px 0 30px; }
        @media (max-width: 900px) { .grid-2 { grid-template-columns: 1fr; } }
        .card { background: #ffffff; border-radius: 28px; padding: 18px 22px 26px; box-shadow: 0 6px 20px rgba(0,30,20,0.04); border: 1px solid #eaf0e8; }
        .card-title { font-weight: 600; font-size: 1.2rem; margin-bottom: 16px; color: #1a3a2a; display: flex; align-items: center; gap: 12px; border-bottom: 2px dashed #d4e8d4; padding-bottom: 10px; }
        .card-title i { color: #2e7d32; width: 28px; }
        label { font-weight: 500; font-size: 0.85rem; color: #1f452f; display: block; margin: 12px 0 4px; }
        input, select, textarea { width: 100%; padding: 10px 14px; border: 2px solid #e2eee2; border-radius: 18px; font-size: 0.95rem; background: #fafffa; transition: 0.2s; }
        input:focus, select:focus, textarea:focus { border-color: #2e7d32; outline: none; background: white; box-shadow: 0 0 0 4px rgba(46,125,50,0.08); }
        .row-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
        @media (max-width: 500px) { .row-2 { grid-template-columns: 1fr; } }
        .btn { background: #2e7d32; border: none; color: white; font-weight: 600; padding: 12px 22px; border-radius: 40px; font-size: 1rem; cursor: pointer; transition: 0.15s; display: inline-flex; align-items: center; justify-content: center; gap: 8px; border: 1px solid transparent; margin-top: 14px; width: 100%; }
        .btn:hover { background: #1f5a23; transform: scale(0.98); }
        .btn-outline { background: transparent; border: 2px solid #2e7d32; color: #2e7d32; }
        .btn-outline:hover { background: #e8f5e8; transform: scale(0.98); }
        .table-wrapper { overflow-x: auto; border-radius: 24px; border: 1px solid #ecf3ec; margin: 18px 0 10px; background: #fafffa; }
        table { width: 100%; border-collapse: collapse; font-size: 0.9rem; min-width: 620px; }
        th { text-align: left; padding: 14px 12px; background: #eaf3ea; color: #1a402a; font-weight: 600; white-space: nowrap; }
        td { padding: 12px 10px; border-bottom: 1px solid #e2eee2; vertical-align: middle; }
        .badge { background: #dff0df; padding: 4px 14px; border-radius: 40px; font-size: 0.75rem; font-weight: 600; color: #1a4a2a; display: inline-block; }
        .badge-warning { background: #fff3d0; color: #8a6500; }
        .badge-danger { background: #ffe6e0; color: #b13e2e; }
        .img-thumb { width: 52px; height: 52px; object-fit: cover; border-radius: 16px; background: #f0f8f0; border: 2px solid #d4e8d4; transition: 0.2s; }
        .img-thumb:hover { transform: scale(1.1); }
        .action-group { display: flex; gap: 6px; flex-wrap: wrap; }
        .btn-icon { background: transparent; border: none; font-size: 1.1rem; cursor: pointer; padding: 4px 8px; border-radius: 30px; transition: 0.1s; }
        .btn-icon.edit { color: #1f6b3a; background: #e4f2e4; }
        .btn-icon.delete { color: #b13e2e; background: #fce8e4; }
        .btn-icon.stock { color: #a57c00; background: #fff3d0; }
        .btn-icon:hover { transform: scale(0.92); opacity: 0.8; }
        .file-upload { border: 2px dashed #b8d9b8; border-radius: 30px; padding: 12px 16px; background: #f6fcf6; text-align: center; margin: 6px 0 10px; cursor: pointer; transition: 0.2s; }
        .file-upload:hover { background: #ecf9ec; border-color: #2e7d32; }
        .file-upload i { font-size: 1.4rem; color: #2e7d32; margin-right: 8px; }
        #imagePreview { display: flex; flex-wrap: wrap; gap: 10px; margin: 12px 0 4px; }
        #editImagePreview { display: flex; flex-wrap: wrap; gap: 10px; margin: 12px 0 4px; }
        .preview-item { position: relative; width: 70px; height: 70px; border-radius: 18px; border: 2px solid #d4e8d4; overflow: hidden; background: #f0f8f0; }
        .preview-item img { width: 100%; height: 100%; object-fit: cover; }
        .preview-item .remove { position: absolute; top: -6px; right: -6px; background: #b13e2e; color: white; border-radius: 30px; width: 22px; height: 22px; display: flex; align-items: center; justify-content: center; font-size: 12px; cursor: pointer; border: 2px solid white; }
        .toast { position: fixed; bottom: 30px; right: 30px; background: #1f3a2a; color: white; padding: 14px 28px; border-radius: 60px; font-weight: 500; box-shadow: 0 8px 24px rgba(0,0,0,0.2); display: none; align-items: center; gap: 12px; z-index: 999; max-width: 380px; }
        .toast.show { display: flex; }
        .modal-overlay { position: fixed; top:0;left:0;width:100%;height:100%; background: rgba(0,20,10,0.5); backdrop-filter: blur(4px); display: none; align-items: center; justify-content: center; z-index: 1000; padding: 20px; }
        .modal-overlay.active { display: flex; }
        .modal-box { background: white; max-width: 640px; width: 100%; max-height: 90vh; overflow-y: auto; border-radius: 40px; padding: 30px 32px; box-shadow: 0 30px 60px rgba(0,0,0,0.2); }
        .modal-box h2 { margin-bottom: 18px; color: #0a2e1f; }
        .modal-actions { display: flex; gap: 14px; margin-top: 24px; }
        .modal-actions .btn { width: auto; padding: 10px 28px; }
        @media (max-width: 600px) { .app { padding: 16px; } .modal-box { padding: 20px; } }
    </style>
</head>
<body>
<div class="app">
    <h1><i class="fas fa-seedling"></i> Pro Stock & Item Manager</h1>
    <div class="sub"><i class="fas fa-store-alt" style="margin-right: 10px;"></i> Vegetable + Grocery · Shop wise · Party wise · Item wise stock · Image upload · <strong>Flask API Connected</strong></div>

    <!-- ===== ADD / EDIT FORM ===== -->
    <div class="grid-2">
        <div class="card">
            <div class="card-title"><i class="fas fa-plus-circle"></i> Add / Edit Item</div>
            <form id="itemForm">
                <label><i class="fas fa-tag"></i> Item Name *</label>
                <input type="text" id="itemName" placeholder="e.g. Potato" required>

                <label><i class="fas fa-language"></i> Name (বাংলা)</label>
                <input type="text" id="itemNameBn" placeholder="আলু">

                <div class="row-2">
                    <div><label>Category</label>
                        <select id="itemCategory">
                            <option value="Vegetables">🥬 Vegetables</option>
                            <option value="Grocery">🛒 Grocery</option>
                            <option value="Fruits">🍎 Fruits</option>
                        </select>
                    </div>
                    <div><label>Sub Category</label>
                        <input type="text" id="itemSubCategory" placeholder="Roots / Grains">
                    </div>
                </div>

                <div class="row-2">
                    <div><label>Price (₹)</label><input type="number" id="itemPrice" step="0.01" placeholder="30"></div>
                    <div><label>MRP (₹)</label><input type="number" id="itemMrp" step="0.01" placeholder="40"></div>
                </div>
                <div class="row-2">
                    <div><label>Unit</label><input type="text" id="itemUnit" placeholder="KG / Piece"></div>
                    <div><label>Discount %</label><input type="number" id="itemDiscount" step="0.1" placeholder="10"></div>
                </div>

                <div class="row-2">
                    <div><label>Stock (Qty)</label><input type="number" id="itemStock" placeholder="100"></div>
                    <div><label>Min Stock Alert</label><input type="number" id="itemMinStock" placeholder="20"></div>
                </div>

                <div class="row-2">
                    <div><label>Shop</label>
                        <select id="itemShop">
                            <option value="shop1">🏪 Main Shop</option>
                            <option value="shop2">🏪 Branch 1</option>
                        </select>
                    </div>
                    <div><label>Supplier / Party</label>
                        <select id="itemSupplier">
                            <option value="sup1">🌾 Green Farms</option>
                            <option value="sup2">🌾 Fresh Supply Co.</option>
                            <option value="">+ Add new (from Suppliers tab)</option>
                        </select>
                    </div>
                </div>

                <label><i class="fas fa-image"></i> Image URL or Upload</label>
                <div class="file-upload" id="imageUploadTrigger">
                    <i class="fas fa-cloud-upload-alt"></i> Click to upload image (JPEG/PNG)
                    <input type="file" id="imageFileInput" accept="image/*" style="display:none">
                </div>
                <input type="text" id="itemImage" placeholder="https://example.com/veg.jpg" style="margin-top:6px;">

                <div id="imagePreview"></div>

                <input type="hidden" id="editId" value="">
                <div style="display:flex; gap:12px; margin-top:16px;">
                    <button type="button" class="btn" id="saveItemBtn"><i class="fas fa-save"></i> Save Item</button>
                    <button type="button" class="btn btn-outline" id="clearFormBtn"><i class="fas fa-undo-alt"></i> Clear</button>
                </div>
            </form>
        </div>

        <!-- ===== QUICK STOCK / SUPPLIER VIEW ===== -->
        <div class="card">
            <div class="card-title"><i class="fas fa-boxes"></i> Supplier & Stock Overview</div>
            <div style="display:flex; gap:10px; flex-wrap:wrap; margin-bottom:14px;">
                <button class="btn btn-outline" style="flex:1;" onclick="filterBySupplier('sup1')"><i class="fas fa-tractor"></i> Green Farms</button>
                <button class="btn btn-outline" style="flex:1;" onclick="filterBySupplier('sup2')"><i class="fas fa-tractor"></i> Fresh Supply</button>
                <button class="btn btn-outline" style="flex:1;" onclick="filterBySupplier('all')"><i class="fas fa-list-ul"></i> All</button>
            </div>
            <div id="supplierStockSummary" style="font-size:0.9rem; background:#f6fcf6; border-radius:20px; padding:10px 14px;">
                <span class="badge"><i class="fas fa-box"></i> Total items: <span id="totalItemsCount">0</span></span>
                <span class="badge badge-warning" style="margin-left:8px;"><i class="fas fa-exclamation-triangle"></i> Low stock: <span id="lowStockCount">0</span></span>
            </div>
            <div style="margin-top:10px; max-height:260px; overflow-y:auto; border-radius:20px; background:#fafffa; padding:4px 4px 4px 12px; border:1px solid #ecf3ec;">
                <div id="supplierStockList"><span style="color:#6a7a6a;">Loading items…</span></div>
            </div>
        </div>
    </div>

    <!-- ===== ITEM TABLE ===== -->
    <div class="card" style="margin-top:8px;">
        <div class="card-title"><i class="fas fa-list-ul"></i> All Items (Modify / Delete / Stock)</div>
        <div class="table-wrapper">
            <table>
                <thead>
                <tr>
                    <th>Image</th><th>Name</th><th>Category</th><th>Shop</th><th>Supplier</th>
                    <th>Price</th><th>MRP</th><th>Stock</th><th>Min</th><th>Actions</th>
                </tr>
                </thead>
                <tbody id="itemTableBody">
                <tr><td colspan="10" style="text-align:center; padding:30px; color:#6a8a6a;">Loading items…</td></tr>
                </tbody>
            </table>
        </div>
    </div>
</div>

<!-- ===== EDIT MODAL ===== -->
<div class="modal-overlay" id="editModal">
    <div class="modal-box">
        <h2><i class="fas fa-edit"></i> Edit Item</h2>
        <form id="editForm">
            <input type="hidden" id="editIdField">
            
            <label>Name *</label><input type="text" id="editName" required>
            <label>Name (বাংলা)</label><input type="text" id="editNameBn">
            
            <div class="row-2">
                <div><label>Category</label><select id="editCategory"><option>Vegetables</option><option>Grocery</option><option>Fruits</option></select></div>
                <div><label>Sub Category</label><input type="text" id="editSubCategory"></div>
            </div>
            
            <div class="row-2">
                <div><label>Price (₹)</label><input type="number" id="editPrice" step="0.01"></div>
                <div><label>MRP (₹)</label><input type="number" id="editMrp" step="0.01"></div>
            </div>
            <div class="row-2">
                <div><label>Unit</label><input type="text" id="editUnit"></div>
                <div><label>Discount %</label><input type="number" id="editDiscount" step="0.1"></div>
            </div>
            <div class="row-2">
                <div><label>Stock</label><input type="number" id="editStock"></div>
                <div><label>Min Stock</label><input type="number" id="editMinStock"></div>
            </div>
            <div class="row-2">
                <div><label>Shop</label><select id="editShop"><option value="shop1">Main Shop</option><option value="shop2">Branch 1</option></select></div>
                <div><label>Supplier</label><select id="editSupplier"><option value="sup1">Green Farms</option><option value="sup2">Fresh Supply</option></select></div>
            </div>
            
            <!-- ===== EDIT MODAL IMAGE UPLOAD ===== -->
            <label><i class="fas fa-image"></i> Image</label>
            <div class="file-upload" id="editImageUploadTrigger">
                <i class="fas fa-cloud-upload-alt"></i> Click to change image (JPEG/PNG)
                <input type="file" id="editImageFileInput" accept="image/*" style="display:none">
            </div>
            <input type="text" id="editImage" placeholder="Image URL" style="margin-top:6px;">
            <div id="editImagePreview"></div>
            
            <div class="modal-actions">
                <button type="button" class="btn" id="updateItemBtn"><i class="fas fa-save"></i> Update</button>
                <button type="button" class="btn btn-outline" id="closeEditModalBtn"><i class="fas fa-times"></i> Cancel</button>
            </div>
        </form>
    </div>
</div>

<!-- Toast -->
<div class="toast" id="toast"><i class="fas fa-check-circle" style="color:#b3e0b3;"></i> <span id="toastMsg">Done</span></div>

<script>
    // ============================================================
    //  FULL FLASK API INTEGRATION
    // ============================================================
    const API_BASE = window.location.origin;

    // ---------- GLOBAL STATE ----------
    let items = [];
    let currentFilter = 'all';

    // DOM refs
    const itemName = document.getElementById('itemName');
    const itemNameBn = document.getElementById('itemNameBn');
    const itemCategory = document.getElementById('itemCategory');
    const itemSubCategory = document.getElementById('itemSubCategory');
    const itemPrice = document.getElementById('itemPrice');
    const itemMrp = document.getElementById('itemMrp');
    const itemUnit = document.getElementById('itemUnit');
    const itemDiscount = document.getElementById('itemDiscount');
    const itemStock = document.getElementById('itemStock');
    const itemMinStock = document.getElementById('itemMinStock');
    const itemShop = document.getElementById('itemShop');
    const itemSupplier = document.getElementById('itemSupplier');
    const itemImage = document.getElementById('itemImage');
    const imagePreview = document.getElementById('imagePreview');
    const itemTableBody = document.getElementById('itemTableBody');
    const toast = document.getElementById('toast');
    const toastMsg = document.getElementById('toastMsg');

    // ---------- TOAST ----------
    function showToast(msg) {
        toastMsg.textContent = msg;
        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 2800);
    }

    // ---------- ADD FORM IMAGE UPLOAD ----------
    document.getElementById('imageUploadTrigger').addEventListener('click', function() {
        document.getElementById('imageFileInput').click();
    });
    document.getElementById('imageFileInput').addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = function(ev) {
            const base64 = ev.target.result;
            itemImage.value = base64;
            showPreview(base64);
            showToast('✅ Image uploaded successfully!');
        };
        reader.readAsDataURL(file);
        this.value = '';
    });

    function showPreview(src) {
        imagePreview.innerHTML = `<div class="preview-item"><img src="${src}" /><span class="remove" onclick="removeImage()">✕</span></div>`;
    }
    function removeImage() {
        itemImage.value = '';
        imagePreview.innerHTML = '';
    }

    // ---------- EDIT FORM IMAGE UPLOAD ----------
    document.getElementById('editImageUploadTrigger').addEventListener('click', function() {
        document.getElementById('editImageFileInput').click();
    });
    document.getElementById('editImageFileInput').addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = function(ev) {
            const base64 = ev.target.result;
            document.getElementById('editImage').value = base64;
            showEditPreview(base64);
            showToast('✅ Image updated for edit!');
        };
        reader.readAsDataURL(file);
        this.value = '';
    });

    function showEditPreview(src) {
        document.getElementById('editImagePreview').innerHTML = `<div class="preview-item"><img src="${src}" /><span class="remove" onclick="removeEditImage()">✕</span></div>`;
    }
    function removeEditImage() {
        document.getElementById('editImage').value = '';
        document.getElementById('editImagePreview').innerHTML = '';
    }

    // ---------- API CALLS ----------
    async function fetchItems() {
        try {
            const resp = await fetch(`${API_BASE}/api/products`);
            if (!resp.ok) throw new Error('Failed to fetch');
            const data = await resp.json();
            items = data;
            renderAll();
        } catch (err) {
            console.error('Fetch error:', err);
            showToast('⚠️ Could not load items from server');
        }
    }

    async function addItemToAPI(item) {
        try {
            const resp = await fetch(`${API_BASE}/api/products`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(item)
            });
            if (!resp.ok) throw new Error('Add failed');
            const result = await resp.json();
            showToast('✅ Item added successfully!');
            await fetchItems();
            return result;
        } catch (err) {
            console.error('Add error:', err);
            showToast('❌ Failed to add item');
        }
    }

    async function updateItemAPI(id, updated) {
        try {
            const resp = await fetch(`${API_BASE}/api/products/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(updated)
            });
            if (!resp.ok) throw new Error('Update failed');
            showToast('✅ Item updated!');
            await fetchItems();
        } catch (err) {
            console.error('Update error:', err);
            showToast('❌ Update failed');
        }
    }

    async function deleteItemAPI(id) {
        if (!confirm('Delete this item?')) return;
        try {
            const resp = await fetch(`${API_BASE}/api/products/${id}`, {
                method: 'DELETE'
            });
            if (!resp.ok) throw new Error('Delete failed');
            showToast('🗑️ Item deleted');
            await fetchItems();
        } catch (err) {
            console.error('Delete error:', err);
            showToast('❌ Delete failed');
        }
    }

    async function updateStockAPI(id, newStock) {
        try {
            const resp = await fetch(`${API_BASE}/api/products/${id}/stock`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ stock: newStock })
            });
            if (!resp.ok) throw new Error('Stock update failed');
            showToast('📦 Stock updated');
            await fetchItems();
        } catch (err) {
            console.error('Stock update error:', err);
            showToast('❌ Stock update failed');
        }
    }

    // ---------- RENDER ----------
    function renderAll() {
        renderTable();
        renderSupplierStock();
        updateStats();
    }

    function renderTable() {
        if (!items.length) {
            itemTableBody.innerHTML = `<tr><td colspan="10" style="text-align:center; padding:30px; color:#6a8a6a;">No items. Add your first product!</td></tr>`;
            return;
        }
        let filtered = items;
        if (currentFilter !== 'all') {
            filtered = items.filter(i => i.supplier_id === currentFilter);
        }
        itemTableBody.innerHTML = filtered.map(item => `
            <tr>
                <td><img class="img-thumb" src="${item.image || 'https://via.placeholder.com/60/ccddcc?text=+'}" onerror="this.src='https://via.placeholder.com/60/ccddcc?text=+'"></td>
                <td><strong>${item.name}</strong><br><small>${item.name_bn || ''}</small></td>
                <td>${item.category || '-'}</td>
                <td>${item.shop_id || '-'}</td>
                <td>${item.supplier_id || '-'}</td>
                <td>₹${item.price}</td>
                <td><span style="text-decoration:line-through;color:#888;">₹${item.mrp}</span></td>
                <td class="${item.stock <= item.min_stock ? 'badge-danger' : ''}" style="font-weight:600;">${item.stock}</td>
                <td>${item.min_stock}</td>
                <td>
                    <div class="action-group">
                        <button class="btn-icon edit" onclick="openEditModal(${item.id})"><i class="fas fa-edit"></i></button>
                        <button class="btn-icon stock" onclick="quickStockUpdate(${item.id})"><i class="fas fa-box"></i></button>
                        <button class="btn-icon delete" onclick="deleteItemAPI(${item.id})"><i class="fas fa-trash-alt"></i></button>
                    </div>
                </td>
            </tr>
        `).join('');
    }

    function renderSupplierStock() {
        const container = document.getElementById('supplierStockList');
        if (!items.length) {
            container.innerHTML = '<span style="color:#6a7a6a;">No items</span>';
            return;
        }
        const grouped = {};
        items.forEach(it => {
            const key = it.supplier_id || 'unknown';
            if (!grouped[key]) grouped[key] = { count: 0, stock: 0, items: [] };
            grouped[key].count += 1;
            grouped[key].stock += it.stock;
            grouped[key].items.push(it);
        });
        let html = '';
        for (const [sup, data] of Object.entries(grouped)) {
            const supName = sup === 'sup1' ? '🌾 Green Farms' : sup === 'sup2' ? '🌾 Fresh Supply' : sup;
            html += `<div style="padding:6px 0; border-bottom:1px solid #eaf3ea;">
                <strong>${supName}</strong> <span class="badge">${data.count} items</span> <span class="badge">📦 ${data.stock} qty</span>
                <div style="font-size:0.75rem; color:#3e5a3e; margin-top:2px;">${data.items.map(i => `${i.name} (${i.stock})`).join(' • ')}</div>
            </div>`;
        }
        container.innerHTML = html;
    }

    function updateStats() {
        document.getElementById('totalItemsCount').textContent = items.length;
        const low = items.filter(i => i.stock <= i.min_stock).length;
        document.getElementById('lowStockCount').textContent = low;
    }

    // ---------- FILTER ----------
    function filterBySupplier(sup) {
        currentFilter = sup;
        renderTable();
    }

    // ---------- QUICK STOCK ----------
    function quickStockUpdate(id) {
        const item = items.find(i => i.id === id);
        if (!item) return;
        const newStock = prompt(`Update stock for ${item.name} (current: ${item.stock})`, item.stock);
        if (newStock !== null && !isNaN(newStock) && Number(newStock) >= 0) {
            updateStockAPI(id, Number(newStock));
        }
    }

    // ---------- EDIT MODAL ----------
    function openEditModal(id) {
        const item = items.find(i => i.id === id);
        if (!item) return;
        document.getElementById('editIdField').value = id;
        document.getElementById('editName').value = item.name || '';
        document.getElementById('editNameBn').value = item.name_bn || '';
        document.getElementById('editCategory').value = item.category || 'Vegetables';
        document.getElementById('editSubCategory').value = item.sub_category || '';
        document.getElementById('editPrice').value = item.price || '';
        document.getElementById('editMrp').value = item.mrp || '';
        document.getElementById('editUnit').value = item.unit || '';
        document.getElementById('editDiscount').value = item.discount || '';
        document.getElementById('editStock').value = item.stock || '';
        document.getElementById('editMinStock').value = item.min_stock || '';
        document.getElementById('editShop').value = item.shop_id || 'shop1';
        document.getElementById('editSupplier').value = item.supplier_id || 'sup1';
        document.getElementById('editImage').value = item.image || '';
        
        // Show existing image in edit preview
        if (item.image) {
            showEditPreview(item.image);
        } else {
            document.getElementById('editImagePreview').innerHTML = '';
        }
        
        document.getElementById('editModal').classList.add('active');
    }

    function closeEditModal() {
        document.getElementById('editModal').classList.remove('active');
        document.getElementById('editImagePreview').innerHTML = '';
    }

    document.getElementById('updateItemBtn').addEventListener('click', function() {
        const id = Number(document.getElementById('editIdField').value);
        const updated = {
            name: document.getElementById('editName').value.trim(),
            name_bn: document.getElementById('editNameBn').value.trim(),
            category: document.getElementById('editCategory').value,
            sub_category: document.getElementById('editSubCategory').value.trim(),
            price: Number(document.getElementById('editPrice').value) || 0,
            mrp: Number(document.getElementById('editMrp').value) || 0,
            unit: document.getElementById('editUnit').value.trim(),
            discount: Number(document.getElementById('editDiscount').value) || 0,
            stock: Number(document.getElementById('editStock').value) || 0,
            min_stock: Number(document.getElementById('editMinStock').value) || 0,
            shop_id: document.getElementById('editShop').value,
            supplier_id: document.getElementById('editSupplier').value,
            image: document.getElementById('editImage').value.trim()
        };
        if (!updated.name) { showToast('⚠️ Name is required'); return; }
        updateItemAPI(id, updated);
        closeEditModal();
    });

    document.getElementById('closeEditModalBtn').addEventListener('click', closeEditModal);
    document.getElementById('editModal').addEventListener('click', function(e) {
        if (e.target === this) closeEditModal();
    });

    // ---------- SAVE (Add) ----------
    document.getElementById('saveItemBtn').addEventListener('click', function() {
        const name = itemName.value.trim();
        if (!name) { showToast('⚠️ Please enter item name'); return; }
        const newItem = {
            name: name,
            name_bn: itemNameBn.value.trim(),
            category: itemCategory.value,
            sub_category: itemSubCategory.value.trim(),
            price: Number(itemPrice.value) || 0,
            mrp: Number(itemMrp.value) || 0,
            unit: itemUnit.value.trim() || 'KG',
            discount: Number(itemDiscount.value) || 0,
            stock: Number(itemStock.value) || 0,
            min_stock: Number(itemMinStock.value) || 10,
            shop_id: itemShop.value,
            supplier_id: itemSupplier.value,
            image: itemImage.value.trim() || 'https://via.placeholder.com/60/ccddcc?text=+'
        };
        addItemToAPI(newItem);
        // clear form
        itemName.value = '';
        itemNameBn.value = '';
        itemSubCategory.value = '';
        itemPrice.value = '';
        itemMrp.value = '';
        itemUnit.value = '';
        itemDiscount.value = '';
        itemStock.value = '';
        itemMinStock.value = '';
        itemImage.value = '';
        imagePreview.innerHTML = '';
    });

    document.getElementById('clearFormBtn').addEventListener('click', function() {
        itemName.value = '';
        itemNameBn.value = '';
        itemSubCategory.value = '';
        itemPrice.value = '';
        itemMrp.value = '';
        itemUnit.value = '';
        itemDiscount.value = '';
        itemStock.value = '';
        itemMinStock.value = '';
        itemImage.value = '';
        imagePreview.innerHTML = '';
    });

    // ---------- INIT ----------
    fetchItems();
</script>
</body>
</html>
    '''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
