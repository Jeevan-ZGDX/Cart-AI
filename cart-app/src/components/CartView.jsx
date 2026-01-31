import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './CartView.css'

const API_BASE = '/api/v1'

function CartView({ cart, onRemoveItem, onRefresh }) {
  const [billing, setBilling] = useState(null)
  const [selectedItem, setSelectedItem] = useState(null)

  useEffect(() => {
    fetchBilling()
  }, [cart])

  const fetchBilling = async () => {
    try {
      const response = await axios.get(`${API_BASE}/cart/${cart.id}/billing`)
      setBilling(response.data)
    } catch (error) {
      console.error('Error fetching billing:', error)
    }
  }

  const verifyItem = async (itemId, productId) => {
    try {
      const response = await axios.post(`${API_BASE}/ai/verify`, {
        cart_id: cart.id,
        product_id: productId
      })
      alert(response.data.message)
      onRefresh()
    } catch (error) {
      console.error('Error verifying item:', error)
      alert('Verification failed')
    }
  }

  return (
    <div className="cart-view">
      <div className="cart-items">
        <h2>Cart Items ({cart.items?.length || 0})</h2>
        {cart.items && cart.items.length > 0 ? (
          <div className="items-list">
            {cart.items.map((item) => (
              <div key={item.id} className="cart-item">
                <div className="item-info">
                  <h3>{item.product?.name || 'Unknown Product'}</h3>
                  <p className="item-details">
                    ${item.unit_price.toFixed(2)} × {item.quantity} = ${item.subtotal.toFixed(2)}
                  </p>
                  <div className="item-badges">
                    {item.scan_verified && (
                      <span className="badge verified">✓ Scanned</span>
                    )}
                    {item.verified_by_ai && (
                      <span className="badge ai-verified">🤖 AI Verified</span>
                    )}
                    {!item.verified_by_ai && item.scan_verified && (
                      <span className="badge warning">⚠️ AI Check Needed</span>
                    )}
                  </div>
                </div>
                <div className="item-actions">
                  <button
                    className="btn-verify"
                    onClick={() => verifyItem(item.id, item.product_id)}
                  >
                    Verify
                  </button>
                  <button
                    className="btn-remove"
                    onClick={() => onRemoveItem(item.id)}
                  >
                    Remove
                  </button>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="empty-cart">Your cart is empty</p>
        )}
      </div>

      {billing && (
        <div className="billing-summary">
          <h2>Bill Summary</h2>
          <div className="bill-details">
            <div className="bill-row">
              <span>Subtotal:</span>
              <span>${billing.calculation.subtotal.toFixed(2)}</span>
            </div>
            <div className="bill-row">
              <span>Tax:</span>
              <span>${billing.calculation.tax_amount.toFixed(2)}</span>
            </div>
            {billing.calculation.discount_amount > 0 && (
              <div className="bill-row discount">
                <span>Discount:</span>
                <span>-${billing.calculation.discount_amount.toFixed(2)}</span>
              </div>
            )}
            <div className="bill-row total">
              <span>Total:</span>
              <span>${billing.calculation.final_amount.toFixed(2)}</span>
            </div>
          </div>
        </div>
      )}

      {cart.has_alert && (
        <div className="alert-banner">
          ⚠️ Alert: {cart.alert_reason}
        </div>
      )}
    </div>
  )
}

export default CartView
