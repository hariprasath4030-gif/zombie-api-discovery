import { useEffect, useState } from 'react'
import { discoverApis, getAlerts, getReport, getResults, runFix } from './api/client'
import SummaryCards from './components/SummaryCards'
import ApiTable from './components/ApiTable'
import AlertsPanel from './components/AlertsPanel'

export default function App() {
  const [urls, setUrls] = useState('https://jsonplaceholder.typicode.com/posts\nhttps://jsonplaceholder.typicode.com/users')
  const [swaggerUrls, setSwaggerUrls] = useState('')
  const [logPaths, setLogPaths] = useState('')
  const [results, setResults] = useState({ total: 0, summary: {}, apis: [] })
  const [alerts, setAlerts] = useState([])
  const [fixes, setFixes] = useState([])
  const [loading, setLoading] = useState(false)

  const splitLines = (text) =>
    text
      .split('\n')
      .map((line) => line.trim())
      .filter(Boolean)

  const refresh = async () => {
    const [res, alertRes] = await Promise.all([getResults(), getAlerts()])
    setResults(res.data)
    setAlerts(alertRes.data.alerts)
  }

  useEffect(() => {
    refresh().catch(() => undefined)
  }, [])

  const handleScan = async () => {
    setLoading(true)
    try {
      const payload = {
        urls: splitLines(urls),
        swagger_urls: splitLines(swaggerUrls),
        log_paths: splitLines(logPaths)
      }
      await discoverApis(payload)
      await refresh()
      setFixes([])
    } finally {
      setLoading(false)
    }
  }

  const handleFix = async () => {
    const res = await runFix()
    setFixes(res.data.fixes || [])
  }

  const handleDownloadReport = async () => {
    const report = await getReport()
    const blob = new Blob([JSON.stringify(report.data, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const anchor = document.createElement('a')
    anchor.href = url
    anchor.download = 'zombie-api-report.json'
    anchor.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="container">
      <h1>Zombie API Discovery & Defence</h1>

      <div className="section card">
        <label>URLs (one per line)</label>
        <textarea rows={4} value={urls} onChange={(e) => setUrls(e.target.value)} />

        <label>Swagger URLs (one per line)</label>
        <textarea rows={3} value={swaggerUrls} onChange={(e) => setSwaggerUrls(e.target.value)} />

        <label>Log file paths (one per line)</label>
        <textarea rows={2} value={logPaths} onChange={(e) => setLogPaths(e.target.value)} />

        <div style={{ marginTop: 12 }}>
          <button onClick={handleScan} disabled={loading}>
            {loading ? 'Scanning...' : 'Run Discovery'}
          </button>
          <button onClick={handleFix}>Run Alert Fix Queue</button>
          <button onClick={handleDownloadReport}>Download Report</button>
          <a className="inline-link" href="http://127.0.0.1:8000/docs" target="_blank" rel="noreferrer">
            API Docs
          </a>
          <a className="inline-link" href="http://127.0.0.1:8000/api/report" target="_blank" rel="noreferrer">
            JSON Report URL
          </a>
        </div>
      </div>

      <SummaryCards summary={results.summary} />
      <ApiTable apis={results.apis} />
      <AlertsPanel alerts={alerts} fixes={fixes} />
    </div>
  )
}
