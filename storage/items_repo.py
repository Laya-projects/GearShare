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

    def add(self, item):
        category = self.connection.execute(
            "SELECT category_id FROM categories WHERE name = ?",
            (item.category,),
        ).fetchone()
        if category is None:
            raise ValueError(f"Unknown category: {item.category}")

        self.connection.execute(
            """INSERT INTO items
               (sku, name, item_type, weight_g, price, total_units, category_id)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                item.sku,
                item.name,
                type(item).__name__.replace("Item", ""),
                item.weight_g,
                item.price,
                item.total_units,
                category["category_id"],
            ),
        )
        for tag in item.tags.split(";") if item.tags else []:
            tag = tag.strip()
            if not tag:
                continue
            tag_row = self.connection.execute(
                "SELECT tag_id FROM tags WHERE name = ?",
                (tag,),
            ).fetchone()
            if tag_row is None:
                tag_id = self.connection.execute(
                    "SELECT COALESCE(MAX(tag_id), 0) + 1 FROM tags"
                ).fetchone()[0]
                self.connection.execute(
                    "INSERT INTO tags (tag_id, name) VALUES (?, ?)",
                    (tag_id, tag),
                )
            else:
                tag_id = tag_row["tag_id"]
            self.connection.execute(
                """INSERT OR IGNORE INTO item_tags (sku, tag_id)
                   VALUES (?, ?)""",
                (item.sku, tag_id),
            )

    def categories(self):
        rows = self.connection.execute(
            """SELECT leaf.category_id AS id, leaf.name AS name,
                      parent.name AS parent
               FROM categories leaf
               LEFT JOIN categories parent ON parent.category_id = leaf.parent_id
               WHERE leaf.name != 'Photography'
               ORDER BY leaf.name"""
        ).fetchall()
        return [
            {"id": row["id"], "name": row["name"], "parent": row["parent"]}
            for row in rows
        ]

    def category_exists(self, name):
        row = self.connection.execute(
            """SELECT 1 FROM categories
               WHERE name = ?
               AND parent_id IS NOT NULL""",
            (name,),
        ).fetchone()
        if row is None and name in ("Drones", "Tripods", "Audio", "Showcase", "Accessories"):
            row = self.connection.execute(
                "SELECT 1 FROM categories WHERE name = ? AND parent_id IS NULL",
                (name,),
            ).fetchone()
        return row is not None
