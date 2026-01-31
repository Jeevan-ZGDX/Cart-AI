import React, { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE = '/api/v1'

function Dashboard() {
  const [overview, setOverview] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchOverview()
    const interval = setInterval(fetchOverview, 5000) // Refresh every 5 seconds
    return () => clearInterval(interval)
  }, [])

  const fetchOverview = async () => {
    try {
      const response = await axios.get(`${API_BASE}/admin/analytics/overview`)
      setOverview(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching overview:', error)
      setLoading(false)
    }
  }

  if (loading) return <div className="loading">Loading dashboard...</div>

  return (
    <div className="dashboard">
      <h2>Overview</h2>
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Active Carts</h3>
          <p className="stat-value">{overview?.active_carts || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Transactions Today</h3>
          <p className="stat-value">{overview?.transactions_today || 0}</p>
        </div>
        <div className="stat-card">
          <h3>Revenue Today</h3>
          <p className="stat-value">${overview?.revenue_today?.toFixed(2) || '0.00'}</p>
        </div>
        <div className="stat-card">
          <h3>Active Alerts</h3>
          <p className="stat-value">{overview?.active_alerts || 0}</p>
        </div>
      </div>

      <div className="popular-products">
        <h3>Popular Products (Last 7 Days)</h3>
        <ul>
          {overview?.popular_products?.map((product, idx) => (
            <li key={idx}>
              {product.name} - {product.purchase_count} purchases
            </li>
          ))}
        </ul>
      </div>
    </div>
  )
}

export default Dashboard
