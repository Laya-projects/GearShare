import { NavLink } from 'react-router-dom'

export default function Navbar({ basketCount }) {
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
            Basket ({basketCount})
          </NavLink>
          <NavLink to="/admin/add" className={linkClass}>Add item</NavLink>
        </div>
      </div>
    </nav>
  )
}
