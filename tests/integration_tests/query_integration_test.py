import decimal
from datetime import datetime

import pytest
import toml

from apteco.query import (
    ArrayClause,
    FlagArrayClause,
    NumericClause,
    SelectorClause,
    TextClause,
)
from apteco.session import login_with_password

credentials = toml.load("credentials.toml")["local"]

holidays = login_with_password(
    credentials["base_url"],
    credentials["data_view"],
    credentials["system"],
    credentials["user"],
    credentials["password"],
)


def test_session():
    assert len(holidays.tables) == 9
    assert len(holidays.variables) == 88
    assert holidays.master_table.name == "Households"


def test_user():
    user = holidays.user
    assert user.first_name == "Admin"
    assert user.surname == "User"
    assert user.username == "Administrator"
    assert user.email_address == "support@apteco.com"


def test_system_info():
    system_info = holidays.system_info
    assert system_info.name == "holidays"
    assert system_info.description == "Holidays Demo Database"
    assert system_info.build_date == datetime(2019, 1, 25, 15, 9, 40)
    assert system_info.view_name == "Holidays"


people = holidays.tables["People"]
bookings = holidays.tables["Bookings"]
households = holidays.tables["Households"]
policies = holidays.tables["Policies"]
web_visits = holidays.tables["WebVisits"]


@pytest.mark.xfail(reason="Variable needs to use table object for creating clauses.")
def test_selector_operators():
    sweden = bookings["Destination"] == "29"
    assert sweden.count() == 25_207
    high_earners = people["Income"] == (f"{i:02}" for i in range(7, 12))
    assert high_earners.count() == 7_114
    not_student = people["Occupation"] != "4"
    assert not_student == 1_029_708
    england = households["Region"] != ["10", "11", "12", "14"]
    assert england.count() == 627_550


def test_selector_clause():
    sweden = SelectorClause(bookings.name, bookings["Destination"].name, ["29"], session=holidays)
    assert sweden.count() == 25_207
    high_earners = SelectorClause(people.name, people["Income"].name, [f"{i:02}" for i in range(7, 12)], session=holidays)
    assert high_earners.count() == 7_114
    not_student = SelectorClause(people.name, people["Occupation"].name, ["4"], include=False, session=holidays)
    assert not_student.count() == 1_029_708
    england = SelectorClause(households.name, households["Region"].name, ["10", "11", "12", "14"], include=False, session=holidays)
    assert england.count() == 627_550


@pytest.mark.xfail(reason="Variable needs to use table object for creating clauses.")
def test_array_operators():
    mazda = households["Car Make Code"] == "MAZ"
    assert mazda.count() == 3_587
    any_v = households["Car Make Code"] == ["VAU", "VLK", "VOL"]
    assert any_v.count() == 15_105
    anything_but_ford = households["Car Make Code"] != "FOR"
    assert anything_but_ford.count() == 690_951
    exclude_top_6 = households["Car Make Code"] != ["FIA", "KIA", "  !", "CHE", "SUZ", "DAI"]
    assert exclude_top_6.count() == 236_798


def test_array_clause():
    mazda = ArrayClause(households.name, households["Car Make Code"].name, ["MAZ"], session=holidays)
    assert mazda.count() == 3_587
    any_v = ArrayClause(households.name, households["Car Make Code"].name, ["VAU", "VLK", "VOL"], session=holidays)
    assert any_v.count() == 12_418
    anything_but_ford = ArrayClause(households.name, households["Car Make Code"].name, ["FOR"], include=False, session=holidays)
    assert anything_but_ford.count() == 690_951
    exclude_top_6 = ArrayClause(households.name, households["Car Make Code"].name, ["FIA", "KIA", "  !", "CHE", "SUZ", "DAI"], include=False, session=holidays)
    assert exclude_top_6.count() == 236_798
    mazda_and = ArrayClause(households.name, households["Car Make Code"].name, ["MAZ"], "AND", session=holidays)
    assert mazda_and.count() == 3_587  # should be same as with OR
    all_aud_toy_vau = ArrayClause(households.name, households["Car Make Code"].name, ["AUD", "TOY", "VAU"], "AND", session=holidays)
    assert all_aud_toy_vau.count() == 34
    anything_but_ford_and = ArrayClause(households.name, households["Car Make Code"].name, ["FOR"], "AND", include=False, session=holidays)
    assert anything_but_ford_and.count() == 690_951  # should be same as with OR
    exclude_both_fiat_kia = ArrayClause(households.name, households["Car Make Code"].name, ["FIA", "KIA"], "AND", include=False, session=holidays)
    assert exclude_both_fiat_kia.count() == 742_265


