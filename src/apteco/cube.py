import itertools

import apteco_api as aa
import numpy as np
import pandas as pd


class Cube:
    def __init__(
        self, dimensions, measures=None, selection=None, table=None, *, session=None
    ):
        self.dimensions = dimensions
        self.measures = measures
        self.selection = selection
        self.table = table
        self.session = session
        self._check_inputs()
        self._data, self._headers, self._sizes = self._get_data()

    def _check_inputs(self):
        if self.session is None:
            raise ValueError("You must provide a valid session (none was given).")
        if not self.dimensions:
            raise ValueError(
                "You must specify at least one variable"
                " to use as a dimension on the cube (none was given)."
            )
        self._check_table()
        self._check_dimensions()
        self._check_measures()
        self._check_relations()

    def _check_table(self):
        if self.table is None:
            if self.selection is None:
                raise ValueError(
                    "You must specify the resolve table of the cube"
                    " (no table or selection was given)."
                )
            self.table = self.selection.table

    def _check_dimensions(self):
        for dimension in self.dimensions:
            if dimension.type != "Selector":
                raise ValueError(
                    f"The variable '{dimension.name}' has type '{dimension.type}'."
                    f"\nOnly Selector variables (excluding sub-types)"
                    f" are currently supported as cube dimensions."
                )
            if not dimension.table.is_related(self.table, allow_same=True):
                raise ValueError(
                    f"The resolve table of the cube is '{self.table.name}',"
                    f" but the variable '{dimension.name}' belongs to the"
                    f" '{dimension.table.name}' table."
                    f"\nOnly variables from the same table as the cube"
                    f" or from related tables can be used as cube dimensions."
                )

    def _check_measures(self):
        if self.measures is None:
            self.measures = [self.table]
            return
        for measure in self.measures:
            if not hasattr(measure, "_to_model_measure"):
                raise ValueError(f"Invalid measure given: must be statistic")
            if not measure.table.is_related(self.table, allow_same=True):
                raise ValueError(
                    f"The resolve table of the cube is '{self.table.name}',"
                    f" but the measure '{measure._name}' belongs to the"
                    f" '{measure.table.name}' table."
                    f"\nOnly measures from the same table as the cube"
                    f" or from related tables can be used as cube dimensions."
                )

    def _check_relations(self):
        elements = [
            (d, f"dimension '{d.name}' (table: {d.table.name})")
            for d in self.dimensions
        ] + [(m, f"measure '{m._name}' (table: {m.table.name})") for m in self.measures]

        non_related = []
        for x, y in itertools.combinations(elements, r=2):
            if not x[0].table.is_related(y[0].table, allow_same=True):
                non_related.append((x, y))

        if not non_related:
            return

        error_msg = "The tables of all elements in the cube must be mutually-related, but the tables of the following pair(s) of elements are not related:"
        for x, y in non_related:
            error_msg += f"\n{x[1]} & {y[1]}"
        raise ValueError(error_msg)

    def _get_data(self):
        cube_result = self._get_cube()
        raw_data = [
            [x for row in mr.rows for x in row.split("\t")]
            for mr in cube_result.measure_results
        ]
        headers = {
            "codes": [
                [
                    "TOTAL" if c == "iTOTAL" else c
                    for c in dimension.header_codes.split("\t")
                ]
                for dimension in cube_result.dimension_results
            ],
            "descs": [
                [
                    "TOTAL" if d == "iTOTAL" else d
                    for d in dimension.header_descriptions.split("\t")
                ]
                for dimension in cube_result.dimension_results
            ],
            "measures": [mr.id for mr in cube_result.measure_results],
        }
        sizes = tuple(len(h) for h in headers["codes"])
        data_as_array = [np.array(raw_measure_data) for raw_measure_data in raw_data]
        data = [
            measure_data_as_array.T.reshape(sizes, order="F")
            for measure_data_as_array in data_as_array
        ]
        dimensions = [dim.id for dim in cube_result.dimension_results]
        return data, headers, sizes

    def _get_cube(self):
        cube = aa.Cube(
            base_query=aa.Query(
                selection=self.selection._to_model_selection()
                if self.selection is not None
                else aa.Selection(table_name=self.table.name)
            ),
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

    def _create_dimensions(self):
        return [
            aa.Dimension(id=str(i), type="Selector", variable_name=v.name)
            for i, v in enumerate(self.dimensions)
        ]

    def _create_measures(self):
        return [m._to_model_measure(self.table) for m in self.measures]

    def to_df(self):
        if len(self.dimensions) == 1:
            index = pd.Index(
                self._headers["descs"][0], name=self.dimensions[0].description
            )
        else:
            index = pd.MultiIndex.from_product(
                self._headers["descs"], names=[d.description for d in self.dimensions]
            )
        return pd.DataFrame(
            {
                measure_name: pd.to_numeric(measure_data.ravel(), errors="coerce")
                for measure_name, measure_data in zip(
                    self._headers["measures"], self._data
                )
            },
            index=index,
        )
