import React, { useState, useEffect } from 'react';
import './index.css';

const Dashboard = () => {
  const [alerts, setAlerts] = useState([]);
  const [stats, setStats] = useState({
    total_processed: 0,
    high_risk_alerts: 0,
    platform_distribution: { Telegram: 0, Instagram: 0 }
  });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 5000); // Poll every 5 seconds
    return () => clearInterval(interval);
  }, []);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

  const fetchData = async () => {
    try {
      const [alertsRes, statsRes] = await Promise.all([
        fetch(`${API_URL}/alerts`),
        fetch(`${API_URL}/stats`)
      ]);
      const alertsData = await alertsRes.json();
      const statsData = await statsRes.json();
      setAlerts(alertsData);
      setStats(statsData);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  };

  return (
    <div className="dashboard">
      <header>
        <div>
          <h1 className="title-gradient">DrugDetect AI</h1>
          <p style={{ color: 'var(--text-muted)' }}>Real-time public social media monitoring platform</p>
        </div>
        <div className="card" style={{ padding: '0.75rem 1.5rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <div style={{ width: 8, height: 8, borderRadius: '50%', backgroundColor: '#10b981' }}></div>
          <span style={{ fontSize: '0.9rem', fontWeight: 500 }}>System Live</span>
        </div>
      </header>

      <div className="stats-grid">
        <div className="card">
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>Total Posts Processed</p>
          <div style={{ fontSize: '2rem', fontWeight: 700 }}>{stats.total_processed}</div>
        </div>
        <div className="card">
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>High Risk Alerts</p>
          <div style={{ fontSize: '2rem', fontWeight: 700, color: 'var(--danger)' }}>{stats.high_risk_alerts}</div>
        </div>
        <div className="card">
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>Telegram Traffic</p>
          <div style={{ fontSize: '2rem', fontWeight: 700 }}>{stats.platform_distribution.Telegram}</div>
        </div>
        <div className="card">
          <p style={{ color: 'var(--text-muted)', fontSize: '0.875rem' }}>Instagram Traffic</p>
          <div style={{ fontSize: '2rem', fontWeight: 700 }}>{stats.platform_distribution.Instagram}</div>
        </div>
      </div>

      <div className="card" style={{ flex: 1 }}>
        <h2 style={{ marginBottom: '1rem' }}>Recent Alerts</h2>
        <table className="alert-table">
          <thead>
            <tr>
              <th>Platform</th>
              <th>Content Snippet</th>
              <th>Risk Score</th>
              <th>Status</th>
              <th>Reasoning</th>
            </tr>
          </thead>
          <tbody>
            {alerts.length > 0 ? alerts.map((alert) => (
              <tr key={alert.id}>
                <td><span className="platform-badge">{alert.platform}</span></td>
                <td>{alert.content_preview}</td>
                <td>
                  <span className={`risk-badge risk-${alert.risk_score.level.toLowerCase()}`}>
                    {alert.risk_score.score}% {alert.risk_score.level}
                  </span>
                </td>
                <td>{alert.status}</td>
                <td style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                  {alert.risk_score.reasoning[0]}
                </td>
              </tr>
            )) : (
              <tr>
                <td colSpan="5" style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-muted)' }}>
                  No alerts detected yet. Monitoring signals...
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Dashboard;
