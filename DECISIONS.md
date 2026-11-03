

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

18. Keep component data flow props-only in Phase 4.2
Problem: The initial catalogue components need predictable rendering before routing, API calls, and shared state exist.
Choice: Pass items and event handlers down explicitly through props, with no component fetching or global context.
Why: Props-only presentational components isolate UI from data source changes, make Phase 4.2 testable with hard-coded data, and avoid adding router or state architecture before later tasks require it.

19. Debounce catalogue search by 300 ms
Problem: Every keystroke could create unnecessary API traffic and allow responses to race.
Choice: Debounce the catalogue search for 300 ms before requesting gear.
Why: 300 ms balances responsiveness with a low request rate, preserving a useful typing experience while reducing server load and overlapping requests.

20. Abort superseded catalogue requests
Problem: A previous slow response could arrive after newer search results.
Choice: Create and abort an AbortController for each search effect, and ignore AbortError without showing an error.
Why: Abort cleanup is scoped to the request lifecycle and reliably cancels superseded work; a manual latest-request counter would duplicate this protection and is unnecessary when the API and browser honor AbortController.

24. Keep item validation in one testable function
Problem: The staff form must keep its submit action disabled and show field-specific errors without validation rules drifting.
Choice: Compute all item field errors through validateItem(form) and derive submit validity from that result.
Why: One pure validation function gives the UI and tests one source of truth and keeps server submission logic separate from input validation.

25. Restore catalogue filters through router state
Problem: Item details navigation must return to a catalogue preserving its search text, category, and sort.
Choice: Pass the catalogue location search string in GearCard Link state and use it for the Back to results URL, with the plain catalogue route as a fallback.
Why: Router state keeps the previous catalogue query together with navigation without duplicating it in application-wide state.

26. Share customer and basket state through context
Problem: The selected customer and basket are needed across navigation, cards, rentals, and checkout, making prop threading brittle.
Choice: Use CustomerContext for customer identity and BasketContext backed by useReducer for basket state.
Why: Context gives route-level consumers direct access to shared state while presentational components retain props for their local data and actions.

27. Enforce the basket limit in React and Python
Problem: A client-side limit improves immediate feedback, but it cannot protect server state when clients bypass the UI or request concurrently.
Choice: Keep the React basket limit from the selected customer's max_items and retain the GearShare server limit as authoritative.
Why: React prevents predictable UX friction, while the server remains the final security and integrity boundary for rentals.

21. Map domain exceptions to HTTP statuses
Problem: Rule failures need stable HTTP semantics without duplicating rules or messages in the API.
Choice: Use 404 for missing customers and items, 422 for invalid SKU input, and 409 for item/rental rule conflicts.
Why: Missing resources are not found, malformed SKU input is unprocessable, and active rule conflicts represent a 409 state conflict; exception handlers preserve the single source of console/domain messages.

22. Restrict CORS to Vite development origins
Problem: Browser requests from the React development server need access while other origins should not.
Choice: Allow only http://localhost:5173 and http://127.0.0.1:5173, with credentials enabled.
Why: These are the two Vite loopback origins specified by the project and avoid opening the API to arbitrary web origins.

23. Read API TODAY in one application-level function
Problem: Date-dependent GearShare operations need a consistent date without reading the clock inside domain methods.
Choice: Read os.environ["TODAY"] in api/main.py and use the real date when it is absent.
Why: This follows the console entry point convention, keeps TODAY at the process boundary, and passes the same date into all service operations.