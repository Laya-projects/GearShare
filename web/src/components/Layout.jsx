import Navbar from './Navbar'

export default function Layout({ children, basketCount = 0 }) {
  return (
    <>
      <Navbar basketCount={basketCount} />
      <main className="mx-auto min-h-screen w-full max-w-6xl px-4 py-6 sm:px-6">
        {children}
      </main>
    </>
  )
}
