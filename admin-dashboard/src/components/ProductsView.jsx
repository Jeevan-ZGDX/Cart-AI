import React, { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE = '/api/v1'

function ProductsView() {
  const [products, setProducts] = useState([])
  const [searchQuery, setSearchQuery] = useState('')
  const [loading, setLoading] = useState(false)

  const searchProducts = async () => {
    if (!searchQuery.trim()) return
    setLoading(true)
    try {
      const response = await axios.get(`${API_BASE}/products/?query=${encodeURIComponent(searchQuery)}&limit=50`)
      setProducts(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error searching products:', error)
      setLoading(false)
    }
  }

  useEffect(() => {
    if (searchQuery) {
      const timer = setTimeout(searchProducts, 500)
      return () => clearTimeout(timer)
    } else {
      setProducts([])
    }
  }, [searchQuery])

  return (
    <div className="products-view">
      <h2>Product Management</h2>
      <div className="search-bar">
        <input
          type="text"
          placeholder="Search products by name, barcode, SKU, or category..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
        />
      </div>
      {loading && <p>Searching...</p>}
      <div className="products-list">
        {products.map((product) => (
          <div key={product.id} className="product-card">
            <h3>{product.name}</h3>
            <p>SKU: {product.sku}</p>
            <p>Barcode: {product.barcode}</p>
            <p>Category: {product.category}</p>
            <p>Price: ${product.price.toFixed(2)}</p>
            <p>Stock: {product.stock_quantity}</p>
          </div>
        ))}
        {searchQuery && products.length === 0 && !loading && (
          <p>No products found</p>
        )}
      </div>
    </div>
  )
}

export default ProductsView
