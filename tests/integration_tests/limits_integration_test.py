from fractions import Fraction

import pytest

from apteco.query import LimitClause, NPerTableClause, NPerVariableClause, TopNClause


@pytest.fixture()
def men(people):
    return people["peGender"] == "M"


@pytest.fixture()
def france(bookings):
    return bookings["boDest"] == "06"


@pytest.fixture()
def usa(bookings):
    return bookings["boDest"] == "38"


@pytest.fixture()
def topn_dg_cols(bookings):
    return [bookings[var] for var in ("Booking URN", "Destination", "Profit", "Cost")]


@pytest.fixture()
def flights(bookings):
    return bookings["Product"] == "2"


@pytest.fixture()
def tablet(web_visits):
    return web_visits["Device Type"] == "2"


class UnrealFrac:
    def __ge__(self, other):
        return False

    def __le__(self, other):
        return False


class TestSample:
    def test_limit(self, men, people):
        men_10 = men.sample(10)
        men_skip_5_first_10pct = men.sample(frac=0.1, skip_first=5)
        men_regular_100 = men.sample(n=100, sample_type="Stratified")
        men_random_two_thirds = men.sample(frac=Fraction(2, 3), sample_type="Random")
        assert men_10.count() == 10
        assert men_skip_5_first_10pct.count() == 37857
        assert men_regular_100.count() == 100
        assert men_random_two_thirds.count() == 252377

        with pytest.raises(ValueError) as exc_info:
            men_no_value = men.sample()
        assert exc_info.value.args[0] == ("Must specify either n or frac")

        with pytest.raises(ValueError) as exc_info:
            men_n_and_frac = men.sample(10, 0.1)
        assert exc_info.value.args[0] == ("Must specify either n or frac")

        with pytest.raises(ValueError) as exc_info:
            men_n_float = men.sample(2.5)
        assert exc_info.value.args[0] == ("n must be an integer greater than 0")

        with pytest.raises(ValueError) as exc_info:
            men_n_small = men.sample(0)
        assert exc_info.value.args[0] == ("n must be an integer greater than 0")

        with pytest.raises(ValueError) as exc_info:
            men_big_frac = men.sample(frac=Fraction(3, 2))
        assert exc_info.value.args[0] == ("frac must be between 0 and 1")

        with pytest.raises(ValueError) as exc_info:
            men_negative_frac = men.sample(frac=-0.2)
        assert exc_info.value.args[0] == ("frac must be between 0 and 1")

        with pytest.raises(ValueError) as exc_info:
            men_1_frac = men.sample(frac=1)
        assert exc_info.value.args[0] == ("frac must be between 0 and 1")

        with pytest.raises(ValueError) as exc_info:
            men_0_frac = men.sample(frac=Fraction(0, 4))
        assert exc_info.value.args[0] == ("frac must be between 0 and 1")

        with pytest.raises(ValueError) as exc_info:
            men_people_frac = men.sample(frac=UnrealFrac())
        assert exc_info.value.args[0] == ("frac must be either a float or a fraction")


class TestLimit:
    def test_top_n(self, men, people):
        men_top_100_by_income = men.limit(n=100, by=people["Income"])
        men_between_bottom_5pct_10pct_by_income = men.limit(
            frac=(0.05, 0.1), by=people["Income"], ascending=True
        )
        men_between_top_20_50_by_income = men.limit(n=(20, 50), by=people["Income"])
        assert men_top_100_by_income.count() == 100
        assert men_between_bottom_5pct_10pct_by_income.count() == 18928
        assert men_between_top_20_50_by_income.count() == 31

    def test_n_per_variable(self, men, people):
        men_highest_5_income_per_surname = men.limit(
            n=5, by=people["Income"], per=people["Surname"]
        )
        men_10_per_surname = men.limit(n=10, per=people["Surname"])
        men_lowest_2_income_per_surname = men.limit(
            n=2, by=people["Income"], ascending=True, per=people["Surname"]
        )
        assert men_highest_5_income_per_surname.count() == 117264
        assert men_10_per_surname.count() == 148541
        assert men_lowest_2_income_per_surname.count() == 81527

    def test_n_per_table(self, france, people, bookings, households):
        france_bookings_1_per_person = france.limit(n=1, per=people)
        france_bookings_highest_2_costs_per_person = france.limit(
            n=2, by=bookings["Cost"], per=people
        )
        france_bookings_lowest_3_profits_per_household = france.limit(
            n=3, by=bookings["Profit"], ascending=True, per=households
        )
        assert france_bookings_1_per_person.count() == 522932
        assert france_bookings_highest_2_costs_per_person.count() == 524349
        assert france_bookings_lowest_3_profits_per_household.count() == 519165


