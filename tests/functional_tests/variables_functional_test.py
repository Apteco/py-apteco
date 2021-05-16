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
    def test_eq(self, chy_selector_var, chy_session):
        high_value_supporters = chy_selector_var == ("Gold", "Platinum")
        assert type(high_value_supporters) == SelectorClause
        assert high_value_supporters.table_name == "Supporters"
        assert high_value_supporters.variable_name == "suMember"
        assert high_value_supporters.values == ["Gold", "Platinum"]
        assert high_value_supporters.include is True
        assert high_value_supporters.session is chy_session

        bronze_supporters = chy_selector_var == "Bronze"
        assert type(bronze_supporters) == SelectorClause
        assert bronze_supporters.table_name == "Supporters"
        assert bronze_supporters.variable_name == "suMember"
        assert bronze_supporters.values == ["Bronze"]
        assert bronze_supporters.include is True
        assert bronze_supporters.session is chy_session

        with pytest.raises(ValueError) as exc_info:
            trying_with_a_number = chy_selector_var == 3
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a selector variable"
            " must be given as a string or an iterable of strings."
        )

    def test_ne(self, chy_selector_var, chy_session):
        higher_value_supporters = chy_selector_var != ("Bronze", "Silver")
        assert type(higher_value_supporters) == SelectorClause
        assert higher_value_supporters.table_name == "Supporters"
        assert higher_value_supporters.variable_name == "suMember"
        assert higher_value_supporters.values == ["Bronze", "Silver"]
        assert higher_value_supporters.include is False
        assert higher_value_supporters.session is chy_session

        not_platinum = chy_selector_var != "Platinum"
        assert type(not_platinum) == SelectorClause
        assert not_platinum.table_name == "Supporters"
        assert not_platinum.variable_name == "suMember"
        assert not_platinum.values == ["Platinum"]
        assert not_platinum.include is False
        assert not_platinum.session is chy_session

        with pytest.raises(ValueError) as exc_info:
            trying_with_a_float = chy_selector_var != 2.5
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a selector variable"
            " must be given as a string or an iterable of strings."
        )


@pytest.mark.xfail(reason="Not yet implemented.")
class TestCombinedCategoriesVariable:
    # TODO: update when implemented
    def test_eq(self, chy_combined_categories_var, chy_session):
        northern_supporters = chy_combined_categories_var == ["NE", "NW", "YRK"]
        assert type(northern_supporters) == CombinedCategoriesClause
        assert northern_supporters.table_name == "Supporters"
        assert northern_supporters.variable_name == "suRegion"
        assert northern_supporters.values == ["NE", "NW", "YRK"]
        assert northern_supporters.include is True
        assert northern_supporters.session is chy_session

    # TODO: update when implemented
    def test_ne(self, chy_combined_categories_var, chy_session):
        supporters_outside_london = chy_combined_categories_var != "LDN"
        assert type(supporters_outside_london) == CombinedCategoriesClause
        assert supporters_outside_london.table_name == "Supporters"
        assert supporters_outside_london.variable_name == "suRegion"
        assert supporters_outside_london.values == ["LDN"]
        assert supporters_outside_london.include is False
        assert supporters_outside_london.session is chy_session


