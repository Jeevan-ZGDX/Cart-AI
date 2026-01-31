import React, { useState } from 'react'
import Dashboard from './components/Dashboard'
import Analytics from './components/Analytics'
import CartsView from './components/CartsView'
import AlertsView from './components/AlertsView'
import ProductsView from './components/ProductsView'
import './App.css'

function App() {
  const [activeView, setActiveView] = useState('dashboard')

  return (
    <div className="admin-app">
      <header className="admin-header">
        <h1>📊 Admin Dashboard</h1>
        <nav className="admin-nav">
          <button
            className={activeView === 'dashboard' ? 'active' : ''}
            onClick={() => setActiveView('dashboard')}
          >
            Dashboard
          </button>
          <button
            className={activeView === 'analytics' ? 'active' : ''}
            onClick={() => setActiveView('analytics')}
          >
            Analytics
          </button>
          <button
            className={activeView === 'carts' ? 'active' : ''}
            onClick={() => setActiveView('carts')}
          >
            Active Carts
          </button>
          <button
            className={activeView === 'alerts' ? 'active' : ''}
            onClick={() => setActiveView('alerts')}
          >
            Alerts
          </button>
          <button
            className={activeView === 'products' ? 'active' : ''}
            onClick={() => setActiveView('products')}
          >
            Products
          </button>
        </nav>
      </header>

      <main className="admin-main">
        {activeView === 'dashboard' && <Dashboard />}
        {activeView === 'analytics' && <Analytics />}
        {activeView === 'carts' && <CartsView />}
        {activeView === 'alerts' && <AlertsView />}
        {activeView === 'products' && <ProductsView />}
      </main>
    </div>
  )
}

export default App
