import apteco_api as aa
import pandas as pd


class DataGrid:
    def __init__(self, columns, table=None, *, session=None):
        self.columns = columns
        self.table = table
        self.session = session
        self._check_inputs()
        self._data = self._get_data()

    def to_df(self, index=None):
        return pd.DataFrame(
            self._data, columns=[v.description for v in self.columns]
        ).set_index(index.description)

    def _check_inputs(self):
        if self.session is None:
            raise ValueError("You must provide a valid session (none was given).")
        if not self.columns:
            raise ValueError(
                "You must specify at least one variable"
                " to use as a column on the data grid (none was given)."
            )
        if self.table is None:
            raise ValueError(
                "You must specify the resolve table of the cube (no table was given)."
            )
        self._check_columns()

    def _check_columns(self):
        for column in self.columns:
            if column.table != self.table:
                raise ValueError(
                    f"The resolve table of the data grid is '{self.table.name}',"
                    f" but the variable '{column.name}' belongs to the"
                    f" '{column.table.name}' table."
                    f"\nCurrently, only variables from the same table as the data grid"
                    f" are supported as data grid columns."
                )

    def _create_columns(self):
        return [
            aa.Column(id=str(i), variable_name=v.name, column_header=v.description)
            for i, v in enumerate(self.columns)
        ]

    def _get_export(self):
        export = aa.Export(
            base_query=aa.Query(selection=aa.Selection(table_name=self.table.name)),
            resolve_table_name=self.table.name,
            maximum_number_of_rows_to_browse=100,
            return_browse_rows=True,
            columns=self._create_columns(),
        )
        exports_controller = aa.ExportsApi(self.session.api_client)
        export_result = exports_controller.exports_perform_export_synchronously(
            self.session.data_view, self.session.system, export=export
        )
        return export_result

    def _get_data(self):
        export_result = self._get_export()
        return [tuple(row.descriptions.split("\t")) for row in export_result.rows]
