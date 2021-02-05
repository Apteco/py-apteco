from datetime import date, datetime
from decimal import Decimal
from fractions import Fraction
from unittest.mock import Mock

import apteco_api as aa
import pytest

from apteco.query import (
    ArrayClause,
    BooleanClause,
    CombinedCategoriesClause,
    DateListClause,
    DateRangeClause,
    DateTimeRangeClause,
    FlagArrayClause,
    NumericClause,
    SelectorClause,
    SubSelectionClause,
    TableClause,
    TextClause,
    normalize_date_input,
    normalize_date_value,
    normalize_datetime_input,
    normalize_datetime_value,
    normalize_number_input,
    normalize_number_value,
    normalize_string_input,
    normalize_string_value,
)


def test_normalize_string_value():
    assert normalize_string_value("MyVarCode", "Error shouldn't be raised") == "MyVarCode"
    assert normalize_string_value("", "Error shouldn't be raised") == ""

    with pytest.raises(ValueError) as exc_info:
        normalize_string_value(True, "Can't have Booleans here.")
    assert exc_info.value.args[0] == "Can't have Booleans here."

    with pytest.raises(ValueError) as exc_info:
        normalize_string_value(3.45, "Can't use floats here.")
    assert exc_info.value.args[0] == "Can't use floats here."

    with pytest.raises(ValueError) as exc_info:
        normalize_string_value(["a", "B", "c"], "Can't have lists here.")
    assert exc_info.value.args[0] == "Can't have lists here."

    with pytest.raises(ValueError) as exc_info:
        normalize_string_value(None, "Can't be None.")
    assert exc_info.value.args[0] == "Can't be None."


def test_normalize_string_input():
    assert normalize_string_input("0", "Error shouldn't be raised") == ["0"]
    assert normalize_string_input("MyVarCode", "Error shouldn't be raised") == ["MyVarCode"]
    assert normalize_string_input(["VarCodeListOfOne"], "Error shouldn't be raised") == ["VarCodeListOfOne"]
    assert normalize_string_input(["VarCode1", "VarCode2"], "Error shouldn't be raised") == ["VarCode1", "VarCode2"]
    assert sorted(normalize_string_input(set(list("TESTED")), "Error shouldn't be raised")) == ["D", "E", "S", "T"]
    assert normalize_string_input((f"VarCodeFromGenerator{i}" for i in range(3)), "Error shouldn't be raised") == ["VarCodeFromGenerator0", "VarCodeFromGenerator1", "VarCodeFromGenerator2"]

    with pytest.raises(ValueError) as exc_info:
        normalize_string_input(True, "Input can't be a bool.")
    assert exc_info.value.args[0] == "Input can't be a bool."

    with pytest.raises(ValueError) as exc_info:
        normalize_string_input(1, "Can't input an int here.")
    assert exc_info.value.args[0] == "Can't input an int here."

    with pytest.raises(ValueError) as exc_info:
        normalize_string_input(1098.765, "Input can't be a float.")
    assert exc_info.value.args[0] == "Input can't be a float."

    with pytest.raises(ValueError) as exc_info:
        normalize_string_input(None, "Input can't be None.")
    assert exc_info.value.args[0] == "Input can't be None."

    with pytest.raises(ValueError) as exc_info:
        normalize_string_input([1, 2, 3], "Lists must contain only strings if given as input here")
    assert exc_info.value.args[0] == "Lists must contain only strings if given as input here"


def test_normalize_number_value():
    assert normalize_number_value(0, "Shouldn't see this...") == "0"
    assert normalize_number_value(999, "Shouldn't see this...") == "999"
    assert normalize_number_value(10.62, "Shouldn't see this...") == "10.62"
    assert normalize_number_value(1234.567890123, "Shouldn't see this...") == "1234.5679"
    assert normalize_number_value(Decimal("67.123456"), "Shouldn't see this...") == "67.1235"
    assert normalize_number_value(Decimal("67.12396"), "Shouldn't see this...") == "67.1240"
    assert normalize_number_value(Fraction(6543, 89), "Shouldn't see this...") == "73.5169"

    with pytest.raises(ValueError) as exc_info:
        normalize_number_value(True, "Can't have Booleans here.")
    assert exc_info.value.args[0] == "Can't have Booleans here."

    with pytest.raises(ValueError) as exc_info:
        normalize_number_value("3.45", "Can't use strings here.")
    assert exc_info.value.args[0] == "Can't use strings here."

    with pytest.raises(ValueError) as exc_info:
        normalize_number_value([16, 18, 21], "Can't have lists here.")
    assert exc_info.value.args[0] == "Can't have lists here."

    with pytest.raises(ValueError) as exc_info:
        normalize_number_value(None, "Can't have None here.")
    assert exc_info.value.args[0] == "Can't have None here."


def test_normalize_number_input():
    assert normalize_number_input(123, "Shouldn't see this error") == ["123"]
    assert normalize_number_input(10.62, "Shouldn't see this error") == ["10.62"]
    assert normalize_number_input(1234.567890123, "Shouldn't see this error") == ["1234.5679"]
    assert normalize_number_input(Decimal("67.123456"), "Shouldn't see this error") == ["67.1235"]
    assert normalize_number_input(Fraction(6543, 89), "Shouldn't see this error") == ["73.5169"]
    assert normalize_number_input([16, 18, 21], "Shouldn't see this error") == ["16", "18", "21"]
    assert normalize_number_input((22, 6546.3216487, Fraction(65421, 984), Decimal("729421.65487")), "Shouldn't see this error") == ["22", "6546.3216", "66.4848", "729421.6549"]

    with pytest.raises(ValueError) as exc_info:
        normalize_number_input(True, "A bool doesn't count as a number.")
    assert exc_info.value.args[0] == "A bool doesn't count as a number."

    with pytest.raises(ValueError) as exc_info:
        normalize_number_input("3.45", "A numeric string doesn't count as a number.")
    assert exc_info.value.args[0] == "A numeric string doesn't count as a number."


