import re
import sqlite3
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA = PROJECT_ROOT / "sql" / "schema.sql"
SEED = PROJECT_ROOT / "sql" / "seed.sql"
QUERIES = PROJECT_ROOT / "sql" / "queries.sql"


EXPECTED = {
    1: [
        ("Canon EOS 200D", "dslr"),
        ("Canon EOS 200D", "photo"),
        ("Sony 50mm Lens", "lens"),
        ("Sony 50mm Lens", "photo"),
    ],
    2: [
        ("RN001", "Vikram Shah", "DJI Mini Drone"),
        ("RN002", "Rohan Das", "Canon EOS 200D"),
        ("RN003", "Meera Joshi", "Manfrotto Tripod"),
    ],
    3: [
        ("Vikram Shah", "DJI Mini Drone", "2026-10-29", 5),
        ("Rohan Das", "Canon EOS 200D", "2026-10-31", 3),
    ],
    4: [
        ("Canon EOS 200D", 3),
        ("DJI Mini Drone", 2),
        ("Rode Wireless Mic", 2),
    ],
    5: [("Vintage Leica (Showcase)",)],
    6: [("Pooja Menon",)],
    7: [
        ("Basic", "2026-07", 600),
        ("Basic", "2026-08", 600),
        ("Plus", "2026-06", 300),
    ],
    8: [("Paid", 900), ("Pending", 600)],
    9: [("Vikram Shah", 3)],
    10: [
        ("Accessories", 22.0),
        ("Audio", 10.0),
        ("Cameras", 5.5),
        ("Drones", 5.0),
    ],
    11: [
        ("Canon EOS 200D", 1),
        ("Sony 50mm Lens", 1),
        ("DJI Mini Drone", 0),
        ("Manfrotto Tripod", 1),
        ("Rode Wireless Mic", 1),
        ("Vintage Leica (Showcase)", 1),
        ("SD Card 128GB", 3),
    ],
    12: [("Canon EOS 200D", "Rode Wireless Mic", 2)],
}


@pytest.fixture
def db():
    connection = sqlite3.connect(":memory:")
    connection.executescript(SCHEMA.read_text(encoding="utf-8"))
    connection.executescript(SEED.read_text(encoding="utf-8"))
    yield connection
    connection.close()


def load_queries():
    sql = QUERIES.read_text(encoding="utf-8")
    blocks = re.split(r"^-- Q(\d+):.*$", sql, flags=re.MULTILINE)
    return {int(blocks[index]): blocks[index + 1].strip() for index in range(1, len(blocks), 2)}


@pytest.mark.parametrize("query_number", range(1, 13))
def test_query_expected_rows(db, query_number):
    query = load_queries()[query_number]
    actual = db.execute(query).fetchall()
    assert actual == EXPECTED[query_number]
