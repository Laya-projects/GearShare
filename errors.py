"""GearShare custom errors."""


class GearShareError(Exception):
    """Base class for GearShare domain errors."""


class InvalidSKUError(GearShareError):
    """Raised when a SKU is not exactly 10 digits."""


class ItemNotFoundError(GearShareError):
    """Raised when an item does not exist."""


class CustomerNotFoundError(GearShareError):
    """Raised when a customer does not exist."""


class ItemNotRentableError(GearShareError):
    """Raised for R1 display items."""


class UnpaidFinesError(GearShareError):
    """Raised for R4 unpaid fines."""


class RentalLimitExceededError(GearShareError):
    """Raised for R3 rental limits."""


class DuplicateRentalError(GearShareError):
    """Raised for R8 duplicate rentals."""


class ItemNotAvailableError(GearShareError):
    """Raised for R7 unavailable items."""


class ExtensionNotAllowedError(GearShareError):
    """Raised for R2 and R6 extension restrictions."""
