import React, { useState, useMemo, useRef, useEffect } from 'react'

export default function AreaSelector({ areas, selected, onChange }) {
  const [search, setSearch] = useState('')
  const [isOpen, setIsOpen] = useState(false)
  const containerRef = useRef(null)

  const filtered = useMemo(() => {
    if (!search) return areas
    return areas.filter(a => a.includes(search))
  }, [areas, search])

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(e) {
      if (containerRef.current && !containerRef.current.contains(e.target)) {
        setIsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  function handleSelect(area) {
    onChange(area)
    setSearch(area)
    setIsOpen(false)
  }

  function handleInputChange(e) {
    setSearch(e.target.value)
    setIsOpen(true)
  }

  function handleFocus() {
    setIsOpen(true)
  }

  return (
    <div style={styles.container} ref={containerRef}>
      <label style={styles.label}>אזור</label>
      <input
        type="text"
        placeholder="חפש אזור..."
        value={search}
        onChange={handleInputChange}
        onFocus={handleFocus}
        style={styles.search}
      />
      {isOpen && filtered.length > 0 && (
        <div style={styles.dropdown}>
          {filtered.slice(0, 50).map(area => (
            <div
              key={area}
              style={{
                ...styles.option,
                backgroundColor: area === selected ? '#e8f0fe' : 'white',
              }}
              onMouseDown={(e) => {
                e.preventDefault()
                handleSelect(area)
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.backgroundColor = '#f0f0f0'
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.backgroundColor = area === selected ? '#e8f0fe' : 'white'
              }}
            >
              {area}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    gap: 6,
    minWidth: 220,
    position: 'relative',
  },
  label: {
    fontWeight: 600,
    fontSize: 14,
  },
  search: {
    padding: '8px 12px',
    borderRadius: 8,
    border: '1px solid #d0d0d0',
    fontSize: 14,
    direction: 'rtl',
  },
  dropdown: {
    position: 'absolute',
    top: '100%',
    left: 0,
    right: 0,
    maxHeight: 250,
    overflowY: 'auto',
    border: '1px solid #d0d0d0',
    borderRadius: 8,
    backgroundColor: 'white',
    zIndex: 1000,
    boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
  },
  option: {
    padding: '8px 12px',
    cursor: 'pointer',
    fontSize: 14,
    direction: 'rtl',
    borderBottom: '1px solid #f0f0f0',
  },
}
