import csv
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_COLUMNS = [
    "rental_id",
    "customer_name",
    "email",
    "tier",
    "item_name",
    "tags",
    "sku",
    "category",
    "parent_category",
    "weight_g",
    "price",
    "issue_date",
    "due_date",
    "return_date",
    "fine",
    "fine_paid",
]


def read_csv(filename):
    with (DATA_DIR / filename).open("r", encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


def build_flat():
    gear = {row["sku"]: row for row in read_csv("gear.csv")}
    customers = {
        row["customer_id"]: row for row in read_csv("customers.csv")
    }
    rentals = read_csv("rentals.csv")
    fines = {row["rental_id"]: row for row in read_csv("fines.csv")}

    rows = []
    for rental in rentals:
        customer = customers[rental["customer_id"]]
        item = gear[rental["sku"]]
        fine = fines.get(rental["rental_id"])
        parent_category = (
            "Photography"
            if item["category"] in {"Cameras", "Lenses"}
            else ""
        )
        rows.append(
            {
                "rental_id": rental["rental_id"],
                "customer_name": customer["name"],
                "email": customer["email"],
                "tier": customer["membership_type"],
                "item_name": item["name"],
                "tags": ";".join(filter(None, item["tags"].split(";"))),
                "sku": item["sku"],
                "category": item["category"],
                "parent_category": parent_category,
                "weight_g": item["weight_g"],
                "price": item["price"],
                "issue_date": rental["issue_date"],
                "due_date": rental["due_date"],
                "return_date": rental["return_date"],
                "fine": fine["amount"] if fine else "",
                "fine_paid": fine["paid"] if fine else "",
            }
        )

    output_path = DATA_DIR / "gearshare_flat.csv"
    with output_path.open("w", encoding="utf-8", newline="") as destination:
        writer = csv.DictWriter(destination, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    build_flat()
