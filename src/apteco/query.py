from datetime import date, datetime
from decimal import Decimal
from numbers import Real, Integral, Number, Rational
from typing import List, Optional, Iterable

import apteco_api as aa
from apteco.exceptions import AptecoException

DECIMAL_PLACES = 4


class OperationError(AptecoException):
    """Raised when invalid operation attempted on clauses."""
    pass


class InvalidValuesError(AptecoException):
    """Raised when invalid values used in selection query."""
    pass


class SelectionCount(object):

    def __init__(self, count_response):
        self.table_name = count_response.table_name
        self.count = count_response.count_value


class Selection:

    def __init__(self,
                 query: aa.Query,
                 session: "Session"
                 ):

        self.queries_controller = aa.QueriesApi(session.api_client)
        self._response = self._run_query(session.data_view, session.system, query)

        self.counts = []
        self.count_names = []
        for count_dict in self._response.counts:
            new_count = SelectionCount(count_dict)
            self.counts.append(new_count)
            self.count_names.append(new_count.table_name)

        self.count = self.counts[0].count
        self.table_name = self.counts[0].table_name

    def _run_query(self, data_view_name: str, system: str, query: aa.Query):
        """Request a query be counted

        Args:
            data_view_name: dataView that the session is logged in to
            system: system with query
            query: query request

        Returns:
            QuerySimpleResult, unused kwargs

        """

        response = self.queries_controller.queries_perform_query_count_synchronously(
            data_view_name=data_view_name,
            system_name=system,
            query=query
        )

        return response  # type:aa.QueryResult

    def get_count(self, table: str = None) -> int:
        """Get the count for the given table.

        If you pass this with no argument,
        it will return the count of the current resolve table
        (so ``selection.get_count()`` is the same as
        ``selection.count``).

        Args:
            table: the name of the table

        Returns:
            int: the number of records in the selection
            for the given table

        """

        if table is None:
            return self.count
        elif table in self.count_names:
            return self.counts[self.count_names.index(table)].count
        else:
            raise ValueError('Table name not found')

    def set_table(self, table: str) -> None:
        """Set the resolve table level for the selection.

        This changes ``count`` and ``table_name``
        correspondingly.
        This is only available for any tables included
        in ancestor table counts.

        Args:
            table: the name of the table

        """

        if table in self.count_names:
            count_idx = self.count_names.index(table)
            self.count = self.counts[count_idx].count
            self.table_name = self.counts[count_idx].table_name
        else:
            raise ValueError('Table name not found')


# TODO: change name to Controller (confusing with APIClient otherwise)
class APIController:

    def __init__(self, controller, session: "Session"):
        self._controller = controller(session.api_client)

    def __call__(self, function_as_string, **kwargs):
        return getattr(self._controller, function_as_string)(**kwargs)


class TableMixin:

    def select(self):
        query_final = aa.Query(
            selection=aa.Selection(table_name=self.name, ancestor_counts=True)
        )
        session = self.session
        return Selection(query_final, session)


class VariableMixin:

    def __eq__(self, other):
        if isinstance(other, str):
            return criteria_clause(self, [other])
        elif isinstance(other, Iterable):
            return criteria_clause(self, list(other))
        else:
            raise ValueError("Can only set variable equal to to a string or Iterable of strings.")

    def isin(self, values):
        return criteria_clause(self, values)

    # TODO: implement contains method for variables
    def contains(self, needle):
        raise NotImplementedError


def normalize_string_value(value, error_msg):
    if isinstance(value, str):
        return value
    else:
        raise ValueError(error_msg)


def normalize_string_input(input_value, error_msg):
    if isinstance(input_value, str):
        return [normalize_string_value(input_value, error_msg)]
    elif isinstance(input_value, Iterable):
        return [normalize_string_value(v, error_msg) for v in input_value]
    else:
        raise ValueError(error_msg)


def normalize_number_value(value, error_msg):
    if isinstance(value, (Real, Decimal)) and not isinstance(value, bool):
        if isinstance(value, Integral):
            return str(int(value))
        if isinstance(value, Decimal):
            return str(value.quantize(Decimal(10) ** -DECIMAL_PLACES))
        if isinstance(value, (Real, Rational)):
            return str(round(float(value), DECIMAL_PLACES))
    else:
        raise ValueError(error_msg)


def normalize_number_input(input_value, error_msg):
    if isinstance(input_value, Number):
        return [normalize_number_value(input_value, error_msg)]
    elif isinstance(input_value, Iterable) and not isinstance(input_value, str):
        return [normalize_number_value(v, error_msg) for v in input_value]
    else:
        raise ValueError(error_msg)


