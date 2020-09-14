import pytest
from apteco.query import LimitClause


@pytest.fixture()
def men(people):
    return people["peGender"] == "M"


@pytest.fixture()
def france(bookings):
    return bookings["boDest"] == "France"


@pytest.mark.xfail(reason="Limits under development")
def test_limit(men):
    men_skip_5_first_10pct = men.limit(
        limit_type="first", value_type="percent", value=10, skip_first=5
    )
    men_regular_100 = men.limit(limit_type="regular", value_type="total", value=100)
    men_random_two_thirds = men.limit(
        limit_type="random", value_type="fraction", value=(2, 3)
    )
    assert men_skip_5_first_10pct.count() == 37857
    assert men_regular_100.count() == 100
    assert men_random_two_thirds.count() == 252377


@pytest.mark.xfail(reason="Top N under development")
def test_top_n(men):
    men_top_100_by_income = men.top_n(
        variable="income", value_type="total", direction="top", between=False, value=100
    )
    men_between_bottom_5pct_10pct_by_income = men.top_n(
        variable="income",
        value_type="percent",
        direction="bottom",
        between=True,
        value=(5, 10),
    )
    men_between_top_20_50_by_income = men.top_n(
        variable="income",
        value_type="total",
        direction="top",
        between=True,
        value=(20, 50),
    )
    assert men_top_100_by_income.count() == 100
    assert men_between_bottom_5pct_10pct_by_income.count() == 18928
    assert men_between_top_20_50_by_income.count() == 31


@pytest.mark.xfail(reason="N per variable under development")
def test_n_per_variable(men):
    men_highest_5_income_per_surname = men.n_per_variable(
        value=5, grouping_variable="surname", sequence_variable="income", top=True
    )
    men_10_per_surname = men.n_per_variable(value=10, grouping_variable="surname")
    assert men_highest_5_income_per_surname.count() == 117264
    assert men_10_per_surname.count() == 148541


@pytest.mark.xfail(reason="N per table under development")
def test_n_per_table(france):
    france_bookings_1_per_person = france.n_per_table(value=1, grouping_table="people")
    france_bookings_highest_2_costs_per_person = france.n_per_table(
        value=2, grouping_table="people", top=True, sequence_variable="cost"
    )
    france_bookings_lowest_3_profits_per_household = france.n_per.table(
        value=3, grouping_table="households", top=False, sequence_variable="profit"
    )
    assert france_bookings_1_per_person.count() == 796794
    assert france_bookings_highest_2_costs_per_person.count() == 926322
    assert france_bookings_lowest_3_profits_per_household.count() == 923771


def test_limit_clause(men, holidays, people):
    men_first_100 = LimitClause(100, men, session=holidays)
    assert men_first_100.count() == 100
    students_men_first_100 = men_first_100 & (people["Occupation"] == "4")
    assert students_men_first_100.count() == 9
