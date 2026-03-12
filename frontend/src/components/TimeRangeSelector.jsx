import React from 'react'

const RANGES = [
  { value: '1d', label: 'יום' },
  { value: '1w', label: 'שבוע' },
  { value: 'custom', label: 'מותאם' },
]

export default function TimeRangeSelector({
  range,
  onRangeChange,
  fromDate,
  toDate,
  onFromChange,
  onToChange,
}) {
  return (
    <div style={styles.container}>
      <label style={styles.label}>טווח זמן</label>
      <div style={styles.buttons}>
        {RANGES.map(r => (
          <button
            key={r.value}
            onClick={() => onRangeChange(r.value)}
            style={{
              ...styles.button,
              ...(range === r.value ? styles.active : {}),
            }}
          >
            {r.label}
          </button>
        ))}
      </div>
      {range === 'custom' && (
        <div style={styles.dates}>
          <div style={styles.dateField}>
            <label style={styles.dateLabel}>מתאריך</label>
            <input
              type="date"
              value={fromDate}
              min="2025-06-01"
              max={toDate}
              onChange={e => onFromChange(e.target.value)}
              style={styles.dateInput}
            />
          </div>
          <div style={styles.dateField}>
            <label style={styles.dateLabel}>עד תאריך</label>
            <input
              type="date"
              value={toDate}
              min={fromDate}
              max={new Date().toISOString().split('T')[0]}
              onChange={e => onToChange(e.target.value)}
              style={styles.dateInput}
            />
          </div>
        </div>
      )}
    </div>
  )
}

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    gap: 8,
  },
  label: {
    fontWeight: 600,
    fontSize: 14,
  },
  buttons: {
    display: 'flex',
    gap: 0,
    borderRadius: 8,
    overflow: 'hidden',
    border: '1px solid #1a1a2e',
  },
  button: {
    padding: '8px 20px',
    border: 'none',
    background: '#fff',
    cursor: 'pointer',
    fontSize: 14,
    fontWeight: 500,
    color: '#1a1a2e',
    transition: 'all 0.15s',
  },
  active: {
    background: '#1a1a2e',
    color: '#fff',
  },
  dates: {
    display: 'flex',
    gap: 12,
  },
  dateField: {
    display: 'flex',
    flexDirection: 'column',
    gap: 4,
  },
  dateLabel: {
    fontSize: 12,
    color: '#666',
  },
  dateInput: {
    padding: '6px 10px',
    borderRadius: 6,
    border: '1px solid #d0d0d0',
    fontSize: 14,
  },
}