def test_normalize_date_value():
    assert normalize_date_value(date(2012, 3, 4), "Shouldn't see this...") == "2012-03-04"
    assert normalize_date_value(date(2012, 3, 4), "Shouldn't see this...", basic=True) == "20120304"
    assert normalize_date_value(datetime(2021, 9, 8, 7, 6, 54), "Shouldn't see this...") == "2021-09-08"
    assert normalize_date_value(datetime(2021, 9, 8, 7, 6, 54), "Shouldn't see this...", basic=True) == "20210908"

    with pytest.raises(ValueError) as exc_info:
        normalize_date_value(True, "Can't have Booleans here.")
    assert exc_info.value.args[0] == "Can't have Booleans here."

    with pytest.raises(ValueError) as exc_info:
        normalize_date_value(49072, "Can't use numbers here.")
    assert exc_info.value.args[0] == "Can't use numbers here."

    with pytest.raises(ValueError) as exc_info:
        normalize_date_value("3.45", "Can't use strings here.")
    assert exc_info.value.args[0] == "Can't use strings here."

    with pytest.raises(ValueError) as exc_info:
        normalize_date_value([date(2012, 12, 20), date(2012, 12, 21), date(2012, 12, 22)], "Can't have lists here.")
    assert exc_info.value.args[0] == "Can't have lists here."

    with pytest.raises(ValueError) as exc_info:
        normalize_date_value(None, "Can't have None here.")
    assert exc_info.value.args[0] == "Can't have None here."


def test_normalize_date_input():
    assert normalize_date_input(date(1952, 2, 6), "Shouldn't see this error") == ["1952-02-06"]
    assert normalize_date_input(date(1952, 2, 6), "Shouldn't see this error", basic=True) == ["19520206"]
    assert normalize_date_input(datetime(1952, 2, 6, 7, 30), "Shouldn't see this error") == ["1952-02-06"]
    assert normalize_date_input(datetime(1952, 2, 6, 7, 30), "Shouldn't see this error", basic=True) == ["19520206"]
    assert normalize_date_input([
        date(2000, 4, 24), date(2000, 5, 1), date(2000, 5, 29), date(2000, 8, 28)
    ], "Shouldn't see this error") == [
        "2000-04-24", "2000-05-01", "2000-05-29", "2000-08-28"
    ]
    assert normalize_date_input([
        date(2000, 4, 24), date(2000, 5, 1), date(2000, 5, 29), date(2000, 8, 28)
    ], "Shouldn't see this error", basic=True) == [
        "20000424", "20000501", "20000529", "20000828"
    ]
    assert normalize_date_input([
        datetime(1926, 4, 21, 4, 20),
        datetime(1948, 11, 14, 9, 14),
        datetime(1982, 6, 21, 9, 3),
    ], "Shouldn't see this error") == ["1926-04-21", "1948-11-14", "1982-06-21"]
    assert normalize_date_input([
        datetime(1926, 4, 21, 4, 20),
        datetime(1948, 11, 14, 9, 14),
        datetime(1982, 6, 21, 9, 3),
    ], "Shouldn't see this error", basic=True) == ["19260421", "19481114", "19820621"]

    with pytest.raises(ValueError) as exc_info:
        normalize_date_input(True, "A bool isn't a date.")
    assert exc_info.value.args[0] == "A bool isn't a date."

    with pytest.raises(ValueError) as exc_info:
        normalize_date_input(49072, "A number isn't a date.")
    assert exc_info.value.args[0] == "A number isn't a date."

    with pytest.raises(ValueError) as exc_info:
        normalize_date_input("2008-12-03", "A date-y string doesn't count as a date.")
    assert exc_info.value.args[0] == "A date-y string doesn't count as a date."

    with pytest.raises(ValueError) as exc_info:
        normalize_date_input([20081203, 20001016], "Can't sneak numbers through inside a list")
    assert exc_info.value.args[0] == "Can't sneak numbers through inside a list"


def test_normalize_datetime_value():
    assert normalize_datetime_value(datetime(2021, 9, 8, 12, 34, 56), "Shouldn't see this...") == "2021-09-08T12:34:56"
    assert normalize_datetime_value(datetime(1912, 6, 23, 7, 6, 54), "Shouldn't see this...") == "1912-06-23T07:06:54"

    with pytest.raises(ValueError) as exc_info:
        normalize_datetime_value(True, "Can't have Booleans here.")
    assert exc_info.value.args[0] == "Can't have Booleans here."

    with pytest.raises(ValueError) as exc_info:
        normalize_datetime_value(49072, "Can't use numbers here.")
    assert exc_info.value.args[0] == "Can't use numbers here."

    with pytest.raises(ValueError) as exc_info:
        normalize_datetime_value("08/09/2021 7:06:54", "Can't use strings here.")
    assert exc_info.value.args[0] == "Can't use strings here."

    with pytest.raises(ValueError) as exc_info:
        normalize_datetime_value(date(2012, 3, 4), "Can't have date-only objects.")
    assert exc_info.value.args[0] == "Can't have date-only objects."

    with pytest.raises(ValueError) as exc_info:
        normalize_datetime_value(
            [
                datetime(2012, 12, 20, 1, 2, 3),
                datetime(2012, 12, 21, 4, 5, 6),
                datetime(2012, 12, 22, 7, 8, 9),
            ],
            "Can't have lists here.",
        )
    assert exc_info.value.args[0] == "Can't have lists here."

    with pytest.raises(ValueError) as exc_info:
        normalize_datetime_value(None, "Can't have None here.")
    assert exc_info.value.args[0] == "Can't have None here."


