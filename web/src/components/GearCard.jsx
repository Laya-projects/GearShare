import AvailabilityBadge from './AvailabilityBadge'
import { Link } from 'react-router-dom'
import { useCustomer } from '../context/CustomerContext'
import { useBasket } from '../context/BasketContext'
import { joinWaitingList } from '../api/client'

export default function GearCard({ item, onAction, catalogueSearch = '', style }) {
  const isDisplay = item.item_type === 'Display'
  const { selectedCustomer } = useCustomer()
  const basket = useBasket()
  const full = selectedCustomer && basket.items.length >= selectedCustomer.max_items

  return (
    <li style={style} className="gear-card card-enter flex flex-col rounded-lg border bg-[var(--color-surface)] p-5 shadow-sm">
      <article>
        <h2 className="gear-card-title text-xl font-semibold text-[var(--color-text)]">
          <Link
            to={`/gear/${item.sku}`}
            state={{ catalogueSearch }}
            className="text-[var(--color-text)] hover:text-[var(--color-soft-pink)] hover:underline"
          >
            {item.name}
          </Link>
        </h2>
        <p className="mt-2 text-sm text-[var(--color-muted)]">{item.tags.join(', ')}</p>
        <p className="mt-1 text-sm text-[var(--color-muted)]">{item.category}</p>
        <div className="mt-4">
          <AvailabilityBadge
            available={item.available}
            total={item.total}
            itemType={item.item_type}
          />
        </div>
        {!isDisplay && (
          <>
            <button
              type="button"
              onClick={async () => {
                if (item.available > 0) {
                  basket.add(item)
                  return
                }
                if (!selectedCustomer) return
                await joinWaitingList(selectedCustomer.customer_id, item.sku)
              }}
              disabled={item.available > 0 && full}
              className="mt-5 w-full rounded-md bg-[var(--color-primary)] px-4 py-2 font-medium text-[var(--color-background)] hover:bg-[var(--color-primary-hover)]"
            >
              {item.available > 0 ? 'Add to basket' : 'Join waiting list'}
            </button>
            {item.available > 0 && (!selectedCustomer || basket.message) && (
              <p role={basket.message ? 'alert' : undefined} className="mt-2 text-sm text-[var(--color-error)]">
                {!selectedCustomer ? 'Pick a customer first.' : basket.message}
              </p>
            )}
          </>
        )}
      </article>
    </li>
  )
}
