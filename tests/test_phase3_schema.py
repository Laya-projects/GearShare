import sqlite3
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA = PROJECT_ROOT / "sql" / "schema.sql"
TABLES = {
    "customers",
    "membership_tiers",
    "items",
    "categories",
    "tags",
    "item_tags",
    "rentals",
    "fines",
    "waiting_list",
    "audit_log",
}


@pytest.fixture
def db():
    connection = sqlite3.connect(":memory:")
    connection.executescript(SCHEMA.read_text(encoding="utf-8"))
    yield connection
    connection.close()


def seed_rental(db):
    db.execute(
        "INSERT INTO membership_tiers VALUES (?, ?, ?, ?)",
        ("Basic", 2, 3, 100),
    )
    db.execute(
        "INSERT INTO categories(category_id, name, parent_id) VALUES (?, ?, NULL)",
        (1, "Cameras"),
    )
    db.execute(
        "INSERT INTO customers(customer_id, name, email, tier) VALUES (?, ?, ?, ?)",
        ("C001", "Ananya Nair", "ananya@example.com", "Basic"),
    )
    db.execute(
        """INSERT INTO items(sku, name, item_type, weight_g, price, total_units, category_id)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        ("1000000001", "Canon EOS 200D", "Equipment", 450, 45000, 2, 1),
    )
    db.execute(
        """INSERT INTO rentals(rental_id, customer_id, sku, issue_date, due_date)
           VALUES (?, ?, ?, ?, ?)""",
        ("RN001", "C001", "1000000001", "2026-11-03", "2026-11-06"),
    )


def test_all_phase3_tables_exist(db):
    names = {
        row[0]
        for row in db.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'"
        )
    }
    assert TABLES <= names


def test_duplicate_sku_fails(db):
    db.execute(
        "INSERT INTO categories(category_id, name, parent_id) VALUES (?, ?, NULL)",
        (1, "Cameras"),
    )
    db.execute(
        """INSERT INTO items(sku, name, item_type, weight_g, price, total_units, category_id)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        ("1000000001", "Camera One", "Equipment", 450, 45000, 1, 1),
    )
    with pytest.raises(sqlite3.IntegrityError):
        db.execute(
            """INSERT INTO items(sku, name, item_type, weight_g, price, total_units, category_id)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            ("1000000001", "Camera Two", "Equipment", 450, 45000, 1, 1),
        )


def test_invalid_dates_and_units_fail(db):
    db.execute(
        "INSERT INTO membership_tiers VALUES (?, ?, ?, ?)",
        ("Basic", 2, 3, 100),
    )
    db.execute(
        "INSERT INTO categories(category_id, name, parent_id) VALUES (?, ?, NULL)",
        (1, "Cameras"),
    )
    db.execute(
        "INSERT INTO customers(customer_id, name, email, tier) VALUES (?, ?, ?, ?)",
        ("C001", "Ananya Nair", "ananya@example.com", "Basic"),
    )
    db.execute(
        """INSERT INTO items(sku, name, item_type, weight_g, price, total_units, category_id)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        ("1000000001", "Canon EOS 200D", "Equipment", 450, 45000, 1, 1),
    )
    with pytest.raises(sqlite3.IntegrityError):
        db.execute(
            """INSERT INTO rentals(rental_id, customer_id, sku, issue_date, due_date)
               VALUES (?, ?, ?, ?, ?)""",
            ("RN001", "C001", "1000000001", "2026-11-03", "2026-11-02"),
        )
    with pytest.raises(sqlite3.IntegrityError):
        db.execute(
            """INSERT INTO items(sku, name, item_type, weight_g, price, total_units, category_id)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            ("1000000002", "Negative Units", "Equipment", 450, 45000, -1, 1),
        )


def test_deleting_customer_with_rental_is_restricted(db):
    seed_rental(db)
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("DELETE FROM customers WHERE customer_id = 'C001'")
