"""GearShare customer models."""

from abc import ABC, abstractmethod


class Customer(ABC):
    """Abstract base class for customers with membership policies."""

    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Customer name cannot be blank.")
        self._name = value.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not isinstance(value, str) or "@" not in value:
            raise ValueError("Customer email must contain '@'.")
        self._email = value.strip()

    @abstractmethod
    def max_items(self):
        """Return the maximum number of items this customer may rent."""

    @abstractmethod
    def rental_period(self):
        """Return the equipment rental period for this customer."""

    @abstractmethod
    def late_fee_per_day(self):
        """Return the customer's daily late fee."""

    def __repr__(self):
        return (
            f"{type(self).__name__}(customer_id={self.customer_id!r}, "
            f"name={self.name!r}, email={self.email!r})"
        )

    def __str__(self):
        return f"{self.name} ({self.customer_id})"


class BasicCustomer(Customer):
    def max_items(self):
        return 2

    def rental_period(self):
        return 3

    def late_fee_per_day(self):
        return 50


class PlusCustomer(Customer):
    def max_items(self):
        return 4

    def rental_period(self):
        return 5

    def late_fee_per_day(self):
        return 100


class ProCustomer(Customer):
    def max_items(self):
        return 8

    def rental_period(self):
        return 7

    def late_fee_per_day(self):
        return 150
