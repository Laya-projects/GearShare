from datetime import date

import pytest

from errors import (
    CustomerNotFoundError,
    DuplicateRentalError,
    ExtensionNotAllowedError,
    InvalidSKUError,
    ItemNotAvailableError,
    ItemNotFoundError,
    ItemNotRentableError,
    RentalLimitExceededError,
    UnpaidFinesError,
)
from gearshare import GearShare


@pytest.fixture
def service():
    gearshare = GearShare()
    gearshare.load_data()
    return gearshare


def test_loaded_collections_and_availability(service):
    assert len(service.items) == 7
    assert len(service.customers) == 5
    assert len(service.rentals) == 10
    assert service._available_units("1000000001") == 1
    assert service._available_units("1000000003") == 0


def test_customer_not_found(service):
    with pytest.raises(CustomerNotFoundError):
        service.rent("C009", "1000000002", date(2026, 11, 3))


def test_invalid_sku(service):
    with pytest.raises(InvalidSKUError):
        service.rent("C001", "123", date(2026, 11, 3))


def test_item_not_found(service):
    with pytest.raises(ItemNotFoundError):
        service.rent("C001", "1000000999", date(2026, 11, 3))


def test_display_item(service):
    with pytest.raises(ItemNotRentableError):
        service.rent("C003", "1000000006", date(2026, 11, 3))


def test_unpaid_fines_above_500(service):
    with pytest.raises(UnpaidFinesError):
        service.rent("C004", "1000000004", date(2026, 11, 3))


def test_exactly_500_fines_are_allowed(service):
    service.unpaid_fines["C002"] = 500
    rental = service.rent("C002", "1000000002", date(2026, 11, 3))
    assert rental["rental_id"] == "RN011"


def test_rental_limit(service):
    service.rent("C001", "1000000002", date(2026, 11, 3))
    service.rent("C001", "1000000007", date(2026, 11, 3))
    with pytest.raises(RentalLimitExceededError):
        service.rent("C001", "1000000004", date(2026, 11, 3))


def test_duplicate_rental(service):
    service.rent("C001", "1000000002", date(2026, 11, 3))
    with pytest.raises(DuplicateRentalError):
        service.rent("C001", "1000000002", date(2026, 11, 3))


def test_item_unavailable(service):
    with pytest.raises(ItemNotAvailableError):
        service.rent("C003", "1000000003", date(2026, 11, 3))


@pytest.mark.parametrize(
    ("customer_id", "sku", "period"),
    [
        ("C001", "1000000001", 3),
        ("C002", "1000000001", 5),
        ("C003", "1000000001", 7),
        ("C003", "1000000007", 2),
    ],
)
def test_due_date_examples(service, customer_id, sku, period):
    rental = service.rent(customer_id, sku, date(2026, 11, 3))
    expected = {
        ("C001", "1000000001"): "2026-11-06",
        ("C002", "1000000001"): "2026-11-08",
        ("C003", "1000000001"): "2026-11-10",
        ("C003", "1000000007"): "2026-11-05",
    }[customer_id, sku]
    assert rental["due_date"] == expected


@pytest.mark.parametrize(
    ("tier", "item", "due", "returned", "days_late", "fee"),
    [
        ("Basic", "Equipment", "2026-10-31", "2026-10-31", 0, 0),
        ("Basic", "Equipment", "2026-10-31", "2026-11-01", 1, 50),
        ("Plus", "Equipment", "2026-10-29", "2026-11-03", 5, 500),
        ("Pro", "Equipment", "2026-09-30", "2026-10-30", 30, 4500),
        ("Basic", "Accessory", "2026-08-03", "2026-08-23", 20, 600),
    ],
)
def test_late_fee_examples(service, tier, item, due, returned, days_late, fee):
    customer_ids = {"Basic": "C001", "Plus": "C002", "Pro": "C003"}
    skus = {"Equipment": "1000000001", "Accessory": "1000000007"}
    rental = next(r for r in service.rentals if r.rental_id == "RN010")
    if item == "Equipment" and tier == "Pro":
        rental = next(r for r in service.rentals if r.rental_id == "RN010")
        service.items[rental.sku].price = 22000
    rental.customer_id = customer_ids[tier]
    rental.sku = skus[item]
    rental.due_date = due
    service.items[rental.sku].price = 600 if item == "Accessory" else (22000 if tier == "Pro" else 45000)
    assert service.late_fee(rental, returned) == fee
    if item == "Accessory":
        assert fee == 600


def test_vikram_return_fee_and_waiting_list(service):
    position = service.join_waiting_list("C003", "1000000003")
    assert position == 1
    result = service.return_item("RN001", date(2026, 11, 3))
    assert result["fee"] == 500
    assert result["days_late"] == 5
    assert result["next_in_waiting_list"] == "Meera Joshi"


def test_rohan_is_blocked_with_unpaid_fines(service):
    with pytest.raises(UnpaidFinesError, match="600"):
        service.rent("C004", "1000000004", date(2026, 11, 3))


def test_extensions_two_steps_and_then_error(service):
    first = service.extend("RN003", date(2026, 11, 3))
    assert first["due_date"] == "2026-11-13"
    second = service.extend("RN003", date(2026, 11, 3))
    assert second["due_date"] == "2026-11-20"
    with pytest.raises(ExtensionNotAllowedError, match="extended 2 times"):
        service.extend("RN003", date(2026, 11, 3))


def test_accessory_cannot_be_extended(service):
    rental = next(r for r in service.rentals if r.rental_id == "RN005")
    with pytest.raises(ExtensionNotAllowedError, match="Accessories cannot be extended"):
        service.extend(rental.rental_id, date(2026, 11, 3))


def test_waiting_customer_blocks_extension(service):
    service.join_waiting_list("C001", "1000000004")
    with pytest.raises(ExtensionNotAllowedError, match="another customer is waiting"):
        service.extend("RN003", date(2026, 11, 3))


def test_return_on_due_date_not_late(service):
    rental = next(r for r in service.rentals if r.rental_id == "RN003")
    result = service.return_item("RN003", rental.due_date)
    assert result["days_late"] == 0
    assert result["fee"] == 0


def test_overdue_report(service):
    report = service.overdue_report(date(2026, 11, 3))
    assert [(row["rental"].rental_id, row["days_late"], row["fine"]) for row in report] == [
        ("RN001", 5, 500),
        ("RN002", 3, 150),
    ]
