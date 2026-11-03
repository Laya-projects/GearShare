import sqlite3
from contextlib import contextmanager
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "sql" / "schema.sql"
SEED = ROOT / "sql" / "seed.sql"


def connect_database(path=":memory:"):
    connection = sqlite3.connect(path, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    if path == ":memory:" and connection.execute(
        "SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'"
    ).fetchone()[0] == 0:
        initialize_database(connection)
    return connection


def initialize_database(connection):
    connection.executescript(SCHEMA.read_text(encoding="utf-8"))
    connection.executescript(SEED.read_text(encoding="utf-8"))


@contextmanager
def transaction(connection):
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
