const BASE_URL = 'https://missile-alert-stats-1.onrender.com/api'

export async function fetchAreas() {
  const res = await fetch(`${BASE_URL}/areas`)
  if (!res.ok) throw new Error('Failed to fetch areas')
  const data = await res.json()
  return data.areas
}

export async function fetchStats({ area, range, from, to }) {
  const params = new URLSearchParams({ area, range })
  if (range === 'custom' && from) params.set('from', from)
  if (range === 'custom' && to) params.set('to', to)

  const res = await fetch(`${BASE_URL}/stats?${params}`)
  if (!res.ok) throw new Error('Failed to fetch stats')
  return res.json()
}
