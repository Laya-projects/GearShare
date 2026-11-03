"""GearShare rental models."""


class Rental:
    # Class-level counter: it identifies new rentals globally, not one rental.
    _next_number = 11

    def __init__(
        self,
        customer_id,
        sku,
        issue_date,
        due_date,
        return_date=None,
        rental_id=None,
        extension_count=0,
    ):
        # Instance fields belong to one rental and vary for every rental.
        self.customer_id = customer_id
        self.sku = sku
        self.issue_date = issue_date
        self.due_date = due_date
        self.return_date = return_date
        self.extension_count = extension_count
        if rental_id is not None:
            self.rental_id = rental_id
        else:
            self.rental_id = f"RN{type(self)._next_number:03d}"
            type(self)._next_number += 1

    def __repr__(self):
        return (
            f"Rental(rental_id={self.rental_id!r}, customer_id={self.customer_id!r}, "
            f"sku={self.sku!r}, issue_date={self.issue_date!r}, due_date={self.due_date!r}, "
            f"return_date={self.return_date!r}, extension_count={self.extension_count!r})"
        )

    def __str__(self):
        return f"{self.rental_id}: {self.customer_id} rented {self.sku}"
