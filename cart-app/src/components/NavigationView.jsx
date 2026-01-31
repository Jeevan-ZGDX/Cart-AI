import React, { useState } from 'react'
import axios from 'axios'
import './NavigationView.css'

const API_BASE = '/api/v1'

function NavigationView({ cartId }) {
  const [productId, setProductId] = useState('')
  const [route, setRoute] = useState(null)
  const [loading, setLoading] = useState(false)

  const getRoute = async () => {
    if (!productId) {
      alert('Please enter a product ID')
      return
    }

    setLoading(true)
    try {
      const response = await axios.post(`${API_BASE}/navigation/route`, {
        cart_id: cartId,
        target_product_id: parseInt(productId)
      })
      setRoute(response.data)
    } catch (error) {
      console.error('Error getting route:', error)
      alert('Failed to get navigation route')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="navigation-view">
      <div className="route-input">
        <h2>Store Navigation</h2>
        <div className="input-group">
          <input
            type="number"
            placeholder="Enter Product ID"
            value={productId}
            onChange={(e) => setProductId(e.target.value)}
            className="product-id-input"
          />
          <button onClick={getRoute} className="get-route-btn" disabled={loading}>
            {loading ? 'Getting Route...' : 'Get Route'}
          </button>
        </div>
      </div>

      {route && (
        <div className="route-display">
          <div className="route-header">
            <h3>Route to {route.target_aisle.name}</h3>
            <p className="route-stats">
              Distance: {route.total_distance.toFixed(1)} units | 
              Est. Time: {route.estimated_time_minutes.toFixed(1)} min
            </p>
          </div>

          <div className="route-steps">
            {route.route.map((step) => (
              <div key={step.step_number} className="route-step">
                <div className="step-number">{step.step_number}</div>
                <div className="step-content">
                  <p className="step-instruction">{step.instruction}</p>
                  <p className="step-location">
                    {step.aisle_name} - Section {route.target_aisle.section}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {!route && (
        <div className="navigation-placeholder">
          <p>Enter a product ID to get navigation instructions</p>
        </div>
      )}
    </div>
  )
}

export default NavigationView
