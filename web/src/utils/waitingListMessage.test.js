import { describe, expect, it } from 'vitest'
import { waitingListMessage } from './waitingListMessage'

const queue = [
  { customer_id: 'C003', name: 'Meera Joshi' },
  { customer_id: 'C005', name: 'Pooja Menon' },
  { customer_id: 'C001', name: 'Rohan Das' },
]

describe('waitingListMessage', () => {
  it("reports the selected customer's position", () => {
    expect(waitingListMessage(queue, 'C005')).toBe('You are #2 on the waiting list.')
  })

  it.each([
    [[{ customer_id: 'C003' }], 'C001', '1 person is waiting.'],
    [queue.slice(0, 2), 'C001', '2 people are waiting.'],
  ])('reports other waiting customers', (otherQueue, customerId, expected) => {
    expect(waitingListMessage(otherQueue, customerId)).toBe(expected)
  })

  it('returns nothing for an empty queue or no selected customer', () => {
    expect(waitingListMessage([], 'C001')).toBe('')
    expect(waitingListMessage(queue, null)).toBe('')
  })
})
