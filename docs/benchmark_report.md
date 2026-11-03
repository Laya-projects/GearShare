# Phase 2.1 Complexity Audit

| operation | predicted time | predicted space | n=1000 | n=5000 | n=10000 | n=50000 | ratio 1000->10000 | ratio 5000->10000 | observed shape |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| list_items | O(n) | O(n) | 0.003 | 0.017 | 0.081 | 2.001 | 26.97x | 4.87x | O(n log n) |
| search | O(n) | O(k) | 0.159 | 1.032 | 2.666 | 9.596 | 16.79x | 2.58x | O(n) |
| rent | O(n) | O(1) | 4.628 | 19.159 | 39.382 | 224.180 | 8.51x | 2.06x | O(n) |
| return_item | O(n) | O(1) | 3.522 | 15.655 | 40.478 | 222.313 | 11.49x | 2.59x | O(n) |
| overdue_report | O(r log r) | O(r) | 5.551 | 19.777 | 32.055 | 209.460 | 5.77x | 1.62x | O(n) |

## Surprises

### list_items
Sentence 1: TODO.
Sentence 2: TODO.

### search
Sentence 1: TODO.
Sentence 2: TODO.

### rent
Sentence 1: TODO.
Sentence 2: TODO.

### return_item
Sentence 1: TODO.
Sentence 2: TODO.

### overdue_report
Sentence 1: TODO.
Sentence 2: TODO.

