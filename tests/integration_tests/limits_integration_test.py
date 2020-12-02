from fractions import Fraction

import pytest

from apteco.query import LimitClause, TopNClause


@pytest.fixture()
def men(people):
    return people["peGender"] == "M"


@pytest.fixture()
def france(bookings):
    return bookings["boDest"] == "06"


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
    @pytest.mark.xfail(reason="Top N under development")
    def test_top_n(self, men, people):
        men_top_100_by_income = men.limit(n=100, by=people["Income"])
        men_between_bottom_5pct_10pct_by_income = men.limit(
            frac=(0.05, 0.1), by=people["Income"], ascending=True
        )
        men_between_top_20_50_by_income = men.limit(n=(20, 50), by=people["Income"])
        assert men_top_100_by_income.count() == 100
        assert men_between_bottom_5pct_10pct_by_income.count() == 18928
        assert men_between_top_20_50_by_income.count() == 31

    @pytest.mark.xfail(reason="N per variable under development")
    def test_n_per_variable(self, men, people):
        men_highest_5_income_per_surname = men.limit(
            value=5, by=people["Income"], per=people["Surname"]
        )
        men_10_per_surname = men.limit(n=10, per=people["Surname"])
        men_lowest_2_income_per_surname = men.limit(
            n=2, by=people["Income"], ascending=True, per=people["Surname"]
        )
        assert men_highest_5_income_per_surname.count() == 117264
        assert men_10_per_surname.count() == 148541
        assert men_lowest_2_income_per_surname.count() == 81527

    @pytest.mark.xfail(reason="N per table under development")
    def test_n_per_table(self, france, people, bookings, households):
        france_bookings_1_per_person = france.limit(n=1, per=people)
        france_bookings_highest_2_costs_per_person = france.limit(
            n=2, by=bookings["Cost"], per=people
        )
        france_bookings_lowest_3_profits_per_household = france.limit(
            n=3, by=bookings["Profit"], ascending=True, per=households
        )
        assert france_bookings_1_per_person.count() == 796794
        assert france_bookings_highest_2_costs_per_person.count() == 926322
        assert france_bookings_lowest_3_profits_per_household.count() == 923771


class TestLimitClause:
    def test_first_n(self, holidays, france):
        france_first_100 = LimitClause(france, 100, session=holidays)
        assert france_first_100.count() == 100
    def test_first_n_skip(self, holidays, france):
        france_first_100_skip_10 = LimitClause(france, 100, skip_first=10, session=holidays)
        assert france_first_100_skip_10.count() == 100

    def test_first_percent(self, holidays, france):
        france_first_8_76pct = LimitClause(france, percent=8.76, session=holidays)
        assert france_first_8_76pct.count() == 45944
    def test_first_percent_skip(self, holidays, france):
        france_first_8_76pct_skip_345 = LimitClause(france, percent=8.76, skip_first=345, session=holidays)
        assert france_first_8_76pct_skip_345.count() == 45944

    def test_first_fraction(self, holidays, france):
        france_first_13_479ths = LimitClause(france, fraction=Fraction(13, 479), session=holidays)
        assert france_first_13_479ths.count() == 14235
    def test_first_fraction_skip(self, holidays, france):
        france_first_13_479ths_skip_6258 = LimitClause(france, fraction=Fraction(13, 479), skip_first=6258, session=holidays)
        assert france_first_13_479ths_skip_6258.count() == 14235

    def test_regular_n(self, holidays, france):
        france_regular_23456 = LimitClause(france, 23456, sample_type="Stratified", session=holidays)
        assert france_regular_23456.count() == 23456
    def test_regular_n_skip(self, holidays, france):
        france_regular_23456_skip_78901 = LimitClause(france, 23456, sample_type="Stratified", skip_first=78901, session=holidays)
        assert france_regular_23456_skip_78901.count() == 23456

    def test_regular_percent(self, holidays, france):
        france_regular_24_68pct = LimitClause(france, percent=24.68, sample_type="Stratified", session=holidays)
        assert france_regular_24_68pct.count() == 129440
    def test_regular_percent_skip(self, holidays, france):
        france_regular_24_68pct_skip_13579 = LimitClause(france, percent=24.68, sample_type="Stratified", skip_first=13579, session=holidays)
        assert france_regular_24_68pct_skip_13579.count() == 126089

    def test_regular_fraction(self, holidays, france):
        france_regular_86_75319ths = LimitClause(france, fraction=Fraction("86/75319"), sample_type="Stratified", session=holidays)
        assert france_regular_86_75319ths.count() == 599
    def test_regular_fraction_skip(self, holidays, france):
        france_regular_86_75319ths_skip_2400 = LimitClause(france, fraction=Fraction("86/75319"), sample_type="Stratified", skip_first=2400, session=holidays)
        assert france_regular_86_75319ths_skip_2400.count() == 597

    def test_random_n(self, holidays, france):
        france_random_45 = LimitClause(france, 45, sample_type="Random", session=holidays)
        assert france_random_45.count() == 45
    def test_random_n_skip(self, holidays, france):
        france_random_45_skip_45000 = LimitClause(france, 45, sample_type="Random", skip_first=45000, session=holidays)
        assert france_random_45_skip_45000.count() == 45

    def test_random_percent(self, holidays, france):
        france_random_30pct = LimitClause(france, percent=30, sample_type="Random", session=holidays)
        assert france_random_30pct.count() == 157343
    def test_random_percent_skip(self, holidays, france):
        france_random_30pct_skip_12345 = LimitClause(france, percent=30, sample_type="Random", skip_first=12345, session=holidays)
        assert france_random_30pct_skip_12345.count() == 157343

    def test_random_fraction(self, holidays, france):
        france_random_12_51sts = LimitClause(france, fraction=Fraction(12, 51), sample_type="Random", session=holidays)
        assert france_random_12_51sts.count() == 123406
    def test_random_fraction_skip(self, holidays, france):
        france_random_12_51sts_skip_678 = LimitClause(france, fraction=Fraction(12, 51), sample_type="Random", skip_first=678, session=holidays)
        assert france_random_12_51sts_skip_678.count() == 123406


class TestTopNClause:
    def test_between_top_percentage(self, holidays, bookings, france):
        between_top_6_28_10_35_pct_by_profit = TopNClause(france, percent=(6.28, 10.35), by=bookings["Profit"], session=holidays)
        assert between_top_6_28_10_35_pct_by_profit.count() == 21346
        df = between_top_6_28_10_35_pct_by_profit.datagrid(
            [bookings[var] for var in ("Booking URN", "Destination", "Profit", "Cost")],
            max_rows=21347,
        ).to_df().sort_values(["Profit", "Cost"], ascending=[False, True])
        assert len(df) == 21346
        assert df.loc[0, "Booking URN"] == "10001265"
