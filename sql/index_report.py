import re
import sqlite3
import statistics
import tempfile
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUERIES = ROOT / "sql" / "queries.sql"
INDEXES = ROOT / "sql" / "indexes.sql"
REPORT = ROOT / "docs" / "index_report.md"

try:
    from .generate_big import create_database, generate
except ImportError:
    from generate_big import create_database, generate


def extract_queries():
    text = QUERIES.read_text(encoding="utf-8")
    parts = re.split(r"^-- Q(\d+):.*$", text, flags=re.MULTILINE)
    queries = []
    for position in range(1, len(parts), 2):
        body = parts[position + 1].strip()
        body = re.sub(r"^-- Join type:.*(?:\n--.*)?\n?", "", body, flags=re.MULTILINE)
        query = body.rsplit(";", 1)[0].strip() + ";"
        queries.append((int(parts[position]), query))
    return queries


def median_time(connection, query):
    samples = []
    for _ in range(3):
        started = time.perf_counter()
        connection.execute(query).fetchall()
        samples.append((time.perf_counter() - started) * 1000)
    return statistics.median(samples)


def plan(connection, query):
    rows = connection.execute("EXPLAIN QUERY PLAN " + query).fetchall()
    return " | ".join(str(row[3]) for row in rows)


def main():
    handle = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    handle.close()
    connection = create_database(handle.name)
    generate(connection)

    queries = extract_queries()
    timings = {number: median_time(connection, query) for number, query in queries}
    slowest = sorted(timings, key=timings.get, reverse=True)[:2]

    rows = []
    for number in slowest:
        query = dict(queries)[number]
        before = timings[number]
        before_plan = plan(connection, query)
        rows.append([number, query, before, before_plan])

    connection.executescript(INDEXES.read_text(encoding="utf-8"))
    connection.commit()

    lines = [
        "| Query | Before ms | After ms | Plan before | Plan after |",
        "|---|---:|---:|---|---|",
    ]
    for number, query, before, before_plan in rows:
        after = median_time(connection, query)
        after_plan = plan(connection, query)
        lines.append(
            f"| Q{number} | {before:.3f} | {after:.3f} | "
            f"{before_plan.replace('|', '&#124;')} | {after_plan.replace('|', '&#124;')} |"
        )

    REPORT.parent.mkdir(exist_ok=True)
    REPORT.write_text(
        "# Index benchmark\n\n"
        + "\n".join(lines)
        + "\n\n## Index I decided not to create\n\n"
        + "<!-- TODO: Rewrite this reasoning in my own words. -->\n"
        + "I decided not to create an index on `fines.paid` because its two values "
        "split most rows very unevenly, so SQLite would still scan much of the table "
        "and the maintenance cost would exceed the likely benefit.\n",
        encoding="utf-8",
    )
    connection.close()
    print(REPORT)


if __name__ == "__main__":
    main()