def test_normalize_datetime_input():
    assert normalize_datetime_input(
        datetime(1952, 2, 6, 7, 30), "Shouldn't see this error"
    ) == ["1952-02-06T07:30:00"]
    assert normalize_datetime_input(
        datetime(2026, 4, 21, 4, 20, 59), "Shouldn't see this error"
    ) == ["2026-04-21T04:20:59"]
    assert normalize_datetime_input(
        [
            datetime(2000, 4, 24, 1, 23, 45),
            datetime(2000, 5, 1, 6, 7),
            datetime(2000, 5, 29, 8),
            datetime(2000, 8, 28),
        ],
        "Shouldn't see this error",
    ) == [
        "2000-04-24T01:23:45",
        "2000-05-01T06:07:00",
        "2000-05-29T08:00:00",
        "2000-08-28T00:00:00",
    ]
    assert normalize_datetime_input(
        (
            datetime(2020 + i, i, i + 23, i ** 2 % (i + 5), i ** 2, i * 8)
            for i in range(4, 8)
        ),
        "Shouldn't see this error",
    ) == [
        "2024-04-27T07:16:32",
        "2025-05-28T05:25:40",
        "2026-06-29T03:36:48",
        "2027-07-30T01:49:56",
    ]

    with pytest.raises(ValueError) as exc_info:
        normalize_datetime_input(True, "A bool isn't a datetime.")
    assert exc_info.value.args[0] == "A bool isn't a datetime."

    with pytest.raises(ValueError) as exc_info:
        normalize_datetime_input(946_684_800, "A number isn't a datetime.")
    assert exc_info.value.args[0] == "A number isn't a datetime."

    with pytest.raises(ValueError) as exc_info:
        normalize_datetime_input(
            "2008-12-03T03:33:30", "A datetime-y string doesn't count as a datetime."
        )
    assert exc_info.value.args[0] == "A datetime-y string doesn't count as a datetime."

    with pytest.raises(ValueError) as exc_info:
        normalize_datetime_input(
            [20_001_016_220_220, 20_081_203_033_330],
            "Can't sneak numbers through inside a list",
        )
    assert exc_info.value.args[0] == "Can't sneak numbers through inside a list"


@pytest.fixture()
def fake_bookings_table():
    fake = Mock()
    fake.configure_mock(name="Bookings")
    return fake


@pytest.fixture()
def fake_people_table():
    fake = Mock()
    fake.configure_mock(name="People")
    return fake


@pytest.fixture()
def fake_households_table():
    fake = Mock()
    fake.configure_mock(name="Households")
    return fake


class TestSelectorClause:
    def test_selector_clause_init(self, fake_bookings_table):
        fake_destination_var = Mock()
        fake_destination_var.configure_mock(name="boDest", table=fake_bookings_table)
        bookings_fr_de_us = SelectorClause(
            fake_destination_var,
            ["06", "07", "38"],
            label="Bookings to France, Germany or USA",
        )
        assert bookings_fr_de_us.table_name == "Bookings"
        assert bookings_fr_de_us.variable_name == "boDest"
        assert bookings_fr_de_us.values == ["06", "07", "38"]
        assert bookings_fr_de_us.label == "Bookings to France, Germany or USA"

    @pytest.mark.xfail(reason="Variable & table parameters as str not implemented.")
    def test_selector_clause_init_var_as_str(self):
        bookings_fr_de_us = SelectorClause(
            "boDest", ["06", "07", "38"], label="Bookings to France, Germany or USA"
        )
        assert bookings_fr_de_us.table_name == "Bookings"
        assert bookings_fr_de_us.variable_name == "boDest"
        assert bookings_fr_de_us.values == ["06", "07", "38"]
        assert bookings_fr_de_us.label == "Bookings to France, Germany or USA"

    def test_selector_clause_to_model_clause(self):
        fake_bookings_fr_de_us = Mock(
            table_name="Bookings",
            variable_name="boDest",
            values=["06", "07", "38"],
            label="Bookings to France, Germany or USA",
            include=True,
            session=None,
        )
        expected_selector_clause_model = aa.Clause(
            criteria=aa.Criteria(
                variable_name="boDest",
                include=True,
                logic="OR",
                ignore_case=False,
                text_match_type="Is",
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(list="06\t07\t38", variable_name="boDest")
                    )
                ],
                table_name="Bookings",
                name="Bookings to France, Germany or USA",
            )
        )
        assert (
            SelectorClause._to_model_clause(fake_bookings_fr_de_us)
            == expected_selector_clause_model
        )


