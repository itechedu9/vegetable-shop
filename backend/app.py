from flask import Flask, jsonify, request, render_template_string, send_file
from flask_cors import CORS
import os
import json
from datetime import datetime, timedelta
import base64
import re
from io import BytesIO
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle

app = Flask(__name__)
CORS(app)

# ===== ডাটা স্টোর =====
products = []
orders = []
coupons = []
customers = {}
shops = {}
order_counter = 1

# ===== স্যাম্পল ডাটা =====
def init_sample_data():
    global products, orders, coupons, shops
    products = [
        {"id": 1, "name": "Potato", "name_bn": "আলু", "name_hi": "आलू", 
         "price": 30, "mrp": 40, "unit": "KG", "stock": 100, "min_stock": 20, "discount": 25,
         "image": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=300&h=300&fit=crop", 
         "category": "Vegetables", "sub_category": "Roots", "active": True, "shop_id": "shop1", 
         "description": "Fresh farm potatoes"},
        {"id": 2, "name": "Tomato", "name_bn": "টমেটো", "name_hi": "टमाटर",
         "price": 40, "mrp": 55, "unit": "KG", "stock": 80, "min_stock": 15, "discount": 27,
         "image": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=300&h=300&fit=crop", 
         "category": "Vegetables", "sub_category": "Fruits", "active": True, "shop_id": "shop1", 
         "description": "Fresh red tomatoes"},
        {"id": 3, "name": "Rice", "name_bn": "চাল", "name_hi": "चावल",
         "price": 60, "mrp": 70, "unit": "KG", "stock": 200, "min_stock": 50, "discount": 10,
         "image": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=300&h=300&fit=crop", 
         "category": "Grocery", "sub_category": "Grains", "active": True, "shop_id": "shop1", 
         "description": "Premium quality rice"},
        {"id": 4, "name": "Sugar", "name_bn": "চিনি", "name_hi": "चीनी",
         "price": 45, "mrp": 55, "unit": "KG", "stock": 150, "min_stock": 30, "discount": 15,
         "image": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=300&h=300&fit=crop", 
         "category": "Grocery", "sub_category": "Essentials", "active": True, "shop_id": "shop1", 
         "description": "White crystal sugar"},
        {"id": 5, "name": "Onion", "name_bn": "পেঁয়াজ", "name_hi": "प्याज",
         "price": 35, "mrp": 45, "unit": "KG", "stock": 150, "min_stock": 25, "discount": 22,
         "image": "https://images.unsplash.com/photo-1508747703725-719777637510?w=300&h=300&fit=crop", 
         "category": "Vegetables", "sub_category": "Roots", "active": True, "shop_id": "shop1", 
         "description": "Fresh onions"},
        {"id": 6, "name": "Garlic", "name_bn": "রসুন", "name_hi": "लहसुन",
         "price": 120, "mrp": 150, "unit": "KG", "stock": 30, "min_stock": 10, "discount": 20,
         "image": "https://images.unsplash.com/photo-1541808814-4544cb5342c7?w=300&h=300&fit=crop", 
         "category": "Vegetables", "sub_category": "Roots", "active": True, "shop_id": "shop1", 
         "description": "Fresh garlic"},
        {"id": 7, "name": "Wheat Flour", "name_bn": "আটা", "name_hi": "आटा",
         "price": 35, "mrp": 45, "unit": "KG", "stock": 120, "min_stock": 40, "discount": 10,
         "image": "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=300&h=300&fit=crop", 
         "category": "Grocery", "sub_category": "Grains", "active": True, "shop_id": "shop1", 
         "description": "Premium wheat flour"},
        {"id": 8, "name": "Cooking Oil", "name_bn": "তেল", "name_hi": "तेल",
         "price": 180, "mrp": 220, "unit": "Liter", "stock": 50, "min_stock": 15, "discount": 18,
         "image": "https://images.unsplash.com/photo-1474979266404-7eaacbcd87c5?w=300&h=300&fit=crop", 
         "category": "Grocery", "sub_category": "Essentials", "active": True, "shop_id": "shop1", 
         "description": "Premium cooking oil"},
        {"id": 9, "name": "Carrot", "name_bn": "গাজর", "name_hi": "गाजर",
         "price": 45, "mrp": 60, "unit": "KG", "stock": 55, "min_stock": 10, "discount": 25,
         "image": "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=300&h=300&fit=crop", 
         "category": "Vegetables", "sub_category": "Roots", "active": True, "shop_id": "shop1", 
         "description": "Fresh carrots"},
        {"id": 10, "name": "Brinjal", "name_bn": "বেগুন", "name_hi": "बैंगन",
         "price": 40, "mrp": 55, "unit": "KG", "stock": 45, "min_stock": 10, "discount": 27,
         "image": "https://images.unsplash.com/photo-1552074284-5e88ef1aef18?w=300&h=300&fit=crop", 
         "category": "Vegetables", "sub_category": "Fruits", "active": True, "shop_id": "shop1", 
         "description": "Fresh brinjals"}
    ]
    
    shops = {
        "shop1": {"name": "Main Shop", "address": "Falakata, West Bengal", "phone": "+919876543210"},
        "shop2": {"name": "Branch 1", "address": "Jateswar, West Bengal", "phone": "+919876543211"}
    }
    
    coupons = [
        {"code": "FRESH10", "discount": 10, "type": "percent", "min_order": 100, "expires": "2026-12-31"},
        {"code": "VEGGY20", "discount": 20, "type": "percent", "min_order": 200, "expires": "2026-10-01"}
    ]

