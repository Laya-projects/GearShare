import { Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import CataloguePage from './pages/CataloguePage'

function App() {
  return (
    <Layout basketCount={0}>
      <Routes>
        <Route path="/" element={<CataloguePage />} />
      </Routes>
    </Layout>
  )
}

export default App