class TestCombinedCategoriesClause:
    def test_combined_categories_clause_init(self, fake_bookings_table):
        fake_continent_var = Mock()
        fake_continent_var.configure_mock(name="boCont", table=fake_bookings_table)
        bookings_contains_u = CombinedCategoriesClause(
            fake_continent_var,
            {"boDest": ["28", "38", "12"], "boCont": ["! ", "AU", "EU"]},
            label="Location contains 'u'",
        )
        assert bookings_contains_u.table_name == "Bookings"
        assert bookings_contains_u.variable_name == "boCont"
        assert bookings_contains_u.value_sets == {
            "boDest": ["28", "38", "12"],
            "boCont": ["! ", "AU", "EU"],
        }
        assert bookings_contains_u.label == "Location contains 'u'"

    @pytest.mark.xfail(reason="Variable & table parameters as str not implemented.")
    def test_combined_categories_clause_init_var_as_str(self):
        bookings_contains_u = CombinedCategoriesClause(
            "boCont",
            {"boDest": ["28", "38", "12"], "boCont": ["! ", "AU", "EU"]},
            label="Location contains 'u'",
        )
        assert bookings_contains_u.table_name == "Bookings"
        assert bookings_contains_u.variable_name == "boCont"
        assert bookings_contains_u.value_sets == {
            "boDest": ["28", "38", "12"],
            "boCont": ["! ", "AU", "EU"],
        }
        assert bookings_contains_u.label == "Location contains 'u'"

    def test_combined_categories_clause_to_model_clause(self):
        fake_bookings_contains_u = Mock(
            table_name="Bookings",
            variable_name="boCont",
            value_sets={"boDest": ["28", "38", "12"], "boCont": ["! ", "AU", "EU"]},
            label="Location contains 'u'",
            include=True,
            session=None,
        )
        expected_combined_categories_model = aa.Clause(
            criteria=aa.Criteria(
                variable_name="boCont",
                include=True,
                logic="OR",
                ignore_case=False,
                text_match_type="Is",
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(list="28\t38\t12", variable_name="boDest")
                    ),
                    aa.ValueRule(
                        list_rule=aa.ListRule(list="! \tAU\tEU", variable_name="boCont")
                    ),
                ],
                table_name="Bookings",
                name="Location contains 'u'",
            )
        )
        assert (
            CombinedCategoriesClause._to_model_clause(fake_bookings_contains_u)
            == expected_combined_categories_model
        )


class TestNumericClause:
    def test_numeric_clause_init(self, fake_people_table):
        fake_total_spend_var = Mock()
        fake_total_spend_var.configure_mock(name="peTotalS", table=fake_people_table)
        example_numeric_clause = NumericClause(
            fake_total_spend_var,
            ["<1066", ">=1558 - <=1603", "=1936", ">1952"],
            include=False,
            label="Exclude total spend matching monarch dates",
        )
        assert example_numeric_clause.table_name == "People"
        assert example_numeric_clause.variable_name == "peTotalS"
        assert example_numeric_clause.values == [
            "<1066",
            ">=1558 - <=1603",
            "=1936",
            ">1952",
        ]
        assert example_numeric_clause.include is False
        assert (
            example_numeric_clause.label == "Exclude total spend matching monarch dates"
        )

    @pytest.mark.xfail(reason="Variable & table parameters as str not implemented.")
    def test_numeric_clause_init_var_as_str(self):
        example_numeric_clause = NumericClause(
            "peTotalS",
            ["<1066", ">=1558 - <=1603", "=1936", ">1952"],
            include=False,
            label="Exclude total spend matching monarch dates",
        )
        assert example_numeric_clause.table_name == "People"
        assert example_numeric_clause.variable_name == "peTotalS"
        assert example_numeric_clause.values == [
            "<1066",
            ">=1558 - <=1603",
            "=1936",
            ">1952",
        ]
        assert example_numeric_clause.include is False
        assert (
            example_numeric_clause.label == "Exclude total spend matching monarch dates"
        )

    def test_numeric_clause_to_model_clause(self):
        fake_numeric_clause = Mock(
            table_name="People",
            variable_name="peTotalS",
            values=["<1066", ">=1558 - <=1603", "=1936", ">1952"],
            include=False,
            label="Exclude total spend matching monarch dates",
            session=None,
        )
        expected_numeric_clause_model = aa.Clause(
            criteria=aa.Criteria(
                variable_name="peTotalS",
                include=False,
                logic="OR",
                ignore_case=False,
                text_match_type="Is",
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(
                            list="<1066\t>=1558 - <=1603\t=1936\t>1952",
                            variable_name="peTotalS",
                        )
                    )
                ],
                table_name="People",
                name="Exclude total spend matching monarch dates",
            )
        )
        assert (
            NumericClause._to_model_clause(fake_numeric_clause)
            == expected_numeric_clause_model
        )


class TestTextClause:
    def test_text_clause_init(self, fake_households_table):
        fake_address_var = Mock()
        fake_address_var.configure_mock(name="hoAddr", table=fake_households_table)
        example_text_clause = TextClause(
            fake_address_var,
            ["Regent", "Oxford", "Bond"],
            "Contains",
            True,
            label="Green Monopoly squares addresses (minus 'Street')",
        )
        assert example_text_clause.table_name == "Households"
        assert example_text_clause.variable_name == "hoAddr"
        assert example_text_clause.values == ["Regent", "Oxford", "Bond"]
        assert example_text_clause.match_type == "Contains"
        assert example_text_clause.match_case is True
        assert (
            example_text_clause.label
            == "Green Monopoly squares addresses (minus 'Street')"
        )

    @pytest.mark.xfail(reason="Variable & table parameters as str not implemented.")
    def test_text_clause_init_var_as_str(self):
        example_text_clause = TextClause(
            "hoAddr",
            ["Regent", "Oxford", "Bond"],
            "Contains",
            True,
            label="Green Monopoly squares addresses (minus 'Street')",
        )
        assert example_text_clause.table_name == "Households"
        assert example_text_clause.variable_name == "hoAddr"
        assert example_text_clause.values == ["Regent", "Oxford", "Bond"]
        assert example_text_clause.match_type == "Contains"
        assert example_text_clause.match_case is True
        assert (
            example_text_clause.label
            == "Green Monopoly squares addresses (minus 'Street')"
        )

    def test_text_clause_to_model_clause(self):
        fake_text_clause = Mock(
            table_name="Households",
            variable_name="hoAddr",
            values=["Regent", "Oxford", "Bond"],
            match_type="Contains",
            match_case=True,
            label="Green Monopoly squares addresses (minus 'Street')",
            include=True,
            session=None,
        )
        expected_text_clause_model = aa.Clause(
            criteria=aa.Criteria(
                variable_name="hoAddr",
                include=True,
                logic="OR",
                ignore_case=False,
                text_match_type="Contains",
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(
                            list="Regent\tOxford\tBond", variable_name="hoAddr"
                        )
                    )
                ],
                table_name="Households",
                name="Green Monopoly squares addresses (minus 'Street')",
            )
        )
        assert TextClause._to_model_clause(fake_text_clause) == expected_text_clause_model


