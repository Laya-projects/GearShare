export function basketReducer(state, action) {
  switch (action.type) {
    case 'ADD': {
      const { item, customer } = action
      if (!customer) {
        return { ...state, message: 'Pick a customer first.' }
      }
      if (state.items.some((basketItem) => basketItem.sku === item.sku)) {
        return { ...state, message: 'Item is already in the basket.' }
      }
      if (state.items.length >= customer.max_items) {
        return {
          ...state,
          message: `Basket full: ${customer.membership_type} members can rent ${customer.max_items} items.`,
        }
      }
      return {
        items: [...state.items, item],
        message: '',
      }
    }
    case 'REMOVE':
      return {
        ...state,
        items: state.items.filter((item) => item.sku !== action.sku),
      }
    case 'CLEAR':
      return { items: [], message: '' }
    default:
      return state
  }
}
