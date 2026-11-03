export default function Navbar({ basketCount }) {
  return (
    <nav className="border-b border-slate-200 bg-white" aria-label="Primary navigation">
      <div className="mx-auto flex max-w-6xl flex-wrap items-center gap-4 px-4 py-4 sm:px-6">
        <a href="#" className="text-lg font-bold text-slate-900">
          GearShare Mini
        </a>
        <div className="ml-auto flex flex-wrap gap-4 text-sm font-medium">
          <a href="#" className="text-slate-700 hover:text-blue-700">Catalogue</a>
          <a href="#" className="text-slate-700 hover:text-blue-700">My rentals</a>
          <a href="#" className="text-slate-700 hover:text-blue-700">
            Basket ({basketCount})
          </a>
        </div>
      </div>
    </nav>
  )
}
