import sqlite3
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCHEMA = PROJECT_ROOT / "sql" / "schema.sql"
SEED = PROJECT_ROOT / "sql" / "seed.sql"

from sql.run_tx_demo import counts, create_database, reset_rn011, run_attempt


def database():
    connection = sqlite3.connect(":memory:")
    connection.executescript(SCHEMA.read_text(encoding="utf-8"))
    connection.executescript(SEED.read_text(encoding="utf-8"))
    return connection


def test_failed_attempt_leaves_no_rental_or_audit():
    connection = database()
    try:
        reset_rn011(connection)
        assert run_attempt(connection, valid=False) is False
        assert counts(connection) == (0, 0)
    finally:
        connection.close()


def test_successful_attempt_adds_one_rental_and_audit():
    connection = database()
    try:
        reset_rn011(connection)
        assert run_attempt(connection, valid=True) is True
        assert counts(connection) == (1, 1)
        assert connection.execute(
            "SELECT customer_id, sku FROM rentals WHERE rental_id = 'RN011'"
        ).fetchone() == ("C001", "1000000002")
        assert connection.execute(
            "SELECT action FROM audit_log WHERE rental_id = 'RN011'"
        ).fetchone() == ("RENT",)
    finally:
        connection.close()
