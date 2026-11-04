import { useEffect, useState } from 'react'
import { useLocation, useSearchParams } from 'react-router-dom'
import { getGear } from '../api/client'
import GearList from '../components/GearList'
import LoadingMessage from '../components/LoadingMessage'
import ErrorMessage from '../components/ErrorMessage'
import EmptyMessage from '../components/EmptyMessage'
import useDebouncedValue from '../hooks/useDebouncedValue'
import { getCategories } from '../api/client'

export default function CataloguePage() {
  const location = useLocation()
  const [searchParams, setSearchParams] = useSearchParams()
  const [q, setQ] = useState(searchParams.get('q') || '')
  const category = searchParams.get('category') || 'All'
  const sort = searchParams.get('sort') || 'name'
  const debouncedQ = useDebouncedValue(q, 300)
  const [items, setItems] = useState([])
  const [status, setStatus] = useState('loading')
  const [error, setError] = useState(null)
  const [retryVersion, setRetryVersion] = useState(0)
  const [categories, setCategories] = useState(['All'])

  useEffect(() => {
    setQ(searchParams.get('q') || '')
  }, [searchParams])

  useEffect(() => {
    const controller = new AbortController()
    getCategories(controller.signal)
      .then((rows) => setCategories(['All', ...rows.map((row) => row.name)]))
      .catch((requestError) => {
        if (requestError.name !== 'AbortError') setCategories(['All'])
      })
    return () => controller.abort()
  }, [])

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
      <header className="catalogue-hero mb-6 rounded-lg px-5 py-4 sm:px-7">
        <h1 className="text-3xl font-bold text-[var(--color-text)]">Catalogue</h1>
      </header>
      <div className="mb-4 grid gap-3 md:grid-cols-3">
        <label className="grid min-w-0 gap-1 text-sm font-medium text-[var(--color-text)]">
          Search
          <input
            type="search"
            value={q}
            onChange={handleSearchChange}
            className="min-w-0 rounded-md px-3 py-2"
          />
        </label>
        <label className="grid min-w-0 gap-1 text-sm font-medium text-[var(--color-text)]">
          Category
          <select
            value={category}
            onChange={(event) => updateSearchParam('category', event.target.value)}
            className="min-w-0 rounded-md px-3 py-2"
          >
            {categories.map((option) => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        </label>
        <label className="grid min-w-0 gap-1 text-sm font-medium text-[var(--color-text)]">
          Sort
          <select
            value={sort}
            onChange={(event) => updateSearchParam('sort', event.target.value)}
            className="min-w-0 rounded-md px-3 py-2"
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
          <p className="mb-4 text-sm text-[var(--color-muted)]">
            {resultCount} {resultCount === 1 ? 'result' : 'results'}
          </p>
          <GearList items={items} onAction={() => {}} catalogueSearch={location.search} />
        </>
      )}
    </div>
  )
}
