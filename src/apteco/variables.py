from typing import Iterable, Mapping, Optional

import apteco_api as aa

from apteco.query import (
    ArrayClause,
    DateListClause,
    DateRangeClause,
    DateTimeRangeClause,
    FlagArrayClause,
    NumericClause,
    SelectorClause,
    TextClause,
    general_error_msg_array,
    general_error_msg_date,
    general_error_msg_flag_array,
    general_error_msg_numeric,
    general_error_msg_selector,
    general_error_msg_text,
    normalize_date_input,
    normalize_date_value,
    normalize_datetime_value,
    normalize_number_input,
    normalize_number_value,
    normalize_string_input,
    normalize_string_value,
    single_value_error_msg_date,
    single_value_error_msg_datetime,
    single_value_error_msg_numeric,
    single_value_error_msg_text,
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

    def __eq__(self, other):
        return SelectorClause(
            self,
            normalize_string_input(other, general_error_msg_selector),
            session=self.session,
        )

    def __ne__(self, other):
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

    def __eq__(self, other):
        raise NotImplementedError

    def __ne__(self, other):
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

    def __eq__(self, other):
        return NumericClause(
            self,
            normalize_number_input(other, general_error_msg_numeric),
            session=self.session,
        )

    def __ne__(self, other):
        return NumericClause(
            self,
            normalize_number_input(other, general_error_msg_numeric),
            include=False,
            session=self.session,
        )

    def __lt__(self, other):
        return NumericClause(
            self,
            [f"<{normalize_number_value(other, single_value_error_msg_numeric)}"],
            session=self.session,
        )

    def __le__(self, other):
        return NumericClause(
            self,
            [f"<={normalize_number_value(other, single_value_error_msg_numeric)}"],
            session=self.session,
        )

    def __gt__(self, other):
        return NumericClause(
            self,
            [f">{normalize_number_value(other, single_value_error_msg_numeric)}"],
            session=self.session,
        )

    def __ge__(self, other):
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

    def equals(self, value, match_case=True, *, include=True, label=None):
        return TextClause(
            self,
            normalize_string_input(value, general_error_msg_text),
            match_type="Is",
            match_case=match_case,
            include=include,
            label=label,
            session=self.session,
        )

    def contains(self, value, match_case=True, *, include=True, label=None):
        return TextClause(
            self,
            normalize_string_input(value, general_error_msg_text),
            match_type="Contains",
            match_case=match_case,
            include=include,
            label=label,
            session=self.session,
        )

    def startswith(self, value, match_case=True, *, include=True, label=None):
        return TextClause(
            self,
            normalize_string_input(value, general_error_msg_text),
            match_type="Begins",
            match_case=match_case,
            include=include,
            label=label,
            session=self.session,
        )

    def endswith(self, value, match_case=True, *, include=True, label=None):
        return TextClause(
            self,
            normalize_string_input(value, general_error_msg_text),
            match_type="Ends",
            match_case=match_case,
            include=include,
            label=label,
            session=self.session,
        )

    # def before(self, value, *, include=True, label=None):
    #     return TextClause(
    #         self,
    #         [f'<="{normalize_string_value(value, single_value_error_msg_text)}"'],
    #         match_type="Ranges",
    #         include=include,
    #         label=label,
    #         session=self.session,
    #     )
    #
    # def after(self, value, *, include=True, label=None):
    #     return TextClause(
    #         self,
    #         [f'>="{normalize_string_value(value, single_value_error_msg_text)}"'],
    #         match_type="Ranges",
    #         include=include,
    #         label=label,
    #         session=self.session,
    #     )

    def between(self, start, end, *, include=True, label=None):
        normalized_start = normalize_string_value(start, single_value_error_msg_text)
        normalized_end = normalize_string_value(end, single_value_error_msg_text)
        return TextClause(
            self,
            [f'>="{normalized_start}" - <="{normalized_end}"'],
            match_type="Ranges",
            include=include,
            label=label,
            session=self.session,
        )

    def matches(self, value, match_case=True, *, include=True, label=None):
        normalized_input = normalize_string_input(value, general_error_msg_text)
        return TextClause(
            self,
            [f'="{v}"' for v in normalized_input],
            match_type="Ranges",
            match_case=match_case,
            include=include,
            label=label,
            session=self.session,
        )

    def __eq__(self, other):
        return self.equals(other, include=True)

    def __ne__(self, other):
        return self.equals(other, include=False)

    # def __le__(self, other):
    #     return self.before(other)
    #
    # def __ge__(self, other):
    #     return self.after(other)


class ArrayVariable(BaseSelectorVariable):
    """Class representing a FastStats Array variable."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type = "Array"

    def __eq__(self, other):
        return ArrayClause(
            self,
            normalize_string_input(other, general_error_msg_array),
            session=self.session,
        )

    def __ne__(self, other):
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

    def __eq__(self, other):
        return FlagArrayClause(
            self,
            normalize_string_input(other, general_error_msg_flag_array),
            session=self.session,
        )

    def __ne__(self, other):
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

    def __eq__(self, other):
        return DateListClause(
            self,
            normalize_date_input(other, general_error_msg_date, basic=True),
            session=self.session,
        )

    def __ne__(self, other):
        return DateListClause(
            self,
            normalize_date_input(other, general_error_msg_date, basic=True),
            include=False,
            session=self.session,
        )

    def __le__(self, other):
        return DateRangeClause(
            self,
            "Earliest",
            normalize_date_value(other, single_value_error_msg_date),
            session=self.session,
        )

    def __ge__(self, other):
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

    def __le__(self, other):
        return DateTimeRangeClause(
            self,
            "Earliest",
            normalize_datetime_value(other, single_value_error_msg_datetime),
            session=self.session,
        )

    def __ge__(self, other):
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

    def __eq__(self, other):
        raise NotImplementedError

    def __ne__(self, other):
        raise NotImplementedError


class VariablesAccessor:
    """List-like and dictionary-like access for variables."""

    def __init__(self, variables: Iterable[Variable]):
        self._variables = list(variables)
        self._variables_by_name = {var.name: var for var in self._variables}
        self._variables_by_desc = {var.description: var for var in self._variables}
        self.names = VariableNamesAccessor(self._variables_by_name)
        self.descs = VariableDescsAccessor(self._variables_by_desc)

    @property
    def descriptions(self):
        """Alias of ``descs``"""
        return self.descs

    def __len__(self):
        return len(self._variables)

    def __iter__(self):
        return iter(self._variables)

    def __getitem__(self, item):
        name_match = self._variables_by_name.get(item)
        desc_match = self._variables_by_desc.get(item)
        match_count = (name_match is not None) + (desc_match is not None)
        if match_count == 1:
            return name_match or desc_match
        elif match_count == 2:
            if name_match.name == desc_match.name:
                return name_match
            raise KeyError(f"Lookup key '{item}' was ambiguous.") from None
        else:
            raise KeyError(
                f"Lookup key '{item}' did not match a variable name or description."
            ) from None


class VariableNamesAccessor:
    """Dictionary-like access for variables by name."""

    def __init__(self, variables_by_name: Mapping[str, Variable]):
        self._variables_by_name = dict(variables_by_name)
        self._variable_names = list(self._variables_by_name.keys())

    def __iter__(self):
        return iter(self._variable_names)

    def __getitem__(self, item):
        try:
            return self._variables_by_name[item]
        except KeyError:
            raise KeyError(
                f"Lookup key '{item}' did not match a variable name."
            ) from None


class VariableDescsAccessor:
    """Dictionary-like access for variables by description."""

    def __init__(self, variables_by_desc: Mapping[str, Variable]):
        self._variables_by_desc = dict(variables_by_desc)
        self._variable_descs = list(self._variables_by_desc.keys())

    def __iter__(self):
        return iter(self._variable_descs)

    def __getitem__(self, item):
        try:
            return self._variables_by_desc[item]
        except KeyError as exc:
            raise KeyError(
                f"Lookup key '{item}' did not match a variable description."
            ) from None
