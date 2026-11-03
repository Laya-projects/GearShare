from datetime import date

from dsa.history import build_customer_history
from gearshare import GearShare


def fresh_service():
    service = GearShare()
    service.load_data()
    return service


def test_undo_rent():
    service = fresh_service()
    result = service.rent("C001", "1000000002", date(2026, 11, 3))
    entry = service.undo()
    assert entry["rental_id"] == result["rental_id"]
    assert not any(rental.rental_id == result["rental_id"] for rental in service.rentals)


def test_undo_empty_and_two_rents():
    service = fresh_service()
    assert service.undo() is None
    first = service.rent("C001", "1000000002", date(2026, 11, 3))
    second = service.rent("C005", "1000000007", date(2026, 11, 3))
    service.undo()
    service.undo()
    ids = {rental.rental_id for rental in service.rentals}
    assert first["rental_id"] not in ids
    assert second["rental_id"] not in ids


def test_undo_return_reopens_rental_and_restores_fine():
    service = fresh_service()
    previous_fine = service.unpaid_fines["C002"]
    service.return_item("RN001", date(2026, 11, 3))
    assert service.unpaid_fines["C002"] == previous_fine + 500
    service.undo()
    rental = next(rental for rental in service.rentals if rental.rental_id == "RN001")
    assert rental.return_date is None
    assert service.unpaid_fines["C002"] == previous_fine
    assert service._available_units("1000000003") == 0


def test_waiting_list_stays_fifo():
    service = fresh_service()
    service.join_waiting_list("C003", "1000000003")
    service.join_waiting_list("C005", "1000000003")
    assert service.waiting_list("1000000003") == ["C003", "C005"]
    assert service.waiting_list_text("1000000003") == (
        "Waiting list for 'DJI Mini Drone': Meera Joshi, Pooja Menon"
    )
    service.return_item("RN001", date(2026, 11, 3))
    assert service.waiting_list_text("1000000003") == (
        "Waiting list for 'DJI Mini Drone': Pooja Menon"
    )


def test_history_samples():
    service = fresh_service()
    vikram = build_customer_history("C002", service.rentals)
    meera = build_customer_history("C003", service.rentals)
    assert list(vikram.traversal()) == ["RN001", "RN007", "RN008"]
    assert list(meera.traversal()) == ["RN003", "RN006"]