class TestArrayClause:
    def test_array_clause_init(self, fake_households_table):
        fake_car_make_code_var = Mock()
        fake_car_make_code_var.configure_mock(
            name="HHCarmak", table=fake_households_table
        )
        example_array_clause = ArrayClause(
            fake_car_make_code_var,
            ["FOR", "PEU", "VOL"],
            "AND",
            label="House has Ford, Peugeot & Volvo",
        )
        assert example_array_clause.table_name == "Households"
        assert example_array_clause.variable_name == "HHCarmak"
        assert example_array_clause.values == ["FOR", "PEU", "VOL"]
        assert example_array_clause.logic == "AND"
        assert example_array_clause.label == "House has Ford, Peugeot & Volvo"

    @pytest.mark.xfail(reason="Variable & table parameters as str not implemented.")
    def test_array_clause_init_var_as_str(self):
        example_array_clause = ArrayClause(
            "HHCarmak",
            ["FOR", "PEU", "VOL"],
            "AND",
            label="House has Ford, Peugeot & Volvo",
        )
        assert example_array_clause.table_name == "Households"
        assert example_array_clause.variable_name == "HHCarmak"
        assert example_array_clause.values == ["FOR", "PEU", "VOL"]
        assert example_array_clause.logic == "AND"
        assert example_array_clause.label == "House has Ford, Peugeot & Volvo"

    def test_array_clause_to_model_clause(self):
        fake_array_clause = Mock(
            table_name="Households",
            variable_name="HHCarmak",
            values=["FOR", "PEU", "VOL"],
            logic="AND",
            label="House has Ford, Peugeot & Volvo",
            include=True,
            Session=None,
        )
        expected_array_clause_model = aa.Clause(
            criteria=aa.Criteria(
                variable_name="HHCarmak",
                include=True,
                logic="AND",
                ignore_case=False,
                text_match_type="Is",
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(
                            list="FOR\tPEU\tVOL", variable_name="HHCarmak"
                        )
                    )
                ],
                table_name="Households",
                name="House has Ford, Peugeot & Volvo",
            )
        )
        assert ArrayClause._to_model_clause(fake_array_clause) == expected_array_clause_model


class TestFlagArrayClause:
    def test_flag_array_clause_init(self, fake_people_table):
        fake_newspapers_var = Mock()
        fake_newspapers_var.configure_mock(name="peNews", table=fake_people_table)
        example_flag_array_clause = FlagArrayClause(
            fake_newspapers_var,
            [
                "Daily Express  ",
                "The Sun        ",
                "Daily Mirror   ",
                "Daily Mail     ",
                "Record         ",
            ],
            "OR",
            label="Tabloid newspaper readers",
        )
        assert example_flag_array_clause.table_name == "People"
        assert example_flag_array_clause.variable_name == "peNews"
        assert example_flag_array_clause.values == [
            "Daily Express  ",
            "The Sun        ",
            "Daily Mirror   ",
            "Daily Mail     ",
            "Record         ",
        ]
        assert example_flag_array_clause.logic == "OR"
        assert example_flag_array_clause.label == "Tabloid newspaper readers"

    @pytest.mark.xfail(reason="Variable & table parameters as str not implemented.")
    def test_flag_array_clause_init_var_as_str(self):
        example_flag_array_clause = FlagArrayClause(
            "peNews",
            [
                "Daily Express  ",
                "The Sun        ",
                "Daily Mirror   ",
                "Daily Mail     ",
                "Record         ",
            ],
            "OR",
            label="Tabloid newspaper readers",
        )
        assert example_flag_array_clause.table_name == "People"
        assert example_flag_array_clause.variable_name == "peNews"
        assert example_flag_array_clause.values == [
            "Daily Express  ",
            "The Sun        ",
            "Daily Mirror   ",
            "Daily Mail     ",
            "Record         ",
        ]
        assert example_flag_array_clause.logic == "OR"
        assert example_flag_array_clause.label == "Tabloid newspaper readers"

    def test_flag_array_clause_to_model_clause(self):
        fake_flag_array_clause = Mock(
            table_name="People",
            variable_name="peNews",
            values=[
                "Daily Express  ",
                "The Sun        ",
                "Daily Mirror   ",
                "Daily Mail     ",
                "Record         ",
            ],
            logic="OR",
            label="Tabloid newspaper readers",
            include=True,
            session=None,
        )
        expected_flag_array_clause_model = aa.Clause(
            criteria=aa.Criteria(
                variable_name="peNews",
                include=True,
                logic="OR",
                ignore_case=False,
                text_match_type="Is",
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(
                            list=(
                                "Daily Express  "
                                "\tThe Sun        "
                                "\tDaily Mirror   "
                                "\tDaily Mail     "
                                "\tRecord         "
                            ),
                            variable_name="peNews",
                        )
                    )
                ],
                table_name="People",
                name="Tabloid newspaper readers",
            )
        )
        assert (
            FlagArrayClause._to_model_clause(fake_flag_array_clause)
            == expected_flag_array_clause_model
        )


