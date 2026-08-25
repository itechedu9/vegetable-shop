import React, { useState, useEffect } from 'react';
import './App.css';

const API_URL = 'https://vegetable-shop-api-no22.onrender.com';

function App() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [cart, setCart] = useState([]);
  const [showCart, setShowCart] = useState(false);
  const [showCheckout, setShowCheckout] = useState(false);
  const [orderPlaced, setOrderPlaced] = useState(false);
  const [orderId, setOrderId] = useState('');
  const [notification, setNotification] = useState('');
  const [language, setLanguage] = useState('en');
  const [search, setSearch] = useState('');

  const [customer, setCustomer] = useState({
    name: '', phone: '', address: '', area: '', landmark: '', payment_method: 'COD'
  });

  const translations = {
    en: {
      title: 'Fresh Veggies', subtitle: 'Farm fresh vegetables delivered to your door',
      search: 'Search vegetables...', addToCart: 'Add to Cart', cart: 'Cart',
      emptyCart: 'Your cart is empty', checkout: 'Proceed to Checkout',
      placeOrder: 'Place Order', orderPlaced: 'Order Placed Successfully!',
      track: 'Track Order', total: 'Total', delivery: 'Delivery',
      subtotal: 'Subtotal', name: 'Full Name', phone: 'Phone Number',
      address: 'Delivery Address', area: 'Area', landmark: 'Landmark',
      payment: 'Payment Method', cod: 'Cash on Delivery', upi: 'UPI',
      orderId: 'Order ID', status: 'Status', continue: 'Continue Shopping',
      marketPrice: 'Market Price', youSave: 'You Save', discount: 'Discount'
    },
    bn: {
      title: 'তাজা সবজি', subtitle: 'খামার থেকে তাজা সবজি আপনার দোরগোড়ায়',
      search: 'সবজি খুঁজুন...', addToCart: 'কার্টে যোগ করুন', cart: 'কার্ট',
      emptyCart: 'আপনার কার্ট খালি', checkout: 'চেকআউট করুন',
      placeOrder: 'অর্ডার করুন', orderPlaced: 'অর্ডার সফল হয়েছে!',
      track: 'অর্ডার ট্র্যাক', total: 'মোট', delivery: 'ডেলিভারি',
      subtotal: 'সাবটোটাল', name: 'পূর্ণ নাম', phone: 'ফোন নম্বর',
      address: 'ডেলিভারি ঠিকানা', area: 'এলাকা', landmark: 'ল্যান্ডমার্ক',
      payment: 'পেমেন্ট পদ্ধতি', cod: 'ডেলিভারিতে পেমেন্ট', upi: 'ইউপিআই',
      orderId: 'অর্ডার আইডি', status: 'স্ট্যাটাস', continue: 'শপিং চালিয়ে যান',
      marketPrice: 'বাজার দর', youSave: 'সংরক্ষণ', discount: 'ছাড়'
    },
    hi: {
      title: 'ताज़ी सब्जियाँ', subtitle: 'खेत से ताज़ी सब्जियाँ आपके दरवाजे पर',
      search: 'सब्जियाँ खोजें...', addToCart: 'कार्ट में डालें', cart: 'कार्ट',
      emptyCart: 'आपकी कार्ट खाली है', checkout: 'चेकआउट करें',
      placeOrder: 'ऑर्डर करें', orderPlaced: 'ऑर्डर सफल हुआ!',
      track: 'ऑर्डर ट्रैक करें', total: 'कुल', delivery: 'डिलीवरी',
      subtotal: 'उप-योग', name: 'पूरा नाम', phone: 'फोन नंबर',
      address: 'डिलीवरी पता', area: 'क्षेत्र', landmark: 'लैंडमार्क',
      payment: 'भुगतान विधि', cod: 'डिलीवरी पर भुगतान', upi: 'यूपीआई',
      orderId: 'ऑर्डर आईडी', status: 'स्थिति', continue: 'खरीदारी जारी रखें',
      marketPrice: 'बाजार मूल्य', youSave: 'बचत', discount: 'छूट'
    }
  };

  const t = translations[language];

  useEffect(() => {
    fetch(`${API_URL}/api/products/active`)
      .then(res => res.json())
      .then(data => { setProducts(data); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const getProductName = (p) => {
    if (language === 'bn') return p.name_bn || p.name;
    if (language === 'hi') return p.name_hi || p.name;
    return p.name;
  };

  const addToCart = (product) => {
    setCart(prev => {
      const existing = prev.find(item => item.id === product.id);
      if (existing) {
        return prev.map(item =>
          item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
        );
      }
      return [...prev, { ...product, quantity: 1 }];
    });
    setNotification(`${getProductName(product)} added to cart!`);
    setTimeout(() => setNotification(''), 2000);
  };

  const removeFromCart = (id) => {
    setCart(prev => {
      const existing = prev.find(item => item.id === id);
      if (existing && existing.quantity > 1) {
        return prev.map(item => item.id === id ? { ...item, quantity: item.quantity - 1 } : item);
      }
      return prev.filter(item => item.id !== id);
    });
  };

  const removeItem = (id) => setCart(prev => prev.filter(item => item.id !== id));
  const getSubtotal = () => cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  const getDeliveryCharge = () => { const s = getSubtotal(); return s === 0 ? 0 : s >= 100 ? 0 : 20; };
  const getTotal = () => getSubtotal() + getDeliveryCharge();
  const clearCart = () => setCart([]);

  const placeOrder = async () => {
    if (!customer.name || !customer.phone || !customer.address) {
      alert('Please fill in all required fields');
      return;
    }
    if (cart.length === 0) {
      alert('Your cart is empty');
      return;
    }
    setLoading(true);
    const orderData = {
      name: customer.name, phone: customer.phone, address: customer.address,
      area: customer.area, landmark: customer.landmark,
      payment_method: customer.payment_method,
      items: cart.map(item => ({ name: item.name, quantity: item.quantity, price: item.price, unit: item.unit })),
      subtotal: getSubtotal(), delivery: getDeliveryCharge(), total: getTotal()
    };
    try {
      const response = await fetch(`${API_URL}/api/order`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(orderData)
      });
      const data = await response.json();
      if (data.success) {
        setOrderId(data.order.order_id);
        setOrderPlaced(true);
        setCart([]);
        setCustomer({ name: '', phone: '', address: '', area: '', landmark: '', payment_method: 'COD' });
        setShowCheckout(false);
        setShowCart(false);
      }
    } catch (error) {
      alert('Error placing order. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const LanguageSelector = () => (
    <div className="language-selector">
      <button className={`lang-btn ${language === 'en' ? 'active' : ''}`} onClick={() => setLanguage('en')}>🇬🇧</button>
      <button className={`lang-btn ${language === 'bn' ? 'active' : ''}`} onClick={() => setLanguage('bn')}>🇧🇩</button>
      <button className={`lang-btn ${language === 'hi' ? 'active' : ''}`} onClick={() => setLanguage('hi')}>🇮🇳</button>
    </div>
  );

  if (orderPlaced) {
    return (
      <div className="order-success">
        <div className="success-card">
          <div className="success-icon">✅</div>
          <h1>{t.orderPlaced}</h1>
          <div className="order-id-box">
            <span className="order-id-label">{t.orderId}</span>
            <h2 className="order-id">{orderId}</h2>
          </div>
          <button className="btn-primary" onClick={() => setOrderPlaced(false)}>{t.continue}</button>
        </div>
      </div>
    );
  }

  if (showCart) {
    return (
      <div className="App">
        <header className="app-header">
          <button className="back-btn" onClick={() => setShowCart(false)}>←</button>
          <h1>🛒 {t.cart}</h1>
          {cart.length > 0 && <button className="clear-btn" onClick={clearCart}>🗑️</button>}
        </header>
        <main className="container">
          {cart.length === 0 ? (
            <div className="empty-cart">
              <div className="empty-icon">🛒</div>
              <h3>{t.emptyCart}</h3>
              <button className="btn-primary" onClick={() => setShowCart(false)}>Browse Vegetables</button>
            </div>
          ) : (
            <>
              <div className="cart-items">
                {cart.map(item => (
                  <div className="cart-item" key={item.id}>
                    <img src={item.image} alt={item.name} className="cart-item-image" />
                    <div className="cart-item-info">
                      <h4>{getProductName(item)}</h4>
                      <p className="cart-item-price">₹{item.price} / {item.unit}</p>
                    </div>
                    <div className="cart-item-controls">
                      <div className="quantity-controls">
                        <button onClick={() => removeFromCart(item.id)}>−</button>
                        <span>{item.quantity}</span>
                        <button onClick={() => addToCart(item)}>+</button>
                      </div>
                      <div className="cart-item-total">₹{item.price * item.quantity}</div>
                      <button className="remove-item" onClick={() => removeItem(item.id)}>✕</button>
                    </div>
                  </div>
                ))}
              </div>
              <div className="cart-summary">
                <div className="summary-row"><span>{t.subtotal}</span><span>₹{getSubtotal()}</span></div>
                <div className="summary-row"><span>{t.delivery}</span><span>{getDeliveryCharge() === 0 ? 'FREE' : `₹${getDeliveryCharge()}`}</span></div>
                <div className="summary-row total"><span>{t.total}</span><span>₹{getTotal()}</span></div>
              </div>
              <button className="btn-primary checkout-btn" onClick={() => setShowCheckout(true)}>{t.checkout} →</button>
            </>
          )}
        </main>
        {showCheckout && (
          <div className="checkout-modal">
            <div className="checkout-content">
              <div className="checkout-header">
                <h2>📋 {t.checkout}</h2>
                <button className="close-modal" onClick={() => setShowCheckout(false)}>✕</button>
              </div>
              <div className="checkout-body">
                <input type="text" placeholder={t.name} value={customer.name}
                  onChange={(e) => setCustomer({ ...customer, name: e.target.value })} className="checkout-input" />
                <input type="tel" placeholder={t.phone} value={customer.phone}
                  onChange={(e) => setCustomer({ ...customer, phone: e.target.value })} className="checkout-input" />
                <input type="text" placeholder={t.area} value={customer.area}
                  onChange={(e) => setCustomer({ ...customer, area: e.target.value })} className="checkout-input" />
                <textarea placeholder={t.address} value={customer.address}
                  onChange={(e) => setCustomer({ ...customer, address: e.target.value })} className="checkout-input" rows="3" />
                <input type="text" placeholder={t.landmark} value={customer.landmark}
                  onChange={(e) => setCustomer({ ...customer, landmark: e.target.value })} className="checkout-input" />
                <div className="payment-methods">
                  <label className="payment-option"><input type="radio" name="payment" value="COD" checked={customer.payment_method === 'COD'}
                    onChange={(e) => setCustomer({ ...customer, payment_method: e.target.value })} /> {t.cod}</label>
                  <label className="payment-option"><input type="radio" name="payment" value="UPI" checked={customer.payment_method === 'UPI'}
                    onChange={(e) => setCustomer({ ...customer, payment_method: e.target.value })} /> {t.upi}</label>
                </div>
                <div className="order-summary-mini">
                  <h4>Order Summary</h4>
                  <div className="summary-mini-row"><span>Items ({cart.length})</span><span>₹{getSubtotal()}</span></div>
                  <div className="summary-mini-row"><span>{t.delivery}</span><span>{getDeliveryCharge() === 0 ? 'FREE' : `₹${getDeliveryCharge()}`}</span></div>
                  <div className="summary-mini-row total-mini"><span>{t.total}</span><span>₹{getTotal()}</span></div>
                </div>
                <button className="btn-primary place-order-btn" onClick={placeOrder} disabled={loading}>
                  {loading ? 'Placing Order...' : `🛍️ ${t.placeOrder}`}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  // Main Shop
  const filteredProducts = products.filter(p =>
    p.name.toLowerCase().includes(search.toLowerCase()) ||
    (p.name_bn && p.name_bn.includes(search)) ||
    (p.name_hi && p.name_hi.includes(search))
  );

  if (loading) {
    return (
      <div className="loading">
        <h2>🔄 Loading Fresh Veggies...</h2>
      </div>
    );
  }

  return (
    <div className="App">
      <header className="app-header">
        <div className="header-left">
          <span className="logo-icon">🌿</span>
          <h1>{t.title}</h1>
        </div>
        <div className="header-right">
          <LanguageSelector />
          <button className="cart-btn" onClick={() => setShowCart(true)}>
            🛒 <span className="cart-count">{cart.length}</span>
          </button>
        </div>
      </header>

      {notification && <div className="notification"><span>{notification}</span></div>}

      <main className="container">
        <div className="hero-section">
          <h2>{t.title}</h2>
          <p>{t.subtitle}</p>
          <div className="features">
            <span>🌱 Fresh</span>
            <span>🚚 Free Delivery</span>
            <span>💰 Best Prices</span>
          </div>
        </div>

        <div className="search-bar">
          <input
            type="text"
            placeholder={t.search}
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="search-input"
          />
          <span className="search-icon">🔍</span>
        </div>

        {filteredProducts.length === 0 ? (
          <div style={{ textAlign: 'center', padding: '40px', color: '#888' }}>
            <p>No products available</p>
          </div>
        ) : (
          <div className="product-grid">
            {filteredProducts.map(product => {
              const discountPercent = product.discount || 0;
              const mrp = product.mrp || product.price;
              const price = product.price;
              const savings = mrp - price;
              
              return (
                <div className="product-card" key={product.id}>
                  <div className="product-image-container">
                    <img src={product.image} alt={product.name} className="product-image" />
                    {discountPercent > 0 && (
                      <span className="discount-badge">{discountPercent}% OFF</span>
                    )}
                    {product.stock < 10 && product.stock > 0 && (
                      <span className="stock-badge low-stock">Only {product.stock} left!</span>
                    )}
                    {product.stock === 0 && (
                      <span className="stock-badge out-of-stock">Out of Stock</span>
                    )}
                  </div>
                  <div className="product-info">
                    <h3>{getProductName(product)}</h3>
                    <div className="product-price">
                      <span className="price">₹{price}</span>
                      <span className="unit">/ {product.unit}</span>
                    </div>
                    {mrp > price && (
                      <div className="price-details">
                        <span className="mrp">MRP: ₹{mrp}</span>
                        <span className="savings">You save ₹{savings}</span>
                      </div>
                    )}
                    <button
                      className={`add-btn ${product.stock === 0 ? 'disabled' : ''}`}
                      onClick={() => addToCart(product)}
                      disabled={product.stock === 0}
                    >
                      {product.stock === 0 ? 'Out of Stock' : t.addToCart}
                    </button>
                  </div>
                </div>
              );
            })}
          </div>
        )}

        <div className="track-section">
          <button className="btn-track" onClick={() => {}}>
            📦 {t.track}
          </button>
        </div>
      </main>
    </div>
  );
}

export default App;