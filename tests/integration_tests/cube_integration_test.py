from datetime import datetime

import pandas as pd
import pytest

from apteco import Cube
from apteco.statistics import Mean, Sum


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
            or if rows are missing other than subtotal rows

    """

    if missing_subtotals:
        missing_ref_indices = test_df.index.difference(expected_df.index)
        assert all("TOTAL" in idx for idx in missing_ref_indices)
        test_df_reduced = test_df.reindex(test_df.index.intersection(expected_df.index))
    else:
        test_df_reduced = test_df

    pd.testing.assert_frame_equal(test_df_reduced, expected_df, check_dtype=False)


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
        df, cube_004_bookings_dimensions_households_selection_people_table
    )


def test_cube_to_df_mixed_households_people_dimensions_households_table(
    holidays,
    households,
    people,
    cube_005_mixed_households_people_dimensions_households_table,
):

    cube = Cube(
        [people[var] for var in ("Income", "Gender")] + [households["Region"]],
        table=households,
        session=holidays,
    )
    df = cube.to_df()

    assert_cube_dataframes_match(
        df, cube_005_mixed_households_people_dimensions_households_table
    )


def test_cube_to_df_mixed_hhds_jnys_ppl_dimensions_people_selection_journeys_table(
    holidays,
    households,
    people,
    bookings,
    journeys,
    cube_006_mixed_hhds_jnys_ppl_dimensions_people_selection_journeys_table,
):

    cube = Cube(
        [households["Region"], journeys["Pool"], people["Gender"]],
        selection=(
            (people["Surname"].contains(["int", "str", "bool"], match_case=False))
            | (bookings["Continent"] == ("AM", "AU"))
        ),
        table=journeys,
        session=holidays,
    )
    df = cube.to_df()

    assert_cube_dataframes_match(
        df, cube_006_mixed_hhds_jnys_ppl_dimensions_people_selection_journeys_table
    )


def test_cube_bad_dimensions_invalid_tables(holidays, people, bookings, policies):
    with pytest.raises(ValueError) as exc_info:
        cube_with_bad_dimensions = Cube(
            [people["Occupation"], bookings["Destination"], policies["Cover"]],
            table=bookings,
            session=holidays,
        )
    assert exc_info.value.args[0] == (
        f"The resolve table of the cube is 'Bookings',"
        f" but the variable 'PoCover' belongs to the"
        f" 'Policies' table."
        f"\nOnly variables from the same table as the cube"
        f" or from related tables can be used as cube dimensions."
    )


def test_cube_to_df_bookings_single_dimension_default_count_measure(
    holidays, bookings, cube_007_bookings_single_dimension_default_count_measure
):

    cube = Cube([bookings["Destination"]], table=bookings, session=holidays)
    df = cube.to_df()

    assert_cube_dataframes_match(
        df, cube_007_bookings_single_dimension_default_count_measure, False
    )


def test_cube_to_df_bookings_single_non_count_measure(
    holidays, bookings, cube_008_bookings_dimension_destination_measure_sum_profit
):

    cube = Cube(
        [bookings["Destination"]],
        [Sum(bookings["Profit"])],
        table=bookings,
        session=holidays,
    )
    df = cube.to_df()

    assert_cube_dataframes_match(
        df, cube_008_bookings_dimension_destination_measure_sum_profit, False
    )


def test_cube_to_df_bookings_multiple_measures(
    holidays, bookings, cube_009_bookings_multiple_measures
):

    cube = Cube(
        [bookings["Destination"]],
        [bookings, Sum(bookings["Profit"]), Mean(bookings["Cost"])],
        table=bookings,
        session=holidays,
    )
    df = cube.to_df()

    assert_cube_dataframes_match(df, cube_009_bookings_multiple_measures)
