import apteco_api as aa
import numpy as np
import pandas as pd

from apteco.session import Table


class Cube:
    def __init__(self, dimensions, measures=None, table=None, *, session=None):
        self.dimensions = dimensions
        self.measures = measures
        self.table = table
        self.session = session
        self._check_inputs()
        self._data, self._headers, self._sizes = self._get_data()

    def to_df(self):
        return pd.DataFrame(
            self._data.ravel(),
            index=pd.MultiIndex.from_product(
                self._headers["descs"], names=[d.description for d in self.dimensions]
            ),
            columns=[f"{self.table.plural_display_name.title()}"],
        )

    def _check_inputs(self):
        if self.session is None:
            raise ValueError("You must provide a valid session (none was given).")
        if not self.dimensions:
            raise ValueError(
                "You must specify at least one variable"
                " to use as a dimension on the cube (none was given)."
            )
        if self.measures is not None:
            if self.table is None and isinstance(self.measures, Table):
                self.table = self.measures
                self.measures = None
            else:
                raise ValueError(
                    "Measures are not currently supported for cubes:"
                    " `measures` argument should either be `None`,"
                    " or used to specify the resolve table of the cube"
                    " using a `Table` object"
                    " (in the latter case the `table` argument should be `None`)."
                )
        if self.table is None:
            raise ValueError(
                "You must specify the resolve table of the cube (no table was given)."
            )
        self._check_dimensions()

    def _check_dimensions(self):
        for dimension in self.dimensions:
            if dimension.type != "Selector":
                raise ValueError(
                    f"The variable '{dimension.name}' has type '{dimension.type}'."
                    f"\nOnly Selector variables (excluding sub-types)"
                    f" are currently supported as cube dimensions."
                )
            if dimension.table != self.table:
                raise ValueError(
                    f"The counting table of the cube is '{self.table.name}',"
                    f" but the variable '{dimension.name}' belongs to the"
                    f" '{dimension.table.name}' table."
                    f"\nCurrently, only variables from the same table as the cube"
                    f" are supported as cube dimensions."
                )

    def _create_dimensions(self):
        return [
            aa.Dimension(id=str(i), type="Selector", variable_name=v.name)
            for i, v in enumerate(self.dimensions)
        ]

    def _create_measures(self):
        if self.measures is None:
            return [
                aa.Measure(
                    id="0",
                    resolve_table_name=self.table.name,
                    function="Count",
                    variable_name=None,
                )
            ]
        return [
            aa.Measure(
                id=str(i),
                resolve_table_name=self.table.name,
                function="Count",
                variable_name=None,
            )
            for i, v in enumerate(self.measures)
        ]

    def _get_cube(self):
        cube = aa.Cube(
            base_query=aa.Query(selection=aa.Selection(table_name=self.table.name)),
            resolve_table_name=self.table.name,
            storage="Full",
            dimensions=self._create_dimensions(),
            measures=self._create_measures(),
        )
        cubes_controller = aa.CubesApi(self.session.api_client)
        cube_result = cubes_controller.cubes_calculate_cube_synchronously(
            self.session.data_view, self.session.system, cube=cube
        )
        return cube_result

    def _get_data(self):
        cube_result = self._get_cube()
        raw_data = [
            int(x)
            for row in cube_result.measure_results[0].rows
            for x in row.split("\t")
        ]
        headers = {
            "codes": [
                dimension.header_codes.split("\t")
                for dimension in cube_result.dimension_results
            ],
            "descs": [
                dimension.header_descriptions.split("\t")
                for dimension in cube_result.dimension_results
            ],
        }
        sizes = tuple(len(h) for h in headers["codes"])
        data_as_array = np.array(raw_data)
        data = data_as_array.T.reshape(sizes, order="F")
        dimensions = [dim.id for dim in cube_result.dimension_results]
        return data, headers, sizes