class TestDateListClause:
    def test_date_list_clause_init(self, fake_bookings_table):
        fake_travel_date_var = Mock()
        fake_travel_date_var.configure_mock(name="boTrav", table=fake_bookings_table)
        exclude_bank_hols_cmas16_new_year17 = DateListClause(
            fake_travel_date_var,
            ["20161225", "20161226", "20170101"],
            label="Not bank holidays within Xmas hols 2016-17",
            include=False,
        )
        assert exclude_bank_hols_cmas16_new_year17.table_name == "Bookings"
        assert exclude_bank_hols_cmas16_new_year17.variable_name == "boTrav"
        assert exclude_bank_hols_cmas16_new_year17.values == [
            "20161225",
            "20161226",
            "20170101",
        ]
        assert exclude_bank_hols_cmas16_new_year17.label == (
            "Not bank holidays within Xmas hols 2016-17"
        )
        assert exclude_bank_hols_cmas16_new_year17.include is False

    @pytest.mark.xfail(reason="Variable & table parameters as str not implemented.")
    def test_date_list_clause_init_var_as_str(self):
        exclude_bank_hols_cmas16_new_year17 = DateListClause(
            "boTrav",
            ["20161225", "20161226", "20170101"],
            label="Not bank holidays within Xmas hols 2016-17",
            include=False,
        )
        assert exclude_bank_hols_cmas16_new_year17.table_name == "Bookings"
        assert exclude_bank_hols_cmas16_new_year17.variable_name == "boTrav"
        assert exclude_bank_hols_cmas16_new_year17.values == [
            "20161225",
            "20161226",
            "20170101",
        ]
        assert exclude_bank_hols_cmas16_new_year17.label == (
            "Not bank holidays within Xmas hols 2016-17"
        )
        assert exclude_bank_hols_cmas16_new_year17.include is False

    def test_date_list_clause_to_model_clause(self):
        fake_date_list_clause = Mock(
            table_name="Bookings",
            variable_name="boTrav",
            values=["20161225", "20161226", "20170101"],
            label="Exclude bank holidays over Christmas/New Year 2016/17",
            include=False,
            session=None,
        )
        expected_date_list_clause_model = aa.Clause(
            criteria=aa.Criteria(
                variable_name="boTrav",
                include=False,
                logic="OR",
                ignore_case=False,
                text_match_type="Is",
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(
                            list="20161225\t20161226\t20170101", variable_name="boTrav"
                        ),
                        predefined_rule="AdhocDates",
                    )
                ],
                table_name="Bookings",
                name="Exclude bank holidays over Christmas/New Year 2016/17",
            )
        )
        assert (
            DateListClause._to_model_clause(fake_date_list_clause)
            == expected_date_list_clause_model
        )


class TestDateRangeClause:
    def test_create_range_parameters(self):
        assert DateRangeClause._create_range_parameters(
            Mock(start="earliest", end="latest")
        ) == {"start_range_limit": "Earliest", "end_range_limit": "Latest"}
        assert DateRangeClause._create_range_parameters(
            Mock(start="2007-06-27", end="LATEST")
        ) == {
            "start_range_limit": "Actual",
            "range_start_date": "2007-06-27T00:00:00",
            "end_range_limit": "Latest",
        }
        assert DateRangeClause._create_range_parameters(
            Mock(start="EaRlIeSt", end="2010-05-11")
        ) == {
            "start_range_limit": "Earliest",
            "end_range_limit": "Actual",
            "range_end_date": "2010-05-11T00:00:00",
        }
        assert DateRangeClause._create_range_parameters(
            Mock(start="2016-07-13", end="2019-07-24")
        ) == {
            "start_range_limit": "Actual",
            "range_start_date": "2016-07-13T00:00:00",
            "end_range_limit": "Actual",
            "range_end_date": "2019-07-24T00:00:00",
        }
        assert DateRangeClause._create_range_parameters(
            Mock(start="doesn't check that these", end="actually look like dates")
        ) == {
            "start_range_limit": "Actual",
            "range_start_date": "doesn't check that theseT00:00:00",
            "end_range_limit": "Actual",
            "range_end_date": "actually look like datesT00:00:00",
        }

    def test_date_range_clause_init(self, fake_bookings_table):
        fake_booking_date_var = Mock()
        fake_booking_date_var.configure_mock(name="boDate", table=fake_bookings_table)
        example_date_range_clause = DateRangeClause(
            fake_booking_date_var,
            "2016-03-27",
            "2016-10-30",
            label="Holidays booked during BST 2016",
        )
        assert example_date_range_clause.table_name == "Bookings"
        assert example_date_range_clause.variable_name == "boDate"
        assert example_date_range_clause.start == "2016-03-27"
        assert example_date_range_clause.end == "2016-10-30"
        assert example_date_range_clause.label == "Holidays booked during BST 2016"
        assert example_date_range_clause.include is True

    @pytest.mark.xfail(reason="Variable & table parameters as str not implemented.")
    def test_date_range_clause_init_var_as_str(self):
        example_date_range_clause = DateRangeClause(
            "boDate",
            "2016-03-27",
            "2016-10-30",
            label="Holidays booked during BST 2016",
        )
        assert example_date_range_clause.table_name == "Bookings"
        assert example_date_range_clause.variable_name == "boDate"
        assert example_date_range_clause.start == "2016-03-27"
        assert example_date_range_clause.end == "2016-10-30"
        assert example_date_range_clause.label == "Holidays booked during BST 2016"
        assert example_date_range_clause.include is True

    def test_date_range_clause_to_model_clause(self):
        fake_date_range_clause = Mock(
            table_name="Bookings",
            variable_name="boDate",
            start="2016-03-27",
            end="Latest",
            label="Holidays booked after change to BST 2016",
            include=True,
            session=None,
            _create_range_parameters=Mock(
                return_value={
                    "start_range_limit": "Actual",
                    "range_start_date": "2016-03-27T00:00:00",
                    "end_range_limit": "Latest",
                }
            ),
        )
        expected_date_range_clause_model = aa.Clause(
            criteria=aa.Criteria(
                variable_name="boDate",
                include=True,
                logic="OR",
                ignore_case=False,
                text_match_type="Is",
                value_rules=[
                    aa.ValueRule(
                        predefined_rule="CustomRule",
                        date_rule=aa.DateRule(
                            pattern_frequency="Daily",
                            pattern_interval=1,
                            pattern_days_of_week=["All"],
                            start_range_limit="Actual",
                            range_start_date="2016-03-27T00:00:00",
                            end_range_limit="Latest",
                        ),
                    )
                ],
                table_name="Bookings",
                name="Holidays booked after change to BST 2016",
            )
        )
        assert (
            DateRangeClause._to_model_clause(fake_date_range_clause)
            == expected_date_range_clause_model
        )


