# Index report (Phase 3.6)

Database: SQLite. Data: 100,000 generated rentals (fixed seed), plus the starter
items, customers and tiers. Each time is the median of 3 runs, in milliseconds.
The real gearshare.db was never touched.

## 1. Method

1. I timed all 12 queries from `queries.sql` on the big database.
2. I picked the 2 slowest: Q11 (units available per item) and Q5 (items never rented).
3. I ran `EXPLAIN QUERY PLAN` on each, created an index, then ran the plan and
   the timing again.

## 2. Results

| Query | Before ms | After ms | Speed-up |
|---|---:|---:|---:|
| Q11 | 348.353 | 158.542 | 2.2x |
| Q5 | 133.087 | 52.778 | 2.5x |

Index created (see `sql/indexes.sql`):

```sql
CREATE INDEX idx_rentals_sku ON rentals(sku);
```

## 3. Query plans

| Query | Plan before | Plan after |
|---|---|---|
| Q11 | SCAN i USING INDEX sqlite_autoindex_items_1 / SEARCH r USING AUTOMATIC COVERING INDEX (sku=?) LEFT-JOIN / USE TEMP B-TREE FOR GROUP BY / USE TEMP B-TREE FOR ORDER BY | SCAN i USING INDEX sqlite_autoindex_items_1 / SEARCH r USING INDEX idx_rentals_sku (sku=?) LEFT-JOIN / USE TEMP B-TREE FOR GROUP BY / USE TEMP B-TREE FOR ORDER BY |
| Q5 | SCAN i / SEARCH r USING AUTOMATIC COVERING INDEX (sku=?) LEFT-JOIN / USE TEMP B-TREE FOR ORDER BY | SCAN i / SEARCH r USING INDEX idx_rentals_sku (sku=?) LEFT-JOIN / USE TEMP B-TREE FOR ORDER BY |

## 4. What the plans show (the surprise)

I expected the "before" plan to scan the whole rentals table. It did not.
`rentals.sku` had no index, so SQLite built a temporary "automatic" index on
`sku` while running the query, used it, and threw it away. It did this on every
execution. The cost of building an index over 100,000 rows is paid again each time.

My permanent index `idx_rentals_sku` removes that rebuild. The join is still a
`SEARCH` in both plans, but now it uses a