export function waitingListMessage(queue, customerId) {
  if (!customerId) return ''
  if (!queue.length) return ''
  const position = queue.findIndex((entry) => entry.customer_id === customerId)
  if (position >= 0) return `You are #${position + 1} on the waiting list.`
  const waitingCount = queue.length
  return waitingCount === 1
    ? '1 person is waiting.'
    : `${waitingCount} people are waiting.`
}