@pytest.mark.xfail(reason="Not implemented yet.")
class TestTimeRangeClause:
    def test_time_range_clause_init(self):
        raise NotImplementedError

    def test_time_range_clause_init_var_as_str(self):
        raise NotImplementedError

    def test_time_range_clause_to_model_clause(self):
        raise NotImplementedError


class TestDateTimeRangeClause:
    def test_create_range_parameters(self):
        assert DateTimeRangeClause._create_range_parameters(
            Mock(start="earliest", end="latest")
        ) == {"start_range_limit": "Earliest", "end_range_limit": "Latest"}
        assert DateTimeRangeClause._create_range_parameters(
            Mock(start="2007-06-27T12:34:56", end="laTesT")
        ) == {
            "start_range_limit": "Actual",
            "range_start_date": "2007-06-27T12:34:56",
            "end_range_limit": "Latest",
        }
        assert DateTimeRangeClause._create_range_parameters(
            Mock(start="EARLIEST", end="2010-05-11T09:08:07")
        ) == {
            "start_range_limit": "Earliest",
            "end_range_limit": "Actual",
            "range_end_date": "2010-05-11T09:08:07",
        }
        assert DateTimeRangeClause._create_range_parameters(
            Mock(start="2016-07-13T17:59:32", end="2019-07-24T16:05:55")
        ) == {
            "start_range_limit": "Actual",
            "range_start_date": "2016-07-13T17:59:32",
            "end_range_limit": "Actual",
            "range_end_date": "2019-07-24T16:05:55",
        }
        assert DateTimeRangeClause._create_range_parameters(
            Mock(start="doesn't check that these", end="actually look like dates")
        ) == {
            "start_range_limit": "Actual",
            "range_start_date": "doesn't check that these",
            "end_range_limit": "Actual",
            "range_end_date": "actually look like dates",
        }

    def test_datetime_range_clause_init(self, fake_bookings_table):
        fake_travel_date_var = Mock()
        fake_travel_date_var.configure_mock(name="boTrav", table=fake_bookings_table)
        example_date_range_clause = DateTimeRangeClause(
            fake_travel_date_var,
            "2001-09-09T02:46:40",
            "2033-05-18T04:33:20",
            label="Holidays taken between 1B and 2B second Unix timestamps",
        )
        assert example_date_range_clause.table_name == "Bookings"
        assert example_date_range_clause.variable_name == "boTrav"
        assert example_date_range_clause.start == "2001-09-09T02:46:40"
        assert example_date_range_clause.end == "2033-05-18T04:33:20"
        assert (
            example_date_range_clause.label
            == "Holidays taken between 1B and 2B second Unix timestamps"
        )
        assert example_date_range_clause.include is True

    @pytest.mark.xfail(reason="Variable & table parameters as str not implemented.")
    def test_datetime_range_clause_init_var_as_str(self):
        example_date_range_clause = DateTimeRangeClause(
            "boTrav",
            "2001-09-09T02:46:40",
            "2033-05-18T04:33:20",
            label="Holidays taken between 1B and 2B second Unix timestamps",
        )
        assert example_date_range_clause.table_name == "Bookings"
        assert example_date_range_clause.variable_name == "boTrav"
        assert example_date_range_clause.start == "2001-09-09T02:46:40"
        assert example_date_range_clause.end == "2033-05-18T04:33:20"
        assert (
            example_date_range_clause.label
            == "Holidays taken between 1B and 2B second Unix timestamps"
        )
        assert example_date_range_clause.include is True

    def test_datetime_range_clause_to_model_clause(self):
        fake_datetime_range_clause = Mock(
            table_name="Bookings",
            variable_name="boTrav",
            start="Earliest",
            end="2033-05-18T04:33:20",
            label="Holidays taken between before 2B second Unix timestamp",
            include=True,
            session=None,
            _create_range_parameters=Mock(
                return_value={
                    "start_range_limit": "Earliest",
                    "end_range_limit": "Actual",
                    "range_end_date": "2033-05-18T04:33:20",
                }
            ),
        )
        expected_datetime_range_clause_model = aa.Clause(
            criteria=aa.Criteria(
                variable_name="boTrav",
                include=True,
                logic="OR",
                ignore_case=False,
                text_match_type="Is",
                value_rules=[
                    aa.ValueRule(
                        predefined_rule="CustomRule",
                        date_rule=aa.DateRule(
                            pattern_frequency="Daily",
                            pattern_interval=1,
                            pattern_days_of_week=["All"],
                            start_range_limit="Earliest",
                            end_range_limit="Actual",
                            range_end_date="2033-05-18T04:33:20",
                        ),
                    )
                ],
                table_name="Bookings",
                name="Holidays taken between before 2B second Unix timestamp",
            )
        )
        assert (
            DateTimeRangeClause._to_model_clause(fake_datetime_range_clause)
            == expected_datetime_range_clause_model
        )


