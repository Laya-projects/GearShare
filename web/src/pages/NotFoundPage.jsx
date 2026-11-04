import { Link } from 'react-router-dom'

export default function NotFoundPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold text-[var(--color-text)]">Page not found</h1>
      <Link to="/" className="mt-4 inline-block text-[var(--color-soft-pink)] hover:underline">
        Back to catalogue
      </Link>
    </div>
  )
}
