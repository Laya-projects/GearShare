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