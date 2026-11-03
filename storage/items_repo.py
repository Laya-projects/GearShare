from customers import BasicCustomer, PlusCustomer, ProCustomer
from items import Accessory, DisplayItem, Equipment


class ItemsRepository:
    def __init__(self, connection):
        self.connection = connection

    def all(self):
        rows = self.connection.execute(
            """SELECT i.*, c.name AS category, parent.name AS parent_category,
                      GROUP_CONCAT(t.name, ';') AS tags
               FROM items i
               JOIN categories c ON c.category_id = i.category_id
               LEFT JOIN categories parent ON parent.category_id = c.parent_id
               LEFT JOIN item_tags it ON it.sku = i.sku
               LEFT JOIN tags t ON t.tag_id = it.tag_id
               GROUP BY i.sku"""
        ).fetchall()
        result = {}
        for row in rows:
            item_type = {
                "Accessory": Accessory,
                "Display": DisplayItem,
            }.get(row["item_type"], Equipment)
            item = item_type(
                row["sku"], row["name"], row["tags"] or "",
                row["category"], row["parent_category"] or "",
                row["weight_g"], row["price"], row["total_units"],
            )
            result[item.sku] = item
        return result
