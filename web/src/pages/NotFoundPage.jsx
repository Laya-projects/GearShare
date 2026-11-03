import { Link } from 'react-router-dom'

export default function NotFoundPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold text-slate-900">Page not found</h1>
      <Link to="/" className="mt-4 inline-block text-blue-700 hover:underline">
        Back to catalogue
      </Link>
    </div>
  )
}
