

## 1. Model membership policies as polymorphic `Customer` subclasses
- **Problem:** Limits, rental periods, and late fees differ by membership and must apply consistently without service-layer branching.
- **Choice:** `Basic`, `Plus`, and `Pro` as subclasses of an abstract `Customer`.
- **Why:** Policy values live with the behavior, callers use one interface, and tier-based conditionals disappear.

## 2. Represent item-specific rental behavior with `GearItem` subclasses
- **Problem:** Equipment uses tier periods, accessories always use two days, and display items cannot be rented.
- **Choice:** `Equipment`, `Accessory`, and `DisplayItem` as subclasses of `GearItem`.
- **Why:** Type-specific behavior stays in the item hierarchy, and `GearShare` simply asks each item for its rentable and period behavior.

## 3. Use `GearShare` as the single service layer
- **Problem:** Domain classes need shared collections and a fixed order of rule checks.
- **Choice:** `GearShare` owns the collections and orchestrates all operations.
- **Why:** One place handles loading, rule order, waiting lists, reports, exceptions, and interactions between customers, items, and rentals.

## 4. Enforce validation inside domain objects
- **Problem:** Invalid SKUs, names, units, and emails could create inconsistent objects.
- **Choice:** Validated properties and constructor setters in `GearItem` and `Customer`.
- **Why:** Objects are protected no matter how they are created or loaded (CSV, service, tests).

## 5. Derive availability from open rentals
- **Problem:** In-memory availability must match starter rentals after loading and stay consistent after returns.
- **Choice:** Available units = total units minus rentals with no return date.
- **Why:** A single source of truth that rebuilds correctly from CSV data and cannot drift.

## 6. Use seeded, repeatable benchmark data
- **Problem:** Complexity measurements must not change between runs.
- **Choice:** A fixed random seed in the item generator, measured against fresh synthetic services.
- **Why:** Reproducible data isolates algorithmic scaling from random catalogue changes.

## 7. Return `(index, comparisons)` from `binary_search`
- **Problem:** Binary search must give both the search result and the comparison count needed for the sample output.
- **Choice:** Return the index and the count together as a tuple.
- **Why:** Keeps the API small while making the exact number of midpoint checks observable and testable.

## 8. Track imported SKUs in a SKU-to-name dictionary
- **Problem:** Repeated imports may encounter the same SKU on multiple lines.
- **Choice:** A dictionary mapping each encountered SKU to the original item name.
- **Why:** O(1) duplicate lookup, and the stored name lets the importer report exactly which earlier item a duplicate conflicts with.

## 9. Store undo records as independent operation snapshots
- **Problem:** Undo must restore both successful rental and return operations exactly.
- **Choice:** Each record holds the action, IDs, SKU, and operation-specific prior state, not a live `Rental` object.
- **Why:** Rent undo removes the correct rental, and return undo restores the return date, fine balance, and waiting-list notification.

## 10. Use one `deque` per SKU for waiting queues
- **Problem:** Customers must be served in strict arrival order when an item becomes available.
- **Choice:** Keep one `collections.deque` per SKU.
- **Why:** `append` and `popleft` give constant-time FIFO, and undo can restore a notified customer to the front with `appendleft`.

## 11. Build a rental-centric flat file for Phase 3.1
- **Problem:** The four starter CSVs must be combined into one rental-level analytical file.
- **Options:** Join at runtime, generate a flat CSV once, or duplicate all source keys in the Python code.
- **Choice:** Generate `gearshare_flat.csv` with joins keyed by customer ID, SKU, and rental ID.
- **Why:** Each rental remains one row, source values stay data-driven, and fine values are optional without invented rows.

## 12. Preserve empty flat-file values
- **Problem:** Open rentals and rentals without fines need an unambiguous representation.
- **Options:** Use null sentinels, text such as None, or empty CSV cells.
- **Choice:** Use empty cells for `return_date` and for fine fields when no fine exists.
- **Why:** Empty cells are consistent with the starter CSV format and keep downstream CSV readers simple.

