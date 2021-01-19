import apteco_api as aa


class Sum:
    def __init__(self, operand):
        self.operand = operand

        self.name = f"Sum({self.operand.description})"
        self.table = operand.table

    def _to_model_measure(self, table):
        return aa.Measure(
            id=self.name,
            resolve_table_name=table.name,
            function="Sum",
            variable_name=self.operand.name,
        )


class Mean:
    def __init__(self, operand):
        self.operand = operand

        self.name = f"Mean({self.operand.description})"
        self.table = operand.table

    def _to_model_measure(self, table):
        return aa.Measure(
            id=self.name,
            resolve_table_name=table.name,
            function="Mean",
            variable_name=self.operand.name,
        )
