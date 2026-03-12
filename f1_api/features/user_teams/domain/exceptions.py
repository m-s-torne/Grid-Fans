"""User Teams domain exceptions."""


class DuplicateDriverError(ValueError):
    """Raised when the same driver appears in more than one team slot."""


class DriverNotInTeamError(ValueError):
    """Raised when a requested driver is not found in the team."""


class DriverAlreadyReserveError(ValueError):
    """Raised when the driver to swap is already the reserve driver."""


class DriverNotFoundError(ValueError):
    """Raised when one or more drivers cannot be found."""


class ConstructorNotFoundError(ValueError):
    """Raised when a constructor cannot be found."""


class BudgetExceededError(ValueError):
    """Raised when the selected team exceeds the allowed budget."""
