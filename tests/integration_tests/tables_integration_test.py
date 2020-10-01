from datetime import datetime

import pandas as pd
import pytest

from tests.integration_tests.cube_integration_test import assert_cube_dataframes_match


class TestTableRelations:
    def test_is_same(self, households, people, bookings, responses):
        assert households.is_same(households)
        assert not households.is_same(people)
        assert not households.is_same(bookings)
        assert not households.is_same(responses)

        assert not people.is_same(households)
        assert people.is_same(people)
        assert not people.is_same(bookings)
        assert not people.is_same(responses)

        assert not bookings.is_same(households)
        assert not bookings.is_same(people)
        assert bookings.is_same(bookings)
        assert not bookings.is_same(responses)

        assert not responses.is_same(households)
        assert not responses.is_same(people)
        assert not responses.is_same(bookings)
        assert responses.is_same(responses)

    def test_is_ancestor(self, households, people, bookings, responses):
        assert not households.is_ancestor(households)
        assert households.is_ancestor(people)
        assert households.is_ancestor(bookings)
        assert households.is_ancestor(responses)
        assert households.is_ancestor(households, allow_same=True)
        assert households.is_ancestor(people, allow_same=True)
        assert households.is_ancestor(bookings, allow_same=True)
        assert households.is_ancestor(responses, allow_same=True)

        assert not people.is_ancestor(households)
        assert not people.is_ancestor(people)
        assert people.is_ancestor(bookings)
        assert people.is_ancestor(responses)
        assert not people.is_ancestor(households, allow_same=True)
        assert people.is_ancestor(people, allow_same=True)
        assert people.is_ancestor(bookings, allow_same=True)
        assert people.is_ancestor(responses, allow_same=True)

        assert not bookings.is_ancestor(households)
        assert not bookings.is_ancestor(people)
        assert not bookings.is_ancestor(bookings)
        assert not bookings.is_ancestor(responses)
        assert not bookings.is_ancestor(households, allow_same=True)
        assert not bookings.is_ancestor(people, allow_same=True)
        assert bookings.is_ancestor(bookings, allow_same=True)
        assert not bookings.is_ancestor(responses, allow_same=True)

        assert not responses.is_ancestor(households)
        assert not responses.is_ancestor(people)
        assert not responses.is_ancestor(bookings)
        assert not responses.is_ancestor(responses)
        assert not responses.is_ancestor(households, allow_same=True)
        assert not responses.is_ancestor(people, allow_same=True)
        assert not responses.is_ancestor(bookings, allow_same=True)
        assert responses.is_ancestor(responses, allow_same=True)

    def test_is_descendant(self, households, people, bookings, responses):
        assert not households.is_descendant(households)
        assert not households.is_descendant(people)
        assert not households.is_descendant(bookings)
        assert not households.is_descendant(responses)
        assert households.is_descendant(households, allow_same=True)
        assert not households.is_descendant(people, allow_same=True)
        assert not households.is_descendant(bookings, allow_same=True)
        assert not households.is_descendant(responses, allow_same=True)

        assert people.is_descendant(households)
        assert not people.is_descendant(people)
        assert not people.is_descendant(bookings)
        assert not people.is_descendant(responses)
        assert people.is_descendant(households, allow_same=True)
        assert people.is_descendant(people, allow_same=True)
        assert not people.is_descendant(bookings, allow_same=True)
        assert not people.is_descendant(responses, allow_same=True)

        assert bookings.is_descendant(households)
        assert bookings.is_descendant(people)
        assert not bookings.is_descendant(bookings)
        assert not bookings.is_descendant(responses)
        assert bookings.is_descendant(households, allow_same=True)
        assert bookings.is_descendant(people, allow_same=True)
        assert bookings.is_descendant(bookings, allow_same=True)
        assert not bookings.is_descendant(responses, allow_same=True)

        assert responses.is_descendant(households)
        assert responses.is_descendant(people)
        assert not responses.is_descendant(bookings)
        assert not responses.is_descendant(responses)
        assert responses.is_descendant(households, allow_same=True)
        assert responses.is_descendant(people, allow_same=True)
        assert not responses.is_descendant(bookings, allow_same=True)
        assert responses.is_descendant(responses, allow_same=True)

    def test_is_related(self, households, people, bookings, responses):
        assert not households.is_related(households)
        assert households.is_related(people)
        assert households.is_related(bookings)
        assert households.is_related(responses)
        assert households.is_related(households, allow_same=True)
        assert households.is_related(people, allow_same=True)
        assert households.is_related(bookings, allow_same=True)
        assert households.is_related(responses, allow_same=True)

        assert people.is_related(households)
        assert not people.is_related(people)
        assert people.is_related(bookings)
        assert people.is_related(responses)
        assert people.is_related(households, allow_same=True)
        assert people.is_related(people, allow_same=True)
        assert people.is_related(bookings, allow_same=True)
        assert people.is_related(responses, allow_same=True)

        assert bookings.is_related(households)
        assert bookings.is_related(people)
        assert not bookings.is_related(bookings)
        assert not bookings.is_related(responses)
        assert bookings.is_related(households, allow_same=True)
        assert bookings.is_related(people, allow_same=True)
        assert bookings.is_related(bookings, allow_same=True)
        assert not bookings.is_related(responses, allow_same=True)

        assert responses.is_related(households)
        assert responses.is_related(people)
        assert not responses.is_related(bookings)
        assert not responses.is_related(responses)
        assert responses.is_related(households, allow_same=True)
        assert responses.is_related(people, allow_same=True)
        assert not responses.is_related(bookings, allow_same=True)
        assert responses.is_related(responses, allow_same=True)


