from apteco.common import VariableType


def test_variable_type_enum_string_comparison():
    assert VariableType.SELECTOR == "Selector"
    assert VariableType.NUMERIC == "Numeric"
    assert VariableType.TEXT == "Text"
    assert VariableType.ARRAY == "Array"
    assert VariableType.FLAG_ARRAY == "FlagArray"
    assert VariableType.DATE == "Date"
    assert VariableType.DATETIME == "DateTime"
    assert VariableType.REFERENCE == "Reference"


def test_variable_type_enum_contains_string():
    assert "Array" in VariableType.ARRAY
    assert "Array" in VariableType.FLAG_ARRAY
