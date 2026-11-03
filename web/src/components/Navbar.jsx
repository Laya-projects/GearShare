import { NavLink } from 'react-router-dom'
import { useCustomer } from '../context/CustomerContext'
import { useBasket } from '../context/BasketContext'

export default function Navbar({ basketCount }) {
  const { customers, selectedCustomer, selectCustomer } = useCustomer()
  const basket = useBasket()
  const linkClass = ({ isActive }) =>
    isActive
      ? 'text-blue-700 underline underline-offset-4'
      : 'text-slate-700 hover:text-blue-700'

  return (
    <nav className="border-b border-slate-200 bg-white" aria-label="Primary navigation">
      <div className="mx-auto flex max-w-6xl flex-wrap items-center gap-4 px-4 py-4 sm:px-6">
        <NavLink to="/" className="text-lg font-bold text-slate-900">
          GearShare Mini
        </NavLink>
        <div className="ml-auto flex flex-wrap gap-4 text-sm font-medium">
          <NavLink to="/" end className={linkClass}>Catalogue</NavLink>
          <NavLink to="/me" className={linkClass}>My rentals</NavLink>
          <NavLink to="/basket" className={linkClass}>
            Basket ({basket.items.length})
          </NavLink>
          <NavLink to="/admin/add" className={linkClass}>Add item</NavLink>
        </div>
        <label htmlFor="customer-picker" className="text-sm font-medium text-slate-700">
          Customer
          <select
            id="customer-picker"
            value={selectedCustomer?.customer_id || ''}
            onChange={(event) => {
              const customer = customers.find((candidate) => candidate.customer_id === event.target.value)
              selectCustomer(customer || null)
            }}
            className="ml-2 rounded-md border border-slate-300 px-2 py-1"
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
