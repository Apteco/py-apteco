from unittest.mock import MagicMock, Mock, call, patch

import apteco_api as aa
import pytest

from apteco.cube import Cube
from tests.unit_tests.apteco.conftest import (
    fake_sel_high_value_purchases, fake_table_purchases
)  # have to import fixtures like this to use in parametrized testing


@pytest.fixture()
def fake_cube_data():
    return Mock(ravel=Mock(return_value="flattened_cube_data"))


@pytest.fixture()
def fake_cube_headers():
    headers = MagicMock()
    headers.__getitem__ = Mock(return_value="cube_header_descriptions")
    return headers


@pytest.fixture()
def fake_cube_sizes():
    return Mock()


@pytest.fixture()
def fake_cube(
    fake_var_purchase_store_type,
    fake_var_purchase_payment_method,
    fake_var_purchase_department,
    fake_sel_high_value_purchases,
    fake_table_purchases,
    fake_session,
    fake_cube_data,
    fake_cube_headers,
    fake_cube_sizes,
):
    cube = Cube.__new__(Cube)
    cube.dimensions = [
        fake_var_purchase_store_type,
        fake_var_purchase_payment_method,
        fake_var_purchase_department,
    ]
    cube.measures = None
    cube.selection = fake_sel_high_value_purchases
    cube.table = fake_table_purchases
    cube.session = fake_session
    cube._data = fake_cube_data
    cube._headers = fake_cube_headers
    cube._sizes = fake_cube_sizes
    return cube