class TestNumericVariable:
    def test_eq(self, chy_numeric_var_amount, chy_session):
        donations_100 = chy_numeric_var_amount == 100
        assert type(donations_100) == NumericClause
        assert donations_100.table_name == "Donations"
        assert donations_100.variable_name == "doAmount"
        assert donations_100.values == ["100"]
        assert donations_100.include is True
        assert donations_100.session is chy_session

        hundreds_donations = chy_numeric_var_amount == (i * 100 for i in range(1, 10))
        assert type(hundreds_donations) == NumericClause
        assert hundreds_donations.table_name == "Donations"
        assert hundreds_donations.variable_name == "doAmount"
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
        assert hundreds_donations.session is chy_session

        with pytest.raises(ValueError) as exc_info:
            trying_with_a_string = chy_numeric_var_amount == "256"
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a numeric variable"
            " must be given as a number or an iterable of numbers."
        )

    def test_ne(self, chy_numeric_var_amount, chy_session):
        not_this = chy_numeric_var_amount != 72.1896
        assert type(not_this) == NumericClause
        assert not_this.table_name == "Donations"
        assert not_this.variable_name == "doAmount"
        assert not_this.values == ["72.1896"]
        assert not_this.include is False
        assert not_this.session is chy_session

        not_one_of_these = chy_numeric_var_amount != (17.5, 8192)
        assert type(not_one_of_these) == NumericClause
        assert not_one_of_these.table_name == "Donations"
        assert not_one_of_these.variable_name == "doAmount"
        assert not_one_of_these.values == ["17.5", "8192"]
        assert not_one_of_these.include is False
        assert not_one_of_these.session is chy_session

        with pytest.raises(ValueError) as exc_info:
            trying_with_a_boolean = chy_numeric_var_amount != False
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a numeric variable"
            " must be given as a number or an iterable of numbers."
        )

    def test_lt(self, chy_numeric_var_amount, chy_session):
        small_donations = chy_numeric_var_amount < Decimal("10.00")
        assert type(small_donations) == NumericClause
        assert small_donations.table_name == "Donations"
        assert small_donations.variable_name == "doAmount"
        assert small_donations.values == ["<10.0000"]
        assert small_donations.include is True
        assert small_donations.session is chy_session

        with pytest.raises(ValueError) as exc_info:
            less_than_a_list = chy_numeric_var_amount < [512.64, 646.464_646]
        assert exc_info.value.args[0] == (
            "Must specify a single number for this type of operation."
        )

    def test_le(self, chy_numeric_var_amount, chy_session):
        up_to_including_10k = chy_numeric_var_amount <= 10000
        assert type(up_to_including_10k) == NumericClause
        assert up_to_including_10k.table_name == "Donations"
        assert up_to_including_10k.variable_name == "doAmount"
        assert up_to_including_10k.values == ["<=10000"]
        assert up_to_including_10k.include is True
        assert up_to_including_10k.session is chy_session

        with pytest.raises(ValueError) as exc_info:
            less_than_equal_tuple = chy_numeric_var_amount <= (52, 27, 9.75)
        assert exc_info.value.args[0] == (
            "Must specify a single number for this type of operation."
        )

    def test_gt(self, chy_numeric_var_amount, chy_session):
        big_donations = chy_numeric_var_amount > 0.01 * 26000
        assert type(big_donations) == NumericClause
        assert big_donations.table_name == "Donations"
        assert big_donations.variable_name == "doAmount"
        assert big_donations.values == [">260.0"]
        assert big_donations.include is True
        assert big_donations.session is chy_session

        with pytest.raises(ValueError) as exc_info:
            more_than_a_set = chy_numeric_var_amount > {15, 30, 40, 40}
        assert exc_info.value.args[0] == (
            "Must specify a single number for this type of operation."
        )

    def test_ge(self, chy_numeric_var_amount, chy_session):
        at_least_this_ratio = chy_numeric_var_amount >= Fraction(65432, 987)
        assert type(at_least_this_ratio) == NumericClause
        assert at_least_this_ratio.table_name == "Donations"
        assert at_least_this_ratio.variable_name == "doAmount"
        assert at_least_this_ratio.values == [">=66.2938"]
        assert at_least_this_ratio.include is True
        assert at_least_this_ratio.session is chy_session

        with pytest.raises(ValueError) as exc_info:
            number_gen = (n for n in "12.3 4.56 789".split())
            at_least_a_generator = chy_numeric_var_amount >= number_gen
        assert exc_info.value.args[0] == (
            "Must specify a single number for this type of operation."
        )


