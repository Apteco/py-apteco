from datetime import date, datetime
from decimal import Decimal
from fractions import Fraction
from unittest.mock import Mock

import apteco_api as aa
import pytest

from apteco.query import (
    SelectorVariableMixin,
    NumericVariableMixin,
    TextVariableMixin,
    ArrayVariableMixin,
    FlagArrayVariableMixin,
    ArrayClause,
    BooleanClause,
    CombinedCategoriesClause,
    FlagArrayClause,
    NumericClause,
    SelectorClause,
    SubSelectionClause,
    TableClause,
    TextClause,
    create_date_range_parameters,
    normalize_string_input,
    normalize_string_value,
    normalize_number_input,
    normalize_number_value,
    normalize_date_input,
    normalize_date_value,
    normalize_datetime_input,
    normalize_datetime_value,
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
        normalize_date_input("2008-12-03", "A date-y string doesn't count as a number.")
    assert exc_info.value.args[0] == "A date-y string doesn't count as a number."

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
        normalize_datetime_value([
            datetime(2012, 12, 20, 1, 2, 3),
            datetime(2012, 12, 21, 4, 5, 6),
            datetime(2012, 12, 22, 7, 8, 9),
        ], "Can't have lists here.")
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
    assert normalize_datetime_input([
        datetime(2000, 4, 24, 1, 23, 45),
        datetime(2000, 5, 1, 6, 7),
        datetime(2000, 5, 29, 8),
        datetime(2000, 8, 28),
    ], "Shouldn't see this error") == [
        "2000-04-24T01:23:45",
        "2000-05-01T06:07:00",
        "2000-05-29T08:00:00",
        "2000-08-28T00:00:00",
    ]
    assert normalize_datetime_input((
        datetime(2020 + i, i, i + 23, i ** 2 % (i + 5), i ** 2, i * 8)
        for i in range(4, 8)
    ), "Shouldn't see this error") == [
        "2024-04-27T07:16:32",
        "2025-05-28T05:25:40",
        "2026-06-29T03:36:48",
        "2027-07-30T01:49:56"
    ]

    with pytest.raises(ValueError) as exc_info:
        normalize_datetime_input(True, "A bool isn't a datetime.")
    assert exc_info.value.args[0] == "A bool isn't a datetime."

    with pytest.raises(ValueError) as exc_info:
        normalize_datetime_input(946684800, "A number isn't a datetime.")
    assert exc_info.value.args[0] == "A number isn't a datetime."

    with pytest.raises(ValueError) as exc_info:
        normalize_datetime_input("2008-12-03T03:33:30", "A datetime-y string doesn't count as a number.")
    assert exc_info.value.args[0] == "A datetime-y string doesn't count as a number."

    with pytest.raises(ValueError) as exc_info:
        normalize_datetime_input([20001016220220, 20081203033330], "Can't sneak numbers through inside a list")
    assert exc_info.value.args[0] == "Can't sneak numbers through inside a list"


class TestSelectorVariableMixin:

    @pytest.fixture()
    def fake_selector_variable_mixin(self):
        svm_example = SelectorVariableMixin.__new__(SelectorVariableMixin)
        svm_example.type = "Selector"
        svm_example.table_name = "Supporters"
        svm_example.name = "Membership"
        svm_example.session = "CharityDataViewSession"
        return svm_example

    def test_eq(self, fake_selector_variable_mixin):
        high_value_supporters = fake_selector_variable_mixin == ("Gold", "Platinum")
        assert type(high_value_supporters) == SelectorClause
        assert high_value_supporters.table_name == "Supporters"
        assert high_value_supporters.variable_name == "Membership"
        assert high_value_supporters.values == ["Gold", "Platinum"]
        assert high_value_supporters.include is True
        assert high_value_supporters.session == "CharityDataViewSession"

        bronze_supporters = fake_selector_variable_mixin == "Bronze"
        assert type(bronze_supporters) == SelectorClause
        assert bronze_supporters.table_name == "Supporters"
        assert bronze_supporters.variable_name == "Membership"
        assert bronze_supporters.values == ["Bronze"]
        assert bronze_supporters.include is True
        assert bronze_supporters.session == "CharityDataViewSession"

    def test_ne(self, fake_selector_variable_mixin):
        higher_value_supporters = fake_selector_variable_mixin != ("Bronze", "Silver")
        assert type(higher_value_supporters) == SelectorClause
        assert higher_value_supporters.table_name == "Supporters"
        assert higher_value_supporters.variable_name == "Membership"
        assert higher_value_supporters.values == ["Bronze", "Silver"]
        assert higher_value_supporters.include is False
        assert higher_value_supporters.session == "CharityDataViewSession"

        not_platinum = fake_selector_variable_mixin != "Platinum"
        assert type(not_platinum) == SelectorClause
        assert not_platinum.table_name == "Supporters"
        assert not_platinum.variable_name == "Membership"
        assert not_platinum.values == ["Platinum"]
        assert not_platinum.include is False
        assert not_platinum.session == "CharityDataViewSession"


class TestNumericVariableMixin:

    @pytest.fixture()
    def fake_numeric_variable_mixin(self):
        nvm_example = NumericVariableMixin.__new__(NumericVariableMixin)
        nvm_example.type = "Numeric"
        nvm_example.table_name = "Donations"
        nvm_example.name = "Amount"
        nvm_example.session = "CharityDataViewSession"
        return nvm_example

    def test_eq(self, fake_numeric_variable_mixin):
        donations_100 = fake_numeric_variable_mixin == 100
        assert type(donations_100) == NumericClause
        assert donations_100.table_name == "Donations"
        assert donations_100.variable_name == "Amount"
        assert donations_100.values == ["100"]
        assert donations_100.include is True
        assert donations_100.session == "CharityDataViewSession"

        hundreds_donations = fake_numeric_variable_mixin == (i * 100 for i in range(1, 10))
        assert type(hundreds_donations) == NumericClause
        assert hundreds_donations.table_name == "Donations"
        assert hundreds_donations.variable_name == "Amount"
        assert hundreds_donations.values == ["100", "200", "300", "400", "500", "600", "700", "800", "900"]
        assert hundreds_donations.include is True
        assert hundreds_donations.session == "CharityDataViewSession"

    def test_ne(self, fake_numeric_variable_mixin):
        not_this = fake_numeric_variable_mixin != 72.1896
        assert type(not_this) == NumericClause
        assert not_this.table_name == "Donations"
        assert not_this.variable_name == "Amount"
        assert not_this.values == ["72.1896"]
        assert not_this.include is False
        assert not_this.session == "CharityDataViewSession"

        not_one_of_these = fake_numeric_variable_mixin != (17.5, 8192)
        assert type(not_one_of_these) == NumericClause
        assert not_one_of_these.table_name == "Donations"
        assert not_one_of_these.variable_name == "Amount"
        assert not_one_of_these.values == ["17.5", "8192"]
        assert not_one_of_these.include is False
        assert not_one_of_these.session == "CharityDataViewSession"

    def test_lt(self, fake_numeric_variable_mixin):
        small_donations = fake_numeric_variable_mixin < Decimal("10.00")
        assert type(small_donations) == NumericClause
        assert small_donations.table_name == "Donations"
        assert small_donations.variable_name == "Amount"
        assert small_donations.values == ["<10.0000"]
        assert small_donations.include is True
        assert small_donations.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            less_than_a_list = fake_numeric_variable_mixin < [512.64, 646.464646]
        assert exc_info.value.args[0] == "Must specify a single number when using inequality operators."

    def test_le(self, fake_numeric_variable_mixin):
        up_to_including_10k = fake_numeric_variable_mixin <= 10_000
        assert type(up_to_including_10k) == NumericClause
        assert up_to_including_10k.table_name == "Donations"
        assert up_to_including_10k.variable_name == "Amount"
        assert up_to_including_10k.values == ["<=10000"]
        assert up_to_including_10k.include is True
        assert up_to_including_10k.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            less_than_equal_tuple = fake_numeric_variable_mixin <= (52, 27, 9.75)
        assert exc_info.value.args[0] == "Must specify a single number when using inequality operators."

    def test_gt(self, fake_numeric_variable_mixin):
        big_donations = fake_numeric_variable_mixin > 0.01 * 26_000
        assert type(big_donations) == NumericClause
        assert big_donations.table_name == "Donations"
        assert big_donations.variable_name == "Amount"
        assert big_donations.values == [">260.0"]
        assert big_donations.include is True
        assert big_donations.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            more_than_a_set = fake_numeric_variable_mixin > {15, 30, 40, 40}
        assert exc_info.value.args[0] == "Must specify a single number when using inequality operators."

    def test_ge(self, fake_numeric_variable_mixin):
        at_least_this_ratio = fake_numeric_variable_mixin >= Fraction(65432, 987)
        assert type(at_least_this_ratio) == NumericClause
        assert at_least_this_ratio.table_name == "Donations"
        assert at_least_this_ratio.variable_name == "Amount"
        assert at_least_this_ratio.values == [">=66.2938"]
        assert at_least_this_ratio.include is True
        assert at_least_this_ratio.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            at_least_a_generator = fake_numeric_variable_mixin >= (n for n in "12.3 4.56 789")
        assert exc_info.value.args[0] == "Must specify a single number when using inequality operators."


class TestTextVariableMixin:

    @pytest.fixture()
    def fake_email_text_variable_mixin(self):
        tvm_example = TextVariableMixin.__new__(TextVariableMixin)
        tvm_example.type = "Text"
        tvm_example.table_name = "Supporters"
        tvm_example.name = "EmailAddress"
        tvm_example.session = "CharityDataViewSession"
        return tvm_example

    @pytest.fixture()
    def fake_surname_text_variable_mixin(self):
        tvm_example = TextVariableMixin.__new__(TextVariableMixin)
        tvm_example.type = "Text"
        tvm_example.table_name = "Supporters"
        tvm_example.name = "Surname"
        tvm_example.session = "CharityDataViewSession"
        return tvm_example

    def test_eq(self, fake_email_text_variable_mixin):
        specific_donor = fake_email_text_variable_mixin == "donor@domain.com"
        assert type(specific_donor) == TextClause
        assert specific_donor.table_name == "Supporters"
        assert specific_donor.variable_name == "EmailAddress"
        assert specific_donor.values == ["donor@domain.com"]
        assert specific_donor.match_type == "Is"
        assert specific_donor.match_case is True
        assert specific_donor.include is True
        assert specific_donor.session == "CharityDataViewSession"

        donors_by_email = fake_email_text_variable_mixin == [
            f"donor_{i}@domain.com" for i in range(4)
        ]
        assert type(donors_by_email) == TextClause
        assert donors_by_email.table_name == "Supporters"
        assert donors_by_email.variable_name == "EmailAddress"
        assert donors_by_email.values == [
            "donor_0@domain.com",
            "donor_1@domain.com",
            "donor_2@domain.com",
            "donor_3@domain.com",
        ]
        assert donors_by_email.match_type == "Is"
        assert donors_by_email.match_case is True
        assert donors_by_email.include is True
        assert donors_by_email.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            donors_by_number = fake_email_text_variable_mixin == {34, 765, 2930}
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a text variable"
            " must be given as a string or an iterable of strings."
        )

    def test_ne(self, fake_email_text_variable_mixin):
        dont_want_this_person = fake_email_text_variable_mixin != "bad_donor@domain.com"
        assert type(dont_want_this_person) == TextClause
        assert dont_want_this_person.table_name == "Supporters"
        assert dont_want_this_person.variable_name == "EmailAddress"
        assert dont_want_this_person.values == ["bad_donor@domain.com"]
        assert dont_want_this_person.match_type == "Is"
        assert dont_want_this_person.match_case is True
        assert dont_want_this_person.include is False
        assert dont_want_this_person.session == "CharityDataViewSession"

        not_these_people = fake_email_text_variable_mixin != {
            "dont_email_me@domain.com", "unsubscribed@domain.org"
        }
        assert type(not_these_people) == TextClause
        assert not_these_people.table_name == "Supporters"
        assert not_these_people.variable_name == "EmailAddress"
        assert sorted(not_these_people.values) == [
            "dont_email_me@domain.com", "unsubscribed@domain.org"
        ]
        assert not_these_people.match_type == "Is"
        assert not_these_people.match_case is True
        assert not_these_people.include is False
        assert not_these_people.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            donor_not_an_obj = fake_email_text_variable_mixin != object()
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a text variable"
            " must be given as a string or an iterable of strings."
        )

    def test_le(self, fake_surname_text_variable_mixin):
        first_half_alphabet = fake_surname_text_variable_mixin <= "n"
        assert type(first_half_alphabet) == TextClause
        assert first_half_alphabet.table_name == "Supporters"
        assert first_half_alphabet.variable_name == "Surname"
        assert first_half_alphabet.values == ['<="n"']
        assert first_half_alphabet.match_type == "Ranges"
        assert first_half_alphabet.match_case is True
        assert first_half_alphabet.include is True
        assert first_half_alphabet.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            earlier_than_letters = fake_surname_text_variable_mixin <= list("abcedfgh")
        assert exc_info.value.args[0] == (
            "Must specify a single string when using inequality operators."
        )

    def test_ge(self, fake_surname_text_variable_mixin):
        smith_or_later = fake_surname_text_variable_mixin >= "Smith"
        assert type(smith_or_later) == TextClause
        assert smith_or_later.table_name == "Supporters"
        assert smith_or_later.variable_name == "Surname"
        assert smith_or_later.values == ['>="Smith"']
        assert smith_or_later.match_type == "Ranges"
        assert smith_or_later.match_case is True
        assert smith_or_later.include is True
        assert smith_or_later.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            later_than_tuple = fake_surname_text_variable_mixin >= ("A", "e", "i", "O")
        assert exc_info.value.args[0] == (
            "Must specify a single string when using inequality operators.")


