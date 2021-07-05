from fractions import Fraction
import math

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
    """Tests for the Clause.sample() method.

    Covers every valid value [type] for each parameter,
    but not each possibility in combination with every other.
    Covers every error case for input validation.

    Tests are grouped by the type of limit clause they ultimately delegate to
    for the given set of inputs; in this case this is always a LimitClause.

    """
    def test_limit(self, men):
        men_10 = men.sample(10)
        men_skip_5_first_10pct = men.sample(frac=0.1, skip_first=5)
        men_regular_100 = men.sample(n=100, sample_type="Stratified")
        men_random_two_thirds = men.sample(frac=Fraction(2, 3), sample_type="Random")
        assert men_10.count() == 10
        assert men_skip_5_first_10pct.count() == 37857
        assert men_regular_100.count() == 100
        assert men_random_two_thirds.count() == 252377

    def test_sample_input_errors(self, men):
        with pytest.raises(ValueError) as exc_info:
            men_no_value = men.sample()
        assert exc_info.value.args[0] == "Must specify either n or frac"

        with pytest.raises(ValueError) as exc_info:
            men_n_and_frac = men.sample(10, 0.1)
        assert exc_info.value.args[0] == "Must specify either n or frac"

        with pytest.raises(ValueError) as exc_info:
            men_n_float = men.sample(2.5)
        assert exc_info.value.args[0] == "n must be an integer greater than 0"

        with pytest.raises(ValueError) as exc_info:
            men_n_range = men.sample((10, 20))
        assert exc_info.value.args[0] == "n must be an integer greater than 0"

        with pytest.raises(ValueError) as exc_info:
            men_n_small = men.sample(0)
        assert exc_info.value.args[0] == "n must be greater than 0"

        with pytest.raises(ValueError) as exc_info:
            men_non_real_frac = men.sample(frac=UnrealFrac())
        assert exc_info.value.args[0] == "frac must be either a float or a fraction"

        with pytest.raises(ValueError) as exc_info:
            men_frac_range = men.sample(frac=(0.1, 0.3))
        assert exc_info.value.args[0] == "frac must be either a float or a fraction"

        with pytest.raises(ValueError) as exc_info:
            men_big_frac = men.sample(frac=Fraction(3, 2))
        assert exc_info.value.args[0] == "frac must be between 0 and 1"

        with pytest.raises(ValueError) as exc_info:
            men_negative_frac = men.sample(frac=-0.2)
        assert exc_info.value.args[0] == "frac must be between 0 and 1"

        with pytest.raises(ValueError) as exc_info:
            men_1_frac = men.sample(frac=1)
        assert exc_info.value.args[0] == "frac must be between 0 and 1"

        with pytest.raises(ValueError) as exc_info:
            men_0_frac = men.sample(frac=Fraction(0, 4))
        assert exc_info.value.args[0] == "frac must be between 0 and 1"

        with pytest.raises(ValueError) as exc_info:
            men_bad_sample_type = men.sample(100, sample_type="Radon")
        assert exc_info.value.args[0] == "'Radon' is not a valid sample type"

        with pytest.raises(ValueError) as exc_info:
            men_skip_first_non_integer = men.sample(100, skip_first=500.0)
        assert exc_info.value.args[0] == "`skip_first` must be a non-negative integer"

        with pytest.raises(ValueError) as exc_info:
            men_skip_first_negative = men.sample(100, skip_first=-1000)
        assert exc_info.value.args[0] == "`skip_first` must be a non-negative integer"


