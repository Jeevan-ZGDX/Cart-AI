import React, { useState, useEffect } from 'react'
import axios from 'axios'
import CartView from './components/CartView'
import ProductSearch from './components/ProductSearch'
import NavigationView from './components/NavigationView'
import RecommendationsView from './components/RecommendationsView'
import PaymentView from './components/PaymentView'
import LandingPage from './components/LandingPage'
import './App.css'

const API_BASE = '/api/v1'

function App() {
  const [cart, setCart] = useState(null)
  const [activeTab, setActiveTab] = useState('cart')
  const [showLanding, setShowLanding] = useState(true)
  const [sessionId, setSessionId] = useState(() => {
    return localStorage.getItem('cart_session_id') || `CART-${Date.now()}`
  })

  useEffect(() => {
    localStorage.setItem('cart_session_id', sessionId)
    createOrGetCart()
  }, [sessionId])

  const createOrGetCart = async () => {
    try {
      const response = await axios.post(`${API_BASE}/cart/`, {
        session_id: sessionId
      })
      setCart(response.data)
    } catch (error) {
      console.error('Error creating cart:', error)
    }
  }

  const refreshCart = async () => {
    if (!cart) return
    try {
      const response = await axios.get(`${API_BASE}/cart/${cart.id}`)
      setCart(response.data)
    } catch (error) {
      console.error('Error refreshing cart:', error)
    }
  }

  const addItemToCart = async (productId, quantity = 1) => {
    if (!cart) return
    try {
      await axios.post(`${API_BASE}/cart/${cart.id}/items`, {
        product_id: productId,
        quantity: quantity
      })
      await refreshCart()
    } catch (error) {
      console.error('Error adding item:', error)
      alert('Failed to add item to cart')
    }
  }

  const removeItemFromCart = async (itemId) => {
    if (!cart) return
    try {
      await axios.delete(`${API_BASE}/cart/${cart.id}/items/${itemId}`)
      await refreshCart()
    } catch (error) {
      console.error('Error removing item:', error)
    }
  }

  if (showLanding) {
    return <LandingPage onStartShopping={() => setShowLanding(false)} />
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>🛒 Smart Retail Cart</h1>
        {cart && (
          <div className="cart-info">
            <span>Session: {cart.session_id}</span>
            {cart.has_alert && (
              <span className="alert-badge">⚠️ Alert</span>
            )}
          </div>
        )}
        <button className="home-button" onClick={() => setShowLanding(true)}>
          Home
        </button>
      </header>

      <nav className="tab-nav">
        <button
          className={activeTab === 'cart' ? 'active' : ''}
          onClick={() => setActiveTab('cart')}
        >
          Cart
        </button>
        <button
          className={activeTab === 'search' ? 'active' : ''}
          onClick={() => setActiveTab('search')}
        >
          Search
        </button>
        <button
          className={activeTab === 'navigation' ? 'active' : ''}
          onClick={() => setActiveTab('navigation')}
        >
          Navigation
        </button>
        <button
          className={activeTab === 'recommendations' ? 'active' : ''}
          onClick={() => setActiveTab('recommendations')}
        >
          Recommendations
        </button>
        <button
          className={activeTab === 'payment' ? 'active' : ''}
          onClick={() => setActiveTab('payment')}
        >
          Payment
        </button>
      </nav>

      <main className="app-main">
        {activeTab === 'cart' && cart && (
          <CartView
            cart={cart}
            onRemoveItem={removeItemFromCart}
            onRefresh={refreshCart}
          />
        )}
        {activeTab === 'search' && (
          <ProductSearch onAddToCart={addItemToCart} />
        )}
        {activeTab === 'navigation' && cart && (
          <NavigationView cartId={cart.id} />
        )}
        {activeTab === 'recommendations' && cart && (
          <RecommendationsView
            cartId={cart.id}
            onAddToCart={addItemToCart}
          />
        )}
        {activeTab === 'payment' && cart && (
          <PaymentView cartId={cart.id} onPaymentComplete={refreshCart} />
        )}
      </main>
    </div>
  )
}

export default App
