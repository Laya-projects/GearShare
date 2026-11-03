

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

11. Choose SQLite for the database
Problem: The database must support the Python application and be portable enough for development and tests.
Choice: Use SQLite.
Why: It is built into Python, needs no server setup, is enough for this small dataset, and makes fresh temporary test databases practical. PostgreSQL would be preferable for higher concurrency, larger deployments, network access, and stronger multi-user administration.

12. Calculate available units instead of storing them
Problem: Availability is needed for listings and rental checks, while rentals can change concurrently.
Choice: Available units = total_units minus rentals with no return date.
Why: A stored counter can drift after returns, failures, or manual updates and risks lost updates under concurrent requests. The calculation should be checked inside a transaction and reserve the final unit atomically.
Denormalise later only if needed: Store available_units only for proven read-heavy workloads, updated through atomic transactions.

13. Use RESTRICT to preserve rental history
Problem: Customer, item, rental, and audit records represent durable business history.
Choice: RESTRICT on rentals.customer_id, rentals.sku, and fine and audit-log references.
Why: Cascading would silently erase rentals, fines, or audit evidence. Restricting is the safer default and forces an explicit retention or archival process before deletion.

14. Commit rental and audit writes atomically
Problem: A rental and its audit row must either both persist or both remain absent.
Choice: Wrap both inserts in one transaction, with a deliberate audit constraint failure to demonstrate rollback and a valid insert to demonstrate commit.
Why: Preserving matching rental and audit records prevents partial service writes.

15. Separate SQL repositories from GearShare rules
Problem: Domain operations need durable persistence without SQL leaking into business logic.
Choice: Repositories own DB API access and object loading, while GearShare validates rules and coordinates transactions.
Why: Parameterized repository methods keep database details replaceable, and GearShare remains the one place for check order and exception messages.

16. Use Tailwind CSS for Phase 4 styling
Problem: The React interface needs a responsive, consistent styling approach across several screens.
Choice: Tailwind CSS.
Why: Tailwind provides utility-first styling directly in JSX, responsive variants, and a smaller integration surface than a component library. Material UI would add heavier theme and component conventions for this small project.

17. Keep catalogue search state in the URL
Problem: Searching, opening an item, and returning to the catalogue must preserve the customer's previous search.
Choice: Store the search text, category, and sort in URL query parameters.
Why: URL state survives route navigation and browser history, so `Back to results` can restore the catalogue without duplicating state in navigation-specific components.