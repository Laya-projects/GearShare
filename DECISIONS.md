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