def normalize_date_value(value, error_msg, *, basic=False):
    if isinstance(value, date):
        if basic:  # format for DateListClause
            return value.strftime("%Y%m%d")
        else:
            return value.strftime("%Y-%m-%d")
    else:
        raise ValueError(error_msg)


def normalize_date_input(input_value, error_msg, *, basic=False):
    if isinstance(input_value, date):
        return [normalize_date_value(input_value, error_msg, basic=basic)]
    elif isinstance(input_value, Iterable) and not isinstance(input_value, str):
        return [normalize_date_value(v, error_msg, basic=basic) for v in input_value]
    else:
        raise ValueError(error_msg)


def normalize_datetime_value(value, error_msg):
    if isinstance(value, datetime):
        return value.isoformat(timespec="seconds")  # "%Y-%m-%dT%H:%M:%S"
    else:
        raise ValueError(error_msg)


def normalize_datetime_input(input_value, error_msg):
    if isinstance(input_value, datetime):
        return [normalize_datetime_value(input_value, error_msg)]
    elif isinstance(input_value, Iterable) and not isinstance(input_value, str):
        return [normalize_datetime_value(v, error_msg) for v in input_value]
    else:
        raise ValueError(error_msg)


class SelectorVariableMixin:
    general_error_msg = (
        "Chosen value(s) for a selector variable"
        " must be given as a string or an iterable of strings."
    )

    def __eq__(self: "SelectorVariable", other):
        return SelectorClause(self.table_name, self.name, normalize_string_input(other, self.general_error_msg), session=self.session)

    def __ne__(self: "SelectorVariable", other):
        return SelectorClause(self.table_name, self.name, normalize_string_input(other, self.general_error_msg), include=False, session=self.session)


class NumericVariableMixin:
    general_error_msg = (
        "Chosen value for a numeric variable"
        " must be a number or an iterable of numbers."
    )
    single_value_error_msg = (
        "Must specify a single number when using inequality operators."
    )

    def __eq__(self: "NumericVariable", other):
        return NumericClause(self.table_name, self.name, normalize_number_input(other, self.general_error_msg), session=self.session)

    def __ne__(self: "NumericVariable", other):
        return NumericClause(self.table_name, self.name, normalize_number_input(other, self.general_error_msg), include=False, session=self.session)

    def __lt__(self: "NumericVariable", other):
        return NumericClause(self.table_name, self.name, [f"<{normalize_number_value(other, self.single_value_error_msg)}"], session=self.session)

    def __le__(self: "NumericVariable", other):
        return NumericClause(self.table_name, self.name, [f"<={normalize_number_value(other, self.single_value_error_msg)}"], session=self.session)

    def __gt__(self: "NumericVariable", other):
        return NumericClause(self.table_name, self.name, [f">{normalize_number_value(other, self.single_value_error_msg)}"], session=self.session)

    def __ge__(self: "NumericVariable", other):
        return NumericClause(self.table_name, self.name, [f">={normalize_number_value(other, self.single_value_error_msg)}"], session=self.session)


class TextVariableMixin:
    general_error_msg = (
        "Chosen value(s) for a text variable"
        " must be given as a string or an iterable of strings."
    )
    single_value_error_msg = (
        "Must specify a single string when using inequality operators."
    )

    def __eq__(self: "TextVariable", other):
        return TextClause(self.table_name, self.name, normalize_string_input(other, self.general_error_msg), session=self.session)

    def __ne__(self: "TextVariable", other):
        return TextClause(self.table_name, self.name, normalize_string_input(other, self.general_error_msg), include=False, session=self.session)

    def __le__(self: "TextVariable", other):
        return TextClause(self.table_name, self.name, [f"<=\"{normalize_string_value(other, self.single_value_error_msg)}\""], "Ranges", session=self.session)

    def __ge__(self: "TextVariable", other):
        return TextClause(self.table_name, self.name, [f">=\"{normalize_string_value(other, self.single_value_error_msg)}\""], "Ranges", session=self.session)


class ArrayVariableMixin:
    general_error_msg = (
        "Chosen value(s) for an array variable"
        " must be given as a string or an iterable of strings."
    )

    def __eq__(self: "ArrayVariable", other):
        return ArrayClause(self.table_name, self.name, normalize_string_input(other, self.general_error_msg), session=self.session)

    def __ne__(self: "ArrayVariable", other):
        return ArrayClause(self.table_name, self.name, normalize_string_input(other, self.general_error_msg), include=False, session=self.session)