class TestLimitClause:
    def test_first_n(self, holidays, france):
        france_first_100 = LimitClause(france, 100, session=holidays)
        assert france_first_100.count() == 100
        france_first_100_skip_10 = LimitClause(
            france, 100, skip_first=10, session=holidays
        )
        assert france_first_100_skip_10.count() == 100

        both = france_first_100 & france_first_100_skip_10
        assert both.count() == 100 - 10

    def test_first_percent(self, holidays, france):
        france_first_8_76pct = LimitClause(france, percent=8.76, session=holidays)
        assert france_first_8_76pct.count() == 45944
        france_first_8_76pct_skip_345 = LimitClause(
            france, percent=8.76, skip_first=345, session=holidays
        )
        assert france_first_8_76pct_skip_345.count() == 45944

        non_overlap = france_first_8_76pct & ~france_first_8_76pct_skip_345
        assert non_overlap.count() == 345  # the number we skipped

    def test_first_fraction(self, holidays, france):
        france_first_13_479ths = LimitClause(
            france, fraction=Fraction(13, 479), session=holidays
        )
        assert france_first_13_479ths.count() == 14235
        france_first_13_479ths_skip_6258 = LimitClause(
            france, fraction=Fraction(13, 479), skip_first=6258, session=holidays
        )
        assert france_first_13_479ths_skip_6258.count() == 14235

        non_overlap = france_first_13_479ths & ~france_first_13_479ths_skip_6258
        assert non_overlap.count() == 6258  # the number we skipped

    def test_regular_n(self, holidays, france):
        france_regular_23456 = LimitClause(
            france, 23456, sample_type="Stratified", session=holidays
        )
        assert france_regular_23456.count() == 23456

    def test_regular_n_skip(self, holidays, france):
        france_regular_23456_skip_78901 = LimitClause(
            france, 23456, sample_type="Stratified", skip_first=78901, session=holidays
        )
        assert france_regular_23456_skip_78901.count() == 23456

    def test_regular_percent(self, holidays, france):
        france_regular_24_68pct = LimitClause(
            france, percent=24.68, sample_type="Stratified", session=holidays
        )
        assert france_regular_24_68pct.count() == 129440

    def test_regular_percent_skip(self, holidays, france):
        france_regular_24_68pct_skip_13579 = LimitClause(
            france,
            percent=24.68,
            sample_type="Stratified",
            skip_first=13579,
            session=holidays,
        )
        assert france_regular_24_68pct_skip_13579.count() == 126089

    def test_regular_fraction(self, holidays, france):
        france_regular_86_75319ths = LimitClause(
            france,
            fraction=Fraction("86/75319"),
            sample_type="Stratified",
            session=holidays,
        )
        assert france_regular_86_75319ths.count() == 599

    def test_regular_fraction_skip(self, holidays, france):
        france_regular_86_75319ths_skip_2400 = LimitClause(
            france,
            fraction=Fraction("86/75319"),
            sample_type="Stratified",
            skip_first=2400,
            session=holidays,
        )
        assert france_regular_86_75319ths_skip_2400.count() == 597

    def test_random_n(self, holidays, france):
        france_random_45 = LimitClause(
            france, 45, sample_type="Random", session=holidays
        )
        assert france_random_45.count() == 45

    def test_random_n_skip(self, holidays, france):
        france_random_45_skip_45000 = LimitClause(
            france, 45, sample_type="Random", skip_first=45000, session=holidays
        )
        assert france_random_45_skip_45000.count() == 45

    def test_random_percent(self, holidays, france):
        france_random_30pct = LimitClause(
            france, percent=30, sample_type="Random", session=holidays
        )
        assert france_random_30pct.count() == 157343

    def test_random_percent_skip(self, holidays, france):
        france_random_30pct_skip_12345 = LimitClause(
            france, percent=30, sample_type="Random", skip_first=12345, session=holidays
        )
        assert france_random_30pct_skip_12345.count() == 157343

    def test_random_fraction(self, holidays, france):
        france_random_12_51sts = LimitClause(
            france, fraction=Fraction(12, 51), sample_type="Random", session=holidays
        )
        assert france_random_12_51sts.count() == 123406

    def test_random_fraction_skip(self, holidays, france):
        france_random_12_51sts_skip_678 = LimitClause(
            france,
            fraction=Fraction(12, 51),
            sample_type="Random",
            skip_first=678,
            session=holidays,
        )
        assert france_random_12_51sts_skip_678.count() == 123406


