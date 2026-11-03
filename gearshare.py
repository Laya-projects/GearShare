"""GearShare application service."""

import csv
from collections import deque
from datetime import datetime
from pathlib import Path

from audit import audit
from customers import BasicCustomer, PlusCustomer, ProCustomer
from errors import (
    CustomerNotFoundError,
    DuplicateRentalError,
    ExtensionNotAllowedError,
    InvalidSKUError,
    ItemNotAvailableError,
    ItemNotFoundError,
    ItemNotRentableError,
    RentalLimitExceededError,
    UnpaidFinesError,
)
from items import Accessory, DisplayItem, Equipment
from rentals import Rental


class GearShare:
    def __init__(self, data_dir=None):
        # Dicts provide direct SKU/customer lookup, the rental list preserves history,
        # and the SKU set supports fast uniqueness checks.
        self.items = {}
        self.customers = {}
        self.rentals = []
        self.skus = set()
        self.waiting_lists = {}
        self.unpaid_fines = {}
        self.audit = []
        self.audit_log = self.audit
        self.data_dir = Path(data_dir) if data_dir else Path(__file__).resolve().parent / "data"

    @staticmethod
    def _date(value):
        if value is None or value == "":
            return None
        if isinstance(value, datetime):
            return value.date()
        if hasattr(value, "isoformat"):
            return value
        return datetime.strptime(str(value), "%Y-%m-%d").date()

    @staticmethod
    def _iso(value):
        if value is None:
            return None
        return value.strftime("%Y-%m-%d") if hasattr(value, "strftime") else str(value)

    def load_data(self):
        customer_types = {
            "Basic": BasicCustomer,
            "Plus": PlusCustomer,
            "Pro": ProCustomer,
        }
        with (self.data_dir / "customers.csv").open(newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                customer_type = customer_types[row["membership_type"]]
                customer = customer_type(row["customer_id"], row["name"], row["email"])
                self.customers[customer.customer_id] = customer
                self.unpaid_fines[customer.customer_id] = 0

        with (self.data_dir / "gear.csv").open(newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                common = (
                    row["sku"],
                    row["name"],
                    row["tags"],
                    row["category"],
                    row["parent_category"],
                    int(row["weight_g"]),
                    int(row["price"]),
                    int(row["total_units"]),
                )
                item_type = Accessory if row["item_type"] == "Accessory" else DisplayItem if row["item_type"] == "Display" else Equipment
                item = item_type(*common)
                self.items[item.sku] = item
                self.skus.add(item.sku)

        self.rentals = []
        with (self.data_dir / "rentals.csv").open(newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                rental = Rental(
                    row["customer_id"],
                    row["sku"],
                    self._date(row["issue_date"]),
                    self._date(row["due_date"]),
                    self._date(row["return_date"]),
                    rental_id=row["rental_id"],
                )
                self.rentals.append(rental)

        with (self.data_dir / "fines.csv").open(newline="", encoding="utf-8") as file:
            for row in csv.DictReader(file):
                if row["paid"].lower() == "no":
                    rental = next(r for r in self.rentals if r.rental_id == row["rental_id"])
                    self.unpaid_fines[rental.customer_id] += int(row["amount"])

        ids = [int(rental.rental_id[2:]) for rental in self.rentals if rental.rental_id[2:].isdigit()]
        Rental._next_number = max(ids, default=10) + 1
        for sku in self.items:
            self.waiting_lists.setdefault(sku, deque())
        return {
            "items": len(self.items),
            "customers": len(self.customers),
            "rentals": len(self.rentals),
            "fines": sum(1 for row in csv.DictReader((self.data_dir / "fines.csv").open(newline="", encoding="utf-8"))),
        }

    def list_items(self):
        return list(self.items.values())

    def _active_rentals(self, customer_id, sku=None):
        return [
            rental for rental in self.rentals
            if rental.customer_id == customer_id
            and rental.return_date is None
            and (sku is None or rental.sku == sku)
        ]

    def _available_units(self, sku):
        rented = sum(rental.return_date is None for rental in self.rentals if rental.sku == sku)
        return self.items[sku].total_units - rented

    @audit
    def rent(self, customer_id, sku, today):
        customer = self.customers.get(customer_id)
        if customer is None:
            raise CustomerNotFoundError(customer_id)
        if not isinstance(sku, str) or len(sku) != 10 or not sku.isdigit():
            raise InvalidSKUError()
        item = self.items.get(sku)
        if item is None:
            raise ItemNotFoundError(sku)
        if not item.is_rentable():
            raise ItemNotRentableError(item.name)

        unpaid = self.unpaid_fines.get(customer_id, 0)
        if unpaid > 500:
            raise UnpaidFinesError(customer.name, unpaid)

        active = self._active_rentals(customer_id)
        if len(active) >= customer.max_items():
            raise RentalLimitExceededError(customer.name, len(active), customer.max_items())
        if self._active_rentals(customer_id, sku):
            raise DuplicateRentalError(customer.name, item.name)
        if self._available_units(sku) <= 0:
            raise ItemNotAvailableError(item.name)

        issue_date = self._date(today)
        due_date = issue_date.__class__.fromordinal(issue_date.toordinal() + item.rental_period(customer))
        rental = Rental(customer_id, sku, issue_date, due_date)
        self.rentals.append(rental)
        return {"rental_id": rental.rental_id, "due_date": self._iso(due_date)}

    def late_fee(self, rental, returned_on):
        item = self.items[rental.sku]
        customer = self.customers[rental.customer_id]
        due = self._date(rental.due_date)
        returned = self._date(returned_on)
        days_late = max(0, (returned - due).days)
        return min(days_late * customer.late_fee_per_day(), item.price)

    @audit
    def return_item(self, rental_id, today):
        rental = next((r for r in self.rentals if r.rental_id == rental_id), None)
        if rental is None:
            raise ItemNotFoundError(rental_id)
        item = self.items[rental.sku]
        customer = self.customers[rental.customer_id]
        due = self._date(rental.due_date)
        returned = self._date(today)
        days_late = max(0, (returned - due).days)
        fee = self.late_fee(rental, returned)
        rental.return_date = returned
        self.unpaid_fines[rental.customer_id] = self.unpaid_fines.get(rental.customer_id, 0) + fee

        waiting = self.waiting_lists.setdefault(rental.sku, deque())
        next_customer = None
        if waiting:
            next_customer_id = waiting.popleft()
            next_customer = self.customers[next_customer_id].name
        return {
            "rental_id": rental_id,
            "customer": customer.name,
            "item": item.name,
            "days_late": days_late,
            "fee": fee,
            "next_in_waiting_list": next_customer,
        }

    @audit
    def extend(self, rental_id, today=None):
        rental = next((r for r in self.rentals if r.rental_id == rental_id), None)
        if rental is None:
            raise ItemNotFoundError(rental_id)
        item = self.items[rental.sku]
        if isinstance(item, Accessory):
            raise ExtensionNotAllowedError(rule="R2")
        waiting = self.waiting_lists.setdefault(rental.sku, deque())
        if waiting:
            raise ExtensionNotAllowedError(
                f"'{item.name}' cannot be extended because another customer is waiting."
            )
        if rental.extension_count >= 2:
            raise ExtensionNotAllowedError(f"'{item.name}' has already been extended 2 times.")

        customer = self.customers[rental.customer_id]
        due = self._date(rental.due_date)
        due = due.__class__.fromordinal(due.toordinal() + item.rental_period(customer))
        rental.due_date = due
        rental.extension_count += 1
        return {"extension_count": rental.extension_count, "due_date": self._iso(due)}

    def join_waiting_list(self, customer_id, sku):
        if customer_id not in self.customers:
            raise CustomerNotFoundError(customer_id)
        if sku not in self.items:
            raise ItemNotFoundError(sku)
        waiting = self.waiting_lists.setdefault(sku, deque())
        if customer_id in waiting:
            return len(waiting)
        waiting.append(customer_id)
        return list(waiting).index(customer_id) + 1

    def customer_rentals(self, customer_id, today):
        if customer_id not in self.customers:
            raise CustomerNotFoundError(customer_id)
        return [rental for rental in self.rentals if rental.customer_id == customer_id]

    def overdue_report(self, today):
        rows = sorted(list(self.iter_overdue(today)), key=lambda row: row["days_late"], reverse=True)
        return rows

    def iter_overdue(self, today):
        today = self._date(today)
        for rental in self.rentals:
            if rental.return_date is not None:
                continue
            due = self._date(rental.due_date)
            days_late = max(0, (today - due).days)
            if days_late > 0:
                yield {
                    "rental": rental,
                    "days_late": days_late,
                    "fine": self.late_fee(rental, today),
                }

    def overdue_report_text(self, today):
        rows = self.overdue_report(today)
        lines = ["Overdue rentals as of " + self._iso(today)]
        lines.append("RENTAL  CUSTOMER     ITEM             DUE         DAYS  FINE SO FAR")
        lines.extend(
            [
                "{rental_id}   {customer:<11}  {item}   {due}  {days}     {fine}".format(
                    rental_id=row["rental"].rental_id,
                    customer=self.customers[row["rental"].customer_id].name,
                    item=self.items[row["rental"].sku].name,
                    due=self._iso(row["rental"].due_date),
                    days=row["days_late"],
                    fine=f"₹{row['fine']}",
                )
                for row in rows
            ]
        )
        total_fines = sum(row["fine"] for row in rows)
        lines.append(f"Total overdue: {len(rows)}   Fines so far: ₹{total_fines}")
        return "\n".join(lines)

    def format_overdue_report(self, today):
        return self.overdue_report_text(today)

    def items_by_category(self):
        categories = {}
        for item in self.items.values():
            category = item.parent_category or item.category
            categories.setdefault(category, []).append(item)
        return {
            category: sorted([item.name for item in categories[category]])
            for category in sorted(categories, key=lambda name: name)
        }

    def customers_with_unpaid_fines(self):
        return {
            customer_id: amount
            for customer_id, amount in sorted(
                self.unpaid_fines.items(), key=lambda pair: pair[0]
            )
            if amount > 0
        }
