from datetime import date, datetime
from decimal import Decimal
from numbers import Integral, Number, Rational, Real
from typing import Iterable, List, Optional

import apteco_api as aa

from apteco.cube import Cube
from apteco.datagrid import DataGrid
from apteco.exceptions import AptecoException
# from apteco.tables import Table
# from apteco.variables import Variable

DECIMAL_PLACES = 4


class OperationError(AptecoException):
    """Raised when invalid operation attempted on clauses."""


class InvalidValuesError(AptecoException):
    """Raised when invalid values used in selection query."""


class SelectionCount(object):
    def __init__(self, count_response):
        self.table_name = count_response.table_name
        self.count = count_response.count_value


class Selection:
    def __init__(self, query: aa.Query, session: "Session"):

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
            data_view_name=data_view_name, system_name=system, query=query
        )

        return response  # type: aa.QueryResult

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
            raise ValueError("Table name not found")

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
            raise ValueError("Table name not found")


# TODO: change name to Controller (confusing with APIClient otherwise)
class APIController:
    def __init__(self, controller, session: "Session"):
        self._controller = controller(session.api_client)

    def __call__(self, function_as_string, **kwargs):
        return getattr(self._controller, function_as_string)(**kwargs)


class TableMixin:
    def count(self):
        query_final = aa.Query(
            selection=aa.Selection(table_name=self.name, ancestor_counts=True)
        )
        session = self.session
        return Selection(query_final, session).count


general_error_msg_selector = (
    "Chosen value(s) for a selector variable"
    " must be given as a string or an iterable of strings."
)
general_error_msg_text = (
    "Chosen value(s) for a text variable"
    " must be given as a string or an iterable of strings."
)
single_value_error_msg_text = "Must specify a single string for this type of operation."
general_error_msg_array = (
    "Chosen value(s) for an array variable"
    " must be given as a string or an iterable of strings."
)
general_error_msg_flag_array = (
    "Chosen value(s) for a flag array variable"
    " must be given as a string or an iterable of strings."
)


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


general_error_msg_numeric = (
    "Chosen value(s) for a numeric variable"
    " must be given as a number or an iterable of numbers."
)
single_value_error_msg_numeric = (
    "Must specify a single number for this type of operation."
)


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


general_error_msg_date = (
    "Chosen value for a date variable"
    " must be a date object or an iterable of date objects."
)
single_value_error_msg_date = "Must specify a single date for this type of operation."


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


single_value_error_msg_datetime = (
    "Must specify a single datetime for this type of operation."
)


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


