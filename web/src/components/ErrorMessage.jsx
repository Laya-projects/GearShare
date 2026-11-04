export default function ErrorMessage({ message, onRetry }) {
  return (
    <div role="alert" className="py-4 text-[var(--color-error)]">
      <p>{message}</p>
      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="mt-3 rounded-md border border-[var(--color-primary)] bg-[var(--color-primary)] px-3 py-2 text-[var(--color-background)]"
        >
          Retry
        </button>
      )}
    </div>
  )
}
