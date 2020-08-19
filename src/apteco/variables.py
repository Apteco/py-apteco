from typing import Optional

from apteco.query import (
    SelectorClause,
    normalize_string_input,
    NumericClause,
    normalize_number_input,
    normalize_number_value,
    TextClause,
    normalize_string_value,
    ArrayClause,
    FlagArrayClause,
    DateListClause,
    normalize_date_input,
    DateRangeClause,
    normalize_date_value,
    DateTimeRangeClause,
    normalize_datetime_value,
    general_error_msg_selector,
    general_error_msg_numeric,
    single_value_error_msg_numeric,
    general_error_msg_text,
    single_value_error_msg_text,
    general_error_msg_array,
    general_error_msg_flag_array,
    general_error_msg_date,
    single_value_error_msg_date,
    single_value_error_msg_datetime,
)


class Variable:
    """Class representing a FastStats system variable."""

    def __init__(
        self,
        name: str,
        description: str,
        type: str,
        folder_name: str,
        table: "Table",
        is_selectable: bool,
        is_browsable: bool,
        is_exportable: bool,
        is_virtual: bool,
        *,
        session: Optional["Session"] = None,
        **kwargs,
    ):
        self.name = name
        self.description = description
        self._model_type = type
        self.folder_name = folder_name
        self.table = table
        self.is_selectable = is_selectable
        self.is_browsable = is_browsable
        self.is_exportable = is_exportable
        self.is_virtual = is_virtual
        self.session = session

    @property
    def table_name(self):
        return self.table.name