class Clause:
    @property
    def table_name(self):
        return self.table.name

    def count(self):
        query_final = aa.Query(selection=self._to_model_selection())
        session = self.session
        return Selection(query_final, session).count

    def _to_model_selection(self):
        return aa.Selection(
            table_name=self.table_name,
            ancestor_counts=True,
            rule=aa.Rule(clause=self._to_model_clause()),
        )

    def _change_table(self, new_table, simplify=False):

        if simplify:
            return self._strip_table_changes()._change_table_main(new_table)
        else:
            return self._change_table_main(new_table)

    def _change_table_main(self, new_table):
        if self.table.is_descendant(new_table):
            if self.table.parent == new_table:
                return logic_clause("ANY", [self], new_table)
            else:
                return logic_clause(
                    "ANY", [self], self.table.parent
                )._change_table_main(new_table)
        elif self.table.is_ancestor(new_table):
            if self.table == new_table.parent:
                return logic_clause("THE", [self], new_table)
            else:
                return logic_clause(
                    "THE", [self._change_table_main(new_table.parent)], new_table
                )
        elif self.table == new_table:
            return self
        else:
            try:
                common_ancestor_names = set(t.name for t in self.table.ancestors) & set(
                    t.name for t in new_table.ancestors
                )
                nearest_common_ancestor = max(
                    self.session.tables[name] for name in common_ancestor_names
                )
            except ValueError:  # empty list passed to max() -> no common ancestors
                raise OperationError(
                    f"Could not establish relationship between tables "
                    f"'{new_table.name}' and '{self.table_name}'."
                ) from None
            return self._change_table_main(nearest_common_ancestor)._change_table_main(
                new_table
            )

    def _strip_table_changes(self):
        if self.logic is None or self.logic.operation.upper() in ["AND", "OR", "NOT"]:
            return self
        elif self.logic.operation.upper() in ["ANY", "THE"]:
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
            return logic_clause("AND", [self, other._change_table(self.table)])
        return logic_clause("AND", [self, other])

    def __or__(self, other):
        if self.table != other.table:
            return logic_clause("OR", [self, other._change_table(self.table)])
        return logic_clause("OR", [self, other])

    def __invert__(self):
        return logic_clause("NOT", [self])

    def __mul__(self, other):
        return self._change_table(other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def datagrid(self, columns, table=None, max_rows=1000):
        return DataGrid(
            columns,
            selection=self,
            table=table if table is not None else self.table,
            max_rows=max_rows,
            session=self.session,
        )

    def cube(self, dimensions, measures=None, table=None):
        return Cube(
            dimensions,
            measures=measures,
            selection=self,
            table=table if table is not None else self.table,
            session=self.session,
        )

    def sample(
        self, n=None, frac=None, sample_type="First", skip_first=0, *, label=None
    ):
        if sum((i is not None) for i in (n, frac)) != 1:
            raise ValueError("Must specify either n or frac")
        percent = None
        fraction = None
        if n is not None:
            if not isinstance(n, Integral) or n < 1:
                raise ValueError("n must be an integer greater than 0")
        else:
            if frac >= 1 or frac <= 0:
                raise ValueError("frac must be between 0 and 1")
            if isinstance(frac, Rational):
                fraction = frac
            elif isinstance(frac, Real):
                percent = frac * 100
            else:
                raise ValueError("frac must be either a float or a fraction")
        return LimitClause(
            total=n,
            percent=percent,
            fraction=(fraction.numerator, fraction.denominator) if fraction else None,
            clause=self,
            sample_type=sample_type,
            skip_first=skip_first,
            label=label,
            session=self.session,
        )

    # def limit(self, n=None, frac=None, by=None, ascending=None, per=None, *, label=None):
    #     if ascending is not None:
    #         if not isinstance(ascending, bool):
    #             raise ValueError("ascending must be True or False")
    #         if by is None:
    #             raise ValueError("Must specify by with ascending")
    #     else:
    #         ascending = False
    #     if by is not None and not isinstance(by, Variable):
    #         raise ValueError("by must be a variable")
    #     if per is not None:
    #         if isinstance(per, Table):
    #             pass
    #             #npertable
    #         if isinstance(per, Variable):
    #             pass
    #             #npervariable
    #         raise ValueError("per must be a table or a variable")
    #     if by is None:
    #         pass
    #         #call.sample()
    #     pass
    #     #topn


class SelectorClauseMixin:
    @staticmethod
    def _verify_values(values: Iterable[str], variable_name: str, session: "Session"):
        systems_controller = APIController(aa.FastStatsSystemsApi, session)

        # TODO: separate this part into a (dynamic) getter for a .values property
        #  on the SelectorVariable class
        var_codes_raw = []
        offset = 0
        while True:
            var_code_results = systems_controller(
                "fast_stats_systems_get_fast_stats_variable_codes",
                data_view_name=session.data_view,
                system_name=session.system,
                variable_name=variable_name,
                offset=offset,
            )
            var_codes_raw.extend(var_code_results.list)
            if (
                var_code_results.offset + var_code_results.count
                >= var_code_results.total_count
            ):
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
    if operation in ["AND", "OR", "NOT"]:
        return BooleanClause(
            operands[0].table,
            operation,
            operands,
            label=name,
            session=operands[0].session,
        )
    elif operation in ["ANY", "THE"]:
        (operand,) = operands
        return TableClause(
            new_table, operation, operand, label=name, session=operand.session
        )
    else:
        valid_operations = ["ANY", "AND", "OR", "NOT", "THE"]
        raise ValueError(
            f"'{operation}' is not a valid operation: "
            f"must be one of: {', '.join(valid_operations)}"
        )


class LogicClauseMixin:
    @staticmethod
    def _validate_operation(operation, operands, new_table):

        if len(operands) == 0:
            raise OperationError("The operands list must contain at least one clause.")
        if operation in ["ANY", "NOT", "THE"] and len(operands) != 1:
            raise OperationError(
                f"'{operation}' can only be performed on a single clause."
            )
        if operation in ["AND", "OR"]:
            if len(operands) == 1:
                raise OperationError(
                    f"'{operation}' requires the operands list to contain "
                    f"at least two clauses."
                )
            if new_table is not None:
                raise OperationError(
                    f"Cannot change tables while performing '{operation}'."
                )

        if operation == "NOT":
            return operands[0]._table

        if operation in ["ANY", "THE"]:
            if new_table is None:
                raise OperationError(
                    f"'{operation}' requires "
                    f"{'an ancestor' if operation == 'ANY' else 'a descendant'} "
                    f"table to be specified (none supplied)."
                )
            operand_table = operands[0]._table
            if operation == "ANY":
                if not new_table.is_ancestor(operand_table):
                    raise OperationError(
                        f"'ANY' requires an ancestor table to be specified."
                    )
            elif operation == "THE":
                if not new_table.is_descendant(operand_table):
                    raise OperationError(
                        f"'THE' requires a descendant table to be specified."
                    )
            return new_table

        if operation in ["AND", "OR", "NOT"]:
            operand_table_names = [op._table.name for op in operands]
            if len(set(operand_table_names)) != 1:
                raise OperationError(
                    f"'{operation}' requires all clauses to have the same "
                    f"resolve table."
                )
            return operands[0]._table


class CriteriaClause(Clause):
    @property
    def variable_name(self):
        return self.variable.name


class SelectorClause(CriteriaClause):
    def __init__(self, variable, values, *, include=True, label=None, session=None):
        self.table = variable.table
        self.variable = variable
        self.values = values

        self.include = include
        self.label = label
        self.session = session

    def _to_model_clause(self):
        return aa.Clause(
            criteria=aa.Criteria(
                variable_name=self.variable_name,
                include=self.include,
                logic="OR",
                ignore_case=False,
                text_match_type="Is",
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(
                            list="\t".join(self.values),
                            variable_name=self.variable_name,
                        )
                    )
                ],
                table_name=self.table_name,
                name=self.label,
            )
        )


