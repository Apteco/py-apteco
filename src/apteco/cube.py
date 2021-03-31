import itertools

import apteco_api as aa
import numpy as np
import pandas as pd

from apteco.common import DimensionType, VariableType


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
        self._data, self._sizes, self._headers, self._measure_names = self._get_data()

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
            if dimension.type != VariableType.SELECTOR:
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
        d_elements = [
            (d, f"dimension '{d.name}' (table: {d.table.name})")
            for d in self.dimensions
        ]
        m_elements = [(m, f"measure '{m._name}' (table: {m.table.name})") for m in self.measures]

        cross_cube = False
        non_related = []
        for x, y in itertools.combinations(d_elements, r=2):
            if x[0].table.is_related(y[0].table, allow_same=True):
                pass
            elif x[0].table.is_descendant(self.table) and y[0].table.is_descendant(self.table):
                cross_cube = True
            else:
                # should be unreachable
                non_related.append((x, y))

        if non_related:
            error_msg = (
                "Dimension tables must either be related,"
                " or be descendants of the resolve table."
                " The following pair(s) of dimensions did not meet those criteria:"
            )
            for x, y in non_related:
                error_msg += f"\n{x[1]} & {y[1]}"
            raise ValueError(error_msg)

        if cross_cube:
            cell_table = self.table
            bad_measures = []
            for m in m_elements:
                if not m[0].table.is_ancestor(cell_table, allow_same=True):
                    bad_measures.append(m)
            if bad_measures:
                error_msg = (
                    "For 'cross cubes' (where two dimensions are unrelated),"
                    " all measures must be from the resolve table"
                    " or one of its ancestors."
                    " The following measure(s) did not meet those criteria:"
                )
                for bm in bad_measures:
                    error_msg += f"\n{bm[1]}"
                raise ValueError(error_msg)

        else:
            # cell_table = max(dim.table for dim in self.dimensions)
            non_related = []
            for m, d in itertools.product(m_elements, d_elements):
                if not m[0].table.is_related(d[0].table, allow_same=True):
                    non_related.append((m, d))
            if non_related:
                error_msg = (
                    "Measure and dimension tables must be related."
                    " The following measure-dimension pair(s) "
                    " did not meet those criteria:"
                )
                for m, d in non_related:
                    error_msg += f"\n{m[1]} & {d[1]}"
                raise ValueError(error_msg)

    def _get_data(self):
        cube_result = self._get_cube()
        raw_data = [
            [x for row in mr.rows for x in row.split("\t")]
            for mr in cube_result.measure_results
        ]
        headers = [
            {
                "codes": [
                    "TOTAL" if c == "iTOTAL" else c
                    for c in dimension.header_codes.split("\t")
                ],
                "descs": [
                    "TOTAL" if d == "iTOTAL" else d
                    for d in dimension.header_descriptions.split("\t")
                ],
            }
            for dimension in reversed(cube_result.dimension_results)
        ]
        sizes = tuple(len(dh["codes"]) for dh in headers)
        data_as_arrays = [np.array(raw_measure_data) for raw_measure_data in raw_data]
        data = [
            measure_data_as_array.reshape(sizes)
            for measure_data_as_array in data_as_arrays
        ]
        measure_names = [mr.id for mr in cube_result.measure_results]
        dimension_names = [dim.id for dim in cube_result.dimension_results]
        return data, sizes, headers, measure_names

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
        return [d._to_model_dimension() for d in reversed(self.dimensions)]

    def _create_measures(self):
        return [m._to_model_measure(self.table) for m in self.measures]

    def to_df(self, totals=False, unclassified=False, no_trans=False, convert_index=True):
        # 1. validate inputs
        if no_trans is not False:
            raise ValueError("no_trans must be False")

        # 2. create index
        chosen_headers, unclassified_headers = zip(*[
            self._choose_headers(headers, dimension, convert_index)
            for headers, dimension in zip(self._headers, self.dimensions)
        ])
        if len(self.dimensions) == 1:
            index = pd.Index(chosen_headers[0], name=self.dimensions[0].description)
        else:
            index = pd.MultiIndex.from_product(
                chosen_headers, names=[d.description for d in self.dimensions],
            )

        # 3. create filter/mask
        mask = True
        for i, __ in enumerate(self.dimensions):
            invalid = []
            if not totals:
                invalid.append("TOTAL")
            if not unclassified:
                invalid.append(unclassified_headers[i])
            if invalid:
                mask &= ~index.get_level_values(i).isin(invalid)

        # 4. apply filter
        index = index[mask]
        data = [measure_data.ravel()[mask] for measure_data in self._data]

        # 5. convert data & index
        converted_headers = [
            self._convert_headers(index.get_level_values(i), dimension)
            for i, dimension in enumerate(self.dimensions)
        ]
        index = pd.MultiIndex.from_arrays(converted_headers)
        return pd.DataFrame(
            {
                measure_name: pd.to_numeric(measure_data, errors="coerce")
                for measure_name, measure_data in zip(self._measure_names, data)
            },
            index=index,
        )

    @staticmethod
    def _choose_headers(headers, dimension, convert_index):
        dimension_type = dimension._dimension_type
        if dimension_type == DimensionType.SELECTOR:
            return headers["descs"], "Unclassified"
        elif dimension_type == DimensionType.BANDED_DATE:
            if not convert_index:
                return headers["descs"], "Unclassified"
            else:
                return (
                    headers["codes"],
                    {
                        "Years": "0000",
                        "Quarters": "000000",
                        "Months": "000000",
                        "Day": "00000000",
                    }[dimension.banding],
                )
        else:
            raise ValueError(f"Unrecognised dimension type: {dimension_type}")

    @staticmethod
    def _convert_headers(headers, dimension):
        if dimension._dimension_type == DimensionType.SELECTOR:
            return headers
        elif dimension._dimension_type == DimensionType.BANDED_DATE:
            period = {"Years": "Y", "Quarters": "Q", "Months": "M", "Day": "D"}[
                dimension.banding
            ]
            unclassified = {
                "Years": "0000",
                "Quarters": "000000",
                "Months": "000000",
                "Day": "00000000",
            }[dimension.banding]

            converted = []
            for c in headers:
                if c == unclassified:
                    converted.append(pd.NaT)
                elif c == "TOTAL":
                    converted.append("TOTAL")
                else:
                    converted.append(pd.Period(c, freq=period))
            return converted
        else:
            raise ValueError(f"Unrecognised dimension type: {dimension}")

