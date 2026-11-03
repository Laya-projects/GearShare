class Node:
    def __init__(self, rental_id, next_node=None):
        self.rental_id = rental_id
        self.next = next_node


class RentalHistory:
    def __init__(self, head=None):
        self.head = head

    def insert_at_head(self, rental_id):
        self.head = Node(rental_id, self.head)

    def traversal(self):
        current = self.head
        while current is not None:
            yield current.rental_id
            current = current.next

    def delete(self, rental_id):
        previous = None
        current = self.head
        while current is not None:
            if current.rental_id == rental_id:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next
                return True
            previous = current
            current = current.next
        return False

    def reverse(self):
        previous = None
        current = self.head
        while current is not None:
            following = current.next
            current.next = previous
            previous = current
            current = following
        self.head = previous

    def second_from_end(self):
        if self.head is None or self.head.next is None:
            return None
        slow = self.head
        fast = self.head.next
        while fast.next is not None:
            slow = slow.next
            fast = fast.next
        return slow.rental_id


def build_customer_history(customer_id, rentals):
    history = RentalHistory()
    customer_rentals = [
        rental for rental in rentals
        if (rental.customer_id if hasattr(rental, "customer_id") else rental["customer_id"]) == customer_id
    ]
    customer_rentals.sort(
        key=lambda rental: (
            rental.issue_date if hasattr(rental, "issue_date") else rental["issue_date"]
        )
    )
    for rental in customer_rentals:
        history.insert_at_head(
            rental.rental_id if hasattr(rental, "rental_id") else rental["rental_id"]
        )
    return history
