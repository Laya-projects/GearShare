# Phase 2.1 Complexity Audit

| operation | predicted time | predicted space | n=1000 | n=5000 | n=10000 | n=50000 | ratio 1000->10000 | ratio 5000->10000 | observed shape |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| list_items | O(n) | O(n) | 0.003 | 0.017 | 0.081 | 2.001 | 26.97x | 4.87x | O(n log n) |
| search | O(n) | O(k) | 0.159 | 1.032 | 2.666 | 9.596 | 16.79x | 2.58x | O(n) |
| rent | O(n) | O(1) | 4.628 | 19.159 | 39.382 | 224.180 | 8.51x | 2.06x | O(n) |
| return_item | O(n) | O(1) | 3.522 | 15.655 | 40.478 | 222.313 | 11.49x | 2.59x | O(n) |
| overdue_report | O(r log r) | O(r) | 5.551 | 19.777 | 32.055 | 209.460 | 5.77x | 1.62x | O(n) |

## Surprises

### list_items (predicted O(n))
I predicted O(n), but the time grew 27x when n grew 10x, and about 25x when n grew 5x (10,000 to 50,000). That is faster growth than linear.
At 0.003 ms the timer noise is large, and at 50,000 items the data no longer fits in the CPU cache. If list_items also formats or sorts each row, that adds more cost. [Verify in code.]

### search (predicted O(n))
I predicted O(n) and saw 16.8x for 10x items, but about 2.6x for 2x items. The shape is linear, with a small constant overhead at small n.
Search checks every item's name and tags, so the work grows with the catalogue. A hash index (task 2.3) could make it faster.

### rent (predicted O(n))
I predicted O(n) and measured 8.5x for 10x items, so it matches. What surprised me is the size: about 4 ms at n=1,000, far more than one lookup should cost.
rent() appears to scan a whole collection (items, rentals or the customer's rentals) instead of using a dict lookup. [Verify the exact line.] Dicts by SKU and customer ID would make it O(1).

### return_item (predicted O(n))
I predicted O(n) and measured 11.5x for 10x items, so it matches. Finding the rental by ID likely scans the rentals list, and rebuilding availability may add more.
A dict keyed by rental ID would reduce this to O(1).

### overdue_report (predicted O(r log r))
I predicted the cost would depend on the number of rentals r, but it grew 5.8x for 10x items, and 6.5x for 5x items. So it grows with n, not with a fixed small r.
In my benchmark data, rentals grow along with items. The report probably also scans every rental, including returned ones, instead of only the open ones. Keeping a separate set of open rentals would fix this.

### Conclusion
rent, return_item and overdue_report all grow linearly with catalogue size, which a hash-based design should avoid. I will rerun this audit after tasks 2.3 and 2.4 (dicts, deque) and compare before and after.