class FlagArrayVariableMixin:
    general_error_msg = (
        "Chosen value(s) for a flag array variable"
        " must be given as a string or an iterable of strings."
    )

    def __eq__(self: "FlagArrayVariable", other):
        return FlagArrayClause(self.table_name, self.name, normalize_string_input(other, self.general_error_msg), session=self.session)

    def __ne__(self: "FlagArrayVariable", other):
        return FlagArrayClause(self.table_name, self.name, normalize_string_input(other, self.general_error_msg), include=False, session=self.session)


class ClauseMixin:

    @property
    def table(self):
        return self.session.tables[self.table_name]

    def select(self, table=None):
        if table is not None:
            return (self * table).select()
        query_final = aa.Query(
            selection=aa.Selection(
                table_name=self.table.name, ancestor_counts=True, rule=aa.Rule(
                    clause=self._to_model()
                )
            )
        )
        session = self.table.session
        return Selection(query_final, session)

    def _change_table(self, new_table, simplify=False):

        if simplify:
            return self._strip_table_changes()._change_table_main(new_table)
        else:
            return self._change_table_main(new_table)

    def _change_table_main(self, new_table):
        if self.table < new_table:
            if self.table.parent == new_table:
                return logic_clause('ANY', [self], new_table)
            else:
                return logic_clause('ANY', [self], self.table.parent)._change_table_main(new_table)
        elif self.table > new_table:
            if self.table == new_table.parent:
                return logic_clause('THE', [self], new_table)
            else:
                return logic_clause('THE', [self._change_table_main(new_table.parent)], new_table)
        elif self.table == new_table:
            return self
        else:
            try:
                common_ancestor_names = set(t.name for t in self.table.ancestors) & set(t.name for t in new_table.ancestors)
                nearest_common_ancestor = min(self.table.system_session.tables[name] for name in common_ancestor_names)
            except:
                raise OperationError(
                    "Could not establish relationship between "
                    "new table and current one."
                )
            return self._change_table_main(nearest_common_ancestor)._change_table_main(new_table)

    def _strip_table_changes(self):
        if self.logic is None or self.logic.operation.upper() in ['AND', 'OR', 'NOT']:
            return self
        elif self.logic.operation.upper() in ['ANY', 'THE']:
            if len(self.logic.operands) != 1:
                raise OperationError(
                    f"'{self.logic.operation.upper()}' has invalid "
                    f"number of operands ({len(self.logic.operands)}). "
                    f"Should be 1."
                )
            return self.logic.operands[0]._strip_table_changes()
        else:
            raise OperationError(
                f"Encountered unexpected logic clause "
                f"'{self.logic.operation.upper()}'."
            )

    def __and__(self, other):
        if self.table != other.table:
            return logic_clause('AND', [self, other._change_table(self.table)])
        return logic_clause('AND', [self, other])

    def __or__(self, other):
        if self.table != other.table:
            return logic_clause('OR', [self, other._change_table(self.table)])
        return logic_clause('OR', [self, other])

    def __invert__(self):
        return logic_clause('NOT', [self])

    def __mul__(self, other):
        return self._change_table(other)

    def __rmul__(self, other):
        return self.__mul__(other)


def criteria_clause(variable: "Variable", values: Iterable):
    if variable.type == "Selector":
        return SelectorClause(variable.table_name, variable.name, values, session=variable.session)
    elif variable.type == "CombinedCategories":
        return CombinedCategoriesClause(variable.table_name, variable.name, values, session=variable.session)
    elif variable.type == "Numeric":
        return NumericClause(variable.table_name, variable.name, values, session=variable.session)
    elif variable.type == "Text":
        return TextClause(variable.table_name, variable.name, values, session=variable.session)
    elif variable.type == "Array":
        return ArrayClause(variable.table_name, variable.name, values, session=variable.session)
    elif variable.type == "FlagArray":
        return FlagArrayClause(variable.table_name, variable.name, values, session=variable.session)
    elif variable.type == "Date":
        return DateListClause(variable.table_name, variable.name, values, session=variable.session)
    elif variable.type in ["DateTime", "Reference"]:
        raise AptecoException(f"The variable type '{variable.type}' is not supported for this operation.")
    else:
        raise AptecoException(f"The operation could not be carried out, variable type: '{variable.type}' not recognised.")


