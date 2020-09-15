import pytest
from apteco.query import LimitClause
from fractions import Fraction


@pytest.fixture()
def men(people):
    return people["peGender"] == "M"


@pytest.fixture()
def france(bookings):
    return bookings["boDest"] == "France"


@pytest.mark.xfail(reason="Limits under development")
def test_limit(men):
    men_10 = men.sample(n=100)
    men_skip_5_first_10pct = men.sample(frac=0.1, skip_first=5)
    men_regular_100 = men.sample(n=100, sample_type="regular")
    men_random_two_thirds = men.sample(frac=Fraction(2, 3), sample_type="random")
    assert men_10.count() == 10
    assert men_skip_5_first_10pct.count() == 37857
    assert men_regular_100.count() == 100
    assert men_random_two_thirds.count() == 252377


@pytest.mark.xfail(reason="Top N under development")
def test_top_n(men, people):
    men_top_100_by_income = men.limit(n=100, by=people["Income"])
    men_between_bottom_5pct_10pct_by_income = men.limit(
        frac=(0.05, 0.1),
        by=people["Income"],
        ascending=True,
    )
    men_between_top_20_50_by_income = men.limit(n=(20, 50), by=people["Income"])
    assert men_top_100_by_income.count() == 100
    assert men_between_bottom_5pct_10pct_by_income.count() == 18928
    assert men_between_top_20_50_by_income.count() == 31


@pytest.mark.xfail(reason="N per variable under development")
def test_n_per_variable(men, people):
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
def test_n_per_table(france, people, bookings, households):
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


def test_limit_clause(men, holidays, people):
    men_first_100 = LimitClause(100, men, session=holidays)
    assert men_first_100.count() == 100
    students_men_first_100 = men_first_100 & (people["Occupation"] == "4")
    assert students_men_first_100.count() == 9
