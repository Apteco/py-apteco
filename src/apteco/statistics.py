import apteco_api as aa


class BaseStatistic:
    def __init__(self, operand, *, label=None):
        self.table = operand.table
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


class Sum(BaseStatistic):
    _model_function = "Sum"
    _display_name = "Sum"


class Mean(BaseStatistic):
    _model_function = "Mean"
    _display_name = "Mean"


class Populated(BaseStatistic):
    _model_function = "VariableCount"
    _display_name = "Populated"


class Min(BaseStatistic):
    _model_function = "Minimum"
    _display_name = "Min"


class Max(BaseStatistic):
    _model_function = "Maximum"
    _display_name = "Max"


class Median(BaseStatistic):
    _model_function = "Median"
    _display_name = "Median"


class Mode(BaseStatistic):
    _model_function = "Mode"
    _display_name = "Mode"


class Variance(BaseStatistic):
    _model_function = "Variance"
    _display_name = "Variance"


class StdDev(BaseStatistic):
    _model_function = "StandardDeviation"
    _display_name = "Std Dev"


class LowerQuartile(BaseStatistic):
    _model_function = "LowerQuartile"
    _display_name = "Lower Quartile"


class UpperQuartile(BaseStatistic):
    _model_function = "UpperQuartile"
    _display_name = "Upper Quartile"


class InterQuartileRange(BaseStatistic):
    _model_function = "InterQuartileRange"
    _display_name = "Inter Quartile Range"


class CountDistinct(BaseStatistic):
    _model_function = "CountDistinct"
    _display_name = "Count Distinct"


class CountMode(BaseStatistic):
    _model_function = "MaxDistinctCount"
    _display_name = "Count Mode"


