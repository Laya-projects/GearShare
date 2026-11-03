import argparse
import sqlite3
from pathlib import Path


SQL_DIR = Path(__file__).resolve().parent
TABLE_NAMES = [
    "membership_tiers",
    "categories",
    "customers",
    "items",
    "tags",
    "item_tags",
    "rentals",
    "fines",
    "waiting_list",
    "audit_log",
]


def load_db(database_path):
    connection = sqlite3.connect(database_path)
    try:
        connection.executescript((SQL_DIR / "schema.sql").read_text(encoding="utf-8"))
        connection.executescript((SQL_DIR / "seed.sql").read_text(encoding="utf-8"))
        connection.commit()
        for table in TABLE_NAMES:
            count = connection.execute(
                f'SELECT COUNT(*) FROM "{table}"'
            ).fetchone()[0]
            print(f"{table}: {count}")
    finally:
        connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("database_path", nargs="?", default="gearshare.db")
    arguments = parser.parse_args()
    load_db(arguments.database_path)
