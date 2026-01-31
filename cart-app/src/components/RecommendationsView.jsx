import React, { useState, useEffect } from 'react'
import axios from 'axios'
import './RecommendationsView.css'

const API_BASE = '/api/v1'

function RecommendationsView({ cartId, onAddToCart }) {
  const [recommendations, setRecommendations] = useState(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    fetchRecommendations()
  }, [cartId])

  const fetchRecommendations = async () => {
    setLoading(true)
    try {
      const response = await axios.get(`${API_BASE}/recommendations/cart/${cartId}`)
      setRecommendations(response.data)
    } catch (error) {
      console.error('Error fetching recommendations:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="recommendations-loading">Loading recommendations...</div>
  }

  if (!recommendations || recommendations.recommendations.length === 0) {
    return (
      <div className="recommendations-empty">
        <p>No recommendations available. Add items to your cart to see recommendations!</p>
      </div>
    )
  }

  return (
    <div className="recommendations-view">
      <h2>Recommended for You</h2>
      <p className="recommendations-subtitle">
        Based on items in your cart
      </p>

      <div className="recommendations-grid">
        {recommendations.recommendations.map((rec, index) => (
          <div key={index} className="recommendation-card">
            <div className="recommendation-header">
              <span className="recommendation-type">{rec.recommendation_type}</span>
              <span className="confidence-score">
                {Math.round(rec.confidence_score * 100)}% match
              </span>
            </div>
            <div className="product-info">
              <h3>{rec.product.name}</h3>
              <p className="product-category">{rec.product.category}</p>
              <p className="product-price">${rec.product.price.toFixed(2)}</p>
              <p className="recommendation-reason">{rec.reason}</p>
            </div>
            <button
              className="add-recommendation-btn"
              onClick={() => onAddToCart(rec.product.id, 1)}
            >
              Add to Cart
            </button>
          </div>
        ))}
      </div>
    </div>
  )
}

export default RecommendationsView
