import Layout from './components/Layout'
import GearList from './components/GearList'
import { sampleGear } from './data/sampleGear'

function App() {
  const handleAction = (item) => {
    console.log(item)
  }

  return (
    <Layout basketCount={0}>
      <h1 className="mb-6 text-3xl font-bold text-slate-900">Catalogue</h1>
      <GearList items={sampleGear} onAction={handleAction} />
    </Layout>
  )
}

export default App
