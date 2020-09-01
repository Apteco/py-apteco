from datetime import date, datetime
from decimal import Decimal
from fractions import Fraction

import pytest

from apteco.query import (
    ArrayClause,
    CombinedCategoriesClause,
    DateListClause,
    DateRangeClause,
    DateTimeRangeClause,
    FlagArrayClause,
    NumericClause,
    ReferenceClause,
    SelectorClause,
    TextClause,
)


class TestSelectorVariable:
    def test_eq(self, fake_selector_variable):
        high_value_supporters = fake_selector_variable == ("Gold", "Platinum")
        assert type(high_value_supporters) == SelectorClause
        assert high_value_supporters.table_name == "Supporters"
        assert high_value_supporters.variable_name == "Membership"
        assert high_value_supporters.values == ["Gold", "Platinum"]
        assert high_value_supporters.include is True
        assert high_value_supporters.session == "CharityDataViewSession"

        bronze_supporters = fake_selector_variable == "Bronze"
        assert type(bronze_supporters) == SelectorClause
        assert bronze_supporters.table_name == "Supporters"
        assert bronze_supporters.variable_name == "Membership"
        assert bronze_supporters.values == ["Bronze"]
        assert bronze_supporters.include is True
        assert bronze_supporters.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            trying_with_a_number = fake_selector_variable == 3
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a selector variable"
            " must be given as a string or an iterable of strings."
        )

    def test_ne(self, fake_selector_variable):
        higher_value_supporters = fake_selector_variable != ("Bronze", "Silver")
        assert type(higher_value_supporters) == SelectorClause
        assert higher_value_supporters.table_name == "Supporters"
        assert higher_value_supporters.variable_name == "Membership"
        assert higher_value_supporters.values == ["Bronze", "Silver"]
        assert higher_value_supporters.include is False
        assert higher_value_supporters.session == "CharityDataViewSession"

        not_platinum = fake_selector_variable != "Platinum"
        assert type(not_platinum) == SelectorClause
        assert not_platinum.table_name == "Supporters"
        assert not_platinum.variable_name == "Membership"
        assert not_platinum.values == ["Platinum"]
        assert not_platinum.include is False
        assert not_platinum.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            trying_with_a_float = fake_selector_variable != 2.5
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a selector variable"
            " must be given as a string or an iterable of strings."
        )


@pytest.mark.xfail(reason="Not yet implemented.")
class TestCombinedCategoriesVariable:
    # TODO: update when implemented
    def test_eq(self, fake_combined_categories_variable):
        northern_supporters = fake_combined_categories_variable == ["NE", "NW", "YRK"]
        assert type(northern_supporters) == CombinedCategoriesClause
        assert northern_supporters.table_name == "Supporters"
        assert northern_supporters.variable_name == "Region"
        assert northern_supporters.values == ["NE", "NW", "YRK"]
        assert northern_supporters.include is True
        assert northern_supporters.session == "CharityDataViewSession"

    # TODO: update when implemented
    def test_ne(self, fake_combined_categories_variable):
        supporters_outside_london = fake_combined_categories_variable != "LDN"
        assert type(supporters_outside_london) == CombinedCategoriesClause
        assert supporters_outside_london.table_name == "Supporters"
        assert supporters_outside_london.variable_name == "Region"
        assert supporters_outside_london.values == ["LDN"]
        assert supporters_outside_london.include is False
        assert supporters_outside_london.session == "CharityDataViewSession"


