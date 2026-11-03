"""GearShare console entry point."""

import os
from datetime import date

from errors import GearShareError, ItemNotAvailableError
from gearshare import GearShare


MENU = """=== GearShare Mini ===
1. List catalogue
2. Search by name or tag
3. Rent
4. Return
5. Extend
6. Join waiting list
7. Customer rentals
8. Overdue report
0. Exit"""


def today_from_environment():
    return os.environ.get("TODAY", date.today().isoformat())


def _date(value):
    return GearShare._date(value)


def print_catalogue(service):
    print("SKU         NAME                       TYPE       AVAILABLE")
    for sku in sorted(service.items):
        item = service.items[sku]
        if not item.is_rentable():
            availability = "not rentable"
        else:
            availability = f"{service._available_units(sku)} of {item.total_units}"
        item_type = {
            "Equipment": "Equipment",
            "DisplayItem": "Display",
            "Accessory": "Accessory",
        }[type(item).__name__]
        print(f"{sku}  {item.name:<27}{item_type:<10} {availability}")


def search(service, query):
    query = query.lower()
    matches = [
        item for item in service.items.values()
        if query in item.name.lower() or query in item.tags.lower()
    ]
    if not matches:
        print(f"No items match '{query}'.")
        return
    label = "result" if len(matches) == 1 else "results"
    print(f"{len(matches)} {label}:")
    for item in sorted(matches, key=lambda value: value.sku):
        tags = ", ".join(item.tags.split(";"))
        availability = (
            "not rentable" if not item.is_rentable()
            else f"{service._available_units(item.sku)} of {item.total_units}"
        )
        print(f"{item.sku}  {item.name} ({tags})  {availability}")


def rent(service, today, input_fn=input):
    customer_id = input_fn("Customer ID: ")
    sku = input_fn("SKU: ")
    try:
        result = service.rent(customer_id.strip(), sku.strip(), today)
        print(f"OK: {service.customers[customer_id].name} rented '{service.items[sku].name}'. Due {result['due_date']}.")
    except ItemNotAvailableError as error:
        print(error.args[0])
        answer = input_fn("Join the waiting list? (y/n): ")
        if answer.strip().lower() == "y":
            item = service.items.get(sku)
            position = service.join_waiting_list(customer_id, sku)
            print(
                f"OK: {service.customers[customer_id].name} is #{position} "
                f"on the waiting list for '{item.name}'."
            )
    except GearShareError as error:
        print(error)


def customer_rentals(service, customer_id, today):
    customer = service.customers.get(customer_id)
    if customer is None:
        print(f"ERROR [CustomerNotFoundError]: No customer with ID {customer_id}.")
        return
    print(
        f"Rentals for {customer.name} ({type(customer).__name__.replace('Customer', '')}: "
        f"{customer.max_items()} items, {customer.rental_period()} days, "
        f"₹{customer.late_fee_per_day()}/day)"
    )
    print("RENTAL  ITEM            ISSUED      DUE         STATUS")
    active = 0
    for rental in service.customer_rentals(customer_id, today):
        item = service.items[rental.sku]
        days_overdue = max(0, (_date(today) - _date(rental.due_date)).days)
        if rental.return_date is None:
            active += 1
            status = f"OVERDUE ({days_overdue} days)" if days_overdue else "On rental"
        else:
            status = "Returned"
        print(
            f"{rental.rental_id}   {item.name:<15} "
            f"{GearShare._iso(rental.issue_date)}  {GearShare._iso(rental.due_date)}  {status}"
        )
    print(f"Active rentals: {active} of {customer.max_items()}")
    print(f"Unpaid fines: ₹{service.unpaid_fines.get(customer_id, 0)}")


def print_overdue(service, today):
    rows = service.overdue_report(today)
    print(f"Overdue rentals as of {GearShare._iso(today)}")
    print("RENTAL  CUSTOMER     ITEM             DUE         DAYS  FINE SO FAR")
    for row in rows:
        rental = row["rental"]
        print(
            f"{rental.rental_id}   {service.customers[rental.customer_id].name:<11}"
            f" {service.items[rental.sku].name:<16} {GearShare._iso(rental.due_date)}  "
            f"{row['days_late']}     ₹{row['fine']}"
        )
    print(f"Total overdue: {len(rows)}   Fines so far: ₹{sum(row['fine'] for row in rows)}")


def run_menu(service, today, input_fn=input):
    print(MENU)
    while True:
        choice = input_fn("> ").strip()
        try:
            if choice == "":
                raise ValueError
            if choice == "0":
                return
            if choice == "1":
                print_catalogue(service)
            elif choice == "2":
                search(service, input_fn("Search: "))
            elif choice == "3":
                rent(service, today, input_fn)
            elif choice == "4":
                rental_id = input_fn("Rental ID: ")
                result = service.return_item(rental_id.strip(), today)
                print(
                    f"OK: {result['customer']} returned '{result['item']}'. "
                    + ("Returned on time. Fee: ₹0." if result["days_late"] == 0 else
                       f"Late by {result['days_late']} days. Fee: ₹{result['fee']}.")
                )
                if result["next_in_waiting_list"]:
                    print(f"Next on waiting list: {result['next_in_waiting_list']}.")
            elif choice == "5":
                rental_id = input_fn("Rental ID: ").strip()
                result = service.extend(rental_id, today)
                print(
                    f"OK: Extended '{service.items[next(r.sku for r in service.rentals if r.rental_id == rental_id)].name}' "
                    f"(extension {result['extension_count']} of 2). New due date {result['due_date']}."
                )
            elif choice == "6":
                customer_id = input_fn("Customer ID: ").strip()
                sku = input_fn("SKU: ").strip()
                position = service.join_waiting_list(customer_id, sku)
                print(
                    f"OK: {service.customers[customer_id].name} is #{position} "
                    f"on the waiting list for '{service.items[sku].name}'."
                )
            elif choice == "7":
                customer_rentals(service, input_fn("Customer ID: ").strip(), today)
            elif choice == "8":
                print_overdue(service, today)
            else:
                print("Please enter a number from 0 to 8.")
        except ValueError:
            print("Please enter a number from 0 to 8.")
        except GearShareError as error:
            print(error)
        finally:
            pass


def main():
    today = today_from_environment()
    service = GearShare()
    service.load_data()
    counts = (
        len(service.items),
        len(service.customers),
        len(service.rentals),
        sum(1 for _ in open(service.data_dir / "fines.csv", encoding="utf-8")) - 1,
    )
    print(f"Loaded {counts[0]} items, {counts[1]} customers, {counts[2]} rentals, {counts[3]} fines.")
    print(f"Today is {today}.")
    print()
    run_menu(service, today)


if __name__ == "__main__":
    main()