class TestArrayVariableMixin:

    @pytest.fixture()
    def fake_array_variable_mixin(self):
        avm_example = ArrayVariableMixin.__new__(ArrayVariableMixin)
        avm_example.type = "Array"
        avm_example.table_name = "Campaigns"
        avm_example.name = "Tags"
        avm_example.session = "CharityDataViewSession"
        return avm_example

    def test_eq(self, fake_array_variable_mixin):
        national_campaigns = fake_array_variable_mixin == "National"
        assert type(national_campaigns) == ArrayClause
        assert national_campaigns.table_name == "Campaigns"
        assert national_campaigns.variable_name == "Tags"
        assert national_campaigns.values == ["National"]
        assert national_campaigns.logic == "OR"
        assert national_campaigns.include is True
        assert national_campaigns.session == "CharityDataViewSession"

        autumn_campaigns = fake_array_variable_mixin == {
            "Autumn", "Fall", "Sep", "Oct", "Nov", "Halloween", "Back-to-School"
        }
        assert type(autumn_campaigns) == ArrayClause
        assert autumn_campaigns.table_name == "Campaigns"
        assert autumn_campaigns.variable_name == "Tags"
        assert sorted(autumn_campaigns.values) == [
            "Autumn", "Back-to-School", "Fall", "Halloween", "Nov", "Oct", "Sep"
        ]
        assert autumn_campaigns.logic == "OR"
        assert autumn_campaigns.include is True
        assert autumn_campaigns.session == "CharityDataViewSession"

    def test_ne(self, fake_array_variable_mixin):
        not_christmas = fake_array_variable_mixin != "Christmas"
        assert type(not_christmas) == ArrayClause
        assert not_christmas.table_name == "Campaigns"
        assert not_christmas.variable_name == "Tags"
        assert not_christmas.values == ["Christmas"]
        assert not_christmas.logic == "OR"
        assert not_christmas.include is False
        assert not_christmas.session == "CharityDataViewSession"

        one_off_campaigns = fake_array_variable_mixin != [
            "Recurrent", "Annual", "Regular", "Monthly", "Weekly", "Daily", "Seasonal"
        ]
        assert type(one_off_campaigns) == ArrayClause
        assert one_off_campaigns.table_name == "Campaigns"
        assert one_off_campaigns.variable_name == "Tags"
        assert one_off_campaigns.values == [
            "Recurrent", "Annual", "Regular", "Monthly", "Weekly", "Daily", "Seasonal"
        ]
        assert one_off_campaigns.logic == "OR"
        assert one_off_campaigns.include is False
        assert one_off_campaigns.session == "CharityDataViewSession"


