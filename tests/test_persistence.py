from datetime import date
from pathlib import Path

import pytest

from gearshare import GearShare
from storage.db import connect_database, initialize_database


@pytest.fixture
def fresh_database(tmp_path):
    path = tmp_path / "gearshare.db"
    connection = connect_database(path)
    initialize_database(connection)
    connection.commit()
    yield connection
    connection.close()


def test_database_repositories_are_bound_to_fresh_file(fresh_database):
    service = GearShare(connection=fresh_database)
    service.load_data()
    result = service.rent("C001", "1000000002", date(2026, 11, 3))
    assert result == {"rental_id": "RN011", "due_date": "2026-11-06"}
    assert fresh_database.execute(
        "SELECT COUNT(*) FROM rentals WHERE rental_id = 'RN011'"
    ).fetchone()[0] == 1


def test_rental_persists_after_connection_reopen(tmp_path):
    path = tmp_path / "gearshare.db"
    connection = connect_database(path)
    initialize_database(connection)
    connection.commit()
    service = GearShare(connection=connection)
    service.load_data()
    service.rent("C001", "1000000002", date(2026, 11, 3))
    connection.close()

    reopened = connect_database(path)
    try:
        row = reopened.execute(
            """SELECT issue_date, due_date FROM rentals WHERE rental_id = 'RN011'"""
        ).fetchone()
        assert tuple(row) == ("2026-11-03", "2026-11-06")
    finally:
        reopened.close()


def test_rent_rolls_back_when_audit_insert_fails(fresh_database):
    service = GearShare(connection=fresh_database)
    service.load_data()

    def fail_audit(*args, **kwargs):
        fresh_database.execute(
            "INSERT INTO audit_log (action, customer_id, sku, created_on) VALUES (NULL, ?, ?, ?)",
            args[1:4],
        )

    service.rentals_repo.audit = fail_audit
    try:
        service.rent("C001", "1000000002", date(2026, 11, 3))
    except Exception:
        pass

    assert fresh_database.execute(
        "SELECT COUNT(*) FROM rentals WHERE rental_id = 'RN011'"
    ).fetchone()[0] == 0
    assert fresh_database.execute(
        "SELECT COUNT(*) FROM audit_log WHERE rental_id = 'RN011'"
    ).fetchone()[0] == 0


def test_gearshare_has_no_repository_sql():
    source = Path("gearshare.py").read_text(encoding="utf-8")
    assert "sqlite3" not in source.lower()
    assert "SELECT" not in source
