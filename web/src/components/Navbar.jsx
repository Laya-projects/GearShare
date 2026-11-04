import { useState } from 'react'
import { NavLink, useLocation } from 'react-router-dom'
import { useCustomer } from '../context/CustomerContext'
import { useBasket } from '../context/BasketContext'

export default function Navbar({ basketCount }) {
  const { customers, selectedCustomer, selectCustomer } = useCustomer()
  const basket = useBasket()
  const [menuOpen, setMenuOpen] = useState(false)
  const location = useLocation()
  const customerPickerDisabled = location.pathname === '/admin/customers/add'
  const linkClass = ({ isActive }) =>
    isActive
      ? 'text-[var(--color-primary)] underline underline-offset-4 drop-shadow-[0_0_5px_var(--color-primary)]'
      : 'text-[var(--color-muted)] hover:text-[var(--color-soft-pink)]'

  return (
    <nav className="sticky top-0 z-50 border-b-2 border-[var(--color-primary)] bg-[var(--color-background)]" aria-label="Primary navigation">
      <div className="mx-auto flex max-w-6xl flex-wrap items-center gap-4 px-4 py-4 sm:px-6">
        <NavLink to="/" className="brand text-lg font-bold text-[var(--color-text)]">
          GearShare Mini
        </NavLink>
        <button
          type="button"
          className="ml-auto rounded-md border border-[var(--color-border)] px-3 py-2 sm:hidden"
          aria-expanded={menuOpen}
          aria-controls="primary-menu"
          onClick={() => setMenuOpen((open) => !open)}
        >
          {menuOpen ? 'Close menu' : 'Menu'}
        </button>
        <div id="primary-menu" className={`${menuOpen ? 'flex' : 'hidden'} w-full flex-col gap-3 text-sm font-medium sm:ml-auto sm:flex sm:w-auto sm:flex-row sm:flex-wrap sm:items-center sm:gap-4`}>
          <NavLink to="/" end className={linkClass}>Catalogue</NavLink>
          <NavLink to="/me" className={linkClass}>My rentals</NavLink>
          <NavLink to="/basket" className={linkClass}>
            Basket ({basket.items.length})
          </NavLink>
          <NavLink to="/admin/add" className={linkClass}>Add item</NavLink>
          <NavLink to="/admin/customers/add" className={linkClass}>Add customer</NavLink>
          <NavLink to="/admin/overdue" className={linkClass}>Overdue</NavLink>
        </div>
        <label htmlFor="customer-picker" className={`${menuOpen ? 'grid' : 'hidden'} w-full gap-1 text-sm font-medium text-[var(--color-text)] sm:grid sm:w-auto sm:grid-cols-[auto_auto] sm:items-center`}>
          Customer
          <select
            id="customer-picker"
            value={selectedCustomer?.customer_id || ''}
            disabled={customerPickerDisabled}
            onChange={(event) => {
              const customer = customers.find((candidate) => candidate.customer_id === event.target.value)
              selectCustomer(customer || null)
            }}
            className="w-full px-2 py-1 sm:w-auto sm:ml-2"
          >
            <option value="">Select customer</option>
            {customers.map((customer) => (
              <option key={customer.customer_id} value={customer.customer_id}>
                {customer.name}
              </option>
            ))}
          </select>
        </label>
      </div>
    </nav>
  )
}
