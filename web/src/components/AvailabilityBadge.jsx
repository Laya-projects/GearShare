export default function AvailabilityBadge({ available, total, itemType }) {
  if (itemType === 'Display') {
    return (
      <span className="inline-flex rounded-full bg-slate-100 px-3 py-1 text-sm font-medium text-slate-700">
        Display only
      </span>
    )
  }

  const availableClass = available > 0
    ? 'bg-green-100 text-green-800'
    : 'bg-red-100 text-red-800'

  return (
    <span className={`inline-flex rounded-full px-3 py-1 text-sm font-medium ${availableClass}`}>
      {available} of {total} available
    </span>
  )
}