class TestFlagArrayVariableMixin:

    @pytest.fixture()
    def fake_flag_array_variable_mixin(self):
        favm_example = FlagArrayVariableMixin.__new__(FlagArrayVariableMixin)
        favm_example.type = "FlagArray"
        favm_example.table_name = "Supporters"
        favm_example.name = "ContactPreferences"
        favm_example.session = "CharityDataViewSession"
        return favm_example

    def test_eq(self, fake_flag_array_variable_mixin):
        can_post = fake_flag_array_variable_mixin == "DirectMail"
        assert type(can_post) == FlagArrayClause
        assert can_post.table_name == "Supporters"
        assert can_post.variable_name == "ContactPreferences"
        assert can_post.values == ["DirectMail"]
        assert can_post.logic == "OR"
        assert can_post.include is True
        assert can_post.session == "CharityDataViewSession"

        phone_or_text = fake_flag_array_variable_mixin == ("SMS", "Telephone")
        assert type(phone_or_text) == FlagArrayClause
        assert phone_or_text.table_name == "Supporters"
        assert phone_or_text.variable_name == "ContactPreferences"
        assert phone_or_text.values == ["SMS", "Telephone"]
        assert phone_or_text.logic == "OR"
        assert phone_or_text.include is True
        assert phone_or_text.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            contactable = fake_flag_array_variable_mixin == True
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a flag array variable"
            " must be given as a string or an iterable of strings."
        )

    def test_ne(self, fake_flag_array_variable_mixin):
        cant_email = fake_flag_array_variable_mixin != "Email"
        assert type(cant_email) == FlagArrayClause
        assert cant_email.table_name == "Supporters"
        assert cant_email.variable_name == "ContactPreferences"
        assert cant_email.values == ["Email"]
        assert cant_email.logic == "OR"
        assert cant_email.include is False
        assert cant_email.session == "CharityDataViewSession"

        not_business = fake_flag_array_variable_mixin != {
            "BusinessPhone", "BusinessDirectMail", "BusinessEmail"
        }
        assert type(not_business) == FlagArrayClause
        assert not_business.table_name == "Supporters"
        assert not_business.variable_name == "ContactPreferences"
        assert sorted(not_business.values) == [
            "BusinessDirectMail", "BusinessEmail", "BusinessPhone"
        ]
        assert not_business.logic == "OR"
        assert not_business.include is False
        assert not_business.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            contactable = fake_flag_array_variable_mixin != 0
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a flag array variable"
            " must be given as a string or an iterable of strings."
        )


