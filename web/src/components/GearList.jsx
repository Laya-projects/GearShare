import GearCard from './GearCard'

export default function GearList({ items, onAction, catalogueSearch = '' }) {
  return (
    <ul className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {items.map((item) => (
        // Use the SKU, because array indexes can point to the wrong item after sorting or filtering.
        <GearCard
          key={item.sku}
          item={item}
          onAction={onAction}
          catalogueSearch={catalogueSearch}
        />
      ))}
    </ul>
  )
}
