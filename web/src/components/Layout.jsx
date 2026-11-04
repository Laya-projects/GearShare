import Navbar from './Navbar'

export default function Layout({ children, basketCount = 0 }) {
  return (
    <>
      <a
        href="#main-content"
        className="sr-only fixed left-4 top-3 z-[60] rounded-md bg-[var(--color-primary)] px-4 py-2 text-[var(--color-background)] focus:not-sr-only"
      >
        Skip to main content
      </a>
      <header>
        <Navbar basketCount={basketCount} />
      </header>
      <main id="main-content" className="mx-auto min-h-screen w-full max-w-6xl px-4 py-6 sm:px-6">
        {children}
      </main>
    </>
  )
}
