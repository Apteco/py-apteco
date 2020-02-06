import decimal
from datetime import datetime, date

import pytest
import toml

from apteco.query import (
    ArrayClause,
    DateListClause,
    DateRangeClause,
    DateTimeRangeClause,
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
    assert len(holidays.variables) == 86
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
    assert system_info.build_date == datetime(2019, 11, 27, 15, 57, 24)
    assert system_info.view_name == "Holidays"


people = holidays.tables["People"]
bookings = holidays.tables["Bookings"]
households = holidays.tables["Households"]
policies = holidays.tables["Policies"]
web_visits = holidays.tables["WebVisits"]
communications = holidays.tables["Communications"]


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


@pytest.mark.xfail(reason="Variable needs to use table object for creating clauses.")
def test_date_operator():
    valentines_day_2018 = bookings["Travel Date"] == date(2018, 2, 14)
    assert valentines_day_2018.count() == 625
    bank_holidays_2020 = bookings["Booking Date"] == [
        date(2020, 1, 1),
        date(2020, 4, 10),
        date(2020, 4, 13),
        date(2020, 5, 8),
        date(2020, 5, 25),
        date(2020, 8, 31),
        date(2020, 12, 25),
        date(2020, 12, 26),
    ]
    assert bank_holidays_2020.count() == 7_847
    not_easter_2017 = policies["Policy Travel Date"] != date(2017, 4, 16)
    assert not_easter_2017.count() == 213_442  # all - 125
    exclude_solstices_and_equinoxes_2021 = policies["Policy Date"] != [
        date(2021, 3, 20),
        date(2021, 6, 21),
        date(2021, 9, 22),
        date(2021, 12, 21),
    ]
    assert exclude_solstices_and_equinoxes_2021.count() == 213_109  # all - 458
    before_tax_year_end_2018_19 = policies["Policy Booking Date"] <= date(2019, 4, 5)
    assert before_tax_year_end_2018_19.count() == 185_601
    after_christmas_2016 = bookings["Booking Date"] >= date(2016, 12, 26)
    assert after_christmas_2016.count() == 1_915_257


def test_date_list_clause():
    valentines_day_2018 = DateListClause(bookings.name, bookings["Travel Date"].name, ["20180214"], session=holidays)
    assert valentines_day_2018.count() == 625
    bank_holidays_2020 = DateListClause(bookings.name, bookings["Booking Date"].name, [
        "20200101",
        "20200410",
        "20200413",
        "20200508",
        "20200525",
        "20200831",
        "20201225",
        "20201226",
    ], session=holidays)
    assert bank_holidays_2020.count() == 7_847
    not_easter_2017 = DateListClause(policies.name, policies["Policy Travel Date"].name, ["20170416"], include=False, session=holidays)
    assert not_easter_2017.count() == 213_442  # all - 125
    exclude_solstices_and_equinoxes_2021 = DateListClause(policies.name, policies["Policy Date"].name, [
        "20210320",
        "20210621",
        "20210922",
        "20211221",
    ], include=False, session=holidays)
    assert exclude_solstices_and_equinoxes_2021.count() == 213_109  # all - 458


def test_date_range_clause():
    olympics_summer_16_to_winter_18 = DateRangeClause(bookings.name, bookings["Travel Date"].name, "2016-08-22", "2018-02-08", session=holidays)
    assert olympics_summer_16_to_winter_18.count() == 328_733
    before_tax_year_end_2018_19 = DateRangeClause(policies.name, policies["Policy Booking Date"].name, "Earliest", "2019-04-05", session=holidays)
    assert before_tax_year_end_2018_19.count() == 185_601
    after_christmas_2016 = DateRangeClause(bookings.name, bookings["Booking Date"].name, "2016-12-26", "Latest", session=holidays)
    assert after_christmas_2016.count() == 1_915_257
    earliest_to_latest_policy_date = DateRangeClause(policies.name, policies["Policy Date"].name, "Earliest", "Latest", session=holidays)
    assert earliest_to_latest_policy_date.count() == 213_567
    not_between_world_cup_18_euro_20 = DateRangeClause(policies.name, policies["Policy Travel Date"].name, "2018-07-16", "2020-06-11", include=False, session=holidays)
    assert not_between_world_cup_18_euro_20.count() == 151_691
    not_before_christmas_2016 = DateRangeClause(bookings.name, bookings["Booking Date"].name, "Earliest", "2016-12-25", include=False, session=holidays)
    assert not_before_christmas_2016.count() == 1_915_257
    not_after_tax_year_end_2018_19 = DateRangeClause(policies.name, policies["Policy Booking Date"].name, "2019-04-06", "Latest", include=False, session=holidays)
    assert not_after_tax_year_end_2018_19.count() == 185_601
    not_earliest_to_latest_booking = DateRangeClause(bookings.name, bookings["Booking Date"].name, "Earliest", "Latest", include=False, session=holidays)
    assert not_earliest_to_latest_booking.count() == 0


@pytest.mark.xfail(reason="Variable needs to use table object for creating clauses.")
def test_datetime_operator():
    before_4pm_halloween_2019 = web_visits["Web Visit Time"] <= datetime(2019, 10, 31, 15, 59, 59)
    assert before_4pm_halloween_2019.count() == 169_019
    after_juy_2016 = communications["Date Of Communication"] >= datetime(2016, 8, 1, 0, 0, 0)
    assert after_juy_2016.count() == 3_926


def test_datetime_range_clause():
    during_week_29_2016 = DateTimeRangeClause(communications.name, communications["Date of Communication"].name, "2016-07-18T08:00:00", "2016-07-22T17:59:59", session=holidays)
    assert during_week_29_2016.count() == 19_298
    before_4pm_halloween_2019 = DateTimeRangeClause(web_visits.name, web_visits["Web Visit Time"].name, "Earliest", "2019-10-31T15:59:59", session=holidays)
    assert before_4pm_halloween_2019.count() == 169_019
    after_juy_2016 = DateTimeRangeClause(communications.name, communications["Date of Communication"].name, "2016-08-01T00:00:00", "Latest", session=holidays)
    assert after_juy_2016.count() == 3_926
    all_web_visits = DateTimeRangeClause(web_visits.name, web_visits["Web Visit Time"].name, "Earliest", "Latest", session=holidays)
    assert all_web_visits.count() == 279_538
    not_during_lent_2021 = DateTimeRangeClause(web_visits.name, web_visits["Web Visit Time"].name, "2021-02-17T07:18:00", "2021-04-03T19:44:00", include=False, session=holidays)
    assert not_during_lent_2021.count() == 270_245  # all - 9_293
    not_before_july_2016 = DateTimeRangeClause(communications.name, communications["Date of Communication"].name, "Earliest", "2016-07-31T23:59:59", include=False, session=holidays)
    assert not_before_july_2016.count() == 3_926
    not_after_4pm_halloween_2019 = DateTimeRangeClause(web_visits.name, web_visits["Web Visit Time"].name, "2019-10-31T16:00:00", "Latest", include=False, session=holidays)
    assert not_after_4pm_halloween_2019.count() == 169_019
    not_all_communications = DateTimeRangeClause(communications.name, communications["Date of Communication"].name, "Earliest", "Latest", include=False, session=holidays)
    assert not_all_communications.count() == 0
