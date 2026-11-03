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
