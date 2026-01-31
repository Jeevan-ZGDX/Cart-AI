import React, { useState, useEffect } from 'react'
import axios from 'axios'

const API_BASE = '/api/v1'

function AlertsView() {
  const [alertsSummary, setAlertsSummary] = useState({})
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAlerts()
    const interval = setInterval(fetchAlerts, 5000)
    return () => clearInterval(interval)
  }, [])

  const fetchAlerts = async () => {
    try {
      const response = await axios.get(`${API_BASE}/admin/alerts/summary?days=7`)
      setAlertsSummary(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Error fetching alerts:', error)
      setLoading(false)
    }
  }

  if (loading) return <div className="loading">Loading alerts...</div>

  return (
    <div className="alerts-view">
      <h2>Alerts Summary (Last 7 Days)</h2>
      <div className="alerts-summary">
        {Object.keys(alertsSummary).length === 0 ? (
          <p>No alerts in the last 7 days</p>
        ) : (
          Object.entries(alertsSummary).map(([type, data]) => (
            <div key={type} className="alert-summary-card">
              <h3>{type.replace(/_/g, ' ').toUpperCase()}</h3>
              <p>Total: {data.count}</p>
              <p>High Severity: {data.high_severity}</p>
              <p>Resolved: {data.resolved}</p>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

export default AlertsView
