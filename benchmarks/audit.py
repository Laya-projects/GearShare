import statistics
import time
from datetime import date, timedelta

from benchmarks.generate_items import generate_and_load
from rentals import Rental


# Predicted before measurements.
PREDICTIONS = {
    "list_items": {"time": "O(n)", "space": "O(n)"},
    "search": {"time": "O(n)", "space": "O(k)"},
    "rent": {"time": "O(n)", "space": "O(1)"},
    "return_item": {"time": "O(n)", "space": "O(1)"},
    "overdue_report": {"time": "O(r log r)", "space": "O(r)"},
}

SIZES = [1000, 5000, 10000, 50000]
TODAY = date(2026, 11, 3)


def median_time(operation, repeats=5):
    samples = []
    for _ in range(repeats):
        start = time.perf_counter()
        operation()
        samples.append((time.perf_counter() - start) * 1000)
    return statistics.median(samples)


def benchmark_operation(operation, n):
    if operation == "list_items":
        service = generate_and_load(n)
        return median_time(service.list_items)
    if operation == "search":
        service = generate_and_load(n)
        return median_time(lambda: service.search("Fake"))
    if operation == "rent":
        def timed_rent():
            service = generate_and_load(n)
            service.rent("CBENCH", next(iter(service.items)), TODAY)
        return median_time(timed_rent)
    if operation == "return_item":
        def timed_return():
            service = generate_and_load(n)
            sku = next(iter(service.items))
            rental = Rental("CBENCH", sku, TODAY - timedelta(days=10), TODAY - timedelta(days=7), rental_id="B0001")
            service.rentals.append(rental)
            service.items[sku].total_units = 2
            service.unpaid_fines["CBENCH"] = 0
            service.return_item(rental.rental_id, TODAY)
        return median_time(timed_return)
    if operation == "overdue_report":
        def timed_overdue():
            service = generate_and_load(n)
            sku = next(iter(service.items))
            service.rentals.append(Rental(
                "CBENCH", sku, TODAY - timedelta(days=10), TODAY - timedelta(days=2), rental_id="B0001"
            ))
            service.overdue_report(TODAY)
        return median_time(timed_overdue)
    raise ValueError(operation)


def render_report(results):
    lines = [
        "# Phase 2.1 Complexity Audit",
        "",
        "| operation | predicted time | predicted space | n=1000 | n=5000 | n=10000 | n=50000 | ratio 1000->10000 | ratio 5000->10000 | observed shape |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    for operation in PREDICTIONS:
        values = [f"{results[operation][n]:.3f}" for n in SIZES]
        ratio_1000_10000 = (
            results[operation][10000] / results[operation][1000]
            if results[operation][1000]
            else 0
        )
        ratio_5000_10000 = (
            results[operation][10000] / results[operation][5000]
            if results[operation][5000]
            else 0
        )
        lines.append(
            f"| {operation} | {PREDICTIONS[operation]['time']} | "
            f"{PREDICTIONS[operation]['space']} | {' | '.join(values)} | "
            f"{ratio_1000_10000:.2f}x | {ratio_5000_10000:.2f}x | "
            f"{observed_shape(ratio_1000_10000, ratio_5000_10000)} |"
        )
    lines.extend(["", "## Surprises", ""])
    for operation in PREDICTIONS:
        lines.append(f"### {operation}")
        lines.append("Sentence 1: TODO.")
        lines.append("Sentence 2: TODO.")
        lines.append("")
    return "\n".join(lines)


def observed_shape(ratio_1000_10000, ratio_5000_10000):
    if ratio_1000_10000 < 3:
        return "O(1)"
    if ratio_1000_10000 >= 60 or ratio_5000_10000 >= 20:
        return "O(n^2)"
    if ratio_1000_10000 >= 20 or ratio_5000_10000 >= 2.7:
        return "O(n log n)"
    return "O(n)"


def main():
    results = {
        operation: {n: benchmark_operation(operation, n) for n in SIZES}
        for operation in PREDICTIONS
    }
    from pathlib import Path
    Path("docs/benchmark_report.md").write_text(render_report(results) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