def verify_topn_values(
    selection, sel_count, dg_cols, dg_max_rows, by, sample_row, sample_col, sample_value
):
    """Helper function to verify TopN selection values.

    Verify TopN selection is correct by:
        - checking the number of rows returned in a maxed-out data grid
        - checking that the values based on the subclause being limited are as expected
        - picking out specific value and checking

    Because a TopN selection specifies the number of records to return
    (either explicitly as a fixed total
    or implicitly as a percentage of the whole selection),
    just checking the count risks being just tautological.
    A way to improve on this would be to verify the URN set of the records selected,
    but this would be quite expensive and lead to lots of large URN set data files.
    A compromise is to pick an arbitrary data point from the selection
    and check it against its expected value (initially retrieved through FastStats).

    We can still check the count and also check that
    the variable used in the subselection has a uniform value
    (in this case Destination of United States).

    We always sort all the data descending, even for 'bottom' limits,
    as the 'bottom' data tends to be a lot of 0s,
    which makes it harder to pick out a unique data point to use for verifying.

    Args:
        selection (TopNClause): TopN selection to verify
        sel_count (int): expected count of selection
        dg_cols (List[Variable]): list of variables to use as columns in data grid
            (this is the same for every test, but it's a fixture and so needs to be
            passed into the test function to be used)
        dg_max_rows (int): number of rows to request from data grid
            (must be greater than count to ensure we fetch all data)
        by (Variable): variable to order records by to select top/bottom
        sample_row (int): row index to sample data from
        sample_col (str): column name to sample data from
        sample_value (float or str): expected value of sampled data point

    Raises:
        AssertionError: if any of the checks fail

    """
    sort_order = (
        ["Profit", "Cost", "Booking URN"]
        if by == "Profit"
        else ["Cost", "Profit", "Booking URN"]
    )
    df = (
        selection.datagrid(dg_cols, max_rows=dg_max_rows)
        .to_df()
        .sort_values(sort_order, ascending=[False, False, False])
        .reset_index(drop=True)
    )
    assert len(df) == sel_count
    assert (df["Destination"] == "United States").all()
    assert df.loc[sample_row, sample_col] == sample_value


class TestTopNClause:
    def test_top_total(self, holidays, bookings, usa, topn_dg_cols):
        top_637_by_cost = TopNClause(usa, 637, by=bookings["Cost"], session=holidays)
        assert top_637_by_cost.count() == 637
        verify_topn_values(
            top_637_by_cost, 637, topn_dg_cols, 750, "Cost", 9, "Cost", 28400.18
        )

    def test_top_percentage(self, holidays, bookings, usa, topn_dg_cols):
        top_1_65_pct_by_cost = TopNClause(
            usa, percent=1.65, by=bookings["Cost"], session=holidays
        )
        assert top_1_65_pct_by_cost.count() == 9270
        verify_topn_values(
            top_1_65_pct_by_cost,
            9270,
            topn_dg_cols,
            10000,
            "Cost",
            17,
            "Profit",
            4309.71,
        )

    def test_bottom_total(self, holidays, bookings, usa, topn_dg_cols):
        bottom_4278_by_cost = TopNClause(
            usa, 4278, by=bookings["Cost"], ascending=True, session=holidays
        )
        assert bottom_4278_by_cost.count() == 4278
        verify_topn_values(
            bottom_4278_by_cost,
            4278,
            topn_dg_cols,
            4300,
            "Cost",
            13,
            "Booking URN",
            "10583471",
        )

    def test_bottom_percentage(self, holidays, bookings, usa, topn_dg_cols):
        bottom_0_827_pct_by_cost = TopNClause(
            usa, percent=0.827, by=bookings["Cost"], ascending=True, session=holidays
        )
        assert bottom_0_827_pct_by_cost.count() == 4646
        verify_topn_values(
            bottom_0_827_pct_by_cost,
            4646,
            topn_dg_cols,
            50000,
            "Cost",
            22,
            "Booking URN",
            "11701935",
        )

    def test_between_top_total(self, holidays, bookings, usa, topn_dg_cols):
        between_top_50_100_by_profit = TopNClause(
            usa, (50, 100), by=bookings["Profit"], session=holidays
        )
        assert between_top_50_100_by_profit.count() == 51
        verify_topn_values(
            between_top_50_100_by_profit,
            51,
            topn_dg_cols,
            1000,
            "Profit",
            33,
            "Profit",
            2733.14,
        )

    def test_between_bottom_total(self, holidays, bookings, usa, topn_dg_cols):
        between_bottom_1_3600_by_profit = TopNClause(
            usa, (1, 3600), by=bookings["Profit"], ascending=True, session=holidays
        )
        assert between_bottom_1_3600_by_profit.count() == 3600
        verify_topn_values(
            between_bottom_1_3600_by_profit,
            3600,
            topn_dg_cols,
            4000,
            "Profit",
            16,
            "Cost",
            87.11,
        )

    def test_between_top_percentage(self, holidays, bookings, usa, topn_dg_cols):
        between_top_6_28_10_35_pct_by_profit = TopNClause(
            usa, percent=(6.28, 10.35), by=bookings["Profit"], session=holidays
        )
        assert between_top_6_28_10_35_pct_by_profit.count() == 22867
        verify_topn_values(
            between_top_6_28_10_35_pct_by_profit,
            22867,
            topn_dg_cols,
            25000,
            "Profit",
            0,
            "Booking URN",
            "10641231",
        )

    def test_between_bottom_percentage(self, holidays, bookings, usa, topn_dg_cols):
        between_bottom_24_63_25_86_pct_by_profit = TopNClause(
            usa,
            percent=(24.63, 25.86),
            by=bookings["Profit"],
            ascending=True,
            session=holidays,
        )
        assert between_bottom_24_63_25_86_pct_by_profit.count() == 6911
        verify_topn_values(
            between_bottom_24_63_25_86_pct_by_profit,
            6911,
            topn_dg_cols,
            7000,
            "Profit",
            8,
            "Cost",
            300.51,
        )