@pytest.mark.xfail(reason="Variable needs to use table object for creating clauses.")
def test_flag_array_operators():
    ft_readers = people["Newspapers"] == "Financial Times"
    assert ft_readers.count() == 11_470
    broadsheet_readers = people["Newspapers"] == [
        "Financial Times",
        "The Times",
        "Daily Telegraph",
        "The Guardian",
        "Independent",
    ]
    assert broadsheet_readers.count() == 531_936
    cant_email = people["Contact Permission"] != "EPS"
    assert cant_email.count() == 1_062_397
    no_activities = bookings["Facilities"] != ["Entertainment", "Kidsclub", "Trips"]
    assert no_activities.count() == 75_774


def test_flag_array_clause():
    ft_readers = FlagArrayClause(people.name, people["Newspapers"].name, ["Financial Times"], session=holidays)
    assert ft_readers.count() == 11_470
    broadsheet_readers = FlagArrayClause(people.name, people["Newspapers"].name, [
        "Financial Times",
        "The Times",
        "Daily Telegraph",
        "The Guardian",
        "Independent",
    ], session=holidays)
    assert broadsheet_readers.count() == 531_936
    cant_email = FlagArrayClause(people.name, people["Contact Permission"].name, ["EPS"], include=False, session=holidays)
    assert cant_email.count() == 1_062_397
    no_activities = FlagArrayClause(bookings.name, bookings["Facilities"].name, ["Entertainment", "Kidsclub", "Trips"], include=False, session=holidays)
    assert no_activities.count() == 75_774
    ft_readers_and = FlagArrayClause(people.name, people["Newspapers"].name, ["Financial Times"], "AND", session=holidays)
    assert ft_readers_and.count() == 11_470  # should be same as with OR
    trips_and_ents = FlagArrayClause(bookings.name, bookings["Facilities"].name, ["Trips", "Entertainment"], "AND", session=holidays)
    assert trips_and_ents.count() == 674_890
    cant_email_and = FlagArrayClause(people.name, people["Contact Permission"].name, ["EPS"], "AND", include=False, session=holidays)
    assert cant_email_and.count() == 1_062_397  # should be same as with OR
    not_both_m = FlagArrayClause(people.name, people["Newspapers"].name, ["Daily Mail", "Daily Mirror"], "AND", include=False, session=holidays)
    assert not_both_m.count() == 1_148_318


@pytest.mark.xfail(reason="Variable needs to use table object for creating clauses.")
def test_numeric_operator():
    thirty_days_to_travel = policies["Days Until Travel"] == 30
    assert thirty_days_to_travel.count() == 2_647
    multiple_of_100 = bookings["Cost"] == (i * 100 for i in range(285))
    assert multiple_of_100.count() == 3_123
    profit_not_33_33 = bookings["Profit"] != decimal.Decimal("33.33")
    assert profit_not_33_33.count() == 2_129_833
    more_than_5_days_until_travel = policies["Days Until Travel"] != [0, 1, 2, 3, 4, 5]
    assert more_than_5_days_until_travel.count() == 172_044
    low_profit = bookings["Profit"] <= 25
    assert low_profit.count() == 211_328
    cost_at_least_2k = bookings["Cost"] >= 2000
    assert cost_at_least_2k.count() == 53_267
    less_than_minute = web_visits["Duration"] < 60
    assert less_than_minute.count() == 44_399
    more_than_8_weeks = policies["Days Since Booking"] > 56
    assert more_than_8_weeks.count() == 23_950


