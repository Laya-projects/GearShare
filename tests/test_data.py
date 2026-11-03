import csv
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def count_rows(filename):
    with (DATA_DIR / filename).open(newline="", encoding="utf-8") as csv_file:
        return sum(1 for _ in csv.DictReader(csv_file))


def test_starter_data_counts():
    assert count_rows("gear.csv") == 7
    assert count_rows("customers.csv") == 5
    assert count_rows("rentals.csv") == 10
    assert count_rows("fines.csv") == 4
