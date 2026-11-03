## Decision 1: Where to model membership policies

- **Problem:** Membership-specific limits, rental periods, and late fees must be applied consistently without service-layer branching.
- **Options:** Store membership values as strings and fields, use a policy dictionary keyed by membership name, or model membership as polymorphic customer subclasses.
- **Choice:** Model Basic, Plus, and Pro as subclasses of an abstract `Customer`.
- **Why:** Subclasses keep policy values with the membership behavior, allow the same methods to be called throughout the service, and eliminate membership-based conditional logic.

## Decision 2: How to represent item-specific rental behavior

- **Problem:** Equipment uses tier periods, accessories always use two days, and display items cannot be rented.
- **Options:** Branch on a category string in `GearShare`, store period behavior in data fields, or use concrete item subclasses derived from `GearItem`.
- **Choice:** Use polymorphic `Equipment`, `Accessory`, and `DisplayItem` subclasses of `GearItem`.
- **Why:** This keeps type-specific behavior in the item hierarchy and lets `GearShare` ask each item for its rentable and period behavior.

## Decision 3: How the service should coordinate the domain

- **Problem:** Domain classes need to share consistent collections and enforce a fixed order of checks.
- **Options:** Put orchestration in each domain class, expose only loose collections, or use a single `GearShare` service.
- **Choice:** Use `GearShare` as the service layer that owns collections and orchestrates operations.
- **Why:** A single service provides one place for loading, rule order, waiting lists, reports, exceptions, and interactions between customers, items, and rentals.

## Decision 4: Validation location for core domain objects

- **Problem:** Invalid SKUs, names, units, and email addresses could create inconsistent objects.
- **Options:** Validate only while loading CSV data, validate through service methods, or enforce invariants in domain properties and constructors.
- **Choice:** Use validated properties and constructor setters in `GearItem` and `Customer`.
- **Why:** Property validation protects every object regardless of how it is created or loaded and gives invalid-object prevention to the domain itself.

## Decision 5: Where membership behavior belongs

- **Problem:** Limits, periods, and late fees differ between membership types and must remain testable independently.
- **Options:** Store values in conditional fields, use a membership lookup table, or implement methods on polymorphic customer subclasses.
- **Choice:** Implement all three policy methods on `BasicCustomer`, `PlusCustomer`, and `ProCustomer`.
- **Why:** Concrete subclasses provide independent values through one interface, avoid tier-based branching in callers, and make each policy naturally extensible.

## Decision 6: Data collection types for the service

- **Problem:** The service repeatedly looks up items and customers, scans rental history, checks SKU uniqueness, and returns overdue records.
- **Options:** Keep one nested list for all records, use separate maps and collections, or store everything in SQL.
- **Choice:** Use a dict keyed by SKU, a dict keyed by customer ID, a list of rentals, and a set of SKUs.
- **Why:** The dictionaries provide direct identity lookup, the list preserves rental chronology for history and availability calculations, and the set gives constant-time SKU membership checks without duplicating item data.

## Decision 7: Availability reconstruction

- **Problem:** In-memory availability must match the starter rentals after loading and remain consistent after returns.
- **Options:** Persist a separate availability counter, mark units in an inventory structure, or calculate availability from open rentals.
- **Choice:** Calculate each item's available units as its total units minus rentals with no return date.
- **Why:** Availability derived from open rentals is a single source of truth, rebuilds correctly from CSV data, and cannot drift when a return state is loaded or updated.

## Decision 8: Audit timing source

- **Problem:** Audit entries need a reliable operation date without making domain methods consult the system clock.
- **Options:** Call the real clock inside each method, read the environment in the decorator, or pass the operation date through the existing method parameters.
- **Choice:** Read `today` from the decorated method arguments and store its ISO value in the audit record.
- **Why:** This keeps auditing deterministic, obeys the project rule that date-dependent methods receive their date, and prevents failed operations from being logged.

## Decision 9: Report construction

- **Problem:** Reports need to be lazy where appropriate while remaining useful for existing service callers.
- **Options:** Build every report eagerly, expose only strings, or combine a lazy overdue generator with eagerly consumed report methods.
- **Choice:** Add `iter_overdue` for lazy row generation and have `overdue_report` consume and sort it; add named methods for text, category, and fine reports.
- **Why:** The generator avoids materializing the full overdue set while the report methods provide stable formatting and collections for callers and tests.

## Decision 10: Console interaction boundary

- **Problem:** The menu must accept bad input, provide waiting-list interaction, and remain testable without changing domain rules.
- **Options:** Scatter prompts and exceptions through the service, use a large monolithic script, or keep a small console adapter around the domain service.
- **Choice:** Put prompting, transcript formatting, and menu dispatch in `main.py`, while leaving all business operations in `GearShare`.
- **Why:** This makes the console replaceable, allows simulated-input tests, and prevents presentation code from duplicating rule logic.

## Decision 11: Environment date handling