def test_numeric_clause():
    thirty_days_to_travel = NumericClause(policies.name, policies["Days Until Travel"].name, ["30"], session=holidays)
    assert thirty_days_to_travel.count() == 2_647
    multiple_of_100 = NumericClause(bookings.name, bookings["Cost"].name, [str(i * 100) for i in range(285)], session=holidays)
    assert multiple_of_100.count() == 3_123
    profit_not_33_33 = NumericClause(bookings.name, bookings["Profit"].name, ["33.33"], include=False, session=holidays)
    assert profit_not_33_33.count() == 2_129_833
    more_than_5_days_until_travel = NumericClause(policies.name, policies["Days Until Travel"].name, ["0", "1", "2", "3", "4", "5"], include=False, session=holidays)
    assert more_than_5_days_until_travel.count() == 172_044
    low_profit = NumericClause(bookings.name, bookings["Profit"].name, ["<=25"], session=holidays)
    assert low_profit.count() == 211_328
    cost_at_least_2k = NumericClause(bookings.name, bookings["Cost"].name, [">=2000"], session=holidays)
    assert cost_at_least_2k.count() == 53_267
    less_than_minute = NumericClause(web_visits.name, web_visits["Duration"].name, ["<60"], session=holidays)
    assert less_than_minute.count() == 44_399
    more_than_8_weeks = NumericClause(policies.name, policies["Days Since Booking"].name, [">56"], session=holidays)
    assert more_than_8_weeks.count() == 23_950
    not_le_8_weeks = NumericClause(policies.name, policies["Days Since Booking"].name, ["<=56"], include=False, session=holidays)
    assert not_le_8_weeks.count() == 23_950  # should be same as > with include
    not_ge_minute = NumericClause(web_visits.name, web_visits["Duration"].name, [">=60"], include=False, session=holidays)
    assert not_ge_minute.count() == 44_399 + 8_673  # should be same as < with include... but there are missing values
    cost_not_less_than_2k = NumericClause(bookings.name, bookings["Cost"].name, ["<2000"], include=False, session=holidays)
    assert cost_not_less_than_2k.count() == 53_267
    not_high_profit = NumericClause(bookings.name, bookings["Profit"].name, [">25"], include=False, session=holidays)
    assert not_high_profit.count() == 211_328 + 67_012  # should be same as > with include... but there are missing values


@pytest.mark.xfail(reason="Variable needs to use table object for creating clauses.")
def test_text_operator():
    smith = people["Surname"] == "Smith"
    assert smith.count() == 13_302
    vowel_initial = people["Initial"] == list("AEIOU")
    assert vowel_initial.count() == 168_548
    not_t_initial = people["Surname"] != "T"
    assert not_t_initial.count() == 1_051_815
    outside_top_5_surnames = people["Initial"] != ["Smith", "Brown", "Jones", "Taylor", "Patel"]
    assert outside_top_5_surnames.count() == 1_113_731
    early_postcode = households["Postcode"] <= "E"
    assert early_postcode.count() == 208_569
    further_down_street = households["Address"] >= "9"
    assert further_down_street.count() == 31_197


def test_text_clause_is():
    smith = TextClause(people.name, people["Surname"].name, ["Smith"], session=holidays)
    assert smith.count() == 13_302
    vowel_initial = TextClause(people.name, people["Initial"].name, list("AEIOU"), session=holidays)
    assert vowel_initial.count() == 168_548
    not_t_initial = TextClause(people.name, people["Initial"].name, ["T"], include=False, session=holidays)
    assert not_t_initial.count() == 1_051_815
    outside_top_5_surnames = TextClause(people.name, people["Surname"].name, ["Smith", "Brown", "Jones", "Taylor", "Patel"], include=False, session=holidays)
    assert outside_top_5_surnames.count() == 1_113_731


def test_text_clause_contains():
    gmail_emails = TextClause(people.name, people["Email Address"].name, ["gmail"], "Contains", session=holidays)
    assert gmail_emails.count() == 20_787
    address_without_1 = TextClause(households.name, households["Address"].name, ["1"], "Contains", include=False, session=holidays)
    assert address_without_1.count() == 480_860
    triple_digit_telephone = TextClause(households.name, households["Telephone"].name, [str(i) * 3 for i in range(10)], "Contains", session=holidays)
    assert triple_digit_telephone.count() == 53_962
    xz_surname = TextClause(people.name, people["Surname"].name, ["x", "z"], "Contains", False, session=holidays)
    assert xz_surname.count() == 25_178
    no_vowel_surname = TextClause(people.name, people["Surname"].name, list("AEIOU"), "Contains", False, include=False, session=holidays)
    assert no_vowel_surname.count() == 2_966


