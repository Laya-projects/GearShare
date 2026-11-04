export default function AvailabilityBadge({ available, total, itemType }) {
  if (itemType === 'Display') {
    return (
      <span className="inline-flex items-center gap-1 rounded-full border border-[var(--color-primary)] bg-[var(--color-surface)] px-3 py-1 text-sm font-medium text-[var(--color-soft-pink)]">
        ◇ Display only
      </span>
    )
  }

  const availableClass = available > 0
    ? 'border border-[var(--color-success)] bg-[color-mix(in_srgb,var(--color-success)_18%,var(--color-surface))] text-[var(--color-success)]'
    : 'border border-[var(--color-error)] bg-[color-mix(in_srgb,var(--color-error)_18%,var(--color-surface))] text-[var(--color-error)]'

  return (
    <span className={`inline-flex rounded-full px-3 py-1 text-sm font-medium ${availableClass}`}>
      {available > 0 ? `● In stock (${available} of ${total} available)` : `● ${available} of ${total} available`}
    </span>
  )
}
