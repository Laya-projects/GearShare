from datetime import date

import pytest
from fastapi.testclient import TestClient

from api.main import app, get_service
from gearshare import GearShare
from storage.db import connect_database, initialize_database


@pytest.fixture
def service(tmp_path):
    connection = connect_database(tmp_path / "gearshare.db")
    initialize_database(connection)
    connection.commit()
    gear_service = GearShare(connection=connection)
    gear_service.load_data()
    app.dependency_overrides[get_service] = lambda: gear_service
    yield gear_service
    app.dependency_overrides.clear()
    connection.close()


@pytest.fixture
def client(service, monkeypatch):
    monkeypatch.setattr("api.main.TODAY", "2026-11-03")
    return TestClient(app)


def test_drone_and_empty_search(client):
    response = client.get("/gear", params={"q": "drone", "sort": "name"})
    assert response.status_code == 200
    assert response.json() == [{
        "sku": "1000000003",
        "name": "DJI Mini Drone",
        "tags": ["video", "aerial"],
        "category": "Drones",
        "item_type": "Equipment",
        "available": 0,
        "total": 1,
        "weight_g": 249,
    }]
    assert client.get("/gear", params={"q": "zzz"}).json() == []


def test_missing_item_and_invalid_sku(client):
    response = client.get("/gear/1000000999")
    assert response.status_code == 404
    assert response.json() == {
        "error": "ItemNotFoundError",
        "message": "No item with SKU 1000000999.",
    }

    response = client.post("/rentals", json={"customer_id": "C001", "sku": "123"})
    assert response.status_code == 422
    assert response.json() == {
        "error": "InvalidSKUError",
        "message": "SKU must be exactly 10 digits.",
    }


def test_rental_samples_and_rule_errors(client):
    response = client.post("/rentals", json={
        "customer_id": "C001",
        "sku": "1000000002",
    })
    assert response.status_code == 201
    assert response.json() == {"rental_id": "RN011", "due_date": "2026-11-06"}

    response = client.post("/rentals", json={
        "customer_id": "C001",
        "sku": "1000000002",
    })
    assert response.status_code == 409
    assert response.json() == {
        "error": "R8",
        "message": "Ananya Nair already has a unit of 'Sony 50mm Lens'.",
    }

    response = client.post("/rentals", json={
        "customer_id": "C004",
        "sku": "1000000004",
    })
    assert response.status_code == 409
    assert response.json() == {
        "error": "R4",
        "message": "Rohan Das has unpaid fines of ₹600 (limit ₹500).",
    }

    response = client.post("/rentals", json={
        "customer_id": "C003",
        "sku": "1000000006",
    })
    assert response.status_code == 409
    assert response.json() == {
        "error": "R1",
        "message": "'Vintage Leica (Showcase)' is a display item and cannot be rented.",
    }

    response = client.post("/rentals", json={
        "customer_id": "C009",
        "sku": "1000000002",
    })
    assert response.status_code == 404
    assert response.json()["error"] == "CustomerNotFoundError"


def test_return_and_customer_rentals(client):
    customer_response = client.get("/customers/C002/rentals")
    assert customer_response.status_code == 200
    assert customer_response.json() == {
        "customer": "Vikram Shah",
        "membership_type": "Plus",
        "max_items": 4,
        "unpaid_fines": 0,
        "active": [{
            "rental_id": "RN001",
            "item": "DJI Mini Drone",
            "due_date": "2026-10-29",
            "days_overdue": 5,
        }],
    }

    response = client.post("/rentals/RN001/return")
    assert response.status_code == 200
    assert response.json() == {
        "rental_id": "RN001",
        "days_late": 5,
        "fine": 500,
        "next_in_waiting_list": None,
    }