class SelectorClauseMixin:

    @staticmethod
    def _verify_values(values: Iterable[str], variable_name: str, session: "Session"):
        systems_controller = APIController(aa.FastStatsSystemsApi, session)

        # TODO: separate this part into a (dynamic) getter for a .values property on the SystemVariable class
        var_codes_raw = []
        offset = 0
        while True:
            var_code_results = systems_controller("fast_stats_systems_get_fast_stats_variable_codes",
                                                  data_view_name=session.data_view,
                                                  system_name=session.system,
                                                  variable_name=variable_name,
                                                  offset=offset)
            var_codes_raw.extend(var_code_results.list)
            if var_code_results.offset + var_code_results.count >= var_code_results.total_count:
                break
            offset = var_code_results.offset + var_code_results.count

        values_by_code = {c.code: c for c in var_codes_raw}
        values_by_desc = {c.description: c for c in var_codes_raw}

        val_set = set(values)
        code_set = set(values_by_code.keys())
        desc_set = set(values_by_desc.keys())
        if val_set <= code_set:
            return sorted(val_set)
        elif val_set <= desc_set:
            return [values_by_desc[desc].code for desc in sorted(val_set)]
        elif val_set <= (code_set | desc_set):
            raise InvalidValuesError(
                "Cannot mix codes and descriptions in selector values list."
            )
        else:
            valid_set = val_set & (code_set | desc_set)
            invalid_set = val_set - (code_set | desc_set)
            invalid_size = len(invalid_set)
            sample_size = min(invalid_size, 3)
            invalid_sample = [f"'{invalid_set.pop()}'" for _ in range(sample_size)]
            sample_msg = f" (sample of {sample_size})" if invalid_size > 3 else ""
            sample_str = ", ".join(invalid_sample) + sample_msg
            if valid_set <= code_set:
                raise InvalidValuesError(
                    f"{invalid_size} invalid code(s) "
                    f"detected in selector values list:\n{sample_str}"
                )
            elif valid_set <= desc_set:
                raise InvalidValuesError(
                    f"{invalid_size} invalid description(s) "
                    f"detected in selector values list:\n{sample_str}"
                )
            elif valid_set <= code_set | desc_set:
                raise InvalidValuesError(
                    f"{invalid_size} invalid value(s) "
                    f"detected in selector values list. "
                    f"Also, cannot mix codes and descriptions "
                    f"in selector values list:\n{sample_str}"
                )
            else:
                raise InvalidValuesError(
                    "Selector values list contains no valid values."
                )


def logic_clause(
    operation: str,
    operands: List["Clause"],
    new_table: Optional["Table"] = None,
    *,
    name: Optional[str] = None,
    ):
    if operation in ['AND', 'OR', 'NOT']:
        return BooleanClause(operands[0].table_name, operation, operands, label=name, session=operands[0].session)
    elif operation in ["ANY", "THE"]:
        (operand,) = operands
        return TableClause(new_table.name, operation, operand, label=name, session=operand.session)
    else:
        valid_operations = ['ANY', 'AND', 'OR', 'NOT', 'THE']
        raise ValueError(f"'{operation}' is not a valid operation: "
                         f"must be one of: {', '.join(valid_operations)}")


class LogicClauseMixin:

    @staticmethod
    def _validate_operation(operation, operands, new_table):

        if len(operands) == 0:
            raise OperationError(
                "The operands list must contain at least one clause."
            )
        if operation in ['ANY', 'NOT', 'THE'] and len(operands) != 1:
            raise OperationError(
                f"'{operation}' can only be performed on a single clause."
            )
        if operation in ['AND', 'OR']:
            if len(operands) == 1:
                raise OperationError(
                    f"'{operation}' requires the operands list to contain "
                    f"at least two clauses."
                )
            if new_table is not None:
                raise OperationError(
                    f"Cannot change tables while performing '{operation}'."
                )

        if operation == 'NOT':
            return operands[0]._table

        if operation in ['ANY', 'THE']:
            if new_table is None:
                raise OperationError(
                    f"'{operation}' requires "
                    f"{'an ancestor' if operation == 'ANY' else 'a descendant'} "
                    f"table to be specified (none supplied)."
                )
            operand_table = operands[0]._table
            if operation == 'ANY':
                if not operand_table < new_table:
                    raise OperationError(
                        f"'ANY' requires an ancestor table"
                        f" to be specified."
                    )
            elif operation == 'THE':
                if not operand_table > new_table:
                    raise OperationError(
                        f"'THE' requires a descendant table"
                        f" to be specified."
                    )
            return new_table

        if operation in ['AND', 'OR', 'NOT']:
            operand_table_names = [op._table.name for op in operands]
            if len(set(operand_table_names)) != 1:
                raise OperationError(
                    f"'{operation}' requires all clauses to have the same "
                    f"resolve table."
                )
            return operands[0]._table


