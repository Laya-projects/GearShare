import { useEffect, useState } from 'react'
import { getCustomerRentals, returnRental } from '../api/client'
import { useCustomer } from '../context/CustomerContext'

export default function MyRentalsPage() {
  const { selectedCustomer } = useCustomer()
  const [status, setStatus] = useState('pick')
  const [data, setData] = useState(null)
  const [error, setError] = useState('')
  const [returnMessages, setReturnMessages] = useState({})
  const [returning, setReturning] = useState('')

  const loadRentals = (controller) => {
    setStatus('loading')
    return getCustomerRentals(selectedCustomer.customer_id, controller.signal)
      .then((result) => {
        setData(result)
        setStatus(result.active.length === 0 ? 'empty' : 'success')
      })
      .catch((requestError) => {
        if (requestError.name !== 'AbortError') {
          setError(requestError.message)
          setStatus('error')
        }
      })
  }

  useEffect(() => {
    if (!selectedCustomer) {
      setStatus('pick')
      setData(null)
      return
    }
    const controller = new AbortController()
    loadRentals(controller)
    return () => controller.abort()
  }, [selectedCustomer])

  const handleReturn = async (rental) => {
    if (!window.confirm(`Return ${rental.item}?`)) return
    setReturning(rental.rental_id)
    try {
      const result = await returnRental(rental.rental_id)
      const returnText = rental.days_overdue > 0
        ? `Returned ${rental.item}. Late by ${rental.days_overdue} days. Fee: ₹${result.fine}.`
        : `Returned on time. Fee: ₹0.`
      const nextText = result.next_in_waiting_list
        ? ` Next on waiting list: ${result.next_in_waiting_list}.`
        : ''
      setReturnMessages((current) => ({
        ...current,
        [rental.rental_id]: `${returnText}${nextText}`,
      }))
      const controller = new AbortController()
      await loadRentals(controller)
    } catch (requestError) {
      setReturnMessages((current) => ({
        ...current,
        [rental.rental_id]: requestError.message,
      }))
    } finally {
      setReturning('')
    }
  }

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
                    <th className="p-2">Action</th>
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
                      <td className="p-2">
                        <button
                          type="button"
                          disabled={returning === rental.rental_id}
                          onClick={() => handleReturn(rental)}
                          className="rounded-md border border-[var(--color-primary)] px-3 py-1"
                        >
                          {returning === rental.rental_id ? 'Returning...' : 'Return'}
                        </button>
                        {returnMessages[rental.rental_id] && (
                          <p
                            role={returnMessages[rental.rental_id].startsWith('Returned') ? 'status' : 'alert'}
                            className="mt-2 max-w-xs"
                          >
                            {returnMessages[rental.rental_id]}
                          </p>
                        )}
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