class TestLimit:
    """Tests for the Clause.limit() method.

    Covers every valid value [type] for each parameter,
    but not each possibility in combination with every other.
    Covers every error case for input validation.

    Tests are grouped by the type of limit clause they ultimately delegate to
    for the given set of inputs (TopNClause, NPerVariableClause, NPerTableClause).

    """
    def test_top_n(self, men, people):
        men_top_100_by_income = men.limit(n=100, by=people["Income"])
        men_bottom_5_23rds = men.limit(
            frac=Fraction(5, 23), by=people["Income"], ascending=True
        )
        men_between_bottom_5pct_10pct_by_income = men.limit(
            frac=(0.05, 0.1), by=people["Income"], ascending=True
        )
        men_between_top_20_50_by_income = men.limit(n=(20, 50), by=people["Income"])
        assert men_top_100_by_income.count() == 100
        assert men_bottom_5_23rds.count() == 82297
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

    def test_limit_input_errors(self, men, people):
        with pytest.raises(ValueError) as exc_info:
            men_no_value = men.limit()
        assert exc_info.value.args[0] == "Must specify either n or frac"

        with pytest.raises(ValueError) as exc_info:
            men_n_and_frac = men.limit(10, 0.1)
        assert exc_info.value.args[0] == "Must specify either n or frac"

        with pytest.raises(ValueError) as exc_info:
            men_n_float = men.limit(2.5, by=people["Income"])
        assert exc_info.value.args[0] == "n must be an integer greater than 0"

        with pytest.raises(ValueError) as exc_info:
            men_n_small = men.limit(0, by=people["Income"])
        assert exc_info.value.args[0] == "n must be greater than 0"

        with pytest.raises(ValueError) as exc_info:
            men_n_bad_range_start_too_small = men.limit((-10, 10), by=people["Income"])
        assert exc_info.value.args[0] == (
            "Invalid range given for n - start of range must be greater than 0"
        )

        with pytest.raises(ValueError) as exc_info:
            men_n_bad_range_end_not_integer = men.limit(
                (1000, math.inf), by=people["Income"]
            )
        assert exc_info.value.args[0] == (
            "Invalid range given for n - end of range must be an integer greater than 0"
        )

        with pytest.raises(ValueError) as exc_info:
            men_n_bad_range_start_greater_than_end = men.limit(
                (2002, 1001), by=people["Income"]
            )
        assert exc_info.value.args[0] == (
            "Invalid range given for n - start of range must be less than the end."
        )

        with pytest.raises(ValueError) as exc_info:
            men_big_frac = men.limit(frac=Fraction(3, 2), by=people["Income"])
        assert exc_info.value.args[0] == "frac must be between 0 and 1"

        with pytest.raises(ValueError) as exc_info:
            men_negative_frac = men.limit(frac=-0.2, by=people["Income"])
        assert exc_info.value.args[0] == "frac must be between 0 and 1"

        with pytest.raises(ValueError) as exc_info:
            men_1_frac = men.limit(frac=1, by=people["Income"])
        assert exc_info.value.args[0] == "frac must be between 0 and 1"

        with pytest.raises(ValueError) as exc_info:
            men_0_frac = men.limit(frac=Fraction(0, 4), by=people["Income"])
        assert exc_info.value.args[0] == "frac must be between 0 and 1"

        with pytest.raises(ValueError) as exc_info:
            men_non_real_frac = men.limit(frac=UnrealFrac(), by=people["Income"])
        assert exc_info.value.args[0] == "frac must be either a float or a fraction"

        with pytest.raises(ValueError) as exc_info:
            men_frac_bad_range_start_too_big = men.limit(
                frac=(25.0, 50.5), by=people["Income"]
            )
        assert exc_info.value.args[0] == (
            "Invalid range given for frac - start of range must be less than 1"
        )

        with pytest.raises(ValueError) as exc_info:
            men_frac_bad_range_start_too_big = men.limit(
                frac=(0.25, 50.5), by=people["Income"]
            )
        assert exc_info.value.args[0] == (
            "Invalid range given for frac - end of range must be less than 1"
        )

        with pytest.raises(ValueError) as exc_info:
            men_frac_bad_range_start_too_big = men.limit(
                frac=(Fraction(1, 2), Fraction(1, 3)), by=people["Income"]
            )
        assert exc_info.value.args[0] == (
            "Invalid range given for frac - start of range must be less than the end."
        )

        with pytest.raises(ValueError) as exc_info:
            men_ascending_not_bool = men.limit(10, ascending="Top")
        assert exc_info.value.args[0] == "ascending must be True or False"

        with pytest.raises(ValueError) as exc_info:
            men_ascending_no_by = men.limit(10, ascending=True)
        assert exc_info.value.args[0] == "Must specify by with ascending"

        with pytest.raises(ValueError) as exc_info:
            men_by_not_variable = men.limit(10, by="Cost")
        assert exc_info.value.args[0] == "by must be an ordered variable"

        with pytest.raises(ValueError) as exc_info:
            men_frac_with_per = men.limit(frac=0.1, per=people["Income"])
        assert exc_info.value.args[0] == "Must specify n with per"

        with pytest.raises(ValueError) as exc_info:
            men_per_bad_type = men.limit(10, per="Booking")
        assert exc_info.value.args[0] == "`per` must be a table or a variable"


