import { useEffect, useState } from 'react'
import { getOverdue } from '../api/client'
import ErrorMessage from '../components/ErrorMessage'
import LoadingMessage from '../components/LoadingMessage'

export default function OverduePage() {
  const [data, setData] = useState(null)
  const [status, setStatus] = useState('loading')
  const [error, setError] = useState(null)
  const [retry, setRetry] = useState(0)

  useEffect(() => {
    const controller = new AbortController()
    setStatus('loading')
    setError(null)
    getOverdue(controller.signal)
      .then((result) => {
        setData(result)
        setStatus(result.rows.length ? 'success' : 'empty')
      })
      .catch((requestError) => {
        if (requestError.name === 'AbortError') return
        setError(requestError)
        setStatus('error')
      })
    return () => controller.abort()
  }, [retry])

  return (
    <div>
      <h1 className="text-3xl font-bold text-[var(--color-text)]">
        Overdue rentals as of {data?.as_of || '2026-11-03'}
      </h1>
      {status === 'loading' && <LoadingMessage message="Loading overdue rentals..." />}
      {status === 'error' && (
        <ErrorMessage
          message={error?.message || "Can't reach the rental server."}
          onRetry={() => setRetry((value) => value + 1)}
        />
      )}
      {status === 'empty' && <p role="status" className="mt-4 text-[var(--color-muted)]">No overdue rentals.</p>}
      {status === 'success' && (
        <>
          <div className="mt-5 max-w-full overflow-x-auto">
            <table className="min-w-[720px] w-full text-left">
              <thead>
                <tr>
                  <th className="p-2">Rental</th>
                  <th className="p-2">Customer</th>
                  <th className="p-2">Item</th>
                  <th className="p-2">Due</th>
                  <th className="p-2">Days late</th>
                  <th className="p-2">Fine so far</th>
                </tr>
              </thead>
              <tbody>
                {data.rows.map((row) => (
                  <tr key={row.rental_id} className="border-l-4 border-[var(--color-primary)] bg-[color-mix(in_srgb,var(--color-primary)_12%,var(--color-surface))]">
                    <td className="p-2">{row.rental_id}</td>
                    <td className="p-2">{row.customer}</td>
                    <td className="p-2">{row.item}</td>
                    <td className="p-2">{row.due_date}</td>
                    <td className="p-2">{row.days_late} days late</td>
                    <td className="p-2">₹{row.fine_so_far}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="mt-4">Total overdue: {data.total_overdue}   Fines so far: ₹{data.total_fines}</p>
        </>
      )}
    </div>
  )
}
