import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
FLAT_FILE = PROJECT_ROOT / "data" / "gearshare_flat.csv"


def read_flat():
    with FLAT_FILE.open("r", encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def test_flat_file_has_ten_rows_and_sixteen_columns():
    rows = read_flat()
    assert len(rows) == 10
    assert len(rows[0]) == 16


def test_specific_flat_rental_values():
    rows = {row["rental_id"]: row for row in read_flat()}
    assert rows["RN001"]["return_date"] == ""
    assert rows["RN005"]["fine"] == "600"
    assert rows["RN005"]["fine_paid"] == "yes"
    assert rows["RN009"]["fine"] == "450"
    assert rows["RN009"]["fine_paid"] == "no"
