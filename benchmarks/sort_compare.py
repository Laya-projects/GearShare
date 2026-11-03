import random
import statistics
import time
from pathlib import Path

from dsa.sorting import bubble_sort, insertion_sort, selection_sort


SIZES = [1000, 5000, 10000]
REPEATS = 5


def median_time(operation, values):
    samples = []
    for _ in range(REPEATS):
        candidate = list(values)
        start = time.perf_counter()
        operation(candidate)
        samples.append((time.perf_counter() - start) * 1000)
    return statistics.median(samples)


def sorted_names(values):
    return sorted(values, key=lambda name: name)


def benchmark():
    randomizer = random.Random(2026)
    results = {}
    for size in SIZES:
        names = [f"Item {randomizer.randrange(size * 10):05d}" for _ in range(size)]
        results[size] = {
            "bubble_sort": median_time(lambda values: bubble_sort(values, print_passes=False), names),
            "insertion_sort": median_time(lambda values: insertion_sort(values, print_passes=False), names),
            "selection_sort": median_time(lambda values: selection_sort(values, print_passes=False), names),
            "sorted(key=...)": median_time(sorted_names, names),
        }
    return results


def render_report(results):
    lines = [
        "# Phase 2.2 Sorting Comparison",
        "",
        "| operation | n=1000 | n=5000 | n=10000 |",
        "|---|---:|---:|---:|",
    ]
    operations = ["bubble_sort", "insertion_sort", "selection_sort", "sorted(key=...)"]
    for operation in operations:
        values = " | ".join(f"{results[size][operation]:.3f}" for size in SIZES)
        lines.append(f"| {operation} | {values} |")
    return "\n".join(lines)


def main():
    Path("docs/sort_report.md").write_text(
        render_report(benchmark()) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