## 13. Calculate available units
- **Problem:** Availability is needed for listings and rental checks, while rentals can change concurrently.
- **Options:** Store `available_units` or calculate it from `total_units` and open rentals.
- **Choice:** Calculate availability from items and rentals (`total_units` minus rentals with no return date).
- **Why:** A stored counter can drift after returns, failures, or manual updates. If two rent requests arrive together, a stored counter also creates a lost-update or oversubscription risk unless transactions lock and recheck it; calculated availability should likewise be checked inside a transaction and must reserve the final unit atomically.
- **Denormalise differently:** Store and maintain `available_units` only for proven, read-heavy workloads where it is updated through atomic transactions, or cache snapshots after measuring stale-data tolerance.

## 14. Choose SQLite for Phase 3
- **Problem:** The database must support the Python application and be portable enough for development and tests.
- **Options:** Use SQLite or PostgreSQL.
- **Choice:** Use SQLite.
- **Why:** It is built into Python, requires no server setup, is enough for this small dataset, and makes fresh temporary databases practical for tests. PostgreSQL would be preferable for higher concurrency, larger deployments, network access, and stronger multi-user administration.

## 15. Preserve rental history on foreign-key deletion
- **Problem:** Customer, item, rental, and audit records represent durable business history.
- **Options:** Restrict deletion, set references to null, or cascade the dependent rows.
- **Choice:** Use `RESTRICT` for `rentals.customer_id`, `rentals.sku`, fine and audit-log references.
- **Why:** Cascading would silently erase rentals, fines, or audit evidence; restricting is the safer default and requires an explicit retention or archival process before deletion.

## 16. Cascade only non-historical link data
- **Problem:** Junction rows and waiting requests should not remain after their source entities disappear.
- **Options:** Restrict every dependent row, use cascades everywhere, or distinguish transient links from history.
- **Choice:** Use `CASCADE` for `item_tags`, waiting-list entries, and `SET NULL` for optional category parent references; restrict all historical relationships.
- **Why:** Removing an item or tag should clean up its many-to-many links, and removing a customer should clean up their current waiting requests, while rentals and audit records remain protected by restrictions.

## 17. Store fine payment as a boolean integer
- **Problem:** The starter fine CSV stores paid status as `yes` and `no`.
- **Options:** Store the text status, store SQLite integer 1/0, or add a separate payment table.
- **Choice:** Store paid as SQLite `INTEGER` with `CHECK (paid IN (0, 1))`, where `1` means yes and `0` means no.
- **Why:** Integer booleans are idiomatic in SQLite, support efficient filtering, and the check constraint prevents values outside the two valid states.

## 18. Treat display items as available in the query pack
- **Problem:** Q11 must report inventory availability for every item, including Vintage Leica (Showcase).
- **Choice:** Display items always contribute their full `total_units` in Q11, regardless of the open-rental count.
- **Why:** The seeded display item has no rentals and the spec expects 1 available. This matches the rental policy that display items cannot be rented while also preserving useful availability output.

## 19. Commit transaction demo changes atomically
- **Problem:** A rental and its audit row must either both persist or both remain absent.
- **Choice:** Use a transaction, an INSERT with a deliberate audit constraint failure for the rollback case, and a valid audit insert for the commit case.
- **Why:** The rental foreign keys point to durable history, so preserving matching rental and audit records prevents partial service writes.

## 20. Benchmark indexes with temporary data
- **Problem:** Query-plan measurements should not alter GearShare's persistent database.
- **Choice:** Generate fixed-seed benchmark rentals in a temporary SQLite database and add indexes only to that database.
- **Why:** The benchmark is reproducible, isolated from seed data, and can safely support EXPLAIN and timing comparisons.

## 21. Keep wait queues persisted and undo records in memory
- **Problem:** Waiting lists and undo operations need consistent behavior without duplicating business state everywhere.
- **Choice:** Persist waiting-list rows in SQLite ordered by insertion ID, while keeping the undo stack in memory.
- **Why:** Waiting requests survive service restarts and retain FIFO order, whereas undo is a short-lived command history tied to the current service session.

## 22. Separate SQL repositories from GearShare rules
- **Problem:** Domain operations need durable persistence without SQL leaking into business logic.
- **Choice:** Repositories own DB API access and object loading, while GearShare validates rules and coordinates transactions.
- **Why:** Parameterized repository methods keep database details replaceable, and GearShare remains the one place for check order and exception messages.