class TestLimitClause:
    """Tests for LimitClause.

    Tests cover every combination of:
        * sample_type (first, regular, random)
        * numeric input type (total, percent, fraction)
        * skip_first given or not

    Some general "mixed" tests at the end.

    """
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

    def test_limit_clause_and(self, men, holidays, people):
        men_first_100 = LimitClause(men, 100, session=holidays)
        assert men_first_100.count() == 100
        students_men_first_100 = men_first_100 & (people["Occupation"] == "4")
        assert students_men_first_100.count() == 9

    def test_limit_clause_or(self, holidays, bookings):
        sweden = bookings["Destination"] == "29"
        sweden_1_20th_regular = LimitClause(sweden, fraction=Fraction(1, 20), sample_type="Stratified", session=holidays)
        assert sweden_1_20th_regular.count() == 1261
        cost_gt_100 = bookings["Cost"] > 100
        cost_gt_100_first_0_38_pct = LimitClause(cost_gt_100, percent=0.38, session=holidays)
        assert cost_gt_100_first_0_38_pct.count() == 8002
        limit_or_clause = sweden_1_20th_regular | cost_gt_100_first_0_38_pct
        assert limit_or_clause.count() == 9258

    def test_limit_clause_of_limit_clause(self, holidays, households, people):
        south_west = households["Region"] == "04"
        assert south_west.count() == 77139
        south_west_1_456th = LimitClause(south_west, fraction=Fraction(1, 456), session=holidays)
        assert south_west_1_456th.count() == 170
        south_west_1_456th_78_9pct = LimitClause(south_west_1_456th, percent=78.9, session=holidays)
        assert south_west_1_456th_78_9pct.count() == 135


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
    and check it against its expected value (originally retrieved through FastStats).

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
    """Tests for TopNClause.

    Tests cover every combination of:
        * numeric input type (total, percent)
        * input kind (single value or range of values)
        * ascending (True or False, i.e. bottom or top)

    """
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
    """Tests for NPerVariableClause.

    Tests cover every combination of different table options
    for clause, per, by:
        * per: same table as clause or not
        * by: None, same table as clause, same table as per, different table from both

    """
    def test_per_same_table_any(self, holidays, bookings, flights):
        """clause: Bookings, per: Bookings, by: None"""
        flight_only_any_250_per_dest = NPerVariableClause(
            flights, 250, bookings["Destination"], session=holidays
        )
        assert flight_only_any_250_per_dest.count() == 3217

    def test_per_by_same_table(self, holidays, bookings, flights):
        """clause: Bookings, per: Bookings, by: Bookings"""
        flights_only_12_per_dest_by_profit = NPerVariableClause(
            flights,
            12,
            bookings["Destination"],
            by=bookings["Profit"],
            session=holidays,
        )
        assert flights_only_12_per_dest_by_profit.count() == 228

    def test_per_different_table_any(self, holidays, people, flights):
        """clause: Bookings, per: People, by: None"""
        flights_only_any_500_per_occupation = NPerVariableClause(
            flights, 500, people["Occupation"], session=holidays
        )
        assert flights_only_any_500_per_occupation.count() == 5500

    def test_per_different_table_by_same_as_clause(
        self, holidays, bookings, people, flights
    ):
        """clause: Bookings, per: People, by: Bookings"""
        flights_only_1000_highest_cost_per_income = NPerVariableClause(
            flights, 1000, people["Income"], by=bookings["Cost"], session=holidays
        )
        assert flights_only_1000_highest_cost_per_income.count() == 9409

    def test_per_different_table_by_same_as_per(self, holidays, people, flights):
        """clause: Bookings, per: People, by: People"""
        flights_only_2_per_surname_by_top_income = NPerVariableClause(
            flights, 2, people["Surname"], by=people["Income"], session=holidays
        )
        assert flights_only_2_per_surname_by_top_income.count() == 89233

    def test_per_different_table_by_different_table(
        self, holidays, households, people, flights
    ):
        """clause: Bookings, per: People, by: households"""
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
    """Tests for NPerTableClause.

    Tests cover every different valid option for per, by, ascending:
        * per: direct parent table, other ancestor table
        * by: None, child table
        * ascending: None (any), True (first), False (last)

    The tests cover all these options between them,
    but not in every possible combination.

    """
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
