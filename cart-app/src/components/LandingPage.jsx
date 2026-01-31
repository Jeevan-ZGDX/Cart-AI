import React from 'react'
import './LandingPage.css'

function LandingPage({ onStartShopping }) {
  return (
    <div className="landing-page">
      <div className="hero-section">
        <div className="hero-content">
          <h1 className="hero-title">Smart Retail Cart</h1>
          <p className="hero-subtitle">AI-Powered Shopping Experience</p>
          <p className="hero-description">
            Experience the future of retail shopping with our intelligent cart system.
            Real-time billing, AI product verification, smart navigation, and personalized recommendations.
          </p>
          <button className="cta-button" onClick={onStartShopping}>
            Start Shopping
          </button>
        </div>
        <div className="hero-features">
          <div className="feature-card">
            <div className="feature-icon">🤖</div>
            <h3>AI Verification</h3>
            <p>Automatic product verification using computer vision</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🧭</div>
            <h3>Smart Navigation</h3>
            <p>Find products quickly with aisle-level navigation</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">💰</div>
            <h3>Real-time Billing</h3>
            <p>See your total update instantly as you shop</p>
          </div>
          <div className="feature-card">
            <div className="feature-icon">🔔</div>
            <h3>Theft Detection</h3>
            <p>Advanced security with automatic alert system</p>
          </div>
        </div>
      </div>
      
      <div className="stats-section">
        <div className="stat-item">
          <div className="stat-number">38+</div>
          <div className="stat-label">Products Available</div>
        </div>
        <div className="stat-item">
          <div className="stat-number">10</div>
          <div className="stat-label">Store Aisles</div>
        </div>
        <div className="stat-item">
          <div className="stat-number">24/7</div>
          <div className="stat-label">Smart Monitoring</div>
        </div>
      </div>
    </div>
  )
}

export default LandingPage
