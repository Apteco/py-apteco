from datetime import datetime

import pandas as pd

from apteco import Cube


def assert_cube_dataframes_match(test_df, expected_df, missing_subtotals=True):
    """Check that two cube DataFrames match.

    Compare test data with reference data, ignoring dtype,
    and optionally allowing for some subtotals to be missing in reference data.

    Args:
        test_df (pd.DataFrame): cube data to check
        expected_df (pd.DataFrame): expected correct data
        missing_subtotals (bool):
            allow for expected data to be missing some subtotals

    Raises:
        AssertionError: if DataFrame entries aren't equal,
            or if missing indices include non-total cells

    """

    if missing_subtotals:
        missing_indices = test_df.index.difference(expected_df.index)
        assert all("TOTAL" in idx for idx in missing_indices)
        df_reduced = test_df.reindex(test_df.index.intersection(expected_df.index))
    else:
        df_reduced = test_df

    pd.testing.assert_frame_equal(
        df_reduced,
        expected_df,
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
