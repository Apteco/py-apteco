import apteco_api as aa
import numpy as np
import pandas as pd


class DataGrid:
    def __init__(
        self,
        columns,
        selection=None,
        table=None,
        max_rows=1000,
        *,
        session=None,
    ):
        self.columns = columns
        self.selection = selection
        self.table = table
        self.max_rows = max_rows
        self.session = session
        self._check_inputs()
        self._data = self._get_data()

    def to_df(self):
        df = pd.DataFrame(
            self._data, columns=[v.description for v in self.columns]
        )
        for i, v in enumerate(self.columns):
            df.iloc[:, i] = self._convert_column(df.iloc[:, i], v.type)
        return df

    @staticmethod
    def _convert_column(data: pd.Series, column_type):
        if column_type in ("Selector", "Text", "Reference"):
            return data.astype(str)
        elif column_type == "Numeric":
            if "." in data.iloc[0]:
                return data.astype(float)
            else:
                try:
                    return data.astype(int)
                except ValueError:
                    return data.replace("", np.NaN).astype(float)
        elif column_type == "Date":
            return pd.to_datetime(data, format="%d-%m-%Y").dt.date
        elif column_type == "DateTime":
            return pd.to_datetime(data, format="%d-%m-%Y %H:%M:%S")
        else:
            raise ValueError(f"Unrecognised column type: {column_type}")

    def _check_inputs(self):
        if self.session is None:
            raise ValueError("You must provide a valid session (none was given).")
        try:
            self.max_rows = int(self.max_rows)
            assert self.max_rows > 0
        except (ValueError, TypeError, AssertionError) as exc:
            raise ValueError("max_rows must be a number greater than 0") from exc
        if not self.columns:
            raise ValueError(
                "You must specify at least one variable"
                " to use as a column on the data grid (none was given)."
            )
        if self.table is None:
            if self.selection is not None:
                self.table = self.selection.table
            else:
                raise ValueError(
                    "You must specify the resolve table of the data grid"
                    " (none was given)."
                )
        self._check_columns()

    def _check_columns(self):
        for column in self.columns:
            if not column.table.is_ancestor(self.table, allow_same=True):
                raise ValueError(
                    f"The resolve table of the data grid is '{self.table.name}',"
                    f" but the variable '{column.name}' belongs to the"
                    f" '{column.table.name}' table."
                    f"\nOnly variables from the same table as the data grid"
                    f" or from ancestor tables can be used as data grid columns."
                )
            if column.type in ("Array", "FlagArray"):
                raise ValueError(
                    f"The variable '{column.name}' has type '{column.type}'."
                    f"\nArray and Flag Array variables"
                    f" are not currently supported as data grid columns."
                )

    def _create_columns(self):
        return [
            aa.Column(id=str(i), variable_name=v.name, column_header=v.description)
            for i, v in enumerate(self.columns)
        ]

    def _get_export(self):
        export = aa.Export(
            base_query=aa.Query(
                selection=aa.Selection(
                    table_name=self.selection.table.name,
                    rule=aa.Rule(clause=self.selection._to_model()),
                ) if self.selection is not None else aa.Selection(
                    table_name=self.table.name,
                )
            ),
            resolve_table_name=self.table.name,
            maximum_number_of_rows_to_browse=self.max_rows,
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