class TestNumericVariable:
    def test_eq(self, fake_numeric_variable):
        donations_100 = fake_numeric_variable == 100
        assert type(donations_100) == NumericClause
        assert donations_100.table_name == "Donations"
        assert donations_100.variable_name == "Amount"
        assert donations_100.values == ["100"]
        assert donations_100.include is True
        assert donations_100.session == "CharityDataViewSession"

        hundreds_donations = fake_numeric_variable == (i * 100 for i in range(1, 10))
        assert type(hundreds_donations) == NumericClause
        assert hundreds_donations.table_name == "Donations"
        assert hundreds_donations.variable_name == "Amount"
        assert hundreds_donations.values == [
            "100",
            "200",
            "300",
            "400",
            "500",
            "600",
            "700",
            "800",
            "900",
        ]
        assert hundreds_donations.include is True
        assert hundreds_donations.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            trying_with_a_string = fake_numeric_variable == "256"
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a numeric variable"
            " must be given as a number or an iterable of numbers."
        )

    def test_ne(self, fake_numeric_variable):
        not_this = fake_numeric_variable != 72.1896
        assert type(not_this) == NumericClause
        assert not_this.table_name == "Donations"
        assert not_this.variable_name == "Amount"
        assert not_this.values == ["72.1896"]
        assert not_this.include is False
        assert not_this.session == "CharityDataViewSession"

        not_one_of_these = fake_numeric_variable != (17.5, 8192)
        assert type(not_one_of_these) == NumericClause
        assert not_one_of_these.table_name == "Donations"
        assert not_one_of_these.variable_name == "Amount"
        assert not_one_of_these.values == ["17.5", "8192"]
        assert not_one_of_these.include is False
        assert not_one_of_these.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            trying_with_a_boolean = fake_numeric_variable != False
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a numeric variable"
            " must be given as a number or an iterable of numbers."
        )

    def test_lt(self, fake_numeric_variable):
        small_donations = fake_numeric_variable < Decimal("10.00")
        assert type(small_donations) == NumericClause
        assert small_donations.table_name == "Donations"
        assert small_donations.variable_name == "Amount"
        assert small_donations.values == ["<10.0000"]
        assert small_donations.include is True
        assert small_donations.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            less_than_a_list = fake_numeric_variable < [512.64, 646.464646]
        assert exc_info.value.args[0] == (
            "Must specify a single number when using inequality operators."
        )

    def test_le(self, fake_numeric_variable):
        up_to_including_10k = fake_numeric_variable <= 10_000
        assert type(up_to_including_10k) == NumericClause
        assert up_to_including_10k.table_name == "Donations"
        assert up_to_including_10k.variable_name == "Amount"
        assert up_to_including_10k.values == ["<=10000"]
        assert up_to_including_10k.include is True
        assert up_to_including_10k.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            less_than_equal_tuple = fake_numeric_variable <= (52, 27, 9.75)
        assert exc_info.value.args[0] == (
            "Must specify a single number when using inequality operators."
        )

    def test_gt(self, fake_numeric_variable):
        big_donations = fake_numeric_variable > 0.01 * 26_000
        assert type(big_donations) == NumericClause
        assert big_donations.table_name == "Donations"
        assert big_donations.variable_name == "Amount"
        assert big_donations.values == [">260.0"]
        assert big_donations.include is True
        assert big_donations.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            more_than_a_set = fake_numeric_variable > {15, 30, 40, 40}
        assert exc_info.value.args[0] == (
            "Must specify a single number when using inequality operators."
        )

    def test_ge(self, fake_numeric_variable):
        at_least_this_ratio = fake_numeric_variable >= Fraction(65432, 987)
        assert type(at_least_this_ratio) == NumericClause
        assert at_least_this_ratio.table_name == "Donations"
        assert at_least_this_ratio.variable_name == "Amount"
        assert at_least_this_ratio.values == [">=66.2938"]
        assert at_least_this_ratio.include is True
        assert at_least_this_ratio.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            number_gen = (n for n in "12.3 4.56 789".split())
            at_least_a_generator = fake_numeric_variable >= number_gen
        assert exc_info.value.args[0] == (
            "Must specify a single number when using inequality operators."
        )