class TestTextVariable:
    def test_eq(self, chy_text_var_email, chy_session):
        specific_donor = chy_text_var_email == "donor@domain.com"
        assert type(specific_donor) == TextClause
        assert specific_donor.table_name == "Supporters"
        assert specific_donor.variable_name == "suEmail"
        assert specific_donor.values == ["donor@domain.com"]
        assert specific_donor.match_type == "Is"
        assert specific_donor.match_case is True
        assert specific_donor.include is True
        assert specific_donor.session is chy_session

        donors_by_email = chy_text_var_email == [
            f"donor_{i}@domain.com" for i in range(4)
        ]
        assert type(donors_by_email) == TextClause
        assert donors_by_email.table_name == "Supporters"
        assert donors_by_email.variable_name == "suEmail"
        assert donors_by_email.values == [
            "donor_0@domain.com",
            "donor_1@domain.com",
            "donor_2@domain.com",
            "donor_3@domain.com",
        ]
        assert donors_by_email.match_type == "Is"
        assert donors_by_email.match_case is True
        assert donors_by_email.include is True
        assert donors_by_email.session is chy_session

        with pytest.raises(ValueError) as exc_info:
            donors_by_number = chy_text_var_email == {34, 765, 2930}
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a text variable"
            " must be given as a string or an iterable of strings."
        )

    def test_ne(self, chy_text_var_email, chy_session):
        dont_want_this_person = chy_text_var_email != "bad_donor@domain.com"
        assert type(dont_want_this_person) == TextClause
        assert dont_want_this_person.table_name == "Supporters"
        assert dont_want_this_person.variable_name == "suEmail"
        assert dont_want_this_person.values == ["bad_donor@domain.com"]
        assert dont_want_this_person.match_type == "Is"
        assert dont_want_this_person.match_case is True
        assert dont_want_this_person.include is False
        assert dont_want_this_person.session is chy_session

        not_these_people = chy_text_var_email != {
            "dont_email_me@domain.com",
            "unsubscribed@domain.org",
        }
        assert type(not_these_people) == TextClause
        assert not_these_people.table_name == "Supporters"
        assert not_these_people.variable_name == "suEmail"
        assert sorted(not_these_people.values) == [
            "dont_email_me@domain.com",
            "unsubscribed@domain.org",
        ]
        assert not_these_people.match_type == "Is"
        assert not_these_people.match_case is True
        assert not_these_people.include is False
        assert not_these_people.session is chy_session

        with pytest.raises(ValueError) as exc_info:
            donor_not_an_obj = chy_text_var_email != object()
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a text variable"
            " must be given as a string or an iterable of strings."
        )

    def test_lt(self, chy_text_var_surname, chy_session):
        before_breakfast = chy_text_var_surname < "breakfast"
        assert type(before_breakfast) == TextClause
        assert before_breakfast.table_name == "Supporters"
        assert before_breakfast.variable_name == "suSrName"
        assert before_breakfast.values == ['<"breakfast"']
        assert before_breakfast.match_type == "Ranges"
        assert before_breakfast.match_case is False
        assert before_breakfast.include is True
        assert before_breakfast.session is chy_session

        with pytest.raises(ValueError) as exc_info:
            less_than_a_zero = chy_text_var_surname < 0
        assert exc_info.value.args[0] == (
            "Must specify a single string for this type of operation."
        )

    def test_le(self, chy_text_var_surname, chy_session):
        first_half_alphabet = chy_text_var_surname <= "n"
        assert type(first_half_alphabet) == TextClause
        assert first_half_alphabet.table_name == "Supporters"
        assert first_half_alphabet.variable_name == "suSrName"
        assert first_half_alphabet.values == ['<="n"']
        assert first_half_alphabet.match_type == "Ranges"
        assert first_half_alphabet.match_case is False
        assert first_half_alphabet.include is True
        assert first_half_alphabet.session is chy_session

        with pytest.raises(ValueError) as exc_info:
            earlier_than_letters = chy_text_var_surname <= list("abcedfgh")
        assert exc_info.value.args[0] == (
            "Must specify a single string for this type of operation."
        )

    def test_gt(self, chy_text_var_surname, chy_session):
        after_tea = chy_text_var_surname > "Tea"
        assert type(after_tea) == TextClause
        assert after_tea.table_name == "Supporters"
        assert after_tea.variable_name == "suSrName"
        assert after_tea.values == ['>"Tea"']
        assert after_tea.match_type == "Ranges"
        assert after_tea.match_case is False
        assert after_tea.include is True
        assert after_tea.session is chy_session

        with pytest.raises(ValueError) as exc_info:
            more_than_a_date = chy_text_var_surname > date(2020, 10, 5)
        assert exc_info.value.args[0] == (
            "Must specify a single string for this type of operation."
        )

    def test_ge(self, chy_text_var_surname, chy_session):
        smith_or_later = chy_text_var_surname >= "Smith"
        assert type(smith_or_later) == TextClause
        assert smith_or_later.table_name == "Supporters"
        assert smith_or_later.variable_name == "suSrName"
        assert smith_or_later.values == ['>="Smith"']
        assert smith_or_later.match_type == "Ranges"
        assert smith_or_later.match_case is False
        assert smith_or_later.include is True
        assert smith_or_later.session is chy_session

        with pytest.raises(ValueError) as exc_info:
            later_than_tuple = chy_text_var_surname >= ("A", "e", "i", "O")
        assert exc_info.value.args[0] == (
            "Must specify a single string for this type of operation."
        )


