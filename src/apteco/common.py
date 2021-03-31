from enum import Enum


class VariableType(str, Enum):
    SELECTOR = "Selector"
    # COMBINED_CATEGORIES = "CombinedCategories"
    NUMERIC = "Numeric"
    TEXT = "Text"
    ARRAY = "Array"
    FLAG_ARRAY = "FlagArray"
    DATE = "Date"
    DATETIME = "DateTime"
    REFERENCE = "Reference"


class DimensionType(str, Enum):
    SELECTOR = "Selector"
    BANDED_DATE = "BandedDate"
