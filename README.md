# GearShare Mini

GearShare Mini is the Python + data structures + SQL + React project described in SPEC.md.

## How to run with TODAY=2026-11-03

### Windows PowerShell

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:TODAY = "2026-11-03"
python main.py
```

### macOS/Linux

```sh
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
TODAY=2026-11-03 python main.py
```

## Run tests

```sh
python -m pytest
```

## Phase 1 rule coverage

| Rule | Method | Test |
|---|---|---|
| R1 | `GearShare.rent()` | `test_display_item` |
| R2 | `Accessory.rental_period()`, `GearShare.extend()` | `test_accessory_is_always_rentable_for_two_days`, `test_accessory_cannot_be_extended` |
| R3 | `GearShare.rent()` | `test_rental_limit` |
| R4 | `GearShare.rent()` | `test_unpaid_fines_above_500`, `test_rohan_is_blocked_with_unpaid_fines` |
| R5 | `GearShare.late_fee()` | `test_late_fee_examples` |
| R6 | `GearShare.extend()` | `test_extensions_two_steps_and_then_error` |
| R7 | `GearShare.join_waiting_list()`, `GearShare.return_item()` | `test_vikram_return_fee_and_waiting_list` |
| R8 | `GearShare.rent()` | `test_duplicate_rental` |
| R9 | `GearItem.sku` setter | `test_invalid_sku`, `test_sku_property_rejects_invalid_values` |
| R10 | `GearShare.late_fee()` | `test_late_fee_examples`, `test_return_on_due_date_not_late` |