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