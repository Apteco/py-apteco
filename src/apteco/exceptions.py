"""Exceptions raised and warnings issued by the py-apteco package."""

import sys
import warnings


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


class AptecoWarning(Warning):
    """Base class for all warnings in the package."""


# https://docs.python.org/3.7/whatsnew/3.7.html#whatsnew37-pep565
if sys.version_info[:2] < (3, 7):
    deprecation_warning_class = FutureWarning
else:
    deprecation_warning_class = DeprecationWarning


class AptecoDeprecationWarning(deprecation_warning_class, AptecoWarning):
    """Warning about deprecated features."""


def get_deprecated_attr(obj, old_name, new_name, version_deprecated, stacklevel=3):
    """Issue warning for accessing deprecated attribute."""
    warnings.warn(
        f"'{old_name}' is deprecated since py-apteco v{version_deprecated},"
        f" use '{new_name}' instead",
        AptecoDeprecationWarning,
        stacklevel=stacklevel,
    )
    return getattr(obj, new_name)
