export default function ErrorMessage({ message, onRetry }) {
  return (
    <div role="alert" className="py-4 text-red-700">
      <p>{message}</p>
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="mt-3 rounded-md border border-slate-300 px-3 py-2 text-slate-800"
        >
          Retry
        </button>
      )}
    </div>
  )
}
