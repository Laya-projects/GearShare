import csv
import sys

from items import Accessory, DisplayItem, Equipment


def import_gear(path):
    seen = {}
    added = 0
    duplicates = 0

    with open(path, newline="", encoding="utf-8-sig") as file:
        for line_number, row in enumerate(csv.DictReader(file), start=2):
            sku = row["sku"]
            if sku in seen:
                print(
                    f"Line {line_number}: duplicate SKU {sku} "
                    f"(already used by '{seen[sku]}'), skipped."
                )
                duplicates += 1
                continue
            seen[sku] = row["name"]
            added += 1

    print(f"Imported {added + duplicates} rows: {added} added, {duplicates} duplicate skipped.")
    return seen


def load_item(row):
    common = [
        row["sku"],
        row["name"],
        row["tags"],
        row["category"],
        row["parent_category"],
        int(row["weight_g"]),
        int(row["price"]),
        int(row["total_units"]),
    ]
    item_types = {"Accessory": Accessory, "Display": DisplayItem}
    return item_types.get(row["item_type"], Equipment)(*common)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python import_gear.py <gear CSV path>")
    import_gear(sys.argv[1])
