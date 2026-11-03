import random

from customers import BasicCustomer
from gearshare import GearShare
from items import Accessory, DisplayItem, Equipment


def generate_items(n, seed=2026):
    random.seed(seed)
    categories = ["Cameras", "Lenses", "Drones", "Accessories", "Showcase"]
    item_types = [("Equipment", Equipment), ("Accessory", Accessory), ("Display", DisplayItem)]
    items = {}
    for index in range(n):
        category = categories[index % len(categories)]
        item_type_name, item_class = item_types[index % len(item_types)]
        sku = f"{1000000000 + index:010d}"
        tags = f"fake;{category.lower()}"
        weight = random.randint(1, 5000)
        item = item_class(sku, f"Fake {item_type_name} {index:05d}", tags, category, "", weight, 1000 + index, 1)
        items[sku] = item
    return items


def generate_and_load(n, gearshare=None, seed=2026):
    service = gearshare or GearShare()
    service.items = generate_items(n, seed)
    service.skus = set(service.items)
    service.customers = {"CBENCH": BasicCustomer("CBENCH", "Benchmark Customer", "bench@example.com")}
    service.unpaid_fines = {"CBENCH": 0}
    service.waiting_lists = {sku: __import__("collections").deque() for sku in service.items}
    service.rentals = []
    return service