class TestTextVariable:
    def test_eq(self, fake_text_variable_email):
        specific_donor = fake_text_variable_email == "donor@domain.com"
        assert type(specific_donor) == TextClause
        assert specific_donor.table_name == "Supporters"
        assert specific_donor.variable_name == "EmailAddress"
        assert specific_donor.values == ["donor@domain.com"]
        assert specific_donor.match_type == "Is"
        assert specific_donor.match_case is True
        assert specific_donor.include is True
        assert specific_donor.session == "CharityDataViewSession"

        donors_by_email = fake_text_variable_email == [
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
            donors_by_number = fake_text_variable_email == {34, 765, 2930}
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a text variable"
            " must be given as a string or an iterable of strings."
        )

    def test_ne(self, fake_text_variable_email):
        dont_want_this_person = fake_text_variable_email != "bad_donor@domain.com"
        assert type(dont_want_this_person) == TextClause
        assert dont_want_this_person.table_name == "Supporters"
        assert dont_want_this_person.variable_name == "EmailAddress"
        assert dont_want_this_person.values == ["bad_donor@domain.com"]
        assert dont_want_this_person.match_type == "Is"
        assert dont_want_this_person.match_case is True
        assert dont_want_this_person.include is False
        assert dont_want_this_person.session == "CharityDataViewSession"

        not_these_people = fake_text_variable_email != {
            "dont_email_me@domain.com",
            "unsubscribed@domain.org",
        }
        assert type(not_these_people) == TextClause
        assert not_these_people.table_name == "Supporters"
        assert not_these_people.variable_name == "EmailAddress"
        assert sorted(not_these_people.values) == [
            "dont_email_me@domain.com",
            "unsubscribed@domain.org",
        ]
        assert not_these_people.match_type == "Is"
        assert not_these_people.match_case is True
        assert not_these_people.include is False
        assert not_these_people.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            donor_not_an_obj = fake_text_variable_email != object()
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a text variable"
            " must be given as a string or an iterable of strings."
        )

    def test_le(self, fake_text_variable_surname):
        first_half_alphabet = fake_text_variable_surname <= "n"
        assert type(first_half_alphabet) == TextClause
        assert first_half_alphabet.table_name == "Supporters"
        assert first_half_alphabet.variable_name == "Surname"
        assert first_half_alphabet.values == ['<="n"']
        assert first_half_alphabet.match_type == "Ranges"
        assert first_half_alphabet.match_case is True
        assert first_half_alphabet.include is True
        assert first_half_alphabet.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            earlier_than_letters = fake_text_variable_surname <= list("abcedfgh")
        assert exc_info.value.args[0] == (
            "Must specify a single string when using inequality operators."
        )

    def test_ge(self, fake_text_variable_surname):
        smith_or_later = fake_text_variable_surname >= "Smith"
        assert type(smith_or_later) == TextClause
        assert smith_or_later.table_name == "Supporters"
        assert smith_or_later.variable_name == "Surname"
        assert smith_or_later.values == ['>="Smith"']
        assert smith_or_later.match_type == "Ranges"
        assert smith_or_later.match_case is True
        assert smith_or_later.include is True
        assert smith_or_later.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            later_than_tuple = fake_text_variable_surname >= ("A", "e", "i", "O")
        assert exc_info.value.args[0] == (
            "Must specify a single string when using inequality operators."
        )

    def test_equals(self, fake_text_variable_email):
        specific_donor = fake_text_variable_email.equals("donor@domain.com")
        assert type(specific_donor) == TextClause
        assert specific_donor.table_name == "Supporters"
        assert specific_donor.variable_name == "EmailAddress"
        assert specific_donor.values == ["donor@domain.com"]
        assert specific_donor.match_type == "Is"
        assert specific_donor.match_case is True
        assert specific_donor.include is True
        assert specific_donor.session == "CharityDataViewSession"

        donors_by_email = fake_text_variable_email.equals(
            [f"donor_{i}@domain.com" for i in range(4)]
        )
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
            donors_by_number = fake_text_variable_email.equals({34, 765, 2930})
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a text variable"
            " must be given as a string or an iterable of strings."
        )

        dont_want_this_person = fake_text_variable_email.equals(
            "bad_donor@domain.com", include=False
        )
        assert type(dont_want_this_person) == TextClause
        assert dont_want_this_person.table_name == "Supporters"
        assert dont_want_this_person.variable_name == "EmailAddress"
        assert dont_want_this_person.values == ["bad_donor@domain.com"]
        assert dont_want_this_person.match_type == "Is"
        assert dont_want_this_person.match_case is True
        assert dont_want_this_person.include is False
        assert dont_want_this_person.session == "CharityDataViewSession"

        not_these_people = fake_text_variable_email.equals(
            {"dont_email_me@domain.com", "unsubscribed@domain.org",}, include=False
        )
        assert type(not_these_people) == TextClause
        assert not_these_people.table_name == "Supporters"
        assert not_these_people.variable_name == "EmailAddress"
        assert sorted(not_these_people.values) == [
            "dont_email_me@domain.com",
            "unsubscribed@domain.org",
        ]
        assert not_these_people.match_type == "Is"
        assert not_these_people.match_case is True
        assert not_these_people.include is False
        assert not_these_people.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            donor_not_an_obj = fake_text_variable_email.equals(object(), include=False)
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a text variable"
            " must be given as a string or an iterable of strings."
        )

    def test_contains(self, fake_text_variable_surname):
        contains_nuts = fake_text_variable_surname.contains("nuts")
        assert type(contains_nuts) == TextClause
        assert contains_nuts.table_name == "Supporters"
        assert contains_nuts.variable_name == "Surname"
        assert contains_nuts.values == ["nuts"]
        assert contains_nuts.match_type == "Contains"
        assert contains_nuts.match_case is True
        assert contains_nuts.include is True
        assert contains_nuts.session == "CharityDataViewSession"

        contains_multiple = fake_text_variable_surname.contains(["a", "b"])
        assert type(contains_multiple) == TextClause
        assert contains_multiple.table_name == "Supporters"
        assert contains_multiple.variable_name == "Surname"
        assert contains_multiple.values == ["a", "b"]
        assert contains_multiple.match_type == "Contains"
        assert contains_multiple.match_case is True
        assert contains_multiple.include is True
        assert contains_multiple.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            contains_ints = fake_text_variable_surname.contains([1, 2, 3])
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a text variable"
            " must be given as a string or an iterable of strings."
        )

    def test_starts_with(self, fake_text_variable_surname):
        starts_with_smith = fake_text_variable_surname.startswith("Smith")
        assert type(starts_with_smith) == TextClause
        assert starts_with_smith.table_name == "Supporters"
        assert starts_with_smith.variable_name == "Surname"
        assert starts_with_smith.values == ["Smith"]
        assert starts_with_smith.match_type == "Begins"
        assert starts_with_smith.match_case is True
        assert starts_with_smith.include is True
        assert starts_with_smith.session == "CharityDataViewSession"

        starts_with_multiple = fake_text_variable_surname.startswith(["Tom", "James", "Dan", "Dav"])
        assert type(starts_with_multiple) == TextClause
        assert starts_with_multiple.table_name == "Supporters"
        assert starts_with_multiple.variable_name == "Surname"
        assert starts_with_multiple.values == ["Tom", "James", "Dan", "Dav"]
        assert starts_with_multiple.match_type == "Begins"
        assert starts_with_multiple.match_case is True
        assert starts_with_multiple.include is True
        assert starts_with_multiple.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            starts_with_boolean = fake_text_variable_surname.startswith(True)
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a text variable"
            " must be given as a string or an iterable of strings."
        )

    def test_ends_with(self, fake_text_variable_surname):
        ends_with_son = fake_text_variable_surname.endswith("son")
        assert type(ends_with_son) == TextClause
        assert ends_with_son.table_name == "Supporters"
        assert ends_with_son.variable_name == "Surname"
        assert ends_with_son.values == ["son"]
        assert ends_with_son.match_type == "Ends"
        assert ends_with_son.match_case is True
        assert ends_with_son.include is True
        assert ends_with_son.session == "CharityDataViewSession"

        ends_with_multiple = fake_text_variable_surname.endswith(["son", "ez"])
        assert type(ends_with_multiple) == TextClause
        assert ends_with_multiple.table_name == "Supporters"
        assert ends_with_multiple.variable_name == "Surname"
        assert ends_with_multiple.values == ["son", "ez"]
        assert ends_with_multiple.match_type == "Ends"
        assert ends_with_multiple.match_case is True
        assert ends_with_multiple.include is True
        assert ends_with_multiple.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            ends_with_float = fake_text_variable_surname.endswith([2.8, 9.4])
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a text variable"
            " must be given as a string or an iterable of strings."
        )

    def test_before(self, fake_text_variable_surname):
        first_half_alphabet = fake_text_variable_surname.before("n")
        assert type(first_half_alphabet) == TextClause
        assert first_half_alphabet.table_name == "Supporters"
        assert first_half_alphabet.variable_name == "Surname"
        assert first_half_alphabet.values == ['<="n"']
        assert first_half_alphabet.match_type == "Ranges"
        assert first_half_alphabet.match_case is True
        assert first_half_alphabet.include is True
        assert first_half_alphabet.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            earlier_than_letters = fake_text_variable_surname.before(list("abcedfgh"))
        assert exc_info.value.args[0] == (
            "Must specify a single string when using inequality operators."
        )

        with pytest.raises(ValueError) as exc_info:
            before_int = fake_text_variable_surname.before(6)
        assert exc_info.value.args[0] == (
            "Must specify a single string when using inequality operators."
        )

    def test_after(self, fake_text_variable_surname):
        smith_or_later = fake_text_variable_surname.after("Smith")
        assert type(smith_or_later) == TextClause
        assert smith_or_later.table_name == "Supporters"
        assert smith_or_later.variable_name == "Surname"
        assert smith_or_later.values == ['>="Smith"']
        assert smith_or_later.match_type == "Ranges"
        assert smith_or_later.match_case is True
        assert smith_or_later.include is True
        assert smith_or_later.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            later_than_tuple = fake_text_variable_surname.after(("A", "e", "i", "O"))
        assert exc_info.value.args[0] == (
            "Must specify a single string when using inequality operators."
        )

        with pytest.raises(ValueError) as exc_info:
            after_boolean = fake_text_variable_surname.after(False)
        assert exc_info.value.args[0] == (
            "Must specify a single string when using inequality operators."
        )

    def test_between(self, fake_text_variable_surname):
        rock_and_hardplace = fake_text_variable_surname.between("hardplace", "rock")
        assert type(rock_and_hardplace) == TextClause
        assert rock_and_hardplace.table_name == "Supporters"
        assert rock_and_hardplace.variable_name == "Surname"
        assert rock_and_hardplace.values == ['>="hardplace" - <="rock"']
        assert rock_and_hardplace.match_type == "Ranges"
        assert rock_and_hardplace.match_case is True
        assert rock_and_hardplace.include is True
        assert rock_and_hardplace.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            between_lists = fake_text_variable_surname.between(["a", "b"], ["y", "z"])
        assert exc_info.value.args[0] == (
            "Must specify a single string when using inequality operators."
        )

        with pytest.raises(ValueError) as exc_info:
            between_ints = fake_text_variable_surname.between(1, 100)
        assert exc_info.value.args[0] == (
            "Must specify a single string when using inequality operators."
        )

    def test_matches(self, fake_text_variable_email):
        gmail_donor = fake_text_variable_email.matches("*@gmail.com")
        assert type(gmail_donor) == TextClause
        assert gmail_donor.table_name == "Supporters"
        assert gmail_donor.variable_name == "EmailAddress"
        assert gmail_donor.values == ['="*@gmail.com"']
        assert gmail_donor.match_type == "Ranges"
        assert gmail_donor.match_case is True
        assert gmail_donor.include is True
        assert gmail_donor.session == "CharityDataViewSession"

        multiple_domain_donors = fake_text_variable_email.matches(
            ["*@gmail.com", "*@hotmail.com", "*@apteco.com"]
        )
        assert type(multiple_domain_donors) == TextClause
        assert multiple_domain_donors.table_name == "Supporters"
        assert multiple_domain_donors.variable_name == "EmailAddress"
        assert multiple_domain_donors.values == [
            '="*@gmail.com"',
            '="*@hotmail.com"',
            '="*@apteco.com"',
        ]
        assert multiple_domain_donors.match_type == "Ranges"
        assert multiple_domain_donors.match_case is True
        assert multiple_domain_donors.include is True
        assert multiple_domain_donors.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            matches_int = fake_text_variable_email.matches(30)
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a text variable"
            " must be given as a string or an iterable of strings."
        )


