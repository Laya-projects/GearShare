import { Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import CataloguePage from './pages/CataloguePage'
import AddItemPage from './pages/AddItemPage'

function App() {
  return (
    <Layout basketCount={0}>
      <Routes>
        <Route path="/" element={<CataloguePage />} />
        <Route path="/admin/add" element={<AddItemPage />} />
      </Routes>
    </Layout>
  )
}

export default App
