import pandas as pd
import pytest

from apteco import DataGrid


def test_datagrid_to_df_bookings_various_columns(
    holidays, bookings, datagrid_001_bookings_various_columns
):

    bookings_dg = DataGrid(
        [
            bookings[var]
            for var in (
                "boURN",  # Reference (Numeric)
                "boDest",  # Selector
                "boProd",  # Selector
                "boCost",  # Currency (2 dp)
                "boDate",  # Date
            )
        ],
        table=bookings,
        session=holidays,
    )
    bookings_df = bookings_dg.to_df()

    pd.testing.assert_frame_equal(bookings_df, datagrid_001_bookings_various_columns)


def test_datagrid_to_df_policies_2000_rows_various_columns(
    holidays, policies, datagrid_002_policies_2000_rows_various_columns
):

    policies_dg = DataGrid(
        [
            policies[var]
            for var in (
                "PoPolicy",  # Reference (Numeric)
                "PoDaysUn",  # Numeric (0 dp)
                "PoPremiu",  # Currency (2 dp)
                "PoPolic1",  # Date
                "PoCover",  # Selector
            )
        ],
        max_rows=2000,
        table=policies,
        session=holidays,
    )
    pol_df = policies_dg.to_df()

    pd.testing.assert_frame_equal(
        pol_df, datagrid_002_policies_2000_rows_various_columns
    )


def test_datagrid_to_df_web_visits_mobile_social_media_1500_rows_all_columns(
    holidays,
    web_visits,
    datagrid_003_web_visits_mobile_social_media_1500_rows_all_columns,
):

    web_visits_dg = DataGrid(
        [
            web_visits[var]
            for var in (
                "wvURN",  # Reference (Numeric)
                "wvURL",  # Text
                "wvTime",  # DateTime
                "wvDevice",  # Selector
                "wvDuratn",  # Numeric (0 dp, with missing)
                "wvSource",  # Selector
            )
        ],
        selection=((web_visits["wvSource"] == "S") & (web_visits["wvDevice"] == "3")),
        max_rows=1500,
        session=holidays,
    )
    web_visits_df = web_visits_dg.to_df()

    pd.testing.assert_frame_equal(
        web_visits_df, datagrid_003_web_visits_mobile_social_media_1500_rows_all_columns
    )


def test_datagrid_to_df_bookings_500_rows_households_selection(
    holidays, households, bookings, datagrid_004_bookings_with_households_selection
):

    bookings_dg = DataGrid(
        [
            bookings[var]
            for var in (
                "Booking URN",  # Reference (Numeric)
                "Destination",  # Selector
                "Travel Date",  # Date
                "Type",  # Selector
                "Profit",  # Currency (2 dp)
            )
        ],
        selection=(
            (households["Region"] == "02")
            & households["Address"].contains("street", match_case=False)
        ),
        table=bookings,
        session=holidays,
    )
    bookings_df = bookings_dg.to_df()

    pd.testing.assert_frame_equal(
        bookings_df, datagrid_004_bookings_with_households_selection
    )


def test_datagrid_bad_columns_invalid_tables(holidays, households, people, bookings):
    with pytest.raises(ValueError) as exc_info:
        datagrid_with_bad_columns = DataGrid(
            [households["Region"], people["Surname"], bookings["Destination"]],
            table=people,
            session=holidays,
        )
    assert exc_info.value.args[0] == (
        "The resolve table of the data grid is 'People',"
        " but the variable 'boDest' belongs to the 'Bookings' table."
        "\nOnly variables from the same table as the data grid"
        " or from ancestor tables can be used as data grid columns."
    )


def test_datagrid_to_df_bookings_columns_mixed_tables(
    holidays, households, people, bookings, datagrid_005_bookings_with_mixed_columns
):

    bookings_dg = DataGrid(
        [
            bookings["Booking URN"],  # Reference (Numeric)
            bookings["Destination"],  # Selector
            people["Occupation"],  # Selector
            people["DOB"],  # Date
            households["Town"],  # Selector
        ],
        table=bookings,
        session=holidays,
    )
    bookings_df = bookings_dg.to_df()

    pd.testing.assert_frame_equal(
        bookings_df, datagrid_005_bookings_with_mixed_columns
    )
