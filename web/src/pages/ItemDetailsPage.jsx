import { useEffect, useState } from 'react'
import { Link, useLocation, useParams } from 'react-router-dom'
import { getGearItem } from '../api/client'
import AvailabilityBadge from '../components/AvailabilityBadge'
import ErrorMessage from '../components/ErrorMessage'
import LoadingMessage from '../components/LoadingMessage'
import { useCustomer } from '../context/CustomerContext'
import { useBasket } from '../context/BasketContext'
import { joinWaitingList } from '../api/client'

export default function ItemDetailsPage() {
  const { sku } = useParams()
  const location = useLocation()
  const { selectedCustomer } = useCustomer()
  const basket = useBasket()
  const [item, setItem] = useState(null)
  const [status, setStatus] = useState('loading')
  const [error, setError] = useState(null)
  const [retryVersion, setRetryVersion] = useState(0)
  const [actionMessage, setActionMessage] = useState('')

  useEffect(() => {
    const controller = new AbortController()
    setStatus('loading')
    setError(null)

    getGearItem(sku, controller.signal)
      .then((gearItem) => {
        setItem(gearItem)
        setStatus('success')
      })
      .catch((requestError) => {
        if (requestError.name === 'AbortError') return
        setError(requestError)
        setStatus(requestError.status === 404 ? 'not-found' : 'error')
      })

    // Aborting this request prevents a stale item response from replacing newer navigation.
    return () => controller.abort()
  }, [sku, retryVersion])

  const catalogueSearch = location.state?.catalogueSearch || ''
  const full = selectedCustomer && basket.items.length >= selectedCustomer.max_items

  if (status === 'loading') return <LoadingMessage message="Loading item..." />
  if (status === 'not-found') return <ErrorMessage message={error.message} />
  if (status === 'error') {
    return (
      <ErrorMessage
        message={error.error ? error.message : "Can't reach the rental server."}
        onRetry={() => setRetryVersion((version) => version + 1)}
      />
    )
  }

  return (
    <article>
      <Link to={`/${catalogueSearch}`} className="mb-5 inline-block text-blue-700 hover:underline">
        Back to results
      </Link>
      <h1 className="text-3xl font-bold text-slate-900">{item.name}</h1>
      <p className="mt-2 text-slate-600">{item.tags.join(', ')}</p>
      <p className="mt-1 text-slate-600">{item.category}</p>
      <p className="mt-1 text-slate-600">{item.weight_g} g</p>
      <div className="mt-4">
        <AvailabilityBadge
          available={item.available}
          total={item.total}
          itemType={item.item_type}
        />
      </div>
      {item.item_type === 'Display' ? (
        <p className="mt-5 font-medium text-slate-700">
          Display item: view in the shop only.
        </p>
      ) : item.available === 0 ? (
        <button
          type="button"
          onClick={async () => {
            try {
              if (!selectedCustomer) {
                setActionMessage('Pick a customer first.')
                return
              }
              const result = await joinWaitingList(selectedCustomer.customer_id, item.sku)
              setActionMessage(`Waiting list position: ${result.position}.`)
            } catch (requestError) {
              setActionMessage(requestError.message)
            }
          }}
          className="mt-5 rounded-md bg-blue-700 px-4 py-2 text-white"
        >
          Join waiting list
        </button>
      ) : (
        <button
          type="button"
          disabled={full}
          onClick={() => basket.add(item)}
          className="mt-5 rounded-md bg-blue-700 px-4 py-2 text-white disabled:bg-slate-300"
        >
          Add to basket
        </button>
      )}
      {!selectedCustomer && !full && item.available > 0 && (
        <p className="mt-2 text-sm text-red-700">Pick a customer first.</p>
      )}
      {basket.message && <p className="mt-2 text-sm text-red-700">{basket.message}</p>}
      {actionMessage && <p className="mt-2 text-sm">{actionMessage}</p>}
    </article>
  )
}