class SelectorClause(ClauseMixin):

    def __init__(self, table_name, variable_name, values, *, label=None, include=True, session=None):
        self.table_name = table_name
        self.variable_name = variable_name
        self.values = values

        self.label = label
        self.include = include
        self.session = session

    def _to_model(self):
        return aa.Clause(
            criteria=aa.Criteria(
                variable_name=self.variable_name,
                include=self.include,
                logic='OR',
                ignore_case=False,
                text_match_type='Is',
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(
                            list='\t'.join(self.values),
                            variable_name=self.variable_name
                        )
                    )
                ],
                table_name=self.table_name,
                name=self.label
            )
        )


class CombinedCategoriesClause(ClauseMixin):

    def __init__(self, table_name, variable_name, value_sets, *, label=None, include=True, session=None):
        self.table_name = table_name
        self.variable_name = variable_name
        self.value_sets = value_sets

        self.label = label
        self.include = include
        self.session = session

    def _to_model(self):
        return aa.Clause(
            criteria=aa.Criteria(
                variable_name=self.variable_name,
                include=self.include,
                logic='OR',
                ignore_case=False,
                text_match_type='Is',
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(
                            list='\t'.join(vals),
                            variable_name=var_name
                        )
                    ) for var_name, vals in self.value_sets.items()],
                table_name=self.table_name,
                name=self.label
            )
        )


class NumericClause(ClauseMixin):

    def __init__(self, table_name, variable_name, values, *, label=None, include=True, session=None):
        self.table_name = table_name
        self.variable_name = variable_name
        self.values = values

        self.label = label
        self.include = include
        self.session = session

    def _to_model(self):
        return aa.Clause(
            criteria=aa.Criteria(
                variable_name=self.variable_name,
                include=self.include,
                logic='OR',
                ignore_case=False,
                text_match_type='Is',
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(
                            list='\t'.join(self.values),
                            variable_name=self.variable_name
                        )
                    )
                ],
                table_name=self.table_name,
                name=self.label
            )
        )


class TextClause(ClauseMixin):

    def __init__(self, table_name, variable_name, values, match_type='Is', match_case=True, *, label=None, include=True, session=None):
        self.table_name = table_name
        self.variable_name = variable_name
        self.values = values
        self.match_type = match_type
        self.match_case = match_case

        self.label = label
        self.include = include
        self.session = session

    def _to_model(self):
        return aa.Clause(
            criteria=aa.Criteria(
                variable_name=self.variable_name,
                include=self.include,
                logic='OR',
                ignore_case=not self.match_case,
                text_match_type=self.match_type,
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(
                            list='\t'.join(self.values),
                            variable_name=self.variable_name
                        )
                    )
                ],
                table_name=self.table_name,
                name=self.label
            )
        )


class ArrayClause(ClauseMixin):

    def __init__(self, table_name, variable_name, values, logic='OR', *, label=None, include=True, session=None):
        self.table_name = table_name
        self.variable_name = variable_name
        self.values = values
        self.logic = logic

        self.label = label
        self.include = include
        self.session = session

    def _to_model(self):
        return aa.Clause(
            criteria=aa.Criteria(
                variable_name=self.variable_name,
                include=self.include,
                logic=self.logic,
                ignore_case=False,
                text_match_type='Is',
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(
                            list='\t'.join(self.values),
                            variable_name=self.variable_name
                        )
                    )
                ],
                table_name=self.table_name,
                name=self.label
            )
        )


class FlagArrayClause(ArrayClause):
    pass


class DateListClause(ClauseMixin):

    def __init__(self, table_name, variable_name, values, *, label=None, include=True, session=None):
        self.table_name = table_name
        self.variable_name = variable_name
        self.values = values

        self.label = label
        self.include = include
        self.session = session

    def _to_model(self):
        return aa.Clause(
            criteria=aa.Criteria(
                variable_name=self.variable_name,
                include=self.include,
                logic='OR',
                ignore_case=False,
                text_match_type='Is',
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(
                            list='\t'.join(self.values),
                            variable_name=self.variable_name
                        ),
                        predefined_rule="AdhocDates"
                    )
                ],
                table_name=self.table_name,
                name=self.label
            )
        )


