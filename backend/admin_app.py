from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Sample orders storage (in memory for now)
orders = []
order_counter = 1

@app.route('/')
def home():
    return jsonify({
        'message': '🌿 Vegetable Shop Admin API',
        'status': 'running'
    })

@app.route('/admin')
def admin_dashboard():
    # Admin HTML dashboard
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1">
        <title>🌿 Admin - Vegetable Shop</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { 
                font-family: -apple-system, 'Segoe UI', Roboto, sans-serif;
                background: #f0f4f8;
                padding: 16px;
            }
            .header {
                background: linear-gradient(135deg, #1a472a, #2E7D32);
                color: white;
                padding: 16px 20px;
                border-radius: 16px;
                margin-bottom: 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .header h1 { font-size: 20px; }
            .badge {
                background: #FFD54F;
                color: #1a472a;
                padding: 4px 12px;
                border-radius: 20px;
                font-weight: 600;
                font-size: 14px;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 10px;
                margin-bottom: 20px;
            }
            .stat-card {
                background: white;
                padding: 14px;
                border-radius: 12px;
                text-align: center;
                box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            }
            .stat-card .number {
                font-size: 24px;
                font-weight: 700;
                color: #2E7D32;
            }
            .stat-card .label {
                font-size: 12px;
                color: #888;
            }
            .order-card {
                background: white;
                border-radius: 14px;
                padding: 16px;
                margin-bottom: 12px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.06);
                border-left: 4px solid #FF9800;
            }
            .order-card.delivered {
                border-left-color: #4CAF50;
            }
            .order-card.cancelled {
                border-left-color: #e74c3c;
            }
            .order-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 8px;
            }
            .order-id {
                font-weight: 700;
                color: #2E7D32;
            }
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
            
            .order-details {
                font-size: 14px;
                color: #444;
                margin: 8px 0;
            }
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
            .btn {
                padding: 8px 16px;
                border: none;
                border-radius: 8px;
                font-size: 13px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s;
            }
            .btn:hover { transform: scale(0.97); }
            .btn-confirm { background: #2196F3; color: white; }
            .btn-prepare { background: #9C27B0; color: white; }
            .btn-deliver { background: #FF9800; color: white; }
            .btn-complete { background: #4CAF50; color: white; }
            .btn-cancel { background: #e74c3c; color: white; }
            .btn-call { background: #4CAF50; color: white; }
            .btn-whatsapp { background: #25D366; color: white; }
            
            .refresh-btn {
                background: white;
                color: #2E7D32;
                padding: 8px 16px;
                border: 2px solid #2E7D32;
                border-radius: 8px;
                font-weight: 600;
                cursor: pointer;
            }
            .refresh-btn:hover { background: #2E7D32; color: white; }
            
            @media (max-width: 600px) {
                .stats { grid-template-columns: repeat(2, 1fr); }
                .order-actions { flex-direction: column; }
                .order-actions .btn { width: 100%; }
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🌿 Admin Dashboard</h1>
            <button class="refresh-btn" onclick="loadOrders()">🔄 Refresh</button>
        </div>
        
        <div class="stats" id="stats">
            <div class="stat-card">
                <div class="number" id="totalOrders">0</div>
                <div class="label">Total Orders</div>
            </div>
            <div class="stat-card">
                <div class="number" id="newOrders">0</div>
                <div class="label">New Orders</div>
            </div>
            <div class="stat-card">
                <div class="number" id="deliveredOrders">0</div>
                <div class="label">Delivered</div>
            </div>
            <div class="stat-card">
                <div class="number" id="totalSales">₹0</div>
                <div class="label">Total Sales</div>
            </div>
        </div>
        
        <div id="ordersList"></div>
        
        <script>
            function loadOrders() {
                fetch('/api/orders')
                    .then(res => res.json())
                    .then(orders => {
                        const list = document.getElementById('ordersList');
                        const total = document.getElementById('totalOrders');
                        const newO = document.getElementById('newOrders');
                        const delivered = document.getElementById('deliveredOrders');
                        const sales = document.getElementById('totalSales');
                        
                        total.textContent = orders.length;
                        const newCount = orders.filter(o => o.status === 'NEW').length;
                        newO.textContent = newCount;
                        const deliveredCount = orders.filter(o => o.status === 'DELIVERED').length;
                        delivered.textContent = deliveredCount;
                        const totalSales = orders.reduce((sum, o) => sum + (o.total || 0), 0);
                        sales.textContent = '₹' + totalSales;
                        
                        if (orders.length === 0) {
                            list.innerHTML = '<p style="text-align:center;color:#888;padding:40px;">No orders yet</p>';
                            return;
                        }
                        
                        // Sort: newest first
                        orders.reverse();
                        
                        list.innerHTML = orders.map(order => `
                            <div class="order-card ${order.status === 'DELIVERED' ? 'delivered' : order.status === 'CANCELLED' ? 'cancelled' : ''}">
                                <div class="order-header">
                                    <span class="order-id">#${order.order_id}</span>
                                    <span class="order-status status-${order.status.toLowerCase()}">${order.status}</span>
                                </div>
                                <div class="order-details">
                                    <strong>${order.customer}</strong> | 📱 ${order.phone}
                                </div>
                                <div class="order-details">
                                    📍 ${order.address}
                                </div>
                                <div class="order-items">
                                    ${order.items.map(item => 
                                        `${item.name} × ${item.quantity} ${item.unit} = ₹${item.price * item.quantity}`
                                    ).join(' | ')}
                                </div>
                                <div class="order-details" style="font-weight:700;color:#2E7D32;">
                                    Total: ₹${order.total}
                                </div>
                                <div class="order-actions">
                                    <button class="btn btn-confirm" onclick="updateStatus('${order.order_id}', 'CONFIRMED')">✅ Confirm</button>
                                    <button class="btn btn-prepare" onclick="updateStatus('${order.order_id}', 'PREPARING')">🔪 Prepare</button>
                                    <button class="btn btn-deliver" onclick="updateStatus('${order.order_id}', 'OUT_FOR_DELIVERY')">🚚 Deliver</button>
                                    <button class="btn btn-complete" onclick="updateStatus('${order.order_id}', 'DELIVERED')">✅ Complete</button>
                                    <button class="btn btn-cancel" onclick="updateStatus('${order.order_id}', 'CANCELLED')">❌ Cancel</button>
                                    <button class="btn btn-call" onclick="window.location.href='tel:${order.phone}'">📞 Call</button>
                                    <button class="btn btn-whatsapp" onclick="window.location.href='https://wa.me/${order.phone}?text=Your%20order%20${order.order_id}%20has%20been%20confirmed'">💬 WhatsApp</button>
                                </div>
                            </div>
                        `).join('');
                    })
                    .catch(err => {
                        document.getElementById('ordersList').innerHTML = 
                            '<p style="color:red;">Error loading orders. Make sure backend is running.</p>';
                    });
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
            
            // Auto refresh every 30 seconds
            loadOrders();
            setInterval(loadOrders, 30000);
        </script>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route('/api/orders')
def get_orders():
    return jsonify(orders)

@app.route('/api/order', methods=['POST'])
def create_order():
    global order_counter
    
    data = request.json
    order = {
        'order_id': f'ORD-20260824-{str(order_counter).zfill(3)}',
        'customer': data.get('name', ''),
        'phone': data.get('phone', ''),
        'address': data.get('address', ''),
        'items': data.get('items', []),
        'total': data.get('total', 0),
        'status': 'NEW',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
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
            return jsonify({'success': True, 'order': order})
    
    return jsonify({'success': False, 'message': 'Order not found'}), 404

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'orders_count': len(orders)
    })

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)