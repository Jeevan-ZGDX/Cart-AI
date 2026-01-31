import React, { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE = '/api/v1'

function CartsView() {
  const [carts, setCarts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchCarts()
    const interval = setInterval(fetchCarts, 3000) // Refresh every 3 seconds
    return () => clearInterval(interval)
  }, [])

  const fetchCarts = async () => {
    try {
      const response = await axios.get(`${API_BASE}/admin/carts/active`)
      setCarts(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching carts:', error)
      setLoading(false)
    }
  }

  if (loading) return <div className="loading">Loading active carts...</div>

  return (
    <div className="carts-view">
      <h2>Active Carts ({carts.length})</h2>
      <div className="carts-list">
        {carts.map((cart) => (
          <div key={cart.id} className="cart-card">
            <div className="cart-header">
              <h3>Session: {cart.session_id}</h3>
              {cart.has_alert && <span className="alert-badge">⚠️ Alert</span>}
            </div>
            <div className="cart-details">
              <p>Items: {cart.item_count}</p>
              <p>Total: ${cart.total_amount?.toFixed(2) || '0.00'}</p>
              <p>Final: ${cart.final_amount?.toFixed(2) || '0.00'}</p>
            </div>
          </div>
        ))}
        {carts.length === 0 && <p>No active carts</p>}
      </div>
    </div>
  )
}

export default CartsView
