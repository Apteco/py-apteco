import apteco_api as aa


class BaseStatistic:
    def __init__(self, operand):
        self.table = operand.table
        self.operand = operand

        self.name = f"{self._model_function}({self.operand.description})"

    def _to_model_measure(self, table):
        return aa.Measure(
            id=self.name,
            resolve_table_name=table.name,
            function=self._model_function,
            variable_name=self.operand.name,
        )


class Sum(BaseStatistic):
    _model_function = "Sum"


class Mean(BaseStatistic):
    _model_function = "Mean"


