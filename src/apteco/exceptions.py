"""Exceptions raised by the py-apteco package."""


class AptecoException(Exception):
    """Base exception class for all exceptions in the package."""


class ApiResultsError(Exception):
    """Raised when API returns inconsistent or unexpected results."""


class AptecoTablesError(Exception):
    """Raised when error occurs initialising tables data or tree."""
