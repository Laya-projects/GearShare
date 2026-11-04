import { Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { postRental } from '../api/client'
import { useBasket } from '../context/BasketContext'
import { useCustomer } from '../context/CustomerContext'

export default function BasketPage() {
  const basket = useBasket()
  const { selectedCustomer } = useCustomer()
  const [renting, setRenting] = useState(false)
  const [messages, setMessages] = useState({})
  const [toast, setToast] = useState('')

  useEffect(() => {
    if (!toast) return undefined
    const timeout = window.setTimeout(() => setToast(''), 5000)
    return () => window.clearTimeout(timeout)
  }, [toast])

  const rentBasket = async () => {
    if (!selectedCustomer || basket.items.length === 0) return
    setRenting(true)
    for (const item of basket.items) {
      try {
        const result = await postRental(selectedCustomer.customer_id, item.sku)
        setMessages((current) => ({
          ...current,
          [item.sku]: `Rented ${item.name}. Due ${result.due_date}.`,
        }))
        setToast(`Rented ${item.name}. Due ${result.due_date}.`)
        basket.dispatch({ type: 'REMOVE', sku: item.sku })
      } catch (error) {
        setMessages((current) => ({ ...current, [item.sku]: error.message }))
      }
    }
    setRenting(false)
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-[var(--color-text)]">Rental basket</h1>
      {toast && (
        <div role="status" aria-live="polite" className="toast-enter fixed right-4 top-20 z-[70] flex max-w-[calc(100vw-2rem)] items-center gap-3 rounded-md border border-[var(--color-success)] bg-[var(--color-surface)] px-4 py-3 text-[var(--color-text)] shadow-lg">
          <span>{toast}</span>
          <button type="button" onClick={() => setToast('')} aria-label="Dismiss notification" className="rounded border px-2 py-1">Close</button>
        </div>
      )}
      {basket.items.length === 0 && (
        <p className="mt-4">
          Your basket is empty. <Link to="/" className="underline text-[var(--color-soft-pink)]">Return to the catalogue</Link>
        </p>
      )}
      <ul className="mt-4 max-w-full space-y-3">
        {basket.items.map((item) => (
          <li key={item.sku} className="min-w-0 rounded-md border border-[var(--color-border)] p-4">
            <div className="flex flex-col items-start justify-between gap-3 sm:flex-row sm:items-center">
              <span>{item.name}</span>
              <button
                type="button"
                onClick={() => basket.dispatch({ type: 'REMOVE', sku: item.sku })}
                className="rounded border px-3 py-1"
              >
                Remove
              </button>
            </div>
            {messages[item.sku] && (
              <p
                role={messages[item.sku].startsWith('Rented ') ? 'status' : 'alert'}
                className={`mt-2 ${messages[item.sku].startsWith('Rented ') ? 'text-[var(--color-success)]' : 'text-[var(--color-error)]'}`}
              >
                {messages[item.sku]}
              </p>
            )}
          </li>
        ))}
      </ul>
      {basket.items.length > 0 && (
        <div className="mt-5 flex gap-3">
          <button
            type="button"
            disabled={renting || !selectedCustomer}
            onClick={rentBasket}
            className="rounded-md bg-[var(--color-primary)] px-4 py-2 text-[var(--color-background)]"
          >
            {renting ? 'Renting...' : 'Rent'}
          </button>
          <button
            type="button"
            disabled={renting}
            onClick={() => basket.dispatch({ type: 'CLEAR' })}
            className="rounded-md border border-[var(--color-border)] px-4 py-2"
          >
            Clear
          </button>
        </div>
      )}
    </div>
  )
}
