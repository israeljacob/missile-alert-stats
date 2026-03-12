import React from 'react'

function formatDuration(totalSeconds) {
  const hours = Math.floor(totalSeconds / 3600)
  const minutes = Math.floor((totalSeconds % 3600) / 60)
  const seconds = Math.floor(totalSeconds % 60)

  const parts = []
  if (hours > 0) parts.push(`${hours} שעות`)
  if (minutes > 0) parts.push(`${minutes} דקות`)
  if (seconds > 0 || parts.length === 0) parts.push(`${seconds} שניות`)
  return parts.join(' ')
}

export default function StatsDisplay({ stats }) {
  return (
    <div style={styles.container}>
      <div style={styles.card}>
        <div style={styles.cardLabel}>אירועים</div>
        <div style={styles.cardValue}>{stats.events_count}</div>
      </div>
      <div style={styles.card}>
        <div style={styles.cardLabel}>זמן במקלט</div>
        <div style={styles.cardValue}>
          {formatDuration(stats.total_shelter_seconds)}
        </div>
      </div>
    </div>
  )
}

const styles = {
  container: {
    display: 'flex',
    gap: 16,
    marginBottom: 20,
  },
  card: {
    flex: 1,
    background: '#fff',
    borderRadius: 12,
    padding: '20px 24px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.08)',
  },
  cardLabel: {
    fontSize: 14,
    color: '#666',
    marginBottom: 8,
    fontWeight: 500,
  },
  cardValue: {
    fontSize: 28,
    fontWeight: 700,
    color: '#1a1a2e',
  },
}