class TestArrayVariable:
    def test_eq(self, chy_array_var, chy_session):
        national_campaigns = chy_array_var == "National"
        assert type(national_campaigns) == ArrayClause
        assert national_campaigns.table_name == "Campaigns"
        assert national_campaigns.variable_name == "caTags"
        assert national_campaigns.values == ["National"]
        assert national_campaigns.logic == "OR"
        assert national_campaigns.include is True
        assert national_campaigns.session is chy_session

        autumn_campaigns = chy_array_var == {
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
        assert autumn_campaigns.variable_name == "caTags"
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
        assert autumn_campaigns.session is chy_session

        with pytest.raises(ValueError) as exc_info:
            forgot_string_quotes = chy_array_var == ["4", 6]
        assert exc_info.value.args[0] == (
            "Chosen value(s) for an array variable"
            " must be given as a string or an iterable of strings."
        )

    def test_ne(self, chy_array_var, chy_session):
        not_christmas = chy_array_var != "Christmas"
        assert type(not_christmas) == ArrayClause
        assert not_christmas.table_name == "Campaigns"
        assert not_christmas.variable_name == "caTags"
        assert not_christmas.values == ["Christmas"]
        assert not_christmas.logic == "OR"
        assert not_christmas.include is False
        assert not_christmas.session is chy_session

        one_off_campaigns = chy_array_var != [
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
        assert one_off_campaigns.variable_name == "caTags"
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
        assert one_off_campaigns.session is chy_session

        with pytest.raises(ValueError) as exc_info:
            undesired_values = ("value_we_dont_like", None)
            not_none = chy_array_var != undesired_values
        assert exc_info.value.args[0] == (
            "Chosen value(s) for an array variable"
            " must be given as a string or an iterable of strings."
        )


class TestFlagArrayVariable:
    def test_eq(self, chy_flag_array_var, chy_session):
        can_post = chy_flag_array_var == "DirectMail"
        assert type(can_post) == FlagArrayClause
        assert can_post.table_name == "Supporters"
        assert can_post.variable_name == "suCtcPrf"
        assert can_post.values == ["DirectMail"]
        assert can_post.logic == "OR"
        assert can_post.include is True
        assert can_post.session is chy_session

        phone_or_text = chy_flag_array_var == ("SMS", "Telephone")
        assert type(phone_or_text) == FlagArrayClause
        assert phone_or_text.table_name == "Supporters"
        assert phone_or_text.variable_name == "suCtcPrf"
        assert phone_or_text.values == ["SMS", "Telephone"]
        assert phone_or_text.logic == "OR"
        assert phone_or_text.include is True
        assert phone_or_text.session is chy_session

        with pytest.raises(ValueError) as exc_info:
            true = True  # so editor doesn't complain about comparison not using `is`
            contactable = chy_flag_array_var == true
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a flag array variable"
            " must be given as a string or an iterable of strings."
        )

    def test_ne(self, chy_flag_array_var, chy_session):
        cant_email = chy_flag_array_var != "Email"
        assert type(cant_email) == FlagArrayClause
        assert cant_email.table_name == "Supporters"
        assert cant_email.variable_name == "suCtcPrf"
        assert cant_email.values == ["Email"]
        assert cant_email.logic == "OR"
        assert cant_email.include is False
        assert cant_email.session is chy_session

        not_business = chy_flag_array_var != {
            "BusinessPhone",
            "BusinessDirectMail",
            "BusinessEmail",
        }
        assert type(not_business) == FlagArrayClause
        assert not_business.table_name == "Supporters"
        assert not_business.variable_name == "suCtcPrf"
        assert sorted(not_business.values) == [
            "BusinessDirectMail",
            "BusinessEmail",
            "BusinessPhone",
        ]
        assert not_business.logic == "OR"
        assert not_business.include is False
        assert not_business.session is chy_session

        with pytest.raises(ValueError) as exc_info:
            contactable = chy_flag_array_var != 0
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a flag array variable"
            " must be given as a string or an iterable of strings."
        )