class TestCube:
    @patch("apteco.cube.Cube._get_data")
    @patch("apteco.cube.Cube._check_inputs")
    def test_init(self, patch__check_inputs, patch__get_data):
        patch__get_data.return_value = ("my_data", "my_headers", "my_sizes")
        cube_example = Cube(
            ["variables", "for", "dimensions"],
            selection="my_selection",
            table="my_table",
            session="my_session",
        )
        assert cube_example.dimensions == ["variables", "for", "dimensions"]
        assert cube_example.measures is None
        assert cube_example.selection == "my_selection"
        assert cube_example.table == "my_table"
        assert cube_example.session == "my_session"
        assert cube_example._data == "my_data"
        assert cube_example._headers == "my_headers"
        assert cube_example._sizes == "my_sizes"
        patch__check_inputs.assert_called_once_with()
        patch__get_data.assert_called_once_with()

    @patch("pandas.MultiIndex.from_product")
    @patch("pandas.DataFrame")
    def test_to_df(self, patch_pd_dataframe, patch_pd_mi_fp, fake_cube, fake_cube_data, fake_cube_headers):
        patch_pd_dataframe.return_value = "my_cube_df"
        patch_pd_mi_fp.return_value = "multi_index_for_cube_df"
        df = fake_cube.to_df()
        assert df == "my_cube_df"
        patch_pd_dataframe.assert_called_once_with(
            "flattened_cube_data",
            index="multi_index_for_cube_df",
            columns=["Purchases"],
        )
        fake_cube_data.ravel.assert_called_once_with()
        patch_pd_mi_fp.assert_called_once_with("cube_header_descriptions", names=[
            "Store Type",
            "Payment Method",
            "Department",
        ])
        fake_cube_headers.__getitem__.assert_called_once_with("descs")

    @patch("apteco.cube.Cube._check_dimensions")
    def test__check_inputs(self, patch__check_dimensions, fake_cube):
        fake_cube._check_inputs()
        patch__check_dimensions.assert_called_once_with()

    @patch("apteco.cube.Cube._check_dimensions")
    def test__check_inputs_no_session(self, patch__check_dimensions, fake_cube):
        fake_cube.session = None
        with pytest.raises(ValueError) as exc_info:
            fake_cube._check_inputs()
        assert exc_info.value.args[0] == (
            "You must provide a valid session (none was given)."
        )
        patch__check_dimensions.assert_not_called()

    @patch("apteco.cube.Cube._check_dimensions")
    def test__check_inputs_no_dimensions(self, patch__check_dimensions, fake_cube):
        fake_cube.dimensions = []
        with pytest.raises(ValueError) as exc_info:
            fake_cube._check_inputs()
        assert exc_info.value.args[0] == (
            "You must specify at least one variable"
            " to use as a dimension on the cube (none was given)."
        )
        patch__check_dimensions.assert_not_called()

    @patch("apteco.cube.Cube._check_dimensions")
    def test__check_inputs_measures_is_bad(self, patch__check_dimensions, fake_cube, fake_var_purchase_department):
        fake_cube.measures = [fake_var_purchase_department]
        with pytest.raises(ValueError) as exc_info:
            fake_cube._check_inputs()
        assert exc_info.value.args[0] == (
            "Only the default count measure is currently supported"
            " for cubes, and this is set automatically."
            " `measures` argument should be `None` or omitted,"
            " and is only included now for forwards-compatibility."
        )
        patch__check_dimensions.assert_not_called()

    @patch("apteco.cube.Cube._check_dimensions")
    def test__check_inputs_no_table_with_sel(self, patch__check_dimensions, fake_cube, fake_table_purchases):
        fake_cube.table = None
        fake_cube._check_inputs()
        assert fake_cube.table == fake_table_purchases
        patch__check_dimensions.assert_called_once_with()

    @patch("apteco.cube.Cube._check_dimensions")
    def test__check_inputs_no_table_no_sel(self, patch__check_dimensions, fake_cube):
        fake_cube.table = None
        fake_cube.selection = None
        with pytest.raises(ValueError) as exc_info:
            fake_cube._check_inputs()
        assert exc_info.value.args[0] == (
            "You must specify the resolve table of the cube"
            " (no table or selection was given)."
        )
        patch__check_dimensions.assert_not_called()

    def test__check_dimensions(self, fake_cube):
        fake_cube._check_dimensions()

    def test__check_dimensions_bad_type(self, fake_cube, fake_var_purchase_date):
        fake_cube.dimensions.append(fake_var_purchase_date)
        with pytest.raises(ValueError) as exc_info:
            fake_cube._check_dimensions()
        assert exc_info.value.args[0] == (
            "The variable 'puDate' has type 'DateTime'."
            "\nOnly Selector variables (excluding sub-types)"
            " are currently supported as cube dimensions."
        )

    def test__check_dimensions_multiple_tables(
        self,
        fake_cube,
        fake_table_purchases,
        fake_table_customers,
        fake_var_customer_gender,
    ):
        fake_cube.dimensions.append(fake_var_customer_gender)
        fake_table_purchases.is_related = Mock(side_effect=[True, True, True])
        fake_table_customers.is_related = Mock(side_effect=[True])
        fake_cube._check_dimensions()

    def test__check_dimensions_bad_table(
        self,
        fake_cube,
        fake_table_purchases,
        fake_table_customers,
        fake_var_customer_gender,
    ):
        fake_cube.dimensions.append(fake_var_customer_gender)
        fake_table_purchases.is_related = Mock(side_effect=[True, True, True])
        fake_table_customers.is_related = Mock(side_effect=[False])
        with pytest.raises(ValueError) as exc_info:
            fake_cube._check_dimensions()
        assert exc_info.value.args[0] == (
            "The counting table of the cube is 'Purchases',"
            " but the variable 'cuGender' belongs to the"
            " 'Customers' table."
            "\nOnly variables from the same table as the cube"
            " or from related tables can be used as cube dimensions."
        )

    @patch("apteco_api.Dimension")
    def test__create_dimensions(self, patch_aa_dimension, fake_cube):
        patch_aa_dimension.side_effect = ["First dim", "Second dim", "Third dim"]
        dimension_calls = [
            call(id="0", type="Selector", variable_name="puStType"),
            call(id="1", type="Selector", variable_name="puPayMtd"),
            call(id="2", type="Selector", variable_name="puDept"),
        ]
        dimensions = fake_cube._create_dimensions()
        assert dimensions == ["First dim", "Second dim", "Third dim"]
        patch_aa_dimension.assert_has_calls(dimension_calls)

    @patch("apteco_api.Measure")
    def test__create_measures(self, patch_aa_measure, fake_cube):
        patch_aa_measure.side_effect = ["Table count measure"]
        measures = fake_cube._create_measures()
        assert measures == ["Table count measure"]
        patch_aa_measure.assert_called_once_with(
            id="0", resolve_table_name="Purchases", function="Count", variable_name=None
        )

    @pytest.mark.parametrize(
        "selection, expected_selection",
        [
            (None, aa.Selection(table_name="Purchases")),
            (
                # https://github.com/pytest-dev/pytest/issues/349#issuecomment-230353026
                fake_sel_high_value_purchases(fake_table_purchases()),
                aa.Selection(
                    table_name="Purchases",
                    rule=aa.Rule(clause="selection_high_value_purchases_model")
                ),
            ),
        ],
        ids=["no_selection", "with_selection"],
    )
    @patch("apteco_api.CubesApi")
    @patch("apteco.cube.Cube._create_measures")
    @patch("apteco.cube.Cube._create_dimensions")
    def test__get_cube(
        self,
        patch__create_dimensions,
        patch__create_measures,
        patch_aa_cubes_api,
        fake_cube,
        selection,
        expected_selection,
    ):
        fake_cube.selection = selection

        patch__create_dimensions.return_value = ["a", "list", "of", "dimensions"]
        patch__create_measures.return_value = ["some", "measures"]
        fake_cubes_calculate_cube_sync = Mock(return_value="your_cube_result")
        patch_aa_cubes_api.return_value = Mock(
            cubes_calculate_cube_synchronously=fake_cubes_calculate_cube_sync
        )
        expected_cube = aa.Cube(
            base_query=aa.Query(selection=expected_selection),
            resolve_table_name="Purchases",
            storage="Full",
            dimensions=["a", "list", "of", "dimensions"],
            measures=["some", "measures"],
        )

        cube_result = fake_cube._get_cube()

        assert cube_result == "your_cube_result"
        patch_aa_cubes_api.assert_called_once_with("my_api_client")
        fake_cubes_calculate_cube_sync.assert_called_once_with(
            "acme_inc", "sales", cube=expected_cube
        )

    @patch("numpy.array")
    @patch("apteco.cube.Cube._get_cube")
    def test__get_data(self, patch__get_cube, patch_np_array, fake_cube):
        fake_cube_result = Mock(
            measure_results=[Mock(rows=["1\t2\t3", "4\t5\t6", "7\t8\t9"])],
            dimension_results=[
                Mock(
                    header_codes="S\tF\tO",
                    header_descriptions="Shop\tFranchise\tOnline",
                ),
                Mock(
                    header_codes="0\t1\t2\t3\t4",
                    header_descriptions="Cash\tCard\tCheque\tVoucher\tGift Card",
                ),
                Mock(
                    header_codes="HO\tGA\tEL\tDI",
                    header_descriptions="Home\tGarden\tElectronics\tDIY",
                ),
            ]
        )
        patch__get_cube.return_value = fake_cube_result
        fake_reshape = Mock(return_value="my_reshaped_data")
        patch_np_array.return_value = Mock(T=Mock(reshape=fake_reshape))
        # expected_raw_data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        expected_raw_data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        expected_headers = {
            "codes": [
                ["S", "F", "O"],
                ["0", "1", "2", "3", "4"],
                ["HO", "GA", "EL", "DI"],
            ],
            "descs": [
                ["Shop", "Franchise", "Online"],
                ["Cash", "Card", "Cheque", "Voucher", "Gift Card"],
                ["Home", "Garden", "Electronics", "DIY"],
            ]
        }
        expected_sizes = (3, 5, 4)

        data, headers, sizes = fake_cube._get_data()

        assert data == "my_reshaped_data"
        assert headers == expected_headers
        assert sizes == expected_sizes
        patch_np_array.assert_called_once_with(expected_raw_data)
        fake_reshape.assert_called_once_with(expected_sizes, order="F")