class TestNPerVariableClause:
    def test_per_same_table_any(self, holidays, bookings, flights):
        flight_only_any_250_per_dest = NPerVariableClause(
            flights, 250, bookings["Destination"], session=holidays
        )
        assert flight_only_any_250_per_dest.count() == 3217

    def test_per_by_same_table(self, holidays, bookings, flights):
        flights_only_12_per_dest_by_profit = NPerVariableClause(
            flights,
            12,
            bookings["Destination"],
            by=bookings["Profit"],
            session=holidays,
        )
        assert flights_only_12_per_dest_by_profit.count() == 228

    def test_per_different_table_any(self, holidays, bookings, people, flights):
        flights_only_any_500_per_occupation = NPerVariableClause(
            flights, 500, people["Occupation"], session=holidays
        )
        assert flights_only_any_500_per_occupation.count() == 5500

    def test_per_different_table_by_same_as_clause(
        self, holidays, bookings, people, flights
    ):
        flights_only_1000_highest_cost_per_income = NPerVariableClause(
            flights, 1000, people["Income"], by=bookings["Cost"], session=holidays
        )
        assert flights_only_1000_highest_cost_per_income.count() == 9409

    def test_per_different_table_by_same_as_per(
        self, holidays, bookings, people, flights
    ):
        flights_only_2_per_surname_by_top_income = NPerVariableClause(
            flights, 2, people["Surname"], by=people["Income"], session=holidays
        )
        assert flights_only_2_per_surname_by_top_income.count() == 89233

    def test_per_different_table_by_different_table(
        self, holidays, households, people, bookings, flights
    ):
        flights_only_75_per_region_by_oldest_person = NPerVariableClause(
            flights,
            75,
            households["Region"],
            by=people["DOB"],
            ascending=True,
            session=holidays,
        )
        assert flights_only_75_per_region_by_oldest_person.count() == 1125


class TestNPerTableClause:
    def test_per_parent_any(self, holidays, people, tablet):
        tablet_any_4_per_person = NPerTableClause(tablet, 4, people, session=holidays)
        assert tablet_any_4_per_person.count() == 32533

    def test_per_parent_first(self, holidays, people, web_visits, tablet):
        tablet_first_2_per_person_by_wv_time = NPerTableClause(
            tablet, 2, people, by=web_visits["Web Visit Time"], session=holidays
        )
        assert tablet_first_2_per_person_by_wv_time.count() == 31811

    def test_per_ancestor_last(self, holidays, households, web_visits, tablet):
        tablet_last_3_per_household_by_duration = NPerTableClause(
            tablet, 3, households, by=web_visits["Duration"], session=holidays
        )
        assert tablet_last_3_per_household_by_duration.count() == 32084
