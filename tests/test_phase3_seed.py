import sqlite3
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA = PROJECT_ROOT / "sql" / "schema.sql"
SEED = PROJECT_ROOT / "sql" / "seed.sql"


@pytest.fixture
def db():
    connection = sqlite3.connect(":memory:")
    connection.executescript(SCHEMA.read_text(encoding="utf-8"))
    connection.executescript(SEED.read_text(encoding="utf-8"))
    return connection


def test_seed_counts(db):
    expected = {
        "items": 7,
        "tags": 10,
        "customers": 5,
        "rentals": 10,
        "fines": 4,
        "categories": 8,
        "membership_tiers": 3,
    }
    for table, count in expected.items():
        assert db.execute(f'SELECT COUNT(*) FROM "{table}"').fetchone()[0] == count


def test_open_rentals(db):
    ids = {
        row[0]
        for row in db.execute(
            "SELECT rental_id FROM rentals WHERE return_date IS NULL ORDER BY rental_id"
        )
    }
    assert ids == {"RN001", "RN002", "RN003"}


def test_photography_parent(db):
    rows = {
        row[0]
        for row in db.execute(
            """SELECT c.name
               FROM categories c JOIN categories p ON c.parent_id = p.category_id
               WHERE p.name = 'Photography'"""
        )
    }
    assert rows == {"Cameras", "Lenses"}


def test_canon_has_two_tags(db):
    tags = {
        row[0]
        for row in db.execute(
            """SELECT t.name FROM tags t
               JOIN item_tags it ON t.tag_id = it.tag_id
               WHERE it.sku = '1000000001'"""
        )
    }
    assert tags == {"photo", "dslr"}


def test_loading_seed_twice_fails(db):
    with pytest.raises(sqlite3.IntegrityError):
        db.executescript(SEED.read_text(encoding="utf-8"))
