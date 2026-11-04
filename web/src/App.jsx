import { Route, Routes } from 'react-router-dom'
import Layout from './components/Layout'
import CataloguePage from './pages/CataloguePage'
import AddItemPage from './pages/AddItemPage'
import AddCustomerPage from './pages/AddCustomerPage'
import OverduePage from './pages/OverduePage'
import ItemDetailsPage from './pages/ItemDetailsPage'
import MyRentalsPage from './pages/MyRentalsPage'
import BasketPage from './pages/BasketPage'
import NotFoundPage from './pages/NotFoundPage'

function App() {
  return (
    <Layout basketCount={0}>
      <Routes>
        <Route path="/" element={<CataloguePage />} />
        <Route path="/gear/:sku" element={<ItemDetailsPage />} />
        <Route path="/me" element={<MyRentalsPage />} />
        <Route path="/basket" element={<BasketPage />} />
        <Route path="/admin/add" element={<AddItemPage />} />
        <Route path="/admin/customers/add" element={<AddCustomerPage />} />
        <Route path="/admin/overdue" element={<OverduePage />} />
        <Route path="*" element={<NotFoundPage />} />
      </Routes>
    </Layout>
  )
}

export default App