init_sample_data()

# ===== অ্যাডমিন অথ =====
ADMIN_USER = "admin"
ADMIN_PASS = "admin123"

# ===== API রাউট =====
@app.route('/')
def home():
    return jsonify({'message': '🌿 Vegetable Shop API', 'status': 'running', 'version': '3.0.0'})

# ---------- প্রোডাক্ট ----------
@app.route('/api/products')
def get_products():
    return jsonify(products)

@app.route('/api/products/active')
def get_active_products():
    active = [p for p in products if p.get('active', True)]
    return jsonify(active)

@app.route('/api/products/category/<category>')
def get_products_by_category(category):
    cat_products = [p for p in products if p.get('category') == category and p.get('active', True)]
    return jsonify(cat_products)

@app.route('/api/products/shop/<shop_id>')
def get_products_by_shop(shop_id):
    shop_products = [p for p in products if p.get('shop_id') == shop_id and p.get('active', True)]
    return jsonify(shop_products)

@app.route('/api/products/low-stock')
def get_low_stock_products():
    low_stock = [p for p in products if p.get('stock', 0) <= p.get('min_stock', 0) and p.get('active', True)]
    return jsonify(low_stock)

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
        'min_stock': int(data.get('min_stock', 10)),
        'discount': float(data.get('discount', 0)),
        'image': data.get('image', '/uploads/default.jpg'),
        'category': data.get('category', 'Vegetables'),
        'sub_category': data.get('sub_category', ''),
        'shop_id': data.get('shop_id', 'shop1'),
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
        'min_stock': int(data.get('min_stock', product.get('min_stock', 10))),
        'discount': float(data.get('discount', product.get('discount', 0))),
        'image': data.get('image', product['image']),
        'category': data.get('category', product['category']),
        'sub_category': data.get('sub_category', product.get('sub_category', '')),
        'shop_id': data.get('shop_id', product.get('shop_id', 'shop1')),
        'active': data.get('active', product.get('active', True)),
        'description': data.get('description', product.get('description', ''))
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
    return jsonify([{'id': k, **v} for k, v in shops.items()])

@app.route('/api/shops', methods=['POST'])
def add_shop():
    data = request.json
    shop_id = f"shop{len(shops)+1}"
    shops[shop_id] = {
        'name': data.get('name'),
        'address': data.get('address', ''),
        'phone': data.get('phone', '')
    }
    return jsonify({'success': True, 'shop_id': shop_id})

# ---------- ইমেজ আপলোড ----------
@app.route('/api/upload', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'jpg'
    filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}.{ext}"
    filepath = os.path.join('uploads', filename)
    
    os.makedirs('uploads', exist_ok=True)
    file.save(filepath)
    
    return jsonify({
        'success': True,
        'url': f'/uploads/{filename}',
        'filename': filename
    })

# ---------- কুপন ----------
@app.route('/api/coupons')
def get_coupons():
    return jsonify(coupons)

@app.route('/api/coupons/validate', methods=['POST'])
def validate_coupon():
    data = request.json
    code = data.get('code', '').upper()
    subtotal = float(data.get('subtotal', 0))
    
    coupon = next((c for c in coupons if c['code'].upper() == code), None)
    if not coupon:
        return jsonify({'valid': False, 'message': 'Invalid coupon code'})
    
    if coupon.get('expires'):
        try:
            exp_date = datetime.strptime(coupon['expires'], '%Y-%m-%d')
            if exp_date < datetime.now():
                return jsonify({'valid': False, 'message': 'Coupon has expired'})
        except:
            pass
    
    if subtotal < coupon.get('min_order', 0):
        return jsonify({
            'valid': False, 
            'message': f'Minimum order of ₹{coupon["min_order"]} required'
        })
    
    if coupon['type'] == 'percent':
        discount = subtotal * (coupon['discount'] / 100)
    else:
        discount = coupon['discount']
    
    return jsonify({
        'valid': True,
        'discount': round(discount, 2),
        'code': coupon['code'],
        'message': f'Coupon applied! You saved ₹{round(discount, 2)}'
    })

