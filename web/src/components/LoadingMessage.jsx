export default function LoadingMessage({ message = 'Loading catalogue...' }) {
  return (
    <div role="status" aria-live="polite" className="py-4 text-slate-600">
      {message}
    </div>
  )
}
