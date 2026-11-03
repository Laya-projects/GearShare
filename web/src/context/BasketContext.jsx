import { createContext, useContext, useEffect, useReducer } from 'react'
import { useCustomer } from './CustomerContext'
import { basketReducer } from './basketReducer'

const BasketContext = createContext(null)

export function BasketProvider({ children }) {
  const { selectedCustomer } = useCustomer()
  const [state, dispatch] = useReducer(basketReducer, { items: [], message: '' })

  useEffect(() => {
    dispatch({ type: 'CLEAR' })
  }, [selectedCustomer?.customer_id])

  const add = (item) => dispatch({
    type: 'ADD',
    item,
    customer: selectedCustomer,
  })

  return (
    <BasketContext.Provider value={{ ...state, dispatch, add }}>
      {children}
    </BasketContext.Provider>
  )
}

export function useBasket() {
  return useContext(BasketContext)
}