@pytest.mark.xfail(reason="Not implemented yet.")
class TestReferenceClause:
    def test_reference_clause_init(self):
        raise NotImplementedError

    def test_reference_clause_init_var_as_str(self):
        raise NotImplementedError

    def test_reference_clause_to_model_clause(self):
        raise NotImplementedError


class TestBooleanClause:
    def test_boolean_clause_init(self, fake_bookings_table):
        clause1 = Mock()
        clause2 = Mock()
        example_boolean_clause = BooleanClause(
            fake_bookings_table,
            "AND",
            [clause1, clause2],
            label="Both of these please!",
        )
        assert example_boolean_clause.table_name == "Bookings"
        assert example_boolean_clause.operation == "AND"
        assert example_boolean_clause.operands == [clause1, clause2]
        assert example_boolean_clause.label == "Both of these please!"

    @pytest.mark.xfail(reason="Table parameter as str not implemented.")
    def test_boolean_clause_init_table_as_str(self):
        clause1 = Mock()
        clause2 = Mock()
        example_boolean_clause = BooleanClause(
            "Bookings", "AND", [clause1, clause2], label="Both of these please!"
        )
        assert example_boolean_clause.table_name == "Bookings"
        assert example_boolean_clause.operation == "AND"
        assert example_boolean_clause.operands == [clause1, clause2]
        assert example_boolean_clause.label == "Both of these please!"

    def test_boolean_clause_to_model_clause(self):
        clause1 = Mock()
        clause2 = Mock()
        clause1._to_model_clause.return_value = "Clause1 model goes here"
        clause2._to_model_clause.return_value = "Clause2 model goes here"
        fake_boolean_clause = Mock(
            table_name="Bookings",
            operation="AND",
            operands=[clause1, clause2],
            label="Both of these please!",
            session=None,
        )
        expected_boolean_clause_model = aa.Clause(
            logic=aa.Logic(
                operation="AND",
                operands=["Clause1 model goes here", "Clause2 model goes here"],
                table_name="Bookings",
                name="Both of these please!",
            )
        )
        assert (
            BooleanClause._to_model_clause(fake_boolean_clause)
            == expected_boolean_clause_model
        )
        clause1._to_model_clause.assert_called_once_with()
        clause2._to_model_clause.assert_called_once_with()


# TODO: unary logic query


class TestTableClause:
    def test_table_clause_init(self, fake_people_table):
        subclause = Mock()
        example_table_clause = TableClause(
            fake_people_table, "THE", subclause, label="People who live at these houses"
        )
        assert example_table_clause.table_name == "People"
        assert example_table_clause.operation == "THE"
        assert example_table_clause.operand is subclause
        assert example_table_clause.label == "People who live at these houses"

    @pytest.mark.xfail(reason="Table parameter as str not implemented.")
    def test_table_clause_init_table_as_str(self):
        subclause = Mock()
        example_table_clause = TableClause(
            "People", "THE", subclause, label="People who live at these houses"
        )
        assert example_table_clause.table_name == "People"
        assert example_table_clause.operation == "THE"
        assert example_table_clause.operand is subclause
        assert example_table_clause.label == "People who live at these houses"

    def test_table_clause_to_model_clause(self):
        subclause = Mock()
        subclause._to_model_clause.return_value = "Subclause model goes here"
        fake_table_clause = Mock(
            table_name="People",
            operation="THE",
            operand=subclause,
            label="People who live at these houses",
            session=None,
        )
        expected_table_clause_model = aa.Clause(
            logic=aa.Logic(
                operation="THE",
                operands=["Subclause model goes here"],
                table_name="People",
                name="People who live at these houses",
            )
        )
        assert TableClause._to_model_clause(fake_table_clause) == expected_table_clause_model
        subclause._to_model_clause.assert_called_once_with()


class TestSubSelectionClause:
    def test_sub_selection_clause_init(self):
        fake_selection = Mock()
        example_subselection_clause = SubSelectionClause(fake_selection)
        assert example_subselection_clause.selection is fake_selection

    def test_sub_selection_clause_to_model_clause(self):
        fake_selection = Mock()
        fake_selection._to_model_selection.return_value = "Selection model goes here"
        fake_subselection_clause = Mock(
            selection=fake_selection, label=None, session=None
        )
        expected_subselection_clause_model = aa.Clause(
            sub_selection="Selection model goes here"
        )
        assert (
            SubSelectionClause._to_model_clause(fake_subselection_clause)
            == expected_subselection_clause_model
        )
        fake_selection._to_model_selection.assert_called_once_with()
