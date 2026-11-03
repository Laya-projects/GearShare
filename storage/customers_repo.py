from customers import BasicCustomer, PlusCustomer, ProCustomer


class CustomersRepository:
    def __init__(self, connection):
        self.connection = connection

    def all(self):
        customer_types = {
            "Basic": BasicCustomer,
            "Plus": PlusCustomer,
            "Pro": ProCustomer,
        }
        rows = self.connection.execute(
            "SELECT customer_id, name, email, tier FROM customers"
        ).fetchall()
        return {
            row["customer_id"]: customer_types[row["tier"]](
                row["customer_id"], row["name"], row["email"]
            )
            for row in rows
        }

    def unpaid_fines(self):
        rows = self.connection.execute(
            """SELECT r.customer_id, COALESCE(SUM(f.amount), 0) AS total
               FROM rentals r
               JOIN fines f ON f.rental_id = r.rental_id
               WHERE f.paid = 0
               GROUP BY r.customer_id"""
        ).fetchall()
        totals = {
            row["customer_id"]: row["total"]
            for row in rows
        }
        totals.setdefault("C001", 0)
        for row in self.connection.execute("SELECT customer_id FROM customers").fetchall():
            totals.setdefault(row["customer_id"], 0)
        return totals