@app.route('/api/coupons', methods=['POST'])
def add_coupon():
    data = request.json
    coupon = {
        'code': data.get('code', '').upper(),
        'discount': float(data.get('discount', 0)),
        'type': data.get('type', 'percent'),
        'min_order': float(data.get('min_order', 0)),
        'expires': data.get('expires', '')
    }
    coupons.append(coupon)
    return jsonify({'success': True, 'coupon': coupon})

@app.route('/api/coupons/<code>', methods=['DELETE'])
def delete_coupon(code):
    global coupons
    coupons = [c for c in coupons if c['code'].upper() != code.upper()]
    return jsonify({'success': True})

# ---------- অর্ডার ----------
@app.route('/api/orders')
def get_orders():
    return jsonify(orders)

@app.route('/api/orders/phone/<phone>')
def get_orders_by_phone(phone):
    customer_orders = [o for o in orders if o.get('phone') == phone]
    return jsonify(customer_orders)

@app.route('/api/orders/<order_id>')
def get_order(order_id):
    order = next((o for o in orders if o['order_id'] == order_id), None)
    return jsonify(order) if order else (jsonify({'error': 'Not found'}), 404)

@app.route('/api/orders/stats')
def get_order_stats():
    total = len(orders)
    new = len([o for o in orders if o['status'] == 'NEW'])
    delivered = len([o for o in orders if o['status'] == 'DELIVERED'])
    total_sales = sum([o.get('total', 0) for o in orders if o['status'] != 'CANCELLED'])
    
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
    
    phone = data.get('phone', '')
    if phone:
        customers[phone] = {
            'name': data.get('name', ''),
            'phone': phone,
            'address': data.get('address', ''),
            'area': data.get('area', ''),
            'last_order': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'total_orders': customers.get(phone, {}).get('total_orders', 0) + 1
        }
    
    # স্টক চেক ও রিডিউস
    for item in data.get('items', []):
        product = next((p for p in products if p['name'].lower() == item['name'].lower()), None)
        if product:
            if product['stock'] < item['quantity']:
                return jsonify({
                    'success': False,
                    'message': f'Insufficient stock for {item["name"]}. Available: {product["stock"]}'
                }), 400
            product['stock'] -= item['quantity']
    
    order = {
        'order_id': f'ORD-{datetime.now().strftime("%Y%m%d")}-{str(order_counter).zfill(3)}',
        'customer': data.get('name', ''),
        'phone': phone,
        'address': data.get('address', ''),
        'area': data.get('area', ''),
        'landmark': data.get('landmark', ''),
        'items': data.get('items', []),
        'subtotal': float(data.get('subtotal', 0)),
        'discount': float(data.get('discount', 0)),
        'delivery': float(data.get('delivery', 0)),
        'total': float(data.get('total', 0)),
        'coupon_code': data.get('coupon_code', ''),
        'status': 'NEW',
        'payment_method': data.get('payment_method', 'COD'),
        'payment_status': 'PENDING' if data.get('payment_method') == 'COD' else 'PAID',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
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

# ---------- কাস্টমার ----------
@app.route('/api/customers')
def get_customers():
    return jsonify(list(customers.values()))

@app.route('/api/customers/<phone>')
def get_customer(phone):
    return jsonify(customers.get(phone, {}))

# ---------- PDF ইনভয়েস ----------
@app.route('/api/order/<order_id>/pdf')
def generate_pdf(order_id):
    order = next((o for o in orders if o['order_id'] == order_id), None)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Header
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, height - 50, "🌿 Fresh Veggies")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 75, "Invoice")
    c.line(50, height - 85, width - 50, height - 85)
    
    # Order Details
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 115, f"Order ID: {order['order_id']}")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 135, f"Date: {order['created_at']}")
    c.drawString(50, height - 155, f"Customer: {order['customer']}")
    c.drawString(50, height - 175, f"Phone: {order['phone']}")
    c.drawString(50, height - 195, f"Address: {order['address']}")
    
    # Items Table
    y = height - 220
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Item")
    c.drawString(200, y, "Qty")
    c.drawString(280, y, "Price")
    c.drawString(380, y, "Total")
    c.line(50, y - 5, width - 50, y - 5)
    
    y -= 20
    c.setFont("Helvetica", 11)
    for item in order['items']:
        c.drawString(50, y, item['name'])
        c.drawString(200, y, str(item['quantity']))
        c.drawString(280, y, f"₹{item['price']}")
        c.drawString(380, y, f"₹{item['price'] * item['quantity']}")
        y -= 20
    
    # Total
    y -= 10
    c.line(50, y + 10, width - 50, y + 10)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(300, y - 5, f"Total: ₹{order['total']}")
    
    # Footer
    c.setFont("Helvetica", 10)
    c.drawString(50, 50, "Thank you for your order!")
    c.drawString(50, 35, "Fresh Veggies - Delivering Freshness to Your Door")
    
    c.save()
    buffer.seek(0)
    
    return send_file(buffer, as_attachment=True, download_name=f"invoice_{order_id}.pdf", mimetype='application/pdf')