class TestSelectorClause:
    def test_selector_clause_init(self):
        bookings_fr_de_us = SelectorClause(
            "Bookings",
            "boDest",
            ["06", "07", "38"],
            label="Bookings to France, Germany or USA",
        )
        assert bookings_fr_de_us.table_name == "Bookings"
        assert bookings_fr_de_us.variable_name == "boDest"
        assert bookings_fr_de_us.values == ["06", "07", "38"]
        assert bookings_fr_de_us.label == "Bookings to France, Germany or USA"

    def test_selector_clause_to_model(self):
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
            SelectorClause._to_model(fake_bookings_fr_de_us)
            == expected_selector_clause_model
        )


class TestCombinedCategoriesClause:
    def test_combined_categories_clause_init(self):
        bookings_contains_u = CombinedCategoriesClause(
            "Bookings",
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

    def test_combined_categories_clause_to_model(self):
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
            CombinedCategoriesClause._to_model(fake_bookings_contains_u)
            == expected_combined_categories_model
        )


class TestNumericClause:
    def test_numeric_clause_init(self):
        example_numeric_clause = NumericClause(
            "People",
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

    def test_numeric_clause_to_model(self):
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
            NumericClause._to_model(fake_numeric_clause)
            == expected_numeric_clause_model
        )


class TestTextClause:
    def test_text_clause_init(self):
        # TODO: add tests for other text match types
        example_text_clause = TextClause(
            "Households",
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

    def test_text_clause_to_model(self):
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
        assert TextClause._to_model(fake_text_clause) == expected_text_clause_model


class TestArrayClause:
    def test_array_clause_init(self):
        example_array_clause = ArrayClause(
            "Households",
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

    def test_array_clause_to_model(self):
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
        assert ArrayClause._to_model(fake_array_clause) == expected_array_clause_model


class TestFlagArrayClause:
    def test_flag_array_clause_init(self):
        example_flag_array_clause = FlagArrayClause(
            "People",
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

    def test_flag_array_clause_to_model(self):
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
            FlagArrayClause._to_model(fake_flag_array_clause)
            == expected_flag_array_clause_model
        )


def test_create_date_range_parameters():
    assert create_date_range_parameters("earliest", "latest") == {
        "start_range_limit": "Earliest",
        "end_range_limit": "Latest",
    }
    assert create_date_range_parameters("2007-06-27", "LATEST") == {
        "start_range_limit": "Actual",
        "start_range_date": "2007-06-27",
        "end_range_limit": "Latest",
    }
    assert create_date_range_parameters("EaRlIeSt", "2010-05-11") == {
        "start_range_limit": "Earliest",
        "end_range_limit": "Actual",
        "end_range_date": "2010-05-11",
    }
    assert create_date_range_parameters(
        "2016-07-13T17:59:32", "2019-07-24T16:05:55"
    ) == {
        "start_range_limit": "Actual",
        "start_range_date": "2016-07-13T17:59:32",
        "end_range_limit": "Actual",
        "end_range_date": "2019-07-24T16:05:55",
    }
    assert create_date_range_parameters(
        "doesn't check that these", "actually look like dates"
    ) == {
        "start_range_limit": "Actual",
        "start_range_date": "doesn't check that these",
        "end_range_limit": "Actual",
        "end_range_date": "actually look like dates",
    }


class TestDateListClause:
    pass


class TestDateRangeClause:
    pass


class TestTimeRangeClause:
    pass


class TestDateTimeRangeClause:
    pass


class TestBooleanClause:
    def test_boolean_clause_init(self):
        clause1 = Mock()
        clause2 = Mock()
        example_boolean_clause = BooleanClause(
            "Bookings", "AND", [clause1, clause2], label="Both of these please!"
        )
        assert example_boolean_clause.table_name == "Bookings"
        assert example_boolean_clause.operation == "AND"
        assert example_boolean_clause.operands == [clause1, clause2]
        assert example_boolean_clause.label == "Both of these please!"

    def test_boolean_clause_to_model(self):
        clause1 = Mock()
        clause2 = Mock()
        clause1._to_model.return_value = "Clause1 model goes here"
        clause2._to_model.return_value = "Clause2 model goes here"
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
            BooleanClause._to_model(fake_boolean_clause)
            == expected_boolean_clause_model
        )
        clause1._to_model.assert_called_once_with()
        clause2._to_model.assert_called_once_with()


# TODO: unary logic query


class TestTableClause:
    def test_table_clause_init(self):
        subclause = Mock()
        example_table_clause = TableClause(
            "People", "THE", subclause, label="People who live at these houses"
        )
        assert example_table_clause.table_name == "People"
        assert example_table_clause.operation == "THE"
        assert example_table_clause.operand is subclause
        assert example_table_clause.label == "People who live at these houses"

    def test_table_clause_to_model(self):
        subclause = Mock()
        subclause._to_model.return_value = "Subclause model goes here"
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
        assert TableClause._to_model(fake_table_clause) == expected_table_clause_model
        subclause._to_model.assert_called_once_with()


class TestSubSelectionClause:
    def test_sub_selection_clause_init(self):
        fake_selection = Mock()
        example_subselection_clause = SubSelectionClause(fake_selection)
        assert example_subselection_clause.selection is fake_selection

    def test_sub_selection_clause_to_model(self):
        fake_selection = Mock()
        fake_selection._to_model.return_value = "Selection model goes here"
        fake_subselection_clause = Mock(
            selection=fake_selection, label=None, session=None
        )
        expected_subselection_clause_model = aa.Clause(
            sub_selection="Selection model goes here"
        )
        assert (
            SubSelectionClause._to_model(fake_subselection_clause)
            == expected_subselection_clause_model
        )
        fake_selection._to_model.assert_called_once_with()
