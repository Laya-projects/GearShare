from functools import wraps


def audit(method):
    @wraps(method)
    def wrapped(self, *args, **kwargs):
        result = method(self, *args, **kwargs)
        today = kwargs.get("today")
        if today is None and method.__name__ == "rent":
            today = args[2] if len(args) > 2 else None
        elif today is None and method.__name__ == "extend":
            today = kwargs.get("today", args[1] if len(args) > 1 else None)

        action = method.__name__
        customer_name = ""
        item_name = ""
        if method.__name__ == "rent":
            customer_name = self.customers[args[0] if args else kwargs["customer_id"]].name
            sku = args[1] if len(args) > 1 else kwargs["sku"]
            item_name = self.items[sku].name
        elif method.__name__ == "return_item":
            rental_id = args[0] if args else kwargs["rental_id"]
            rental = next(r for r in self.rentals if r.rental_id == rental_id)
            customer_name = self.customers[rental.customer_id].name
            item_name = self.items[rental.sku].name
            if today is None and len(args) > 1:
                today = args[1]
        elif method.__name__ == "extend":
            rental_id = args[0] if args else kwargs["rental_id"]
            rental = next(r for r in self.rentals if r.rental_id == rental_id)
            customer_name = self.customers[rental.customer_id].name
            item_name = self.items[rental.sku].name

        self.audit.append({
            "time": self._iso(today),
            "action": action,
            "customer": customer_name,
            "item": item_name,
        })
        return result

    return wrapped