class TestArrayVariable:
    def test_eq(self, fake_array_variable):
        national_campaigns = fake_array_variable == "National"
        assert type(national_campaigns) == ArrayClause
        assert national_campaigns.table_name == "Campaigns"
        assert national_campaigns.variable_name == "Tags"
        assert national_campaigns.values == ["National"]
        assert national_campaigns.logic == "OR"
        assert national_campaigns.include is True
        assert national_campaigns.session == "CharityDataViewSession"

        autumn_campaigns = fake_array_variable == {
            "Autumn",
            "Fall",
            "Sep",
            "Oct",
            "Nov",
            "Halloween",
            "Back-to-School",
        }
        assert type(autumn_campaigns) == ArrayClause
        assert autumn_campaigns.table_name == "Campaigns"
        assert autumn_campaigns.variable_name == "Tags"
        assert sorted(autumn_campaigns.values) == [
            "Autumn",
            "Back-to-School",
            "Fall",
            "Halloween",
            "Nov",
            "Oct",
            "Sep",
        ]
        assert autumn_campaigns.logic == "OR"
        assert autumn_campaigns.include is True
        assert autumn_campaigns.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            forgot_string_quotes = fake_array_variable == ["4", 6]
        assert exc_info.value.args[0] == (
            "Chosen value(s) for an array variable"
            " must be given as a string or an iterable of strings."
        )

    def test_ne(self, fake_array_variable):
        not_christmas = fake_array_variable != "Christmas"
        assert type(not_christmas) == ArrayClause
        assert not_christmas.table_name == "Campaigns"
        assert not_christmas.variable_name == "Tags"
        assert not_christmas.values == ["Christmas"]
        assert not_christmas.logic == "OR"
        assert not_christmas.include is False
        assert not_christmas.session == "CharityDataViewSession"

        one_off_campaigns = fake_array_variable != [
            "Recurrent",
            "Annual",
            "Regular",
            "Monthly",
            "Weekly",
            "Daily",
            "Seasonal",
        ]
        assert type(one_off_campaigns) == ArrayClause
        assert one_off_campaigns.table_name == "Campaigns"
        assert one_off_campaigns.variable_name == "Tags"
        assert one_off_campaigns.values == [
            "Recurrent",
            "Annual",
            "Regular",
            "Monthly",
            "Weekly",
            "Daily",
            "Seasonal",
        ]
        assert one_off_campaigns.logic == "OR"
        assert one_off_campaigns.include is False
        assert one_off_campaigns.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            undesired_values = ("value_we_dont_like", None)
            not_none = fake_array_variable != undesired_values
        assert exc_info.value.args[0] == (
            "Chosen value(s) for an array variable"
            " must be given as a string or an iterable of strings."
        )


