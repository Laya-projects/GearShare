import pytest

from customers import BasicCustomer, PlusCustomer, ProCustomer
from errors import (
    GearShareError,
    InvalidSKUError,
    ItemNotFoundError,
    CustomerNotFoundError,
    ItemNotRentableError,
    UnpaidFinesError,
    RentalLimitExceededError,
    DuplicateRentalError,
    ItemNotAvailableError,
    ExtensionNotAllowedError,
)
from items import Accessory, DisplayItem, Equipment
from rentals import Rental


def test_invalid_sku_is_rejected():
    with pytest.raises(InvalidSKUError, match="SKU must be exactly 10 digits"):
        Equipment("123", "Camera", total_units=1)


@pytest.mark.parametrize("sku", ["", "12345678901", "123456789A"])
def test_sku_property_rejects_invalid_values(sku):
    item = Equipment("1000000001", "Camera")
    with pytest.raises(InvalidSKUError):
        item.sku = sku


@pytest.mark.parametrize("name", ["", "   ", None])
def test_item_name_cannot_be_blank(name):
    with pytest.raises(ValueError, match="Item name cannot be blank"):
        Equipment("1000000001", name)


@pytest.mark.parametrize("units", [-1, -100])
def test_item_units_cannot_be_negative(units):
    with pytest.raises(ValueError, match="Item units cannot be negative"):
        Equipment("1000000001", "Camera", total_units=units)


@pytest.mark.parametrize("units", [1, 0, 3])
def test_item_units_property_accepts_non_negative_values(units):
    item = Equipment("1000000001", "Camera", total_units=units)
    assert item.total_units == units
    assert item.units == units


def test_item_units_property_can_be_updated():
    item = Equipment("1000000001", "Camera", total_units=1)
    item.units = 2
    assert item.total_units == 2


@pytest.mark.parametrize("name", ["", "   ", None])
def test_customer_name_cannot_be_blank(name):
    with pytest.raises(ValueError, match="Customer name cannot be blank"):
        BasicCustomer("C001", name, "person@example.com")


@pytest.mark.parametrize("email", ["", "invalid", None])
def test_customer_email_must_contain_at(email):
    with pytest.raises(ValueError, match="Customer email must contain '@'"):
        BasicCustomer("C001", "Ananya Nair", email)


def test_customer_email_can_be_updated():
    customer = BasicCustomer("C001", "Ananya Nair", "ananya@example.com")
    customer.email = "new@example.com"
    assert customer.email == "new@example.com"


@pytest.mark.parametrize(
    ("customer_type", "max_items", "rental_period", "late_fee_per_day"),
    [
        (BasicCustomer, 2, 3, 50),
        (PlusCustomer, 4, 5, 100),
        (ProCustomer, 8, 7, 150),
    ],
)
def test_membership_policy(
    customer_type, max_items, rental_period, late_fee_per_day
):
    customer = customer_type("C001", "Customer", "customer@example.com")
    assert customer.max_items() == max_items
    assert customer.rental_period() == rental_period
    assert customer.late_fee_per_day() == late_fee_per_day


def test_equipment_uses_customer_rental_period():
    item = Equipment("1000000001", "Camera")
    assert item.is_rentable() is True
    assert item.rental_period(BasicCustomer("C001", "A", "a@example.com")) == 3
    assert item.rental_period(ProCustomer("C003", "C", "c@example.com")) == 7


def test_accessory_is_always_rentable_for_two_days():
    item = Accessory("1000000007", "SD Card")
    customer = ProCustomer("C003", "Meera", "meera@example.com")
    assert item.is_rentable() is True
    assert item.rental_period(customer) == 2


def test_display_item_is_not_rentable():
    item = DisplayItem("1000000006", "Vintage Leica")
    customer = ProCustomer("C003", "Meera", "meera@example.com")
    assert item.is_rentable() is False
    assert item.rental_period(customer) == 0


@pytest.mark.parametrize(
    "exception_type",
    [
        GearShareError,
        InvalidSKUError,
        ItemNotFoundError,
        CustomerNotFoundError,
        ItemNotRentableError,
        UnpaidFinesError,
        RentalLimitExceededError,
        DuplicateRentalError,
        ItemNotAvailableError,
        ExtensionNotAllowedError,
    ],
)
def test_domain_exception_can_be_raised(exception_type):
    with pytest.raises(exception_type):
        raise exception_type("test")


def test_exception_hierarchy():
    assert issubclass(InvalidSKUError, GearShareError)
    assert issubclass(ExtensionNotAllowedError, GearShareError)


def test_rental_uses_starter_next_number():
    Rental._next_number = 11
    rental = Rental("C001", "1000000001", "2026-11-03", "2026-11-06")
    assert rental.rental_id == "RN011"
    assert Rental("C001", "1000000001", "2026-11-03", "2026-11-06").rental_id == "RN012"


def test_rental_explicit_id_is_preserved():
    rental = Rental(
        "C002",
        "1000000003",
        "2026-10-24",
        "2026-10-29",
        return_date=None,
        rental_id="RN001",
    )
    assert rental.rental_id == "RN001"


def test_domain_string_representations():
    item = Equipment("1000000001", "Canon EOS 200D")
    customer = BasicCustomer("C001", "Ananya Nair", "ananya@example.com")
    rental = Rental("C001", "1000000001", "2026-11-03", "2026-11-06", rental_id="RN011")

    assert "Canon EOS 200D" in str(item)
    assert "1000000001" in repr(item)
    assert "Ananya Nair" in str(customer)
    assert "C001" in repr(customer)
    assert "RN011" in str(rental)
    assert "1000000001" in repr(rental)
