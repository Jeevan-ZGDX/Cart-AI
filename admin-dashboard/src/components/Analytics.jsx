import React, { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE = '/api/v1'

function Analytics() {
  const [popularProducts, setPopularProducts] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAnalytics()
  }, [])

  const fetchAnalytics = async () => {
    try {
      const response = await axios.get(`${API_BASE}/admin/products/popular?days=7&limit=20`)
      setPopularProducts(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching analytics:', error)
      setLoading(false)
    }
  }

  if (loading) return <div className="loading">Loading analytics...</div>

  return (
    <div className="analytics">
      <h2>Product Analytics</h2>
      <table className="analytics-table">
        <thead>
          <tr>
            <th>Product Name</th>
            <th>Category</th>
            <th>Price</th>
            <th>Purchase Count</th>
            <th>Total Quantity</th>
          </tr>
        </thead>
        <tbody>
          {popularProducts.map((product) => (
            <tr key={product.product_id}>
              <td>{product.name}</td>
              <td>{product.category}</td>
              <td>${product.price.toFixed(2)}</td>
              <td>{product.purchase_count}</td>
              <td>{product.total_quantity}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default Analytics