class TestFlagArrayVariable:
    def test_eq(self, fake_flag_array_variable):
        can_post = fake_flag_array_variable == "DirectMail"
        assert type(can_post) == FlagArrayClause
        assert can_post.table_name == "Supporters"
        assert can_post.variable_name == "ContactPreferences"
        assert can_post.values == ["DirectMail"]
        assert can_post.logic == "OR"
        assert can_post.include is True
        assert can_post.session == "CharityDataViewSession"

        phone_or_text = fake_flag_array_variable == ("SMS", "Telephone")
        assert type(phone_or_text) == FlagArrayClause
        assert phone_or_text.table_name == "Supporters"
        assert phone_or_text.variable_name == "ContactPreferences"
        assert phone_or_text.values == ["SMS", "Telephone"]
        assert phone_or_text.logic == "OR"
        assert phone_or_text.include is True
        assert phone_or_text.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            true = True  # so editor doesn't complain about comparison not using `is`
            contactable = fake_flag_array_variable == true
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a flag array variable"
            " must be given as a string or an iterable of strings."
        )

    def test_ne(self, fake_flag_array_variable):
        cant_email = fake_flag_array_variable != "Email"
        assert type(cant_email) == FlagArrayClause
        assert cant_email.table_name == "Supporters"
        assert cant_email.variable_name == "ContactPreferences"
        assert cant_email.values == ["Email"]
        assert cant_email.logic == "OR"
        assert cant_email.include is False
        assert cant_email.session == "CharityDataViewSession"

        not_business = fake_flag_array_variable != {
            "BusinessPhone",
            "BusinessDirectMail",
            "BusinessEmail",
        }
        assert type(not_business) == FlagArrayClause
        assert not_business.table_name == "Supporters"
        assert not_business.variable_name == "ContactPreferences"
        assert sorted(not_business.values) == [
            "BusinessDirectMail",
            "BusinessEmail",
            "BusinessPhone",
        ]
        assert not_business.logic == "OR"
        assert not_business.include is False
        assert not_business.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            contactable = fake_flag_array_variable != 0
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a flag array variable"
            " must be given as a string or an iterable of strings."
        )


