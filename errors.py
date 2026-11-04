"""GearShare custom errors."""


class GearShareError(Exception):
    """Base class for GearShare domain errors."""

    def __init__(self, message=None):
        super().__init__(message or self.default_message)
        self.message = str(self)

    def __str__(self):
        return f"ERROR [{self.prefix}]: {super().__str__()}"

    prefix = "GearShareError"
    default_message = ""


class InvalidSKUError(GearShareError):
    """Raised when a SKU is not exactly 10 digits."""
    prefix = "InvalidSKUError"
    default_message = "SKU must be exactly 10 digits."


class ItemNotFoundError(GearShareError):
    """Raised when an item does not exist."""

    def __init__(self, sku):
        super().__init__(f"No item with SKU {sku}.")
    prefix = "ItemNotFoundError"


class CustomerNotFoundError(GearShareError):
    """Raised when a customer does not exist."""

    def __init__(self, customer_id):
        super().__init__(f"No customer with ID {customer_id}.")
    prefix = "CustomerNotFoundError"


class DuplicateEmailError(GearShareError):
    """Raised when a customer email is already registered."""

    def __init__(self, email):
        super().__init__(f"A customer with email {email} already exists.")
    prefix = "DuplicateEmailError"


class InvalidMembershipError(GearShareError):
    """Raised when a membership type is not supported."""

    prefix = "InvalidMembershipError"
    default_message = "Membership must be Basic, Plus or Pro."


class InvalidCustomerError(GearShareError):
    """Raised for invalid customer name or email values."""

    prefix = "InvalidCustomerError"

    def __init__(self, message):
        super().__init__(message)


class InvalidCategoryError(GearShareError):
    """Raised when an item category does not exist."""

    def __init__(self, category):
        super().__init__(f"Unknown category '{category}'.")
    prefix = "InvalidCategoryError"


class ItemNotRentableError(GearShareError):
    """Raised for R1 display items."""

    def __init__(self, item_name):
        super().__init__(f"'{item_name}' is a display item and cannot be rented.")
    prefix = "R1"


class UnpaidFinesError(GearShareError):
    """Raised for R4 unpaid fines."""

    def __init__(self, customer_name="Customer", amount=501):
        super().__init__(f"{customer_name} has unpaid fines of ₹{amount} (limit ₹500).")
    prefix = "R4"


class RentalLimitExceededError(GearShareError):
    """Raised for R3 rental limits."""

    def __init__(self, customer_name="Customer", active_count=1, maximum=1):
        super().__init__(
            f"{customer_name} already has {active_count} of {maximum} items on rental."
        )
    prefix = "R3"


class DuplicateRentalError(GearShareError):
    """Raised for R8 duplicate rentals."""

    def __init__(self, customer_name="Customer", item_name="Item"):
        super().__init__(f"{customer_name} already has a unit of '{item_name}'.")
    prefix = "R8"


class ItemNotAvailableError(GearShareError):
    """Raised for R7 unavailable items."""

    def __init__(self, item_name):
        super().__init__(f"No units of '{item_name}' are available.")
    prefix = "R7"


class ExtensionNotAllowedError(GearShareError):
    """Raised for R2 and R6 extension restrictions."""

    prefix = "R6"

    def __init__(self, message=None, rule=None):
        if rule == "R2":
            self.prefix = "R2"
            message = "Accessories cannot be extended."
        super().__init__(message)
