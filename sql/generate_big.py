import random
import sqlite3
import tempfile
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "sql" / "schema.sql"
SEED = ROOT / "sql" / "seed.sql"
SCHEMA_SQL = SCHEMA.read_text(encoding="utf-8")
SEED_SQL = SEED.read_text(encoding="utf-8")


def create_database(path):
    connection = sqlite3.connect(path)
    connection.executescript(SCHEMA_SQL)
    connection.executescript(SEED_SQL)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def generate(connection, count=100_000):
    random.seed(20261103)
    customers = ["C001", "C002", "C003", "C004", "C005"]
    skus = [
        "1000000001",
        "1000000002",
        "1000000003",
        "1000000004",
        "1000000005",
        "1000000007",
    ]
    start = date(2025, 1, 1)
    rows = []
    for number in range(1, count + 1):
        issue = start + timedelta(days=random.randint(0, 650))
        period = random.randint(1, 14)
        due = issue + timedelta(days=period)
        returned = None if random.random() < 0.08 else issue + timedelta(days=random.randint(0, period + 4))
        rows.append(
            (
                f"BIG{number:07d}",
                random.choice(customers),
                random.choice(skus),
                issue.isoformat(),
                due.isoformat(),
                returned.isoformat() if returned else None,
                random.randint(0, 2),
            )
        )
        if len(rows) == 5_000:
            connection.executemany(
                """INSERT INTO rentals
                   (rental_id, customer_id, sku, issue_date, due_date, return_date, extensions)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                rows,
            )
            rows.clear()
    if rows:
        connection.executemany(
            """INSERT INTO rentals
               (rental_id, customer_id, sku, issue_date, due_date, return_date, extensions)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            rows,
        )
    connection.commit()


def main():
    handle = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    handle.close()
    path = Path(handle.name)
    connection = create_database(path)
    try:
        generate(connection)
        print(path)
    finally:
        connection.close()


if __name__ == "__main__":
    main()