class CombinedCategoriesClause(CriteriaClause):
    def __init__(self, variable, value_sets, *, include=True, label=None, session=None):
        self.table = variable.table
        self.variable = variable
        self.value_sets = value_sets

        self.include = include
        self.label = label
        self.session = session

    def _to_model_clause(self):
        return aa.Clause(
            criteria=aa.Criteria(
                variable_name=self.variable_name,
                include=self.include,
                logic="OR",
                ignore_case=False,
                text_match_type="Is",
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(
                            list="\t".join(vals), variable_name=var_name
                        )
                    )
                    for var_name, vals in self.value_sets.items()
                ],
                table_name=self.table_name,
                name=self.label,
            )
        )


class NumericClause(CriteriaClause):
    def __init__(self, variable, values, *, include=True, label=None, session=None):
        self.table = variable.table
        self.variable = variable
        self.values = values

        self.include = include
        self.label = label
        self.session = session

    def _to_model_clause(self):
        return aa.Clause(
            criteria=aa.Criteria(
                variable_name=self.variable_name,
                include=self.include,
                logic="OR",
                ignore_case=False,
                text_match_type="Is",
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(
                            list="\t".join(self.values),
                            variable_name=self.variable_name,
                        )
                    )
                ],
                table_name=self.table_name,
                name=self.label,
            )
        )


class TextClause(CriteriaClause):
    def __init__(
        self,
        variable,
        values,
        match_type="Is",
        match_case=True,
        *,
        include=True,
        label=None,
        session=None,
    ):
        self.table = variable.table
        self.variable = variable
        self.values = values
        self.match_type = match_type
        self.match_case = match_case

        self.include = include
        self.label = label
        self.session = session

    def _to_model_clause(self):
        return aa.Clause(
            criteria=aa.Criteria(
                variable_name=self.variable_name,
                include=self.include,
                logic="OR",
                ignore_case=not self.match_case,
                text_match_type=self.match_type,
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(
                            list="\t".join(self.values),
                            variable_name=self.variable_name,
                        )
                    )
                ],
                table_name=self.table_name,
                name=self.label,
            )
        )


class ArrayClause(CriteriaClause):
    def __init__(
        self, variable, values, logic="OR", *, include=True, label=None, session=None
    ):
        self.table = variable.table
        self.variable = variable
        self.values = values
        self.logic = logic

        self.include = include
        self.label = label
        self.session = session

    def _to_model_clause(self):
        return aa.Clause(
            criteria=aa.Criteria(
                variable_name=self.variable_name,
                include=self.include,
                logic=self.logic,
                ignore_case=False,
                text_match_type="Is",
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(
                            list="\t".join(self.values),
                            variable_name=self.variable_name,
                        )
                    )
                ],
                table_name=self.table_name,
                name=self.label,
            )
        )


class FlagArrayClause(ArrayClause):
    pass


class DateListClause(CriteriaClause):
    def __init__(self, variable, values, *, include=True, label=None, session=None):
        self.table = variable.table
        self.variable = variable
        self.values = values

        self.include = include
        self.label = label
        self.session = session

    def _to_model_clause(self):
        return aa.Clause(
            criteria=aa.Criteria(
                variable_name=self.variable_name,
                include=self.include,
                logic="OR",
                ignore_case=False,
                text_match_type="Is",
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(
                            list="\t".join(self.values),
                            variable_name=self.variable_name,
                        ),
                        predefined_rule="AdhocDates",
                    )
                ],
                table_name=self.table_name,
                name=self.label,
            )
        )