class TestTablesAccessor:
    def test_tables_getitem(self, holidays):
        people = holidays.tables["People"]
        assert people.singular == "Person"

    def test_tables_getitem_bad_key(self, holidays):
        with pytest.raises(KeyError) as exc_info:
            not_a_table = holidays.tables["not a table"]
        assert exc_info.value.args[0] == (
            "Lookup key 'not a table' did not match a table name."
        )

    def test_tables_iter(self, holidays):
        tables_with_children = [
            table.name for table in holidays.tables if table.has_children
        ]
        assert sorted(tables_with_children) == [
            "Communications",
            "Households",
            "People",
        ]

    def test_tables_len(self, holidays):
        assert len(holidays.tables) == 9


class TestTablesDataGrid:
    def test_tables_datagrid_bookings_various_columns(
        self, bookings, datagrid_001_bookings_various_columns
    ):

        bookings_dg = bookings.datagrid(
            [
                bookings[var]
                for var in (
                    "Booking URN",
                    "Destination",
                    "Product",
                    "Cost",
                    "Booking Date",
                )
            ]
        )
        bookings_df = bookings_dg.to_df()

        pd.testing.assert_frame_equal(
            bookings_df, datagrid_001_bookings_various_columns
        )

    def test_tables_datagrid_bookings_500_rows_households_selection(
        self, households, bookings, datagrid_004_bookings_with_households_selection
    ):

        bookings_dg = bookings.datagrid(
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
        )
        bookings_df = bookings_dg.to_df()

        pd.testing.assert_frame_equal(
            bookings_df,
            datagrid_004_bookings_with_households_selection,
            check_dtype=False,
        )


class TestTablesCube:
    def test_cube_to_df_people_various_dimensions(
        self, people, cube_001_people_various_dimensions
    ):
        cube = people.cube([people[var] for var in ("Income", "Occupation", "Source")])
        df = cube.to_df()

        assert_cube_dataframes_match(df, cube_001_people_various_dimensions)

    def test_cube_to_df_bookings_before_2020_cost_less_than_500(
        self, bookings, cube_002_bookings_before_2020_cost_less_than_500
    ):
        cube = bookings.cube(
            [bookings[var] for var in ("Destination", "Product", "Response Code")],
            selection=(
                (bookings["Cost"] < 500)
                & (bookings["boDate"] <= datetime(2019, 12, 31))
            ),
        )
        df = cube.to_df()

        assert_cube_dataframes_match(
            df, cube_002_bookings_before_2020_cost_less_than_500
        )

    def test_cube_to_df_people_dimensions_bookings_table(
        self, people, bookings, cube_003_people_dimensions_bookings_table
    ):
        cube = bookings.cube([people[var] for var in ("Source", "Occupation")])
        df = cube.to_df()

        assert_cube_dataframes_match(df, cube_003_people_dimensions_bookings_table)

    def test_cube_to_df_bookings_dimensions_households_selection_people_table(
        self,
        households,
        people,
        bookings,
        cube_004_bookings_dimensions_households_selection_people_table,
    ):
        cube = people.cube(
            [bookings[var] for var in ("Product", "Continent")],
            selection=(
                (households["Region"] == ("02", "13"))
                | (households["HHCarmak"] == ("FER", "FIA", "FOR"))
            ),
        )
        df = cube.to_df()

        assert_cube_dataframes_match(
            df, cube_004_bookings_dimensions_households_selection_people_table
        )

    def test_cube_to_df_mixed_households_people_dimensions_households_table(
        self,
        households,
        people,
        cube_005_mixed_households_people_dimensions_households_table,
    ):
        cube = households.cube(
            [people[var] for var in ("Income", "Gender")] + [households["Region"]]
        )
        df = cube.to_df()

        assert_cube_dataframes_match(
            df, cube_005_mixed_households_people_dimensions_households_table
        )

    def test_cube_to_df_mixed_hhds_jnys_ppl_dimensions_people_selection_journeys_table(
        self,
        households,
        people,
        bookings,
        journeys,
        cube_006_mixed_hhds_jnys_ppl_dimensions_people_selection_journeys_table,
    ):
        cube = journeys.cube(
            [households["Region"], journeys["Pool"], people["Gender"]],
            selection=(
                (people["Surname"].contains(["int", "str", "bool"], match_case=False))
                | (bookings["Continent"] == ("AM", "AU"))
            ),
        )
        df = cube.to_df()

        assert_cube_dataframes_match(
            df, cube_006_mixed_hhds_jnys_ppl_dimensions_people_selection_journeys_table
        )
