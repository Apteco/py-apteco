from unittest.mock import MagicMock, Mock, call, patch

import apteco_api as aa
import pytest

from apteco.datagrid import DataGrid


@pytest.fixture()
def fake_datagrid(
    rtl_var_customer_id,
    rtl_var_customer_first_name,
    rtl_var_customer_surname,
    rtl_sel_last_week_customers,
    rtl_table_customers,
    rtl_session,
):
    dg = DataGrid.__new__(DataGrid)
    dg.columns = [
        rtl_var_customer_id,
        rtl_var_customer_first_name,
        rtl_var_customer_surname,
    ]
    dg.selection = rtl_sel_last_week_customers
    dg.table = rtl_table_customers
    dg.max_rows = 1234
    dg.session = rtl_session
    dg._data = "my_datagrid_data"
    return dg


class TestDataGrid:
    @patch("apteco.datagrid.DataGrid._get_data")
    @patch("apteco.datagrid.DataGrid._check_inputs")
    def test_init(self, patch__check_inputs, patch__get_data):
        patch__get_data.return_value = "my_datagrid_data"
        datagrid_example = DataGrid(
            ["variables", "for", "my", "columns"],
            "my_selection",
            "my_table",
            session="my_session"
        )
        assert datagrid_example.columns == ["variables", "for", "my", "columns"]
        assert datagrid_example.selection == "my_selection"
        assert datagrid_example.table == "my_table"
        assert datagrid_example.session == "my_session"
        assert datagrid_example._data == "my_datagrid_data"
        patch__check_inputs.assert_called_once_with()
        patch__check_inputs.assert_called_once_with()

    @patch("pandas.DataFrame")
    def test_to_df(
        self,
        patch_pd_dataframe,
        fake_datagrid,
    ):
        fake_getitem = MagicMock(side_effect=["column1", "column2", "column3"])
        fake_setitem = MagicMock()
        fake_dataframe = Mock(iloc=MagicMock(
            __getitem__=fake_getitem,
            __setitem__=fake_setitem,
        ))
        patch_pd_dataframe.return_value = fake_dataframe
        fake_datagrid._convert_column = Mock(side_effect=[
            "converted_column1",
            "converted_column2",
            "converted_column3",
        ])

        df = fake_datagrid.to_df()

        assert df is fake_dataframe
        patch_pd_dataframe.assert_called_once_with(
            "my_datagrid_data",
            columns=["Customer ID", "Customer First Name", "Customer Surname"]
        )
        convert_column_calls = [
            call("column1", "Reference"),
            call("column2", "Text"),
            call("column3", "Text"),
        ]
        getitem_calls = [
            call((slice(None, None, None), 0)),
            call((slice(None, None, None), 1)),
            call((slice(None, None, None), 2)),
        ]
        setitem_calls = [
            call((slice(None, None, None), 0), "converted_column1"),
            call((slice(None, None, None), 1), "converted_column2"),
            call((slice(None, None, None), 2), "converted_column3"),
        ]
        fake_datagrid._convert_column.assert_has_calls(convert_column_calls)
        fake_getitem.assert_has_calls(getitem_calls)
        fake_setitem.assert_has_calls(setitem_calls)

    @patch("apteco.datagrid.DataGrid._check_columns")
    def test__check_inputs(self, patch__check_columns, fake_datagrid):
        fake_datagrid._check_inputs()
        patch__check_columns.assert_called_once_with()

    @patch("apteco.datagrid.DataGrid._check_columns")
    def test__check_inputs_no_session(self, patch__check_columns, fake_datagrid):
        fake_datagrid.session = None
        with pytest.raises(ValueError) as exc_info:
            fake_datagrid._check_inputs()
        assert exc_info.value.args[0] == (
            "You must provide a valid session (none was given)."
        )
        patch__check_columns.assert_not_called()

    @patch("apteco.datagrid.DataGrid._check_columns")
    def test__check_inputs_max_rows_is_float(self, patch__check_columns, fake_datagrid):
        fake_datagrid.max_rows = 987.6
        fake_datagrid._check_inputs()
        assert fake_datagrid.max_rows == 987
        patch__check_columns.assert_called_once_with()

    @patch("apteco.datagrid.DataGrid._check_columns")
    def test__check_inputs_max_rows_is_int_as_str(
        self,
        patch__check_columns,
        fake_datagrid
    ):
        fake_datagrid.max_rows = "456"
        fake_datagrid._check_inputs()
        assert fake_datagrid.max_rows == 456
        patch__check_columns.assert_called_once_with()

    @patch("apteco.datagrid.DataGrid._check_columns")
    def test__check_inputs_max_rows_is_negative(
        self,
        patch__check_columns,
        fake_datagrid
    ):
        fake_datagrid.max_rows = -2468
        with pytest.raises(ValueError) as exc_info:
            fake_datagrid._check_inputs()
        assert exc_info.value.args[0] == "max_rows must be a number greater than 0"
        patch__check_columns.assert_not_called()

    @patch("apteco.datagrid.DataGrid._check_columns")
    def test__check_inputs_max_rows_is_not_number(
        self,
        patch__check_columns,
        fake_datagrid
    ):
        fake_datagrid.max_rows = "all"
        with pytest.raises(ValueError) as exc_info:
            fake_datagrid._check_inputs()
        assert exc_info.value.args[0] == "max_rows must be a number greater than 0"
        patch__check_columns.assert_not_called()

    @patch("apteco.datagrid.DataGrid._check_columns")
    def test__check_inputs_max_rows_is_none(self, patch__check_columns, fake_datagrid):
        fake_datagrid.max_rows = None
        with pytest.raises(ValueError) as exc_info:
            fake_datagrid._check_inputs()
        assert exc_info.value.args[0] == "max_rows must be a number greater than 0"
        patch__check_columns.assert_not_called()

    @patch("apteco.datagrid.DataGrid._check_columns")
    def test__check_inputs_no_columns(self, patch__check_columns, fake_datagrid):
        fake_datagrid.columns = []
        with pytest.raises(ValueError) as exc_info:
            fake_datagrid._check_inputs()
        assert exc_info.value.args[0] == (
            "You must specify at least one variable"
            " to use as a column on the data grid (none was given)."
        )
        patch__check_columns.assert_not_called()

    @patch("apteco.datagrid.DataGrid._check_columns")
    def test__check_inputs_no_table_with_sel(
        self,
        patch__check_columns,
        fake_datagrid,
        rtl_table_customers
    ):
        fake_datagrid.table = None
        fake_datagrid._check_inputs()
        assert fake_datagrid.table is rtl_table_customers
        patch__check_columns.assert_called_once_with()

    @patch("apteco.datagrid.DataGrid._check_columns")
    def test__check_inputs_no_table_no_sel(self, patch__check_columns, fake_datagrid):
        fake_datagrid.table = None
        fake_datagrid.selection = None
        with pytest.raises(ValueError) as exc_info:
            fake_datagrid._check_inputs()
        assert exc_info.value.args[0] == (
            "You must specify the resolve table of the data grid (none was given)."
        )
        patch__check_columns.assert_not_called()

    def test__check_columns(self, fake_datagrid):
        fake_datagrid._check_columns()

    def test__check_columns_multiple_tables(
        self, fake_datagrid, rtl_table_customers, rtl_var_purchase_id
    ):
        fake_datagrid.columns.append(rtl_var_purchase_id)
        rtl_table_customers.is_ancestor = Mock(side_effect=[True, True, True])
        rtl_var_purchase_id.table.is_ancestor = Mock(side_effect=[True])
        fake_datagrid._check_columns()

    def test__check_columns_bad_table(
        self, fake_datagrid, rtl_table_customers, rtl_var_purchase_id
    ):
        fake_datagrid.columns.append(rtl_var_purchase_id)
        rtl_table_customers.is_ancestor = Mock(side_effect=[True, True, True])
        rtl_var_purchase_id.table.is_ancestor = Mock(side_effect=[False])
        with pytest.raises(ValueError) as exc_info:
            fake_datagrid._check_columns()
        assert exc_info.value.args[0] == (
            "The resolve table of the data grid is 'Customers',"
            " but the variable 'puID' belongs to the"
            " 'Purchases' table."
            "\nOnly variables from the same table as the data grid"
            " or from ancestor tables can be used as data grid columns."
        )

    def test__check_columns_bad_variable(
        self,
        fake_datagrid,
        rtl_var_customer_contact_pref,
    ):
        fake_datagrid.columns.append(rtl_var_customer_contact_pref)
        with pytest.raises(ValueError) as exc_info:
            fake_datagrid._check_columns()
        assert exc_info.value.args[0] == (
            "The variable 'cuContac' has type 'FlagArray'."
            "\nArray and Flag Array variables"
            " are not currently supported as data grid columns."
        )

    @patch("apteco_api.Column")
    def test__create_columns(self, patch_aa_column, fake_datagrid):
        patch_aa_column.side_effect = ["First column", "Second column", "Third column"]
        column_calls = [
            call(id="0", variable_name="cuID", column_header="Customer ID"),
            call(id="1", variable_name="cuFName", column_header="Customer First Name"),
            call(id="2", variable_name="cuSName", column_header="Customer Surname"),
        ]
        columns = fake_datagrid._create_columns()
        assert columns == ["First column", "Second column", "Third column"]
        patch_aa_column.assert_has_calls(column_calls)

    @patch("apteco_api.ExportsApi")
    @patch("apteco.datagrid.DataGrid._create_columns")
    def test__get_export(self, patch__create_columns, patch_aa_exports_api, fake_datagrid):
        patch__create_columns.return_value = ["a", "list", "of", "columns"]
        fake_exports_perform_export_sync = Mock(return_value="your_export_result")
        patch_aa_exports_api.return_value = Mock(
            exports_perform_export_synchronously=fake_exports_perform_export_sync
        )
        expected_export = aa.Export(
            base_query=aa.Query(
                selection=aa.Selection(
                    table_name="Customers",
                    rule=aa.Rule(clause="selection_model")
                )
            ),
            resolve_table_name="Customers",
            maximum_number_of_rows_to_browse=1234,
            return_browse_rows=True,
            columns=["a", "list", "of", "columns"]
        )
        export_result = fake_datagrid._get_export()
        assert export_result == "your_export_result"
        patch_aa_exports_api.assert_called_once_with("my_api_client")
        fake_exports_perform_export_sync.assert_called_once_with(
            "acme_inc", "retail", export=expected_export
        )

    @patch("apteco.datagrid.DataGrid._get_export")
    def test__get_data(self, patch__get_export, fake_datagrid):
        fake_export_result = Mock(rows=[
            Mock(descriptions="Sweden\tMale\tMidlands\t87.65"),
            Mock(descriptions="France\tFemale\tLondon\t0.00"),
            Mock(descriptions="Germany\tMale\tSouth East\t345.67"),
        ])
        patch__get_export.return_value = fake_export_result
        export_result = fake_datagrid._get_data()
        patch__get_export.assert_called_once_with()
        assert export_result == [
            ("Sweden", "Male", "Midlands", "87.65"),
            ("France", "Female", "London", "0.00"),
            ("Germany", "Male", "South East", "345.67"),
        ]
