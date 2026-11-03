const API_URL = import.meta.env.VITE_API_URL

export async function getGear({ q, category, sort }, signal) {
  const params = new URLSearchParams()

  if (q) params.set('q', q)
  if (category && category !== 'All') params.set('category', category)
  if (sort) params.set('sort', sort)

  const response = await fetch(`${API_URL}/gear?${params.toString()}`, { signal })

  if (!response.ok) {
    let body
    try {
      body = await response.json()
    } catch {
      body = { message: 'The rental server returned an invalid response.' }
    }

    const error = new Error(body.message || 'The rental server request failed.')
    error.error = body.error
    error.body = body
    throw error
  }

  return response.json()
}

export async function addGear(item, signal) {
  const response = await fetch(`${API_URL}/gear`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(item),
    signal,
  })

  if (!response.ok) {
    let body
    try {
      body = await response.json()
    } catch {
      body = { message: 'The rental server returned an invalid response.' }
    }

    const error = new Error(body.message || body.detail || 'The rental server request failed.')
    error.error = body.error
    error.body = body
    throw error
  }

  return response.json()
}

export async function getGearItem(sku, signal) {
  const response = await fetch(`${API_URL}/gear/${encodeURIComponent(sku)}`, { signal })

  if (!response.ok) {
    let body
    try {
      body = await response.json()
    } catch {
      body = { message: 'The rental server returned an invalid response.' }
    }

    const error = new Error(body.message || 'The rental server request failed.')
    error.error = body.error
    error.status = response.status
    error.body = body
    throw error
  }

  return response.json()
}

async function requestJson(url, options = {}) {
  const response = await fetch(`${API_URL}${url}`, options)
  if (!response.ok) {
    let body
    try {
      body = await response.json()
    } catch {
      body = { message: 'The rental server returned an invalid response.' }
    }
    const error = new Error(body.message || body.detail || 'The rental server request failed.')
    error.error = body.error
    error.status = response.status
    error.body = body
    throw error
  }
  return response.json()
}

export const getCustomers = (signal) => requestJson('/customers', { signal })
export const postRental = (customer_id, sku, signal) =>
  requestJson('/rentals', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ customer_id, sku }),
    signal,
  })
export const joinWaitingList = (customer_id, sku, signal) =>
  requestJson('/waiting-list', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ customer_id, sku }),
    signal,
  })
export const getCustomerRentals = (customerId, signal) =>
  requestJson(`/customers/${encodeURIComponent(customerId)}/rentals`, { signal })