class DateRangeClause(ClauseMixin):
    def __init__(self, table_name, variable, start, end, *, label=None, include=True, session=None):
        self.table_name = table_name
        self.variable = variable
        self.start = start
        self.end = end

        self.label = label
        self.include = include
        self.session = session

    def _to_model(self):
        return aa.Clause(
            criteria=aa.Criteria(
                variable_name=self.variable,
                include=self.include,
                logic="OR",
                ignore_case=False,
                text_match_type="Is",
                value_rules=[
                    aa.ValueRule(
                        predefined_rule="CustomRule",
                        date_rule=aa.DateRule(
                            pattern_frequency="Daily",
                            pattern_interval=1,
                            pattern_days_of_week=["All"],
                            start_range_limit="Actual",
                            range_start_date=self.start,
                            end_range_limit="Actual",
                            range_end_date=self.end
                        ),
                    )
                ],
                table_name=self.table.name,
                name=self.label
            )
        )


class TimeRangeClause(ClauseMixin):
    def __init__(self, table_name, variable, start, end, *, label=None, include=True, session=None):
        self.table_name = table_name
        self.variable = variable
        self.start = start
        self.end = end

        self.label = label
        self.include = include
        self.session = session

    def _to_model(self):
        return aa.Clause(
            criteria=aa.Criteria(
                variable_name=self.variable,
                include=self.include,
                logic="OR",
                ignore_case=False,
                text_match_type="Is",
                value_rules=[
                    aa.ValueRule(
                        predefined_rule="CustomTimeRule",
                        time_rule=aa.TimeRule(
                            range_low=self.start, range_high=self.end
                        ),
                    )
                ],
                table_name=self.table.name,
                name=self.label
            )
        )


class DateTimeRangeClause(ClauseMixin):
    def __init__(self, table_name, variable, start, end, *, label=None, include=True, session=None):
        self.table_name = table_name
        self.variable = variable
        self.start = start
        self.end = end

        self.label = label
        self.include = include
        self.session = session

    def _to_model(self):
        return aa.Clause(
            criteria=aa.Criteria(
                variable_name=self.variable,
                include=self.include,
                logic="OR",
                ignore_case=False,
                text_match_type="Is",
                value_rules=[
                    aa.ValueRule(
                        predefined_rule="CustomRule",
                        date_rule=aa.DateRule(
                            pattern_frequency="Daily",
                            pattern_interval=1,
                            pattern_days_of_week=["All"],
                            start_range_limit="Actual",
                            range_start_date=self.start,
                            end_range_limit="Actual",
                            range_end_date=self.end
                        ),
                    )
                ],
                table_name=self.table.name,
                name=self.label
            )
        )


class BooleanClause(ClauseMixin):

    def __init__(self, table_name, operation, operands, *, label=None, session=None):
        self.table_name = table_name
        self.operation = operation
        self.operands = operands

        self.label = label
        self.session = session

    def _to_model(self):
        return aa.Clause(
            logic=aa.Logic(
                operation=self.operation,
                operands=[op._to_model() for op in self.operands],
                table_name=self.table_name,
                name=self.label
            )
        )


class TableClause(ClauseMixin):

    def __init__(self, table_name, operation, operand, *, label=None, session=None):
        self.table_name = table_name
        self.operation = operation
        self.operand = operand

        self.label = label
        self.session = session

    def _to_model(self):
        return aa.Clause(
            logic=aa.Logic(
                operation=self.operation,
                operands=[self.operand._to_model()],
                table_name=self.table_name,
                name=self.label
            )
        )


class SubSelectionClause(ClauseMixin):

    def __init__(self, selection, *, label=None, session=None):
        self.selection = selection

        self.label = label
        self.session = session

    def _to_model(self):
        return aa.Clause(
            # TODO: this may need to be changed depending on
            #  the final shape of the base py-apteco Selection object
            sub_selection=self.selection._to_model()
        )


# def select(clause, system_session):
#     query_final = aa.Query(
#         selection=aa.Selection(
#             table_name=clause.table_name, rule=aa.Rule(
#                 clause=clause._to_model()
#             )
#         )
#     )
#     return Selection(system_session.system_name, query_final, system_session.api_session)


def select(clause, api_session, system_name):
    query_final = aa.Query(
        selection=aa.Selection(
            table_name=clause.table_name, rule=aa.Rule(
                clause=clause._to_model()
            )
        )
    )
    return Selection(system_name, query_final, api_session)
