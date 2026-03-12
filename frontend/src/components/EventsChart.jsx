import React, { useMemo } from 'react'
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

export default function EventsChart({ events }) {
  const chartData = useMemo(() => {
    if (!events || events.length === 0) return []

    // Group events by date
    const byDate = {}
    for (const event of events) {
      const date = event.start.split('T')[0]
      if (!byDate[date]) {
        byDate[date] = { date, count: 0, totalMinutes: 0 }
      }
      byDate[date].count += 1
      byDate[date].totalMinutes += Math.round(event.duration_seconds / 60)
    }

    return Object.values(byDate).sort((a, b) => a.date.localeCompare(b.date))
  }, [events])

  if (chartData.length === 0) {
    return (
      <div style={styles.empty}>
        אין נתונים להצגה בגרף
      </div>
    )
  }

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>אירועים לפי תאריך</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData} margin={{ top: 10, right: 10, left: 10, bottom: 10 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#eee" />
          <XAxis dataKey="date" tick={{ fontSize: 12 }} />
          <YAxis tick={{ fontSize: 12 }} />
          <Tooltip
            formatter={(value, name) => {
              if (name === 'count') return [value, 'אירועים']
              if (name === 'totalMinutes') return [`${value} דקות`, 'זמן במקלט']
              return [value, name]
            }}
            labelFormatter={label => `תאריך: ${label}`}
          />
          <Bar dataKey="count" fill="#1a1a2e" name="count" radius={[4, 4, 0, 0]} />
          <Bar dataKey="totalMinutes" fill="#e94560" name="totalMinutes" radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

const styles = {
  container: {
    background: '#fff',
    borderRadius: 12,
    padding: 20,
    marginBottom: 20,
    boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
  },
  title: {
    marginBottom: 16,
    fontSize: 18,
  },
  empty: {
    background: '#fff',
    borderRadius: 12,
    padding: 40,
    marginBottom: 20,
    textAlign: 'center',
    color: '#999',
    boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
  },
}