class BaseSelectorVariable(Variable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        selector_info = kwargs["selector_info"]  # type: aa.SelectorVariableInfo
        self.code_length = selector_info.code_length
        self.num_codes = selector_info.number_of_codes
        self.var_code_min_count = selector_info.minimum_var_code_count
        self.var_code_max_count = selector_info.maximum_var_code_count
        self.var_code_order = selector_info.var_code_order


class SelectorVariable(BaseSelectorVariable):
    """Class representing a FastStats Selector variable."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "Selector"

    def __eq__(self: "SelectorVariable", other):
        return SelectorClause(
            self,
            normalize_string_input(other, general_error_msg_selector),
            session=self.session,
        )

    def __ne__(self: "SelectorVariable", other):
        return SelectorClause(
            self,
            normalize_string_input(other, general_error_msg_selector),
            include=False,
            session=self.session,
        )


class CombinedCategoriesVariable(BaseSelectorVariable):
    """Class representing a FastStats Combined Categories variable."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "CombinedCategories"
        selector_info = kwargs["selector_info"]  # type: aa.SelectorVariableInfo
        self.combined_from = selector_info.combined_from_variable_name

    def __eq__(self: "CombinedCategoriesVariable", other):
        raise NotImplementedError

    def __ne__(self: "CombinedCategoriesVariable", other):
        raise NotImplementedError


class NumericVariable(Variable):
    """Class representing a FastStats Numeric variable."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "Numeric"
        numeric_info = kwargs["numeric_info"]  # type: aa.NumericVariableInfo
        self.min = numeric_info.minimum
        self.max = numeric_info.maximum
        self.is_currency = numeric_info.is_currency
        self.currency_locale = numeric_info.currency_locale
        self.currency_symbol = numeric_info.currency_symbol

    def __eq__(self: "NumericVariable", other):
        return NumericClause(
            self,
            normalize_number_input(other, general_error_msg_numeric),
            session=self.session,
        )

    def __ne__(self: "NumericVariable", other):
        return NumericClause(
            self,
            normalize_number_input(other, general_error_msg_numeric),
            include=False,
            session=self.session,
        )

    def __lt__(self: "NumericVariable", other):
        return NumericClause(
            self,
            [f"<{normalize_number_value(other, single_value_error_msg_numeric)}"],
            session=self.session,
        )

    def __le__(self: "NumericVariable", other):
        return NumericClause(
            self,
            [f"<={normalize_number_value(other, single_value_error_msg_numeric)}"],
            session=self.session,
        )

    def __gt__(self: "NumericVariable", other):
        return NumericClause(
            self,
            [f">{normalize_number_value(other, single_value_error_msg_numeric)}"],
            session=self.session,
        )

    def __ge__(self: "NumericVariable", other):
        return NumericClause(
            self,
            [f">={normalize_number_value(other, single_value_error_msg_numeric)}"],
            session=self.session,
        )


class TextVariable(Variable):
    """Class representing a FastStats Text variable."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "Text"
        text_info = kwargs["text_info"]  # type: aa.TextVariableInfo
        self.max_length = text_info.maximum_text_length

    def __eq__(self: "TextVariable", other):
        return TextClause(
            self,
            normalize_string_input(other, general_error_msg_text),
            session=self.session,
        )

    def __ne__(self: "TextVariable", other):
        return TextClause(
            self,
            normalize_string_input(other, general_error_msg_text),
            include=False,
            session=self.session,
        )

    def __le__(self: "TextVariable", other):
        return TextClause(
            self,
            [f'<="{normalize_string_value(other, single_value_error_msg_text)}"'],
            "Ranges",
            session=self.session,
        )

    def __ge__(self: "TextVariable", other):
        return TextClause(
            self,
            [f'>="{normalize_string_value(other, single_value_error_msg_text)}"'],
            "Ranges",
            session=self.session,
        )


class ArrayVariable(BaseSelectorVariable):
    """Class representing a FastStats Array variable."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "Array"

    def __eq__(self: "ArrayVariable", other):
        return ArrayClause(
            self,
            normalize_string_input(other, general_error_msg_array),
            session=self.session,
        )

    def __ne__(self: "ArrayVariable", other):
        return ArrayClause(
            self,
            normalize_string_input(other, general_error_msg_array),
            include=False,
            session=self.session,
        )


class FlagArrayVariable(BaseSelectorVariable):
    """Class representing a FastStats Flag Array variable."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "FlagArray"

    def __eq__(self: "FlagArrayVariable", other):
        return FlagArrayClause(
            self,
            normalize_string_input(other, general_error_msg_flag_array),
            session=self.session,
        )

    def __ne__(self: "FlagArrayVariable", other):
        return FlagArrayClause(
            self,
            normalize_string_input(other, general_error_msg_flag_array),
            include=False,
            session=self.session,
        )


class BaseDateVariable(BaseSelectorVariable):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        selector_info = kwargs["selector_info"]  # type: aa.SelectorVariableInfo
        self.min_date = selector_info.minimum_date
        self.max_date = selector_info.maximum_date


class DateVariable(BaseDateVariable):
    """Class representing a FastStats Date variable."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "Date"

    def __eq__(self: "DateVariable", other):
        return DateListClause(
            self,
            normalize_date_input(other, general_error_msg_date, basic=True),
            session=self.session,
        )

    def __ne__(self: "DateVariable", other):
        return DateListClause(
            self,
            normalize_date_input(other, general_error_msg_date, basic=True),
            include=False,
            session=self.session,
        )

    def __le__(self: "DateVariable", other):
        return DateRangeClause(
            self,
            "Earliest",
            normalize_date_value(other, single_value_error_msg_date),
            session=self.session,
        )

    def __ge__(self: "DateVariable", other):
        return DateRangeClause(
            self,
            normalize_date_value(other, single_value_error_msg_date),
            "Latest",
            session=self.session,
        )


class DateTimeVariable(BaseDateVariable):
    """Class representing a FastStats DateTime variable."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "DateTime"

    def __eq__(self, other):
        raise NotImplementedError

    def __ne__(self, other):
        raise NotImplementedError

    def __le__(self: "DateTimeVariable", other):
        return DateTimeRangeClause(
            self,
            "Earliest",
            normalize_datetime_value(other, single_value_error_msg_datetime),
            session=self.session,
        )

    def __ge__(self: "DateTimeVariable", other):
        return DateTimeRangeClause(
            self,
            normalize_datetime_value(other, single_value_error_msg_datetime),
            "Latest",
            session=self.session,
        )


class ReferenceVariable(Variable):
    """Class representing a FastStats Reference variable."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "Reference"

    def __eq__(self: "ReferenceVariable", other):
        raise NotImplementedError

    def __ne__(self: "ReferenceVariable", other):
        raise NotImplementedError