def test_text_clause_begins():
    scottish_surname = TextClause(people.name, people["Surname"].name, ["Mc", "Mac"], "Begins", False, session=holidays)
    assert scottish_surname.count() == 28_303
    coventry_postcode = TextClause(households.name, households["Postcode"].name, ["CV"], "Begins", session=holidays)
    assert coventry_postcode.count() == 9_267
    not_cheap_domain_visits = TextClause(web_visits.name, web_visits["URL"].name, ["www.onecheapholiday.co.uk", "www.shabbychichotels.co.uk"], "Begins", include=False, session=holidays)
    assert not_cheap_domain_visits.count() == 223_658
    not_t_surname = TextClause(people.name, people["Surname"].name, ["t"], "Begins", False, include=False, session=holidays)
    assert not_t_surname.count() == 1_108_912


def test_text_clause_ends():
    son_surname = TextClause(people.name, people["Surname"].name, ["son", "SON"], "Ends", True, session=holidays)
    assert son_surname.count() == 62_775
    no_dot_com_email = TextClause(people.name, people["Email Address"].name, [".com"], "Ends", include=False, session=holidays)
    assert no_dot_com_email.count() == 451_433
    not_common_road_type = TextClause(households.name, households["Address"].name, [" Road", " Close", " Avenue", " Drive", " Street"], "Ends", False, include=False, session=holidays)
    assert not_common_road_type.count() == 303_948
    profession_surnames = TextClause(people.name, people["Surname"].name, ["er"], "Ends", False, session=holidays)
    assert profession_surnames.count() == 89_460


def test_text_clause_ranges():
    early_postcode = TextClause(households.name, households["Postcode"].name, ["<=\"E\""], "Ranges", session=holidays)
    assert early_postcode.count() == 208_569
    further_down_street = TextClause(households.name, households["Address"].name, [">=\"9\""], "Ranges", session=holidays)
    assert further_down_street.count() == 31_197


def test_text_clause_wildcards():
    like_smith = TextClause(people.name, people["Surname"].name, ["=\"Sm?th\""], "Ranges", session=holidays)
    assert like_smith.count() == 13_653
    like_smith_long = TextClause(people.name, people["Surname"].name, ["=\"Sm?th*\""], "Ranges", session=holidays)
    assert like_smith_long.count() == 14_172
    no_space_address = TextClause(households.name, households["Address"].name, ["=\"* *\""], "Ranges", include=False, session=holidays)
    assert no_space_address.count() == 366
    two_digit_high_street = TextClause(households.name, households["Address"].name, ["=\"?? High Street\""], "Ranges", False, session=holidays)
    assert two_digit_high_street.count() == 2_187
    not_10_something_road = TextClause(households.name, households["Address"].name, ["=\"10 *Road\""], "Ranges", False, include=False, session=holidays)
    assert not_10_something_road.count() == 739_313
    surname_5_long_2_4_vowels = TextClause(people.name, people["Surname"].name, [f"=\"?{i}?{j}?\"" for i in list("aeiou") for j in list("aeiou")], "Ranges", session=holidays)
    assert surname_5_long_2_4_vowels.count() == 59_824
    like_short_middle_long = TextClause(people.name, people["Surname"].name, ["=\"Sh?rt\"", "=\"M?ddle*\"", "=\"Lo*ng\""], "Ranges", session=holidays)
    assert like_short_middle_long.count() == 2_121
    not_common_email_domains = TextClause(people.name, people["Email Address"].name, [f"=\"*@*{i}.{j}\"" for i in ("Mail", "Post") for j in ("com", "uk.com", "co.uk")], "Ranges", include=False, session=holidays)
    assert not_common_email_domains.count() == 948_831
    smith_like_double_barrelled = TextClause(people.name, people["Surname"].name, ["=\"Sm?th-*\"", "=\"*-Sm?th\""], "Ranges", False, session=holidays)
    assert smith_like_double_barrelled.count() == 660
    first_2_not_vowel = TextClause(people.name, people["Surname"].name, [f"=\"{i}{j}*\"" for i in ("", "?") for j in list("aeiou")], "Ranges", False, include=False, session=holidays)
    assert first_2_not_vowel.count() == 295_815