class TestDateVariable:
    def test_eq(self, fake_date_variable):
        august_bank_holiday_2018 = fake_date_variable == date(2018, 8, 27)
        assert type(august_bank_holiday_2018) == DateListClause
        assert august_bank_holiday_2018.table_name == "Donations"
        assert august_bank_holiday_2018.variable_name == "DonationDate"
        assert august_bank_holiday_2018.values == ["20180827"]
        assert august_bank_holiday_2018.include is True
        assert august_bank_holiday_2018.session == "CharityDataViewSession"

        festive_days_from_random_years = fake_date_variable == [
            date(1912, 12, 25),
            date(1934, 2, 14),
            date(1956, 4, 1),
            date(1978, 10, 31),
            date(1990, 11, 5),
            date(2011, 4, 29),
            date(2023, 9, 23),
        ]
        assert type(festive_days_from_random_years) == DateListClause
        assert festive_days_from_random_years.table_name == "Donations"
        assert festive_days_from_random_years.variable_name == "DonationDate"
        assert festive_days_from_random_years.values == [
            "19121225",
            "19340214",
            "19560401",
            "19781031",
            "19901105",
            "20110429",
            "20230923",
        ]
        assert festive_days_from_random_years.include is True
        assert festive_days_from_random_years.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            trying_with_date_string = fake_date_variable == "20180528"
        assert exc_info.value.args[0] == (
            "Chosen value for a date variable"
            " must be a date object or an iterable of date objects."
        )

    def test_ne(self, fake_date_variable):
        not_easter_2050 = fake_date_variable != date(2050, 4, 10)
        assert type(not_easter_2050) == DateListClause
        assert not_easter_2050.table_name == "Donations"
        assert not_easter_2050.variable_name == "DonationDate"
        assert not_easter_2050.values == ["20500410"]
        assert not_easter_2050.include is False
        assert not_easter_2050.session == "CharityDataViewSession"

        exclude_solstices_and_equinoxes_2030 = fake_date_variable != [
            date(2030, 3, 20),
            datetime(2030, 6, 21, 7, 31),
            date(2030, 9, 22),
            datetime(2030, 12, 21, 20, 9),
        ]
        assert type(exclude_solstices_and_equinoxes_2030) == DateListClause
        assert exclude_solstices_and_equinoxes_2030.table_name == "Donations"
        assert exclude_solstices_and_equinoxes_2030.variable_name == "DonationDate"
        assert exclude_solstices_and_equinoxes_2030.values == [
            "20300320",
            "20300621",
            "20300922",
            "20301221",
        ]
        assert exclude_solstices_and_equinoxes_2030.include is False
        assert exclude_solstices_and_equinoxes_2030.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            trying_with_list_some_invalid = fake_date_variable == [
                date(2012, 7, 27),
                "20221121",
                datetime(2018, 2, 9, 11, 0, 0),
            ]
        assert exc_info.value.args[0] == (
            "Chosen value for a date variable"
            " must be a date object or an iterable of date objects."
        )

    def test_le(self, fake_date_variable):
        before_tax_year_end_2018_19 = fake_date_variable <= date(2019, 4, 5)
        assert type(before_tax_year_end_2018_19) == DateRangeClause
        assert before_tax_year_end_2018_19.table_name == "Donations"
        assert before_tax_year_end_2018_19.variable_name == "DonationDate"
        assert before_tax_year_end_2018_19.start == "Earliest"
        assert before_tax_year_end_2018_19.end == "2019-04-05"
        assert before_tax_year_end_2018_19.include is True
        assert before_tax_year_end_2018_19.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            two_dates = (date(2019, 2, 14), date(2019, 6, 21))
            less_than_equal_a_pair = fake_date_variable <= two_dates
        assert exc_info.value.args[0] == (
            "Must specify a single date when using inequality operators."
        )

    def test_ge(self, fake_date_variable):
        after_christmas_2015 = fake_date_variable >= date(2015, 12, 25)
        assert type(after_christmas_2015) == DateRangeClause
        assert after_christmas_2015.table_name == "Donations"
        assert after_christmas_2015.variable_name == "DonationDate"
        assert after_christmas_2015.start == "2015-12-25"
        assert after_christmas_2015.end == "Latest"
        assert after_christmas_2015.include is True
        assert after_christmas_2015.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            trying_with_a_string = fake_date_variable >= "2011-11-20"
        assert exc_info.value.args[0] == (
            "Must specify a single date when using inequality operators."
        )


