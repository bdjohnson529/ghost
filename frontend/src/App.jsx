import { useState } from 'react'
import './App.css'
import { scanEmails } from './services/api'

function App() {
  const [services, setServices] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleScan = async () => {
    setLoading(true)
    setError(null)
    console.log('[Ghost App] handleScan: starting')
    try {
      const data = await scanEmails()
      console.log('[Ghost App] handleScan: got data', { success: data.success, serviceCount: data.services?.length })
      if (data.success) {
        setServices(data.services)
      } else {
        setError(data.error || 'Scan failed')
      }
    } catch (err) {
      console.error('[Ghost App] handleScan: error', err.name, err.message, err)
      setError(err.message)
    }
    setLoading(false)
  }

  return (
    <div className="container">
      <div className="brand">
        <p className="eyebrow">Classified</p>
        <h1>Ghost Security</h1>
        <p className="tagline">Automated security scans</p>
      </div>

      <button
        onClick={handleScan}
        disabled={loading}
        className="scan-button"
      >
        {loading ? 'Scanning...' : 'Scan Services'}
      </button>

      {error && <p className="error">{error}</p>}

      {services.length > 0 && (
        <div className="results">
          <h2>Found {services.length} services:</h2>
          <ul>
            {services.map(service => (
              <li key={service}>{service}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default App
