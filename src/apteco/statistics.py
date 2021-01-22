import apteco_api as aa


def _ensure_correct_type(operand, accepted_types):
    try:
        if operand.type in accepted_types:
            return
    except AttributeError:
        pass
    raise ValueError(
        f"The operand must be a" f" {' or '.join(t for t in accepted_types)} variable"
    ) from None


class Statistic:
    def __init__(self, operand, *, label=None):
        self.table = operand.table
        _ensure_correct_type(operand, self._accepted_types)
        self.operand = operand

        self.label = label

        self._name = f"{self._display_name}({self.operand.description})"

    def _to_model_measure(self, table):
        return aa.Measure(
            id=self.label if self.label is not None else self._name,
            resolve_table_name=table.name,
            function=self._model_function,
            variable_name=self.operand.name,
        )


class Sum(Statistic):
    _model_function = "Sum"
    _display_name = "Sum"
    _accepted_types = ("Numeric",)


class Mean(Statistic):
    _model_function = "Mean"
    _display_name = "Mean"
    _accepted_types = ("Numeric",)


class Populated(Statistic):
    _model_function = "VariableCount"
    _display_name = "Populated"
    _accepted_types = ("Numeric",)


class Min(Statistic):
    _model_function = "Minimum"
    _display_name = "Min"
    _accepted_types = ("Numeric",)


class Max(Statistic):
    _model_function = "Maximum"
    _display_name = "Max"
    _accepted_types = ("Numeric",)


class Median(Statistic):
    _model_function = "Median"
    _display_name = "Median"
    _accepted_types = ("Numeric",)


class Mode(Statistic):
    _model_function = "Mode"
    _display_name = "Mode"
    _accepted_types = ("Numeric",)


class Variance(Statistic):
    _model_function = "Variance"
    _display_name = "Variance"
    _accepted_types = ("Numeric",)


class StdDev(Statistic):
    _model_function = "StandardDeviation"
    _display_name = "Std Dev"
    _accepted_types = ("Numeric",)


class LowerQuartile(Statistic):
    _model_function = "LowerQuartile"
    _display_name = "Lower Quartile"
    _accepted_types = ("Numeric",)


class UpperQuartile(Statistic):
    _model_function = "UpperQuartile"
    _display_name = "Upper Quartile"
    _accepted_types = ("Numeric",)


class InterQuartileRange(Statistic):
    _model_function = "InterQuartileRange"
    _display_name = "Inter Quartile Range"
    _accepted_types = ("Numeric",)


class CountDistinct(Statistic):
    _model_function = "CountDistinct"
    _display_name = "Count Distinct"
    _accepted_types = ("Numeric", "Selector")


class CountMode(Statistic):
    _model_function = "MaxDistinctCount"
    _display_name = "Count Mode"
    _accepted_types = ("Numeric", "Selector")
