export default function ApiTable({ apis }) {
  return (
    <div className="section card" style={{ padding: 0 }}>
      <table>
        <thead>
          <tr>
            <th>Endpoint</th>
            <th>Method</th>
            <th>Status</th>
            <th>Reachable</th>
            <th>Security</th>
          </tr>
        </thead>
        <tbody>
          {apis?.length ? (
            apis.map((api, index) => (
              <tr key={`${api.endpoint}-${index}`}>
                <td>{api.endpoint}</td>
                <td>{api.method}</td>
                <td>{api.status}</td>
                <td>{api.is_reachable ? 'Yes' : 'No'}</td>
                <td>
                  Auth: {api.security?.authentication}, TLS: {api.security?.encryption}, RL: {api.security?.rate_limiting}
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan={5}>No APIs scanned yet</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  )
}