class DateRangeClause(CriteriaClause):
    def __init__(self, variable, start, end, *, include=True, label=None, session=None):
        self.table = variable.table
        self.variable = variable
        self.start = start
        self.end = end

        self.include = include
        self.label = label
        self.session = session

    def _create_range_parameters(self):
        params = {}
        if self.start.lower() == "earliest":
            params["start_range_limit"] = "Earliest"
        else:
            params["start_range_limit"] = "Actual"
            params["range_start_date"] = self.start + "T00:00:00"
        if self.end.lower() == "latest":
            params["end_range_limit"] = "Latest"
        else:
            params["end_range_limit"] = "Actual"
            params["range_end_date"] = self.end + "T00:00:00"
        return params

    def _to_model_clause(self):
        return aa.Clause(
            criteria=aa.Criteria(
                variable_name=self.variable_name,
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
                            **self._create_range_parameters(),
                        ),
                    )
                ],
                table_name=self.table_name,
                name=self.label,
            )
        )


class TimeRangeClause(CriteriaClause):
    def __init__(self, variable, start, end, *, include=True, label=None, session=None):
        self.table = variable.table
        self.variable = variable
        self.start = start
        self.end = end

        self.include = include
        self.label = label
        self.session = session

    def _to_model_clause(self):
        return aa.Clause(
            criteria=aa.Criteria(
                variable_name=self.variable_name,
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
                table_name=self.table_name,
                name=self.label,
            )
        )


class DateTimeRangeClause(DateRangeClause):
    def _create_range_parameters(self):
        params = {}
        if self.start.lower() == "earliest":
            params["start_range_limit"] = "Earliest"
        else:
            params["start_range_limit"] = "Actual"
            params["range_start_date"] = self.start
        if self.end.lower() == "latest":
            params["end_range_limit"] = "Latest"
        else:
            params["end_range_limit"] = "Actual"
            params["range_end_date"] = self.end
        return params


# TODO: write implementation
class ReferenceClause(CriteriaClause):
    def __init__(self, variable, values, *, include=True, label=None, session=None):
        raise NotImplementedError

    def _to_model_clause(self):
        raise NotImplementedError


class BooleanClause(Clause):
    def __init__(self, table, operation, operands, *, label=None, session=None):
        self.table = table
        self.operation = operation
        self.operands = operands

        self.label = label
        self.session = session

    def _to_model_clause(self):
        return aa.Clause(
            logic=aa.Logic(
                operation=self.operation,
                operands=[op._to_model_clause() for op in self.operands],
                table_name=self.table_name,
                name=self.label,
            )
        )


class TableClause(Clause):
    def __init__(self, table, operation, operand, *, label=None, session=None):
        self.table = table
        self.operation = operation
        self.operand = operand

        self.label = label
        self.session = session

    def _to_model_clause(self):
        return aa.Clause(
            logic=aa.Logic(
                operation=self.operation,
                operands=[self.operand._to_model_clause()],
                table_name=self.table_name,
                name=self.label,
            )
        )


class SubSelectionClause(Clause):
    def __init__(self, selection, *, label=None, session=None):
        self.selection = selection

        self.label = label
        self.session = session

    def _to_model_clause(self):
        return aa.Clause(
            # TODO: this may need to be changed depending on
            #  the final shape of the base py-apteco Selection object
            sub_selection=self.selection._to_model_selection()
        )


class LimitClause(Clause):
    def __init__(
        self,
        total=None,
        percent=None,
        fraction=None,
        clause=None,
        sample_type="First",
        skip_first=0,
        *,
        label=None,
        session=None,
    ):
        input_flag = tuple((i is not None) for i in (total, percent, fraction))
        if sum(input_flag) != 1:
            raise ValueError("Must specify one of total, percent or fraction")
        self.type_ = {0: "Total", 1: "Percent", 2: "Fraction"}[input_flag.index(True)]
        if sample_type not in ("First", "Stratified", "Random"):
            raise ValueError(f"{sample_type} is not a valid sample type")

        self.total = total
        self.percent = percent
        self.fraction = fraction
        self.clause = clause
        self.sample_type = sample_type
        self.skip_first = skip_first
        self.table = clause.table

        self.label = label
        self.session = session

    def _to_model_clause(self):
        return aa.Clause(
            sub_selection=aa.SubSelection(
                selection=self._to_model_selection()
            )
        )

    def _to_model_selection(self):
        return aa.Selection(
            rule=aa.Rule(clause=self.clause._to_model_clause()),
            limits=aa.Limits(
                sampling=self.sample_type,
                total=self.total,
                type=self.type_,
                start_at=self.skip_first,
                percent=self.percent,
                fraction=aa.Fraction(self.fraction[0], self.fraction[1])
                if self.fraction
                else None,
            ),
            table_name=self.clause.table_name,
            name=self.label,
        )
