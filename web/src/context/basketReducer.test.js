import { describe, expect, it } from 'vitest'
import { basketReducer } from './basketReducer'

const customer = (membership_type, max_items) => ({ membership_type, max_items })
const item = (sku) => ({ sku, name: sku })
const initial = { items: [], message: '' }

describe('basketReducer', () => {
  it('adds an item under the limit', () => {
    expect(basketReducer(initial, { type: 'ADD', item: item('1'), customer: customer('Basic', 2) }).items).toEqual([item('1')])
  })

  it.each([
    ['Basic', 2],
    ['Plus', 4],
    ['Pro', 8],
  ])('blocks adding beyond the %s limit', (membership, maxItems) => {
    const state = { items: Array.from({ length: maxItems }, (_, index) => item(String(index))), message: '' }
    const result = basketReducer(state, { type: 'ADD', item: item('extra'), customer: customer(membership, maxItems) })
    expect(result.message).toBe(`Basket full: ${membership} members can rent ${maxItems} items.`)
    expect(result.items).toEqual(state.items)
  })

  it('blocks duplicate SKUs', () => {
    const state = { items: [item('1')], message: '' }
    const result = basketReducer(state, { type: 'ADD', item: item('1'), customer: customer('Basic', 2) })
    expect(result.items).toEqual(state.items)
    expect(result.message).toBe('Item is already in the basket.')
  })

  it('removes an item', () => {
    const state = { items: [item('1'), item('2')], message: '' }
    expect(basketReducer(state, { type: 'REMOVE', sku: '1' }).items).toEqual([item('2')])
  })

  it('clears the basket', () => {
    expect(basketReducer({ items: [item('1')], message: 'x' }, { type: 'CLEAR' })).toEqual(initial)
  })
})