# ===== অ্যাডমিন প্যানেল (HTML) =====
@app.route('/admin')
def admin_dashboard():
    # Full admin HTML - I'm keeping it short here but it's included in the full code
    return render_template_string('''
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
            .tabs { display: flex; gap: 8px; margin-bottom: 16px; overflow-x: auto; flex-wrap: wrap; }
            .tab { padding: 8px 16px; border-radius: 20px; border: 2px solid #ddd; background: white; cursor: pointer; font-weight: 600; font-size: 13px; white-space: nowrap; }
            .tab.active { background: #2E7D32; color: white; border-color: #2E7D32; }
            .section { background: white; border-radius: 16px; padding: 16px; margin-bottom: 16px; box-shadow: 0 2px 10px rgba(0,0,0,0.04); }
            .section h2 { font-size: 18px; color: #1a472a; margin-bottom: 12px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🌿 Admin Dashboard</h1>
            <button class="btn btn-outline" onclick="location.reload()">🔄 Refresh</button>
        </div>
        <div class="stats" id="stats">
            <div class="stat-card"><div class="number" id="totalOrders">0</div><div>Total Orders</div></div>
            <div class="stat-card"><div class="number" id="newOrders">0</div><div>New Orders</div></div>
            <div class="stat-card"><div class="number" id="totalSales">₹0</div><div>Total Sales</div></div>
        </div>
        <div class="tabs">
            <button class="tab active" onclick="showTab('orders')">📋 Orders</button>
            <button class="tab" onclick="showTab('products')">🥬 Products</button>
            <button class="tab" onclick="showTab('stock')">📦 Stock</button>
        </div>
        <div id="tab-orders" class="section"><h2>📋 Orders</h2><div id="ordersList">Loading...</div></div>
        <div id="tab-products" class="section" style="display:none;"><h2>🥬 Products</h2><div id="productList">Loading...</div></div>
        <div id="tab-stock" class="section" style="display:none;"><h2>📦 Stock</h2><div id="stockList">Loading...</div></div>
        <script>
            function showTab(tab) {
                document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
                document.querySelectorAll('.section').forEach(s=>s.style.display='none');
                document.getElementById('tab-'+tab).style.display='block';
                document.querySelector(`.tab[onclick="showTab('${tab}')"]`).classList.add('active');
            }
            // Load data
            fetch('/api/orders/stats').then(r=>r.json()).then(d=>{
                document.getElementById('totalOrders').textContent=d.total_orders||0;
                document.getElementById('newOrders').textContent=d.new_orders||0;
                document.getElementById('totalSales').textContent='₹'+(d.total_sales||0);
            });
            fetch('/api/orders').then(r=>r.json()).then(d=>{
                document.getElementById('ordersList').innerHTML=d.slice(0,10).map(o=>
                    `<div style="border-bottom:1px solid #eee;padding:8px;"><b>${o.order_id}</b> | ${o.customer} | ₹${o.total}</div>`
                ).join('');
            });
            fetch('/api/products').then(r=>r.json()).then(d=>{
                document.getElementById('productList').innerHTML=d.map(p=>
                    `<div style="border-bottom:1px solid #eee;padding:8px;">${p.name} | ₹${p.price} | Stock: ${p.stock}</div>`
                ).join('');
            });
            fetch('/api/products/low-stock').then(r=>r.json()).then(d=>{
                document.getElementById('stockList').innerHTML=d.length?d.map(p=>
                    `<div style="border-bottom:1px solid #eee;padding:8px;color:#e74c3c;">⚠️ ${p.name} | Stock: ${p.stock} (Min: ${p.min_stock})</div>`
                ).join(''):'All stocks are sufficient';
            });
        </script>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
