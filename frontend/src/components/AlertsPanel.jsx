export default function AlertsPanel({ alerts, fixes }) {
  return (
    <div className="section grid">
      <div className="card">
        <h3>Alerts</h3>
        {alerts?.length ? (
          alerts.map((a, index) => (
            <div key={`${a.endpoint}-${index}`} style={{ marginBottom: 10 }}>
              <strong>{a.severity.toUpperCase()}</strong> - {a.endpoint}
              <div>{a.reason}</div>
              <small>{a.recommendation}</small>
            </div>
          ))
        ) : (
          <div>No alerts</div>
        )}
      </div>

      <div className="card">
        <h3>Fix Queue</h3>
        {fixes?.length ? (
          fixes.map((f, index) => (
            <div key={`${f.endpoint}-${index}`} style={{ marginBottom: 10 }}>
              <div>{f.endpoint}</div>
              <small>{f.action}</small>
            </div>
          ))
        ) : (
          <div>No fixes queued</div>
        )}
      </div>
    </div>
  )
}
