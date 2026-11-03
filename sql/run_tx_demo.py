import sqlite3
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "sql" / "schema.sql"
SEED = ROOT / "sql" / "seed.sql"


def create_database():
    connection = sqlite3.connect(":memory:")
    connection.executescript(SCHEMA.read_text(encoding="utf-8"))
    connection.executescript(SEED.read_text(encoding="utf-8"))
    return connection


def reset_rn011(connection):
    connection.execute("DELETE FROM audit_log WHERE rental_id = 'RN011'")
    connection.execute("DELETE FROM rentals WHERE rental_id = 'RN011'")
    connection.commit()


def run_attempt(connection, valid):
    connection.execute("BEGIN")
    connection.execute(
        """INSERT INTO rentals
           (rental_id, customer_id, sku, issue_date, due_date, return_date, extensions)
           VALUES (?, ?, ?, ?, ?, NULL, 0)""",
        ("RN011", "C001", "1000000002", "2026-11-03", "2026-11-06"),
    )
    try:
        connection.execute(
            """INSERT INTO audit_log
               (action, customer_id, sku, created_on, rental_id)
               VALUES (?, ?, ?, ?, ?)""",
            ("RENT" if valid else None, "C001", "1000000002", "2026-11-03", "RN011"),
        )
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        connection.rollback()
        return False


def counts(connection):
    rental_count = connection.execute(
        "SELECT COUNT(*) FROM rentals WHERE rental_id = 'RN011'"
    ).fetchone()[0]
    audit_count = connection.execute(
        "SELECT COUNT(*) FROM audit_log"
    ).fetchone()[0]
    return rental_count, audit_count


def main():
    connection = create_database()
    try:
        print("BEFORE:", counts(connection))

        reset_rn011(connection)
        run_attempt(connection, valid=False)
        print("ATTEMPT 1 AFTER ROLLBACK:", counts(connection))

        run_attempt(connection, valid=True)
        print("ATTEMPT 2 AFTER COMMIT:", counts(connection))
    finally:
        connection.close()


if __name__ == "__main__":
    main()
