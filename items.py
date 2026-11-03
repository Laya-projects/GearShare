"""GearShare item models."""

from abc import ABC, abstractmethod

from errors import InvalidSKUError


class GearItem(ABC):
    """Abstract base class for rentable and display gear."""

    def __init__(
        self,
        sku,
        name,
        tags="",
        category="",
        parent_category="",
        weight_g=0,
        price=0,
        total_units=1,
    ):
        self.sku = sku
        self.name = name
        self.tags = tags
        self.category = category
        self.parent_category = parent_category
        self.weight_g = weight_g
        self.price = price
        self.total_units = total_units

    @property
    def sku(self):
        return self._sku

    @sku.setter
    def sku(self, value):
        if not isinstance(value, str) or len(value) != 10 or not value.isdigit():
            raise InvalidSKUError("SKU must be exactly 10 digits.")
        self._sku = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Item name cannot be blank.")
        self._name = value.strip()

    @property
    def total_units(self):
        return self._total_units

    @total_units.setter
    def total_units(self, value):
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError("Item units cannot be negative.")
        self._total_units = value

    units = total_units

    @abstractmethod
    def is_rentable(self):
        """Return whether this item type can be rented."""

    @abstractmethod
    def rental_period(self, customer):
        """Return the number of days this item can be rented."""

    def __repr__(self):
        return (
            f"{type(self).__name__}(sku={self.sku!r}, name={self.name!r}, "
            f"tags={self.tags!r}, category={self.category!r}, "
            f"parent_category={self.parent_category!r}, weight_g={self.weight_g!r}, "
            f"price={self.price!r}, total_units={self.total_units!r})"
        )

    def __str__(self):
        return f"{self.name} ({self.sku})"


class Equipment(GearItem):
    def is_rentable(self):
        return True

    def rental_period(self, customer):
        return customer.rental_period()

    def __repr__(self):
        return super().__repr__()


class Accessory(GearItem):
    def is_rentable(self):
        return True

    def rental_period(self, customer):
        return 2

    def __repr__(self):
        return super().__repr__()


class DisplayItem(GearItem):
    def is_rentable(self):
        return False

    def rental_period(self, customer):
        return 0

    def __repr__(self):
        return super().__repr__()
