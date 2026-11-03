# DELIBERATELY UNSAFE DEMO. The only file allowed to build SQL with string formatting.

import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "sql" / "schema.sql"
SEED = ROOT / "sql" / "seed.sql"


def create_database():
    connection = sqlite3.connect(":memory:")
    connection.executescript(SCHEMA.read_text(encoding="utf-8"))
    connection.executescript(SEED.read_text(encoding="utf-8"))
    return connection


def search_unsafe(connection, term):
    query = (
        "SELECT sku, name FROM items "
        f"WHERE name LIKE '%{term}%' "
        "ORDER BY name"
    )
    connection.execute(query)
    return connection.execute(query).fetchall(), query


def search_safe(connection, term):
    query = (
        "SELECT sku, name FROM items "
        "WHERE name LIKE ? "
        "ORDER BY name"
    )
    return connection.execute(query, ("%" + term + "%",)).fetchall()


def main():
    connection = create_database()
    try:
        unsafe_drone, _ = search_unsafe(connection, "Drone")
        unsafe_attack, attack_sql = search_unsafe(connection, "' OR '1'='1")
        safe_attack = search_safe(connection, "' OR '1'='1")
        safe_drone = search_safe(connection, "Drone")

        print("Unsafe SQL injection demo")
        print(f"search_unsafe(\"Drone\") -> {len(unsafe_drone)} row")
        print(f"search_unsafe(\"' OR '1'='1\") -> {len(unsafe_attack)} rows")
        print(f"Unsafe attack SQL: {attack_sql}")
        print("\nSafe parameterised demo")
        print(f"search_safe(\"' OR '1'='1\") -> {len(safe_attack)} rows")
        print(f"search_safe(\"Drone\") -> {len(safe_drone)} row")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
