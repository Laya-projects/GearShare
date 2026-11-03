

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