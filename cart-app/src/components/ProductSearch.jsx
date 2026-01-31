import React, { useState } from 'react'
import axios from 'axios'
import './ProductSearch.css'

const API_BASE = '/api/v1'

function ProductSearch({ onAddToCart }) {
  const [query, setQuery] = useState('')
  const [products, setProducts] = useState([])
  const [loading, setLoading] = useState(false)

  const searchProducts = async () => {
    if (!query.trim()) return
    
    setLoading(true)
    try {
      const response = await axios.get(`${API_BASE}/products/`, {
        params: { query: query, limit: 20 }
      })
      setProducts(response.data)
    } catch (error) {
      console.error('Error searching products:', error)
      alert('Failed to search products')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    searchProducts()
  }

  const scanBarcode = async (barcode) => {
    try {
      const response = await axios.get(`${API_BASE}/products/barcode/${barcode}`)
      onAddToCart(response.data.id, 1)
      alert(`Added ${response.data.name} to cart`)
    } catch (error) {
      alert('Product not found')
    }
  }

  return (
    <div className="product-search">
      <div className="search-section">
        <form onSubmit={handleSubmit} className="search-form">
          <input
            type="text"
            placeholder="Search products by name, barcode, SKU, or category..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="search-input"
          />
          <button type="submit" className="search-btn" disabled={loading}>
            {loading ? 'Searching...' : 'Search'}
          </button>
        </form>

        <div className="barcode-section">
          <h3>Scan Barcode</h3>
          <input
            type="text"
            placeholder="Enter barcode"
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                scanBarcode(e.target.value)
                e.target.value = ''
              }
            }}
            className="barcode-input"
          />
        </div>
      </div>

      <div className="products-grid">
        {products.map((product) => (
          <div key={product.id} className="product-card">
            <div className="product-info">
              <h3>{product.name}</h3>
              <p className="product-category">{product.category}</p>
              <p className="product-price">${product.price.toFixed(2)}</p>
              <p className="product-sku">SKU: {product.sku}</p>
            </div>
            <button
              className="add-to-cart-btn"
              onClick={() => onAddToCart(product.id, 1)}
            >
              Add to Cart
            </button>
          </div>
        ))}
      </div>

      {products.length === 0 && !loading && query && (
        <p className="no-results">No products found</p>
      )}
    </div>
  )
}

export default ProductSearch
