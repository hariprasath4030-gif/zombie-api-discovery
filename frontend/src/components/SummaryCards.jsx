export default function SummaryCards({ summary }) {
  const keys = ['active', 'deprecated', 'orphaned', 'zombie']

  return (
    <div className="grid section">
      {keys.map((key) => (
        <div className="card" key={key}>
          <div style={{ fontSize: 12, color: '#6b7280' }}>{key.toUpperCase()}</div>
          <div style={{ fontSize: 26, fontWeight: 700 }}>{summary?.[key] || 0}</div>
        </div>
      ))}
    </div>
  )
}
