# Phase 4 behaviour checklist

| Action | Expected result | Pass/Fail | Notes |
|---|---|---|---|
| Open `/` | Spinner `Loading catalogue...` then 7 cards |  |  |
| Type `drone` | List shows only DJI Mini Drone. Text: `1 result` |  |  |
| Type `zzz` | `No items match 'zzz'. Try a different word.` |  |  |
| Click the Sony 50mm Lens card | URL becomes `/gear/1000000002`. Shows `1 of 1 available` |  |  |
| Open DJI Mini Drone | `0 of 1 available`. Button reads `Join waiting list` |  |  |
| Open Vintage Leica (Showcase) | `Display item: view in the shop only`. No rent button |  |  |
| Pick Ananya (Basic). Add 2 items, try a 3rd | Message: `Basket full: Basic members can rent 2 items.` 3rd button disabled |  |  |
| Click Rent with a valid basket | Button shows `Renting...` then toast: `Rented Sony 50mm Lens. Due 2026-11-06.` |  |  |
| Back on the catalogue after renting | Sony 50mm Lens now shows `0 of 1 available` |  |  |
| Pick Rohan. Try to rent Manfrotto Tripod | Red message from the server: `Rohan Das has unpaid fines of ₹600 (limit ₹500).` |  |  |
| Pick Vikram. Open My rentals | Table row: DJI Mini Drone, due 2026-10-29, `OVERDUE (5 days)` |  |  |
| Stop the API server, reload | `Can't reach the rental server.` with a `Retry` button |  |  |
| Open `/nothing` | 404 page with a link back to the catalogue |  |  |
| Add item: SKU `123` | Under the field: `SKU must be exactly 10 digits.` Submit disabled |  |  |
| Add item: all fields valid | Success message, form clears, item appears in the catalogue |  |  |
| Resize to 360 px wide | One column of cards, nothing cut off, no sideways scrolling |  |  |
