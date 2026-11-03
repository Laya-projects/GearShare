# GearShare Mini component tree and state ownership

```text
App
+-- CustomerContext
+-- Basket reducer
+-- Layout
|   +-- Navbar
|   +-- CataloguePage
|   |   +-- SearchBar
|   |   +-- GearList
|   |   |   +-- GearCard
|   |   |       +-- AvailabilityBadge
|   +-- ItemDetailsPage
|   +-- MyRentalsPage
|   +-- BasketPage
|   +-- AddItemPage
|   +-- NotFoundPage
```

Every entry below names the state owned by that component and the props it
receives.

| Component | State it owns | Props it receives |
|---|---|---|
| `App` | Router state and application composition | None |
| `Navbar` | No local state | `customer`, `customers`, `basketCount`, `onCustomerChange` |
| `Layout` | No local state | `children` |
| `CataloguePage` | Loading, error, fetched data, category filter, sort | `searchParams`, `setSearchParams`, API client |
| `GearList` | No local state | `gear`, `onSelect`, `waitingListAction` |
| `GearCard` | No local state | `gear`, `availability`, `onOpen`, `onWaitingList` |
| `AvailabilityBadge` | No local state | `available`, `total`, `itemType` |
| `SearchBar` | Controlled input value synchronized with URL search parameters | `value`, `onChange` |
| `ItemDetailsPage` | Loading, error, fetched item | `sku` route parameter |
| `MyRentalsPage` | Loading, error, fetched rentals | `customer` |
| `BasketPage` | Checkout loading and server message | `basket`, `customer`, `dispatch` |
| `AddItemPage` | Controlled form values and field errors | API client |
| `NotFoundPage` | No local state | None |
| `CustomerContext` | Selected customer and customer list | `children`, API client |
| `basket reducer` | Basket item list | `ADD`, `REMOVE`, and `CLEAR` actions |

## Where each piece of state lives

| State | Location | Reason |
|---|---|---|
| Search text | URL query parameters | It makes the result URL shareable and allows `Back to results` to restore the previous search. |
| Category filter | URL query parameters | It belongs with catalogue navigation and should survive entry into item details. |
| Sort | URL query parameters | It should survive navigation and can be represented in and restored from the catalogue URL. |
| Selected customer | `CustomerContext` | It is global customer identity used by navigation, rental limits, pages, and checkout. |
| Basket | `useReducer` | Basket actions are explicit state transitions and can enforce limits and immutable additions/removals consistently. |
| Loading/error flags | The page or feature that owns its fetched request | Each request can render independently without exposing its request lifecycle to unrelated components. |
| Fetched data | The page that fetches it | Catalogue, item details, and rentals are route-scoped data and are passed downward to presentational components. |
