export default function EmptyMessage({ query }) {
  return (
    <p className="py-4 text-slate-600">
      No items match '{query}'. Try a different word.
    </p>
  )
}
