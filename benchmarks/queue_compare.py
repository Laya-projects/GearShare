import statistics
import time
from collections import deque
from pathlib import Path


SIZE = 100_000
REPEATS = 5


def median_list_pop():
    samples = []
    for _ in range(REPEATS):
        values = list(range(SIZE))
        start = time.perf_counter()
        while values:
            values.pop(0)
        samples.append((time.perf_counter() - start) * 1000)
    return statistics.median(samples)


def median_deque_popleft():
    samples = []
    for _ in range(REPEATS):
        values = deque(range(SIZE))
        start = time.perf_counter()
        while values:
            values.popleft()
        samples.append((time.perf_counter() - start) * 1000)
    return statistics.median(samples)


def render_report(list_ms, deque_ms):
    return (
        "# Phase 2.4 Queue Comparison\n\n"
        "| operation | entries | median (milliseconds) |\n"
        "|---|---:|---:|\n"
        f"| list.pop(0) | {SIZE:,} | {list_ms:.3f} |\n"
        f"| deque.popleft() | {SIZE:,} | {deque_ms:.3f} |\n"
    )


def main():
    Path("docs/queue_report.md").write_text(
        render_report(median_list_pop(), median_deque_popleft()),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
