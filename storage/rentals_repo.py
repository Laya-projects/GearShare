from datetime import datetime

from rentals import Rental


def date_value(value):
    if value is None or value == "":
        return None
    if hasattr(value, "year"):
        return value
    return datetime.strptime(value, "%Y-%m-%d").date()


class RentalsRepository:
    def __init__(self, connection):
        self.connection = connection

    def all(self):
        rows = self.connection.execute(
            """SELECT rental_id, customer_id, sku, issue_date, due_date,
                      return_date, extensions
               FROM rentals
               ORDER BY rental_id"""
        ).fetchall()
        return [
            Rental(
                row["customer_id"],
                row["sku"],
                date_value(row["issue_date"]),
                date_value(row["due_date"]),
                date_value(row["return_date"]),
                rental_id=row["rental_id"],
                extension_count=row["extensions"],
            )
            for row in rows
        ]

    def fine_count(self):
        return self.connection.execute(
            "SELECT COUNT(*) FROM fines"
        ).fetchone()[0]

    def insert(self, rental):
        self.connection.execute(
            """INSERT INTO rentals
               (rental_id, customer_id, sku, issue_date, due_date, return_date, extensions)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                rental.rental_id, rental.customer_id, rental.sku,
                GearShareDate(rental.issue_date), GearShareDate(rental.due_date),
                GearShareDate(rental.return_date), rental.extension_count,
            ),
        )

    def update(self, rental):
        self.connection.execute(
            """UPDATE rentals
               SET customer_id = ?, sku = ?, issue_date = ?, due_date = ?,
                   return_date = ?, extensions = ?
               WHERE rental_id = ?""",
            (
                rental.customer_id, rental.sku, GearShareDate(rental.issue_date),
                GearShareDate(rental.due_date), GearShareDate(rental.return_date),
                rental.extension_count, rental.rental_id,
            ),
        )

    def delete(self, rental_id):
        self.connection.execute(
            "DELETE FROM audit_log WHERE rental_id = ?",
            (rental_id,),
        )
        self.connection.execute("DELETE FROM rentals WHERE rental_id = ?", (rental_id,))

    def audit(self, action, customer_id, sku, rental_id, created_on):
        self.connection.execute(
            """INSERT INTO audit_log
               (action, customer_id, sku, created_on, rental_id)
               VALUES (?, ?, ?, ?, ?)""",
            (action, customer_id, sku, GearShareDate(created_on), rental_id),
        )

    def save_fine(self, rental_id, amount):
        if amount <= 0:
            return
        existing = self.connection.execute(
            "SELECT fine_id FROM fines WHERE rental_id = ?",
            (rental_id,),
        ).fetchone()
        if existing is None:
            fine_id = self.connection.execute(
                "SELECT COALESCE(MAX(fine_id), 0) + 1 FROM fines"
            ).fetchone()[0]
            self.connection.execute(
                "INSERT INTO fines (fine_id, rental_id, amount, paid) VALUES (?, ?, ?, 0)",
                (fine_id, rental_id, amount),
            )
        else:
            self.connection.execute(
                "UPDATE fines SET amount = ?, paid = 0 WHERE rental_id = ?",
                (amount, rental_id),
            )

    def waiting_all(self):
        rows = self.connection.execute(
            """SELECT sku, customer_id
               FROM waiting_list
               ORDER BY sku, waiting_id"""
        ).fetchall()
        result = {}
        for row in rows:
            result.setdefault(row["sku"], []).append(row["customer_id"])
        return result

    def waiting_add(self, sku, customer_id, joined_at):
        if self.connection.execute(
            "SELECT 1 FROM waiting_list WHERE sku = ? AND customer_id = ?",
            (sku, customer_id),
        ).fetchone() is None:
            waiting_id = self.connection.execute(
                "SELECT COALESCE(MAX(waiting_id), 0) + 1 FROM waiting_list"
            ).fetchone()[0]
            self.connection.execute(
                """INSERT INTO waiting_list
                   (waiting_id, sku, customer_id, joined_at, notified)
                   VALUES (?, ?, ?, ?, 0)""",
                (waiting_id, sku, customer_id, GearShareDate(joined_at)),
            )

    def waiting_remove_first(self, sku):
        row = self.connection.execute(
            """SELECT waiting_id, customer_id FROM waiting_list
               WHERE sku = ?
               ORDER BY waiting_id LIMIT 1""",
            (sku,),
        ).fetchone()
        if row is None:
            return None
        self.connection.execute(
            "DELETE FROM waiting_list WHERE waiting_id = ?",
            (row["waiting_id"],),
        )
        return row["customer_id"]

    def waiting_reinsert_first(self, sku, customer_id):
        first_id = self.connection.execute(
            "SELECT COALESCE(MIN(waiting_id), 1) FROM waiting_list WHERE sku = ?",
            (sku,),
        ).fetchone()[0]
        waiting_id = max(1, first_id - 1)
        self.connection.execute(
            """INSERT INTO waiting_list
               (waiting_id, sku, customer_id, joined_at, notified)
               VALUES (?, ?, ?, ?, 0)""",
            (waiting_id, sku, customer_id, "2026-11-03"),
        )


def GearShareDate(value):
    if value is None:
        return None
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)