class TestDateTimeVariable:
    def test_le(self, fake_datetime_variable):
        xmas_campaign_launch = datetime(2019, 11, 25, 11, 22, 33)
        before_christmas_campaign = fake_datetime_variable <= xmas_campaign_launch
        assert type(before_christmas_campaign) == DateTimeRangeClause
        assert before_christmas_campaign.table_name == "WebVisits"
        assert before_christmas_campaign.variable_name == "BrowsingSessionStart"
        assert before_christmas_campaign.start == "Earliest"
        assert before_christmas_campaign.end == "2019-11-25T11:22:33"
        assert before_christmas_campaign.include is True
        assert before_christmas_campaign.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            trying_with_date_only = fake_datetime_variable <= date(2019, 11, 25)
        assert exc_info.value.args[0] == (
            "Must specify a single datetime when using inequality operators."
        )

    def test_ge(self, fake_datetime_variable):
        sale_start = datetime(2019, 12, 26, 4, 32, 10)
        after_boxing_day_sale_start = fake_datetime_variable >= sale_start
        assert type(after_boxing_day_sale_start) == DateTimeRangeClause
        assert after_boxing_day_sale_start.table_name == "WebVisits"
        assert after_boxing_day_sale_start.variable_name == "BrowsingSessionStart"
        assert after_boxing_day_sale_start.start == "2019-12-26T04:32:10"
        assert after_boxing_day_sale_start.end == "Latest"
        assert after_boxing_day_sale_start.include is True
        assert after_boxing_day_sale_start.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            trying_with_number = fake_datetime_variable >= 2019122643210
        assert exc_info.value.args[0] == (
            "Must specify a single datetime when using inequality operators."
        )


@pytest.mark.xfail(reason="Not yet implemented.")
class TestReferenceVariable:
    def test_eq(self, fake_reference_variable):
        abc_campaign = fake_reference_variable == "abc"
        assert type(abc_campaign) == ReferenceClause
        assert abc_campaign.table_name == "Campaigns"
        assert abc_campaign.variable_name == "CampaignID"
        assert abc_campaign.values == ["abc"]
        assert abc_campaign.include is True
        assert abc_campaign.session == "CharityDataViewSession"

    def test_ne(self, fake_reference_variable):
        not_x_campaigns = fake_reference_variable != ["x", "xy", "xs", "xyz", "x1"]
        assert type(not_x_campaigns) == ReferenceClause
        assert not_x_campaigns.table_name == "Campaigns"
        assert not_x_campaigns.variable_name == "CampaignID"
        assert not_x_campaigns.values == ["x", "xy", "xs", "xyz", "x1"]
        assert not_x_campaigns.include is False
        assert not_x_campaigns.session == "CharityDataViewSession"
