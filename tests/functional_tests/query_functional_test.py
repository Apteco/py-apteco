from datetime import date

import pytest

from apteco.query import (
    SelectorClause,
    NumericClause,
    TextClause,
    ArrayClause,
    FlagArrayClause,
    DateListClause,
)
from apteco.session import (
    SelectorVariable,
    NumericVariable,
    TextVariable,
    ArrayVariable,
    FlagArrayVariable,
    DateVariable,
    DateTimeVariable,
)


@pytest.fixture()
def fake_selector_variable():
    sv_example = SelectorVariable.__new__(SelectorVariable)
    sv_example.type = "Selector"
    sv_example.table_name = "Supporters"
    sv_example.name = "Membership"
    sv_example.session = "CharityDataViewSession"
    return sv_example


@pytest.fixture()
def fake_numeric_variable():
    nv_example = NumericVariable.__new__(NumericVariable)
    nv_example.type = "Numeric"
    nv_example.table_name = "Donations"
    nv_example.name = "Amount"
    nv_example.session = "CharityDataViewSession"
    return nv_example


@pytest.fixture()
def fake_email_text_variable():
    tv_example = TextVariable.__new__(TextVariable)
    tv_example.type = "Text"
    tv_example.table_name = "Supporters"
    tv_example.name = "EmailAddress"
    tv_example.session = "CharityDataViewSession"
    return tv_example


@pytest.fixture()
def fake_array_variable():
    av_example = ArrayVariable.__new__(ArrayVariable)
    av_example.type = "Array"
    av_example.table_name = "Campaigns"
    av_example.name = "Tags"
    av_example.session = "CharityDataViewSession"
    return av_example


@pytest.fixture()
def fake_flag_array_variable():
    fav_example = FlagArrayVariable.__new__(FlagArrayVariable)
    fav_example.type = "FlagArray"
    fav_example.table_name = "Supporters"
    fav_example.name = "ContactPreferences"
    fav_example.session = "CharityDataViewSession"
    return fav_example


@pytest.fixture()
def fake_date_variable():
    dv_example = DateVariable.__new__(DateVariable)
    dv_example.type = "Date"
    dv_example.table_name = "Donations"
    dv_example.name = "DonationDate"
    dv_example.session = "CharityDataViewSession"
    return dv_example


@pytest.fixture()
def fake_datetime_variable():
    dtv_example = DateTimeVariable.__new__(DateTimeVariable)
    dtv_example.type = "DateTime"
    dtv_example.table_name = "WebVisits"
    dtv_example.name = "BrowsingSessionStart"
    dtv_example.session = "CharityDataViewSession"
    return dtv_example


class TestVariableOperators:
    def test_selector_eq(self, fake_selector_variable):
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

    def test_numeric_eq(self, fake_numeric_variable):
        donations_100 = fake_numeric_variable == 100
        assert type(donations_100) == NumericClause
        assert donations_100.table_name == "Donations"
        assert donations_100.variable_name == "Amount"
        assert donations_100.values == ["100"]
        assert donations_100.include is True
        assert donations_100.session == "CharityDataViewSession"

        hundreds_donations = fake_numeric_variable == (
            i * 100 for i in range(1, 10)
        )
        assert type(hundreds_donations) == NumericClause
        assert hundreds_donations.table_name == "Donations"
        assert hundreds_donations.variable_name == "Amount"
        assert hundreds_donations.values == [
            "100", "200", "300", "400", "500", "600", "700", "800", "900"
        ]
        assert hundreds_donations.include is True
        assert hundreds_donations.session == "CharityDataViewSession"

        with pytest.raises(ValueError) as exc_info:
            trying_with_a_string = fake_numeric_variable == "256"
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a numeric variable"
            " must be given as a number or an iterable of numbers."
        )

    def test_text_eq(self, fake_email_text_variable):
        specific_donor = fake_email_text_variable == "donor@domain.com"
        assert type(specific_donor) == TextClause
        assert specific_donor.table_name == "Supporters"
        assert specific_donor.variable_name == "EmailAddress"
        assert specific_donor.values == ["donor@domain.com"]
        assert specific_donor.match_type == "Is"
        assert specific_donor.match_case is True
        assert specific_donor.include is True
        assert specific_donor.session == "CharityDataViewSession"

        donors_by_email = fake_email_text_variable == [
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
            donors_by_number = fake_email_text_variable == {34, 765, 2930}
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a text variable"
            " must be given as a string or an iterable of strings."
        )

    def test_array_eq(self, fake_array_variable):
        national_campaigns = fake_array_variable == "National"
        assert type(national_campaigns) == ArrayClause
        assert national_campaigns.table_name == "Campaigns"
        assert national_campaigns.variable_name == "Tags"
        assert national_campaigns.values == ["National"]
        assert national_campaigns.logic == "OR"
        assert national_campaigns.include is True
        assert national_campaigns.session == "CharityDataViewSession"

        autumn_campaigns = fake_array_variable == {
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

        with pytest.raises(ValueError) as exc_info:
            forgot_string_quotes = fake_array_variable == ["4", 6]
        assert exc_info.value.args[0] == (
            "Chosen value(s) for an array variable"
            " must be given as a string or an iterable of strings."
        )

    def test_flag_array_eq(self, fake_flag_array_variable):
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

    def test_date_eq(self, fake_date_variable):
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
