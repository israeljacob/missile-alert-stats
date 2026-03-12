import React, { useState, useEffect, useCallback } from 'react'
import { fetchAreas, fetchStats } from './api'
import AreaSelector from './components/AreaSelector'
import TimeRangeSelector from './components/TimeRangeSelector'
import StatsDisplay from './components/StatsDisplay'
import EventsChart from './components/EventsChart'

function formatDateTime(isoStr) {
  return isoStr.replace('T', ' ').replace(/:\d{2}$/, '')
}

export default function App() {
  const [areas, setAreas] = useState([])
  const [selectedArea, setSelectedArea] = useState('')
  const [range, setRange] = useState('1d')
  const [fromDate, setFromDate] = useState('2025-06-01')
  const [toDate, setToDate] = useState(new Date().toISOString().split('T')[0])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchAreas()
      .then(data => {
        setAreas(data)
        if (data.length > 0) setSelectedArea(data[0])
      })
      .catch(() => setError('שגיאה בטעינת רשימת האזורים'))
  }, [])

  const loadStats = useCallback(async () => {
    if (!selectedArea) return
    setLoading(true)
    setError(null)
    try {
      const data = await fetchStats({
        area: selectedArea,
        range,
        from: fromDate,
        to: toDate,
      })
      setStats(data)
    } catch {
      setError('שגיאה בטעינת נתונים')
    } finally {
      setLoading(false)
    }
  }, [selectedArea, range, fromDate, toDate])

  useEffect(() => {
    loadStats()
  }, [loadStats])

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.title}>סטטיסטיקות התרעות פיקוד העורף</h1>
      </header>

      <div style={styles.controls}>
        <AreaSelector
          areas={areas}
          selected={selectedArea}
          onChange={setSelectedArea}
        />
        <TimeRangeSelector
          range={range}
          onRangeChange={setRange}
          fromDate={fromDate}
          toDate={toDate}
          onFromChange={setFromDate}
          onToChange={setToDate}
        />
      </div>

      {error && <div style={styles.error}>{error}</div>}
      {loading && <div style={styles.loading}>טוען...</div>}

      {stats && !loading && (
        <>
          <StatsDisplay stats={stats} />
          <EventsChart events={stats.events} />
          <div style={styles.tableContainer}>
            <h3 style={styles.tableTitle}>פירוט אירועים</h3>
            <table style={styles.table}>
              <thead>
                <tr>
                  <th style={styles.th}>התחלה</th>
                  <th style={styles.th}>סיום</th>
                  <th style={styles.th}>משך (דקות)</th>
                  <th style={styles.th}>סוג</th>
                </tr>
              </thead>
              <tbody>
                {stats.events.map((e, i) => (
                  <tr key={i} style={i % 2 === 0 ? styles.evenRow : {}}>
                    <td style={styles.td}>{formatDateTime(e.start)}</td>
                    <td style={styles.td}>{formatDateTime(e.end)}</td>
                    <td style={styles.td}>{(e.duration_seconds / 60).toFixed(1)}</td>
                    <td style={styles.td}>{e.type}</td>
                  </tr>
                ))}
                {stats.events.length === 0 && (
                  <tr>
                    <td colSpan={4} style={{ ...styles.td, textAlign: 'center' }}>
                      אין אירועים בטווח הזמן הנבחר
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </>
      )}

      {!selectedArea && !loading && (
        <div style={styles.placeholder}>בחר אזור כדי לראות סטטיסטיקות</div>
      )}
    </div>
  )
}

const styles = {
  container: {
    maxWidth: 900,
    margin: '0 auto',
    padding: 20,
  },
  header: {
    background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 100%)',
    color: '#fff',
    padding: '24px 32px',
    borderRadius: 12,
    marginBottom: 20,
  },
  title: {
    fontSize: 24,
    fontWeight: 700,
  },
  controls: {
    display: 'flex',
    gap: 16,
    flexWrap: 'wrap',
    marginBottom: 20,
    alignItems: 'flex-start',
  },
  error: {
    background: '#ffeef0',
    color: '#d32f2f',
    padding: '12px 16px',
    borderRadius: 8,
    marginBottom: 16,
  },
  loading: {
    textAlign: 'center',
    padding: 40,
    color: '#666',
    fontSize: 18,
  },
  placeholder: {
    textAlign: 'center',
    padding: 60,
    color: '#999',
    fontSize: 18,
  },
  tableContainer: {
    background: '#fff',
    borderRadius: 12,
    padding: 20,
    boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
  },
  tableTitle: {
    marginBottom: 12,
    fontSize: 18,
  },
  table: {
    width: '100%',
    borderCollapse: 'collapse',
    fontSize: 14,
  },
  th: {
    textAlign: 'right',
    padding: '10px 12px',
    borderBottom: '2px solid #e0e0e0',
    fontWeight: 600,
  },
  td: {
    padding: '8px 12px',
    borderBottom: '1px solid #f0f0f0',
  },
  evenRow: {
    background: '#fafafa',
  },
}
