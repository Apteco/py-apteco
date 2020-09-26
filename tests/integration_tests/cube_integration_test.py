from datetime import datetime

import pandas as pd

from apteco import Cube


def assert_cube_dataframes_match(
        test_df, expected_df, missing_subtotals=True, missing_recordless=False
):
    """Check that two cube DataFrames match.

    Compare test data with reference data, ignoring dtype,
    and optionally allowing for some subtotals to be missing in reference data.

    Args:
        test_df (pd.DataFrame): cube data to check
        expected_df (pd.DataFrame): expected correct data
        missing_subtotals (bool):
            allow for expected data to be missing some subtotals
        missing_recordless (bool):
            allow for test data to be missing "NO RECORDS" rows
            (applicable when resolve table is ancestor of dimensions table)

    Raises:
        AssertionError: if DataFrame entries aren't equal,
            or if rows are missing other than subtotal or "NO RECORDS" rows

    """

    if missing_subtotals:
        missing_ref_indices = test_df.index.difference(expected_df.index)
        assert all("TOTAL" in idx for idx in missing_ref_indices)
        test_df_reduced = test_df.reindex(test_df.index.intersection(expected_df.index))
    else:
        test_df_reduced = test_df

    if missing_recordless:
        missing_test_indices = expected_df.index.difference(test_df.index)
        assert all(any("NO " in i for i in idx) for idx in missing_test_indices)
        expected_df_reduced = expected_df.reindex(test_df.index.intersection(expected_df.index))
    else:
        expected_df_reduced = expected_df

    pd.testing.assert_frame_equal(
        test_df_reduced,
        expected_df_reduced,
        check_dtype=False,
    )


def test_cube_to_df_people_various_dimensions(
    holidays, people, cube_001_people_various_dimensions
):

    cube = Cube(
        [people[var] for var in ("Income", "Occupation", "Source")],
        table=people,
        session=holidays,
    )
    df = cube.to_df()

    assert_cube_dataframes_match(df, cube_001_people_various_dimensions)


def test_cube_to_df_bookings_before_2020_cost_less_than_500(
    holidays, bookings, cube_002_bookings_before_2020_cost_less_than_500
):

    cube = Cube(
        [bookings[var] for var in ("Destination", "Product", "Response Code")],
        selection=(
            (bookings["Cost"] < 500) & (bookings["boDate"] <= datetime(2019, 12, 31))
        ),
        session=holidays,
    )
    df = cube.to_df()

    assert_cube_dataframes_match(df, cube_002_bookings_before_2020_cost_less_than_500)


def test_cube_to_df_people_dimensions_bookings_table(
    holidays, people, bookings, cube_003_people_dimensions_bookings_table
):

    cube = Cube(
        [people[var] for var in ("Source", "Occupation")],
        table=bookings,
        session=holidays,
    )
    df = cube.to_df()

    assert_cube_dataframes_match(df, cube_003_people_dimensions_bookings_table)


def test_cube_to_df_bookings_dimensions_households_selection_people_table(
    holidays,
    households,
    people,
    bookings,
    cube_004_bookings_dimensions_households_selection_people_table,
):

    cube = Cube(
        [bookings[var] for var in ("Product", "Continent")],
        selection=(
            (households["Region"] == ("02", "13"))
            | (households["HHCarmak"] == ("FER", "FIA", "FOR"))
        ),
        table=people,
        session=holidays,
    )
    df = cube.to_df()

    assert_cube_dataframes_match(
        df,
        cube_004_bookings_dimensions_households_selection_people_table,
        missing_recordless=True,
    )
