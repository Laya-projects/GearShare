import { useEffect, useState } from 'react'
import { useSearchParams } from 'react-router-dom'
import { getGear } from '../api/client'
import GearList from '../components/GearList'
import LoadingMessage from '../components/LoadingMessage'
import ErrorMessage from '../components/ErrorMessage'
import EmptyMessage from '../components/EmptyMessage'
import useDebouncedValue from '../hooks/useDebouncedValue'

const categories = [
  'All',
  'Cameras',
  'Lenses',
  'Drones',
  'Tripods',
  'Audio',
  'Showcase',
  'Accessories',
]

export default function CataloguePage() {
  const [searchParams, setSearchParams] = useSearchParams()
  const [q, setQ] = useState(searchParams.get('q') || '')
  const category = searchParams.get('category') || 'All'
  const sort = searchParams.get('sort') || 'name'
  const debouncedQ = useDebouncedValue(q, 300)
  const [items, setItems] = useState([])
  const [status, setStatus] = useState('loading')
  const [error, setError] = useState(null)
  const [retryVersion, setRetryVersion] = useState(0)

  useEffect(() => {
    setQ(searchParams.get('q') || '')
  }, [searchParams])

  const updateSearchParam = (key, value) => {
    const nextParams = new URLSearchParams(searchParams)
    if (!value || value === 'All' || (key === 'sort' && value === 'name')) {
      nextParams.delete(key)
    } else {
      nextParams.set(key, value)
    }
    setSearchParams(nextParams)
  }

  useEffect(() => {
    const controller = new AbortController()
    setStatus('loading')
    setError(null)

    getGear({ q: debouncedQ, category, sort }, controller.signal)
      .then((gear) => {
        setItems(gear)
        setStatus(gear.length === 0 ? 'empty' : 'success')
      })
      .catch((requestError) => {
        if (requestError.name === 'AbortError') return

        setError(requestError)
        setStatus('error')
      })

    // Aborting the previous request in cleanup prevents its slow response from
    // overwriting the newer catalogue result.
    return () => controller.abort()
  }, [debouncedQ, category, sort, retryVersion])

  const handleSearchChange = (event) => {
    const value = event.target.value
    setQ(value)
    const nextParams = new URLSearchParams(searchParams)
    if (value) nextParams.set('q', value)
    else nextParams.delete('q')
    setSearchParams(nextParams)
  }

  const resultCount = items.length
  return (
    <div>
      <h1 className="mb-6 text-3xl font-bold text-slate-900">Catalogue</h1>
      <div className="mb-4 grid gap-3 md:grid-cols-3">
        <label className="grid gap-1 text-sm font-medium text-slate-700">
          Search
          <input
            type="search"
            value={q}
            onChange={handleSearchChange}
            className="rounded-md border border-slate-300 px-3 py-2"
          />
        </label>
        <label className="grid gap-1 text-sm font-medium text-slate-700">
          Category
          <select
            value={category}
            onChange={(event) => updateSearchParam('category', event.target.value)}
            className="rounded-md border border-slate-300 px-3 py-2"
          >
            {categories.map((option) => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        </label>
        <label className="grid gap-1 text-sm font-medium text-slate-700">
          Sort
          <select
            value={sort}
            onChange={(event) => updateSearchParam('sort', event.target.value)}
            className="rounded-md border border-slate-300 px-3 py-2"
          >
            <option value="name">Name</option>
            <option value="weight">Weight</option>
            <option value="category">Category</option>
          </select>
        </label>
      </div>

      {status === 'loading' && <LoadingMessage />}
      {status === 'error' && (
        <ErrorMessage
          message={
            error?.error || error?.body
              ? error.message
              : "Can't reach the rental server."
          }
          onRetry={() => setRetryVersion((version) => version + 1)}
        />
      )}
      {status === 'empty' && <EmptyMessage query={debouncedQ} />}
      {status === 'success' && (
        <>
          <p className="mb-4 text-sm text-slate-600">
            {resultCount} {resultCount === 1 ? 'result' : 'results'}
          </p>
          <GearList items={items} onAction={() => {}} />
        </>
      )}
    </div>
  )
}
