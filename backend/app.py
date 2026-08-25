from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Sample data
products = [
    {"id": 1, "name": "Potato", "price": 30, "unit": "KG", 
     "image": "https://images.unsplash.com/photo-1518977676601-b53f82aba655?w=300&h=300&fit=crop", 
     "stock": 100},
    {"id": 2, "name": "Tomato", "price": 40, "unit": "KG", 
     "image": "https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=300&h=300&fit=crop", 
     "stock": 80},
    {"id": 3, "name": "Cauliflower", "price": 50, "unit": "Piece", 
     "image": "https://images.unsplash.com/photo-1568585100875-6dd3721b43ed?w=300&h=300&fit=crop", 
     "stock": 40},
    {"id": 4, "name": "Spinach", "price": 20, "unit": "Bundle", 
     "image": "https://images.unsplash.com/photo-1576045057995-568f588f82fb?w=300&h=300&fit=crop", 
     "stock": 60},
    {"id": 5, "name": "Onion", "price": 35, "unit": "KG", 
     "image": "https://images.unsplash.com/photo-1508747703725-719777637510?w=300&h=300&fit=crop", 
     "stock": 150},
    {"id": 6, "name": "Garlic", "price": 120, "unit": "KG", 
     "image": "https://images.unsplash.com/photo-1541808814-4544cb5342c7?w=300&h=300&fit=crop", 
     "stock": 30},
    {"id": 7, "name": "Carrot", "price": 45, "unit": "KG", 
     "image": "https://images.unsplash.com/photo-1598170845058-32b9d6a5da37?w=300&h=300&fit=crop", 
     "stock": 55},
    {"id": 8, "name": "Brinjal", "price": 40, "unit": "KG", 
     "image": "https://images.unsplash.com/photo-1552074284-5e88ef1aef18?w=300&h=300&fit=crop", 
     "stock": 45}
]

orders = []
order_counter = 1

@app.route('/')
def home():
    return jsonify({
        'message': '🌿 Vegetable Shop API',
        'status': 'running',
        'version': '2.0.0'
    })

@app.route('/api/products')
def get_products():
    return jsonify(products)

@app.route('/api/orders')
def get_orders():
    return jsonify(orders)

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
def update_order_status():
    data = request.json
    order_id = data.get('order_id')
    new_status = data.get('status')
    for order in orders:
        if order['order_id'] == order_id:
            order['status'] = new_status
            return jsonify({'success': True, 'order': order})
    return jsonify({'success': False, 'message': 'Order not found'}), 404

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'orders_count': len(orders),
        'products_count': len(products)
    })

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
            .stats { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 16px; }
            .stat-card { background: white; padding: 12px; border-radius: 10px; text-align: center; }
            .stat-card .number { font-size: 24px; font-weight: 700; color: #2E7D32; }
            .order-card { background: white; padding: 16px; border-radius: 12px; margin-bottom: 12px; border-left: 4px solid #FF9800; }
            .btn { padding: 6px 12px; border: none; border-radius: 6px; font-size: 12px; font-weight: 600; cursor: pointer; margin: 2px; }
            .btn-confirm { background: #2196F3; color: white; }
            .btn-complete { background: #4CAF50; color: white; }
            .btn-cancel { background: #e74c3c; color: white; }
            .btn-refresh { background: #2E7D32; color: white; padding: 8px 16px; border: none; border-radius: 8px; cursor: pointer; }
        </style>
    </head>
    <body>
        <div class="header"><h1>🌿 Admin</h1><button class="btn-refresh" onclick="loadOrders()">Refresh</button></div>
        <div class="stats"><div class="stat-card"><div class="number" id="totalOrders">0</div><div>Total</div></div>
        <div class="stat-card"><div class="number" id="newOrders">0</div><div>New</div></div></div>
        <div id="ordersList"></div>
        <script>
            function loadOrders(){
                fetch('/api/orders').then(r=>r.json()).then(data=>{
                    document.getElementById('totalOrders').textContent=data.length;
                    document.getElementById('newOrders').textContent=data.filter(o=>o.status==='NEW').length;
                    const list=document.getElementById('ordersList');
                    if(data.length===0){list.innerHTML='<p>No orders</p>';return;}
                    list.innerHTML=data.map(o=>`
                        <div class="order-card">
                            <div><b>${o.order_id}</b> | ${o.status}</div>
                            <div>${o.customer} | ${o.phone}</div>
                            <div>Total: ₹${o.total}</div>
                            <div>
                                ${o.status==='NEW'?`<button class="btn btn-confirm" onclick="updateStatus('${o.order_id}','CONFIRMED')">Confirm</button>`:''}
                                ${o.status==='CONFIRMED'?`<button class="btn btn-complete" onclick="updateStatus('${o.order_id}','DELIVERED')">Deliver</button>`:''}
                            </div>
                        </div>
                    `).join('');
                });
            }
            function updateStatus(id,status){
                fetch('/api/order/status',{method:'PUT',headers:{'Content-Type':'application/json'},body:JSON.stringify({order_id:id,status:status})})
                .then(()=>loadOrders());
            }
            loadOrders();
            setInterval(loadOrders,30000);
        </script>
    </body>
    </html>
    '''
    return html

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)