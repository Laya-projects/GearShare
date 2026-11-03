import AvailabilityBadge from './AvailabilityBadge'
import { Link } from 'react-router-dom'

export default function GearCard({ item, onAction, catalogueSearch = '' }) {
  const isDisplay = item.item_type === 'Display'

  return (
    <li className="flex flex-col rounded-lg border border-slate-200 bg-white p-5 shadow-sm">
      <article>
        <h2 className="text-xl font-semibold text-slate-900">
          <Link
            to={`/gear/${item.sku}`}
            state={{ catalogueSearch }}
            className="hover:text-blue-700 hover:underline"
          >
            {item.name}
          </Link>
        </h2>
        <p className="mt-2 text-sm text-slate-600">{item.tags.join(', ')}</p>
        <p className="mt-1 text-sm text-slate-500">{item.category}</p>
        <div className="mt-4">
          <AvailabilityBadge
            available={item.available}
            total={item.total}
            itemType={item.item_type}
          />
        </div>
        {!isDisplay && (
          <button
            type="button"
            onClick={() => onAction(item)}
            className="mt-5 w-full rounded-md bg-blue-700 px-4 py-2 font-medium text-white hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            {item.available > 0 ? 'Add to basket' : 'Join waiting list'}
          </button>
        )}
      </article>
    </li>
  )
}
