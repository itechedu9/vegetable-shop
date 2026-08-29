from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import os
import psycopg2
import psycopg2.extras
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

# ===== ডাটাবেস সংযোগ =====
DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    if not DATABASE_URL:
        print("⚠️ DATABASE_URL not set! Using in-memory fallback.")
        return None
    try:
        conn = psycopg2.connect(DATABASE_URL)
        return conn
    except Exception as e:
        print(f"⚠️ Database connection error: {e}")
        return None

def execute_query(query, params=None, fetch=False):
    conn = get_db_connection()
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

# ===== ইনিশিয়াল ডাটাবেস সেটআপ =====
def init_db():
    # Shops
    execute_query("""
        CREATE TABLE IF NOT EXISTS shops (
            id VARCHAR(20) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            address TEXT,
            phone VARCHAR(20)
        )
    """)
    # Suppliers
    execute_query("""
        CREATE TABLE IF NOT EXISTS suppliers (
            id VARCHAR(20) PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            phone VARCHAR(20),
            address TEXT
        )
    """)
    # Products
    execute_query("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            name_bn VARCHAR(100),
            category VARCHAR(50),
            sub_category VARCHAR(50),
            price DECIMAL(10,2) DEFAULT 0,
            mrp DECIMAL(10,2) DEFAULT 0,
            unit VARCHAR(20),
            stock INTEGER DEFAULT 0,
            min_stock INTEGER DEFAULT 10,
            discount DECIMAL(5,2) DEFAULT 0,
            image TEXT,
            shop_id VARCHAR(20),
            supplier_id VARCHAR(20),
            active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Orders
    execute_query("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            order_id VARCHAR(50) UNIQUE NOT NULL,
            customer VARCHAR(100),
            phone VARCHAR(20),
            address TEXT,
            items JSONB,
            total DECIMAL(10,2),
            status VARCHAR(20),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

# ===== API রাউট =====
@app.route('/')
def home():
    return jsonify({'message': '🌿 Vegetable & Grocery Shop API', 'status': 'running', 'version': '4.0 (DB)'})

@app.route('/api/products')
def get_products():
    result = execute_query("SELECT * FROM products ORDER BY id", fetch=True)
    if result is None:
        return jsonify([])
    return jsonify([dict(row) for row in result])

@app.route('/api/products/low-stock')
def get_low_stock():
    result = execute_query("SELECT * FROM products WHERE stock <= min_stock AND active = TRUE ORDER BY id", fetch=True)
    if result is None:
        return jsonify([])
    return jsonify([dict(row) for row in result])

@app.route('/api/products', methods=['POST'])
def add_product():
    data = request.json
    try:
        execute_query("""
            INSERT INTO products (name, name_bn, category, sub_category, price, mrp, unit, stock, min_stock, discount, image, shop_id, supplier_id, active)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data.get('name'), data.get('name_bn', ''), data.get('category', 'Vegetables'),
            data.get('sub_category', ''), float(data.get('price', 0)), float(data.get('mrp', 0)),
            data.get('unit', 'KG'), int(data.get('stock', 0)), int(data.get('min_stock', 10)),
            float(data.get('discount', 0)), data.get('image', ''), data.get('shop_id', 'shop1'),
            data.get('supplier_id', ''), data.get('active', True)
        ))
        return jsonify({'success': True, 'message': 'Product added successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    data = request.json
    try:
        execute_query("""
            UPDATE products SET 
                name=%s, name_bn=%s, category=%s, sub_category=%s, price=%s, mrp=%s, unit=%s, 
                stock=%s, min_stock=%s, discount=%s, image=%s, shop_id=%s, supplier_id=%s, active=%s 
            WHERE id=%s
        """, (
            data.get('name'), data.get('name_bn', ''), data.get('category'), data.get('sub_category', ''),
            float(data.get('price', 0)), float(data.get('mrp', 0)), data.get('unit', 'KG'),
            int(data.get('stock', 0)), int(data.get('min_stock', 10)), float(data.get('discount', 0)),
            data.get('image', ''), data.get('shop_id', 'shop1'), data.get('supplier_id', ''),
            data.get('active', True), product_id
        ))
        return jsonify({'success': True, 'message': 'Product updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products/<int:product_id>/stock', methods=['PUT'])
def update_stock(product_id):
    data = request.json
    try:
        execute_query("UPDATE products SET stock=%s WHERE id=%s", (int(data.get('stock', 0)), product_id))
        return jsonify({'success': True, 'message': 'Stock updated successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products/<int:product_id>/toggle', methods=['PUT'])
def toggle_product(product_id):
    try:
        result = execute_query("SELECT active FROM products WHERE id=%s", (product_id,), fetch=True)
        if result:
            current = result[0][0]
            execute_query("UPDATE products SET active=%s WHERE id=%s", (not current, product_id))
            return jsonify({'success': True})
        return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        execute_query("DELETE FROM products WHERE id=%s", (product_id,))
        return jsonify({'success': True, 'message': 'Product deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/shops')
def get_shops():
    result = execute_query("SELECT * FROM shops ORDER BY id", fetch=True)
    if result is None:
        return jsonify([])
    return jsonify([dict(row) for row in result])

@app.route('/api/suppliers')
def get_suppliers():
    result = execute_query("SELECT * FROM suppliers ORDER BY id", fetch=True)
    if result is None:
        return jsonify([])
    return jsonify([dict(row) for row in result])

# ---------- অর্ডার (ইন-মেমরি, পরে ডাটাবেসে স্থানান্তর) ----------
orders = []
order_counter = 1

@app.route('/api/orders')
def get_orders():
    return jsonify(orders)

@app.route('/api/orders/stats')
def get_stats():
    total = len(orders)
    new = len([o for o in orders if o.get('status') == 'NEW'])
    delivered = len([o for o in orders if o.get('status') == 'DELIVERED'])
    total_sales = sum([o.get('total', 0) for o in orders if o.get('status') != 'CANCELLED'])
    return jsonify({'total_orders': total, 'new_orders': new, 'delivered_orders': delivered, 'total_sales': total_sales})

@app.route('/api/order', methods=['POST'])
def create_order():
    global order_counter
    data = request.json
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

# ===== অ্যাডমিন প্যানেল (HTML) =====
@app.route('/admin')
def admin_dashboard():
    # আপনার আগের পূর্ণাঙ্গ HTML এখানে রাখুন
    return '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🌿 Pro Stock & Item Manager</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            /* আপনার CSS */
        </style>
    </head>
    <body>
        <!-- আপনার HTML -->
        <script>
            const API_BASE = window.location.origin;
            // আপনার JavaScript
        </script>
    </body>
    </html>
    '''

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)