- **Problem:** Console operation must be reproducible with `TODAY` while also remaining usable outside a configured shell.
- **Options:** Read the environment inside the service, hard-code the training date, or read the environment once in `main.py` with a real-date fallback.
- **Choice:** Resolve `today` in `main.py` and pass it into each date-dependent service call.
- **Why:** Production behavior remains functional without configuration, samples remain deterministic, and no domain method is coupled to the system clock.

## Decision 12: Class diagram relationships

- **Problem:** The design needed inheritance and ownership shown without introducing renderer-dependent notation.
- **Options:** Include detailed associations for every object reference, use implementation UML syntax, or show only the mandated inheritance and service composition relationships.
- **Choice:** Show inheritance with `<|--` and service ownership with `*--`, using only Mermaid class diagram syntax supported by mermaid.live.
- **Why:** This is readable, simple, and directly communicates type substitution and GearShare ownership.

## Decision 13: Membership policy placement

- **Problem:** Basic, Plus, and Pro values must remain separate from branching in the service.
- **Options:** Store values on `GearShare`, use a lookup table, or place them on concrete customer subclasses.
- **Choice:** Place polymorphic policy methods on concrete customer subclasses.
- **Why:** Each membership owns its own limits and rates, and callers use one interface without tier comparisons.

## Decision 14: Display of item rental rules

- **Problem:** Display items and accessories need different behavior while sharing common item data.
- **Options:** Branch on item category in `GearShare`, add flags to `GearItem`, or use concrete item subclasses.
- **Choice:** Model display items and accessories as subclasses of `GearItem`.
- **Why:** Each subtype can implement rental behavior directly while common validation and identity remain in the abstract base class.

## Decision 15: Repeatable benchmark data

- **Problem:** Complexity measurements must not change between runs.
- **Options:** Use nondeterministic random data, depend on the current clock, or seed one generator used by every benchmark.
- **Choice:** Use a fixed random seed in the item generator and measure fresh synthetic services.
- **Why:** Reproducible data isolates algorithmic scaling from random catalogue changes.

## Decision 16: Measurement isolation

- **Problem:** Timed operations can include setup work or alter state for later repetitions.
- **Options:** Run one service permanently, reset state after every sample, or construct fresh state before timed measurements.
- **Choice:** Construct and reset state outside each timed operation where operation state permits, with one fresh service per measured call.
- **Why:** Setup isolation prevents one sample from changing availability, audit history, or rental state for the next sample.

## Decision 17: Binary search comparison contract

- **Problem:** Binary search must support both the search result and the comparison count needed by the sample output.
- **Options:** Return only an index and calculate comparisons separately, return a result object, or return the index and count together.
- **Choice:** Return `(index, comparisons)` from `binary_search`.
- **Why:** A tuple keeps the API small while making the exact number of midpoint checks observable and testable.

## Decision 18: Catalogue sorting order

- **Problem:** The catalogue needs deterministic mixed-direction ordering across top-level categories.
- **Options:** Several separate passes, category-specific branches, or one tuple key.
- **Choice:** Sort once with a tuple key containing top-level category, negated weight, and name.
- **Why:** Negating weight provides descending weight within an ascending category, while `sorted` supplies stable deterministic ordering for names.

## Decision 19: Hash-based duplicate imports

- **Problem:** Importing gear repeatedly may encounter the same SKU on multiple lines.
- **Options:** Rescan previously imported items, use a list membership check, or maintain a SKU-to-name set.
- **Choice:** Track each encountered SKU in a dictionary that maps it to the original item name.
- **Why:** Dictionary lookup is O(1), and retaining the name lets the importer report exactly which earlier item a duplicate conflicts with.

## Decision 20: Hash indexes for Phase 2 hashing tasks

- **Problem:** Tag grouping, rental frequencies, packing pairs, and multi-word search each need repeated key-based lookup.
- **Options:** Rescan the catalogue for every query or build purpose-specific hash structures.
- **Choice:** Use dictionaries and Counters for grouping and frequency data, a weight dictionary for two-sum, and a word-to-SKU index.
- **Why:** Hash-based structures keep each operation simple and make repeated lookup independent of catalogue length in the common case.

## Decision 21: Undo stack entries

- **Problem:** Undo must restore both successful rental and return operations exactly.
- **Options:** Store only rental objects, store action summaries, or store independent operation records with previous state.
- **Choice:** Store each undo record with action, IDs, SKU, and operation-specific prior state rather than a live Rental object.
- **Why:** The copied state allows rent undo to remove the correct rental and return undo to restore its return date, fine balance, and waiting-list notification.

## Decision 22: Waiting queue collection

- **Problem:** Customers must be served in strict arrival order when an item becomes available.
- **Options:** Use a list, a linked queue, or `collections.deque`.
- **Choice:** Continue using one `deque` per SKU for waiting customers.
- **Why:** `deque.append` and `popleft` provide constant-time FIFO operations, while undo can restore a notified customer at the front with `appendleft`.