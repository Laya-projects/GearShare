import { useState } from 'react'
import { postRental } from '../api/client'
import { useBasket } from '../context/BasketContext'
import { useCustomer } from '../context/CustomerContext'

export default function BasketPage() {
  const basket = useBasket()
  const { selectedCustomer } = useCustomer()
  const [renting, setRenting] = useState(false)
  const [messages, setMessages] = useState({})

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
        basket.dispatch({ type: 'REMOVE', sku: item.sku })
      } catch (error) {
        setMessages((current) => ({ ...current, [item.sku]: error.message }))
      }
    }
    setRenting(false)
  }

  return (
    <div>
      <h1 className="text-3xl font-bold text-slate-900">Rental basket</h1>
      {basket.items.length === 0 && <p className="mt-4">Your rental basket is empty.</p>}
      <ul className="mt-4 space-y-3">
        {basket.items.map((item) => (
          <li key={item.sku} className="rounded-md border border-slate-200 p-4">
            <div className="flex items-center justify-between gap-3">
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
              <p className={`mt-2 ${messages[item.sku].startsWith('Rented ') ? 'text-green-700' : 'text-red-700'}`}>
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
            className="rounded-md bg-blue-700 px-4 py-2 text-white disabled:bg-slate-300"
          >
            {renting ? 'Renting...' : 'Rent'}
          </button>
          <button
            type="button"
            disabled={renting}
            onClick={() => basket.dispatch({ type: 'CLEAR' })}
            className="rounded-md border border-slate-300 px-4 py-2"
          >
            Clear
          </button>
        </div>
      )}
    </div>
  )
}
