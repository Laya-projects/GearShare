import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import './index.css'
import App from './App.jsx'
import { CustomerProvider } from './context/CustomerContext'
import { BasketProvider } from './context/BasketContext'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <CustomerProvider>
        <BasketProvider>
          <App />
        </BasketProvider>
      </CustomerProvider>
    </BrowserRouter>
  </StrictMode>,
)
