"""Exceptions raised by the py-apteco package."""


class AptecoException(Exception):
    """Base exception class for all exceptions in the package."""


class ApiResultsError(AptecoException):
    """Raised when API returns inconsistent or unexpected results."""


class TablesError(AptecoException):
    """Raised when error occurs initialising tables data or tree."""


class VariablesError(AptecoException):
    """Raised when error occurs initialising variables."""


class DeserializeError(AptecoException):
    """Raised when error occurs when deserializing objects."""
