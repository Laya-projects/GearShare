export default function LoadingMessage({ message = 'Loading catalogue...' }) {
  return (
    <div role="status" aria-live="polite" className="py-4 text-[var(--color-muted)]">
      <p className="mb-4">{message}</p>
      <ul className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3" aria-hidden="true">
        {[0, 1, 2].map((index) => (
          <li key={index} className="skeleton h-48 rounded-lg border border-[var(--color-border)]" />
        ))}
      </ul>
    </div>
  )
}
