import { createContext, useContext, useEffect, useState } from 'react'
import { getCustomers } from '../api/client'

const CustomerContext = createContext(null)

export function CustomerProvider({ children }) {
  const [customers, setCustomers] = useState([])
  const [selectedCustomer, setSelectedCustomer] = useState(null)
  const [loading, setLoading] = useState(true)

  const refreshCustomers = async () => {
    const customerList = await getCustomers()
    setCustomers(customerList)
    return customerList
  }

  useEffect(() => {
    let storedId = ''
    try {
      storedId = window.localStorage.getItem('gearshare.customerId') || ''
    } catch {
      storedId = ''
    }

    getCustomers()
      .then((customerList) => {
        setCustomers(customerList)
        const stored = customerList.find((customer) => customer.customer_id === storedId)
        if (stored) setSelectedCustomer(stored)
      })
      .finally(() => setLoading(false))
  }, [])

  const selectCustomer = (customer) => {
    setSelectedCustomer(customer)
    try {
      if (customer) window.localStorage.setItem('gearshare.customerId', customer.customer_id)
      else window.localStorage.removeItem('gearshare.customerId')
    } catch {
      // Storage can be disabled; customer selection still works in memory.
    }
  }

  return (
    <CustomerContext.Provider
      value={{ customers, selectedCustomer, selectCustomer, loading, refreshCustomers }}
    >
      {children}
    </CustomerContext.Provider>
  )
}

export function useCustomer() {
  return useContext(CustomerContext)
}