class TestDateVariable:
    def test_eq(self, chy_date_var, chy_session):
        august_bank_holiday_2018 = chy_date_var == date(2018, 8, 27)
        assert type(august_bank_holiday_2018) == DateListClause
        assert august_bank_holiday_2018.table_name == "Donations"
        assert august_bank_holiday_2018.variable_name == "doDate"
        assert august_bank_holiday_2018.values == ["20180827"]
        assert august_bank_holiday_2018.include is True
        assert august_bank_holiday_2018.session is chy_session

        festive_days_from_random_years = chy_date_var == [
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
        assert festive_days_from_random_years.variable_name == "doDate"
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
        assert festive_days_from_random_years.session is chy_session

        with pytest.raises(ValueError) as exc_info:
            trying_with_date_string = chy_date_var == "20180528"
        assert exc_info.value.args[0] == (
            "Chosen value for a date variable"
            " must be a date object or an iterable of date objects."
        )

    def test_ne(self, chy_date_var, chy_session):
        not_easter_2050 = chy_date_var != date(2050, 4, 10)
        assert type(not_easter_2050) == DateListClause
        assert not_easter_2050.table_name == "Donations"
        assert not_easter_2050.variable_name == "doDate"
        assert not_easter_2050.values == ["20500410"]
        assert not_easter_2050.include is False
        assert not_easter_2050.session is chy_session

        exclude_solstices_and_equinoxes_2030 = chy_date_var != [
            date(2030, 3, 20),
            datetime(2030, 6, 21, 7, 31),
            date(2030, 9, 22),
            datetime(2030, 12, 21, 20, 9),
        ]
        assert type(exclude_solstices_and_equinoxes_2030) == DateListClause
        assert exclude_solstices_and_equinoxes_2030.table_name == "Donations"
        assert exclude_solstices_and_equinoxes_2030.variable_name == "doDate"
        assert exclude_solstices_and_equinoxes_2030.values == [
            "20300320",
            "20300621",
            "20300922",
            "20301221",
        ]
        assert exclude_solstices_and_equinoxes_2030.include is False
        assert exclude_solstices_and_equinoxes_2030.session is chy_session

        with pytest.raises(ValueError) as exc_info:
            trying_with_list_some_invalid = chy_date_var == [
                date(2012, 7, 27),
                "20221121",
                datetime(2018, 2, 9, 11, 0, 0),
            ]
        assert exc_info.value.args[0] == (
            "Chosen value for a date variable"
            " must be a date object or an iterable of date objects."
        )

    def test_le(self, chy_date_var, chy_session):
        before_tax_year_end_2018_19 = chy_date_var <= date(2019, 4, 5)
        assert type(before_tax_year_end_2018_19) == DateRangeClause
        assert before_tax_year_end_2018_19.table_name == "Donations"
        assert before_tax_year_end_2018_19.variable_name == "doDate"
        assert before_tax_year_end_2018_19.start == "Earliest"
        assert before_tax_year_end_2018_19.end == "2019-04-05"
        assert before_tax_year_end_2018_19.include is True
        assert before_tax_year_end_2018_19.session is chy_session

        with pytest.raises(ValueError) as exc_info:
            two_dates = (date(2019, 2, 14), date(2019, 6, 21))
            less_than_equal_a_pair = chy_date_var <= two_dates
        assert exc_info.value.args[0] == (
            "Must specify a single date for this type of operation."
        )

    def test_ge(self, chy_date_var, chy_session):
        after_christmas_2015 = chy_date_var >= date(2015, 12, 25)
        assert type(after_christmas_2015) == DateRangeClause
        assert after_christmas_2015.table_name == "Donations"
        assert after_christmas_2015.variable_name == "doDate"
        assert after_christmas_2015.start == "2015-12-25"
        assert after_christmas_2015.end == "Latest"
        assert after_christmas_2015.include is True
        assert after_christmas_2015.session is chy_session

        with pytest.raises(ValueError) as exc_info:
            trying_with_a_string = chy_date_var >= "2011-11-20"
        assert exc_info.value.args[0] == (
            "Must specify a single date for this type of operation."
        )


class TestDateTimeVariable:
    def test_le(self, chy_datetime_var, chy_session):
        xmas_campaign_launch = datetime(2019, 11, 25, 11, 22, 33)
        before_christmas_campaign = chy_datetime_var <= xmas_campaign_launch
        assert type(before_christmas_campaign) == DateTimeRangeClause
        assert before_christmas_campaign.table_name == "WebsiteVisits"
        assert before_christmas_campaign.variable_name == "weSessSt"
        assert before_christmas_campaign.start == "Earliest"
        assert before_christmas_campaign.end == "2019-11-25T11:22:33"
        assert before_christmas_campaign.include is True
        assert before_christmas_campaign.session is chy_session

        with pytest.raises(ValueError) as exc_info:
            trying_with_date_only = chy_datetime_var <= date(2019, 11, 25)
        assert exc_info.value.args[0] == (
            "Must specify a single datetime for this type of operation."
        )

    def test_ge(self, chy_datetime_var, chy_session):
        sale_start = datetime(2019, 12, 26, 4, 32, 10)
        after_boxing_day_sale_start = chy_datetime_var >= sale_start
        assert type(after_boxing_day_sale_start) == DateTimeRangeClause
        assert after_boxing_day_sale_start.table_name == "WebsiteVisits"
        assert after_boxing_day_sale_start.variable_name == "weSessSt"
        assert after_boxing_day_sale_start.start == "2019-12-26T04:32:10"
        assert after_boxing_day_sale_start.end == "Latest"
        assert after_boxing_day_sale_start.include is True
        assert after_boxing_day_sale_start.session is chy_session

        with pytest.raises(ValueError) as exc_info:
            trying_with_number = chy_datetime_var >= 2_019_122_643_210
        assert exc_info.value.args[0] == (
            "Must specify a single datetime for this type of operation."
        )


@pytest.mark.xfail(reason="Not yet implemented.")
class TestReferenceVariable:
    def test_eq(self, chy_reference_var, chy_session):
        abc_campaign = chy_reference_var == "abc"
        assert type(abc_campaign) == ReferenceClause
        assert abc_campaign.table_name == "Campaigns"
        assert abc_campaign.variable_name == "caID"
        assert abc_campaign.values == ["abc"]
        assert abc_campaign.include is True
        assert abc_campaign.session is chy_session

    def test_ne(self, chy_reference_var, chy_session):
        not_x_campaigns = chy_reference_var != ["x", "xy", "xs", "xyz", "x1"]
        assert type(not_x_campaigns) == ReferenceClause
        assert not_x_campaigns.table_name == "Campaigns"
        assert not_x_campaigns.variable_name == "caID"
        assert not_x_campaigns.values == ["x", "xy", "xs", "xyz", "x1"]
        assert not_x_campaigns.include is False
        assert not_x_campaigns.session is chy_session
