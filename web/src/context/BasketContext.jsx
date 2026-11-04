import { createContext, useContext, useEffect, useReducer, useState } from 'react'
import { useCustomer } from './CustomerContext'
import { basketReducer } from './basketReducer'

const BasketContext = createContext(null)

export function BasketProvider({ children }) {
  const { selectedCustomer } = useCustomer()
  const [state, dispatch] = useReducer(basketReducer, { items: [], message: '' })
  const [toast, setToast] = useState('')

  useEffect(() => {
    dispatch({ type: 'CLEAR' })
  }, [selectedCustomer?.customer_id])

  useEffect(() => {
    if (!toast) return undefined
    const timeout = window.setTimeout(() => setToast(''), 4000)
    return () => window.clearTimeout(timeout)
  }, [toast])

  const add = (item) => {
    if (!selectedCustomer) {
      dispatch({ type: 'ADD', item, customer: selectedCustomer })
      return
    }
    if (state.items.some((basketItem) => basketItem.sku === item.sku)) {
      dispatch({ type: 'ADD', item, customer: selectedCustomer })
      return
    }
    if (state.items.length >= selectedCustomer.max_items) {
      dispatch({ type: 'ADD', item, customer: selectedCustomer })
      return
    }
    dispatch({ type: 'ADD', item, customer: selectedCustomer })
    setToast(`${item.name} product added to the basket`)
  }

  return (
    <BasketContext.Provider value={{ ...state, dispatch, add }}>
      {children}
      {toast && (
        <div
          role="status"
          aria-live="polite"
          className="toast-enter fixed right-4 top-20 z-[70] flex max-w-[calc(100vw-2rem)] items-center gap-3 rounded-md border border-[var(--color-primary)] bg-[var(--color-surface)] px-4 py-3 text-[var(--color-text)] shadow-lg"
        >
          <span>{toast}</span>
          <button
            type="button"
            aria-label="Dismiss notification"
            onClick={() => setToast('')}
            className="rounded border border-[var(--color-border)] px-2 py-1"
          >
            Close
          </button>
        </div>
      )}
    </BasketContext.Provider>
  )
}

export function useBasket() {
  return useContext(BasketContext)
}
