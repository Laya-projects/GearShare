from datetime import date

import pytest

from errors import ItemNotRentableError
from gearshare import GearShare


@pytest.fixture
def service():
    gearshare = GearShare()
    gearshare.load_data()
    return gearshare


def test_audit_logs_successful_rent(service):
    result = service.rent("C005", "1000000002", date(2026, 11, 3))
    assert result["rental_id"] == "RN011"
    assert service.audit == [{
        "time": "2026-11-03",
        "action": "rent",
        "customer": "Pooja Menon",
        "item": "Sony 50mm Lens",
    }]


def test_audit_does_not_log_failed_rent(service):
    with pytest.raises(ItemNotRentableError):
        service.rent("C003", "1000000006", date(2026, 11, 3))
    assert service.audit == []


def test_audit_logs_successful_return(service):
    service.return_item("RN003", date(2026, 11, 3))
    assert service.audit[0]["action"] == "return_item"
    assert service.audit[0]["time"] == "2026-11-03"
    assert service.audit[0]["customer"] == "Meera Joshi"
    assert service.audit[0]["item"] == "Manfrotto Tripod"


def test_iter_overdue_is_lazy(service):
    overdue = service.iter_overdue(date(2026, 11, 3))
    first = next(overdue)
    assert first["rental"].rental_id == "RN001"
    second = next(overdue)
    assert second["rental"].rental_id == "RN002"


def test_overdue_report_text_matches_sample(service):
    assert service.overdue_report_text(date(2026, 11, 3)) == """Overdue rentals as of 2026-11-03
RENTAL  CUSTOMER     ITEM             DUE         DAYS  FINE SO FAR
RN001   Vikram Shah  DJI Mini Drone   2026-10-29  5     ₹500
RN002   Rohan Das    Canon EOS 200D   2026-10-31  3     ₹150
Total overdue: 2   Fines so far: ₹650"""


def test_unpaid_fines_report(service):
    fines = service.customers_with_unpaid_fines()
    assert fines == {"C004": 600}
    assert service.customers[fines.keys().__iter__().__next__()].name == "Rohan Das"


def test_items_by_category(service):
    categories = service.items_by_category()
    assert categories["Accessories"] == ["SD Card 128GB"]
    assert categories["Photography"] == ["Canon EOS 200D", "Sony 50mm Lens"]
