import { useEffect, useState } from 'react'
import { getCustomerRentals } from '../api/client'
import { useCustomer } from '../context/CustomerContext'

export default function MyRentalsPage() {
  const { selectedCustomer } = useCustomer()
  const [status, setStatus] = useState('pick')
  const [data, setData] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    if (!selectedCustomer) {
      setStatus('pick')
      setData(null)
      return
    }
    const controller = new AbortController()
    setStatus('loading')
    getCustomerRentals(selectedCustomer.customer_id, controller.signal)
      .then((result) => {
        setData(result)
        setStatus(result.active.length === 0 ? 'empty' : 'success')
      })
      .catch((requestError) => {
        if (requestError.name === 'AbortError') return
        setError(requestError.message)
        setStatus('error')
      })
    return () => controller.abort()
  }, [selectedCustomer])

  return (
    <div>
      <h1 className="text-3xl font-bold text-[var(--color-text)]">My rentals</h1>
      {status === 'pick' && <p className="mt-4">Pick a customer first.</p>}
      {status === 'loading' && <p role="status" aria-live="polite" className="mt-4">Loading rentals...</p>}
      {status === 'error' && <p role="alert" className="mt-4 text-[var(--color-error)]">{error}</p>}
      {(status === 'success' || status === 'empty') && (
        <>
          <p className="mt-4">Active rentals: {data.active.length} of {data.max_items}</p>
          <p>Unpaid fines: ₹{data.unpaid_fines}</p>
          {status === 'empty' && <p className="mt-4">No active rentals.</p>}
          {status === 'success' && (
            <div className="mt-4 max-w-full overflow-x-auto">
              <table className="min-w-[640px] w-full text-left">
                <thead>
                  <tr>
                    <th className="p-2">Rental</th>
                    <th className="p-2">Item</th>
                    <th className="p-2">Due date</th>
                    <th className="p-2">Status</th>
                  </tr>
                </thead>
                <tbody>
                  {data.active.map((rental) => (
                    <tr key={rental.rental_id}>
                      <td className="p-2">{rental.rental_id}</td>
                      <td className="p-2">{rental.item}</td>
                      <td className="p-2">{rental.due_date}</td>
                      <td className="p-2">
                        {rental.days_overdue > 0
                          ? `OVERDUE (${rental.days_overdue} days)`
                          : 'On rental'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </>
      )}
    </div>
  )
}
