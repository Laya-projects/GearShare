export default function EmptyMessage({ query }) {
  return (
    <p className="my-4 rounded-lg border border-[var(--color-border)] bg-[var(--color-surface)] px-5 py-8 text-center text-[var(--color-muted)]">
      No items match '{query}'. Try a different word.
    </p>
  )
}
