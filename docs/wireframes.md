# GearShare Mini wireframes

## Catalogue (`/`)

```text
+---------------------------------------------------------------------+
| GearShare Mini    Catalogue   My rentals   Basket (2)  [Ananya Nair v] |
+---------------------------------------------------------------------+
| Search [ drone_______ ]   Category [All v]   Sort [Name v]          |
|                                                                     |
| Loading: Loading catalogue...                                       |
|                                                                     |
| 1 result                                                            |
| +-----------------------------+                                     |
| | DJI Mini Drone              |                                     |
| | video, aerial               |                                     |
| | Drones                      |                                     |
| | 0 of 1 available            |                                     |
| | [Join waiting list]         |                                     |
| +-----------------------------+                                     |
+---------------------------------------------------------------------+
```

States:
- Loading: `Loading catalogue...`
- Empty: `No items match 'zzz'. Try a different word.`
- Error: `Can't reach the rental server.` plus a `Retry` button.

## Item details (`/gear/:sku`)

```text
+---------------------------------------------------------------------+
| GearShare Mini    Catalogue   My rentals   Basket (2)              |
+---------------------------------------------------------------------+
| [Back to results]                                                   |
|                                                                     |
| DJI Mini Drone                                                      |
| video, aerial                                                        |
| Drones                                                              |
| 0 of 1 available                                                    |
| [Join waiting list]                                                 |
+---------------------------------------------------------------------+
```

States:
- Loading: `Loading item...`
- Empty/not found: `No item with SKU ...`
- Error: `Can't reach the rental server.` plus a `Retry` button.

## My rentals (`/me`)

```text
+---------------------------------------------------------------------+
| GearShare Mini    Catalogue   My rentals   Basket (2)              |
+---------------------------------------------------------------------+
| My rentals - Vikram Shah                                            |
| Item             Due date    Status                                  |
| DJI Mini Drone   2026-10-29  OVERDUE (5 days)                       |
+---------------------------------------------------------------------+
```

States:
- Loading: `Loading rentals...`
- Empty: `You have no active rentals.`
- Error: `Can't reach the rental server.` plus a `Retry` button.

## Rental basket (`/basket`)

```text
+---------------------------------------------------------------------+
| GearShare Mini    Catalogue   My rentals   Basket (2)              |
+---------------------------------------------------------------------+
| Rental basket                                                       |
| Sony 50mm Lens                                            [Remove] |
| Manfrotto Tripod                                          [Remove] |
|                                                                     |
| Basket message                                                      |
| [Renting...]                                                        |
+---------------------------------------------------------------------+
```

The basket can be empty: `Your rental basket is empty.`. Checkout can be loading
with `Renting...`; it reports server errors exactly and shows checkout failure
with a retry action if the API is unavailable.

## Add item - staff (`/admin/add`)

```text
+---------------------------------------------------------------------+
| GearShare Mini    Catalogue   My rentals   Basket (2)              |
+---------------------------------------------------------------------+
| Add item                                                            |
| SKU *                                                               |
| [____________]                                                       |
| SKU must be exactly 10 digits.                                      |
| Name *                                                              | 
| [____________]                                                       |
| Units *                                                             |
| [1___________]                                                       |
| Category                                                            |
| [____________]                                                       |
| [Add item - disabled until valid]                                   |
+---------------------------------------------------------------------+
```

After success: `Item added.`; the form clears. Server errors are shown under
the form or next to the related field.
