"""Test that algorithm identifies the correct variable class
to create py-apteco variables from raw apteco-api variables."""

from apteco.session import (
    ArrayVariable,
    CombinedCategoriesVariable,
    DateTimeVariable,
    DateVariable,
    FlagArrayVariable,
)
from apteco.session import InitializeVariablesAlgorithm as IVA
from apteco.session import (
    NumericVariable,
    ReferenceVariable,
    SelectorVariable,
    TextVariable,
)


def test_selector_var(mocker):
    raw_selector_var = mocker.Mock(
        type="Selector",
        selector_info=mocker.Mock(
            sub_type="Categorical",
            selector_type="SingleValue",
            combined_from_variable_name=None,
        ),
    )
    assert IVA._choose_variable(raw_selector_var) == SelectorVariable


def test_combined_categories_var(mocker):
    raw_combined_cat_var = mocker.Mock(
        type="Selector",
        selector_info=mocker.Mock(
            sub_type="Categorical",
            selector_type="SingleValue",
            combined_from_variable_name="my_original_variable",
        ),
    )
    assert IVA._choose_variable(raw_combined_cat_var) == CombinedCategoriesVariable


def test_numeric_var(mocker):
    raw_numeric_var = mocker.Mock(type="Numeric")
    assert IVA._choose_variable(raw_numeric_var) == NumericVariable


def test_text_var(mocker):
    raw_text_var = mocker.Mock(type="Text")
    assert IVA._choose_variable(raw_text_var) == TextVariable


def test_array_var(mocker):
    raw_array_var = mocker.Mock(
        type="Selector",
        selector_info=mocker.Mock(sub_type="Categorical", selector_type="OrArray"),
    )
    assert IVA._choose_variable(raw_array_var) == ArrayVariable


def test_flag_array_var(mocker):
    raw_flag_array_var = mocker.Mock(
        type="Selector",
        selector_info=mocker.Mock(sub_type="Categorical", selector_type="OrBitArray"),
    )
    assert IVA._choose_variable(raw_flag_array_var) == FlagArrayVariable


def test_date_var(mocker):
    raw_date_var = mocker.Mock(
        type="Selector", selector_info=mocker.Mock(sub_type="Date")
    )
    assert IVA._choose_variable(raw_date_var) == DateVariable


def test_datetime_var(mocker):
    raw_date_var = mocker.Mock(
        type="Selector", selector_info=mocker.Mock(sub_type="DateTime")
    )
    assert IVA._choose_variable(raw_date_var) == DateTimeVariable


def test_reference_var(mocker):
    raw_reference_var = mocker.Mock(type="Reference")
    assert IVA._choose_variable(raw_reference_var) == ReferenceVariable
