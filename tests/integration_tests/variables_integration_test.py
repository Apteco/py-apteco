import decimal
from datetime import date, datetime

import pytest


def test_selector_operators(bookings, people, households):
    sweden = bookings["boDest"] == "29"
    assert sweden.count() == 25_207
    high_earners = people["peIncome"] == (f"{i:02}" for i in range(7, 12))
    assert high_earners.count() == 7_114
    not_student = people["peOccu"] != "4"
    assert not_student.count() == 1_029_708
    england = households["hoRegion"] != ["10", "11", "12", "14"]
    assert england.count() == 627_550


@pytest.mark.xfail(reason="Not yet implemented.")
def test_combined_categories_operators():
    raise NotImplementedError


def test_array_operators(households):
    mazda = households["HHCarmak"] == "MAZ"
    assert mazda.count() == 3_587
    any_v = households["HHCarmak"] == ["VAU", "VLK", "VOL"]
    assert any_v.count() == 12_418
    anything_but_ford = households["HHCarmak"] != "FOR"
    assert anything_but_ford.count() == 690_951
    exclude_top_6 = households["HHCarmak"] != ["FIA", "KIA", "  !", "CHE", "SUZ", "DAI"]
    assert exclude_top_6.count() == 236_798


def test_flag_array_operators(people, bookings):
    ft_readers = people["peNews"] == "Financial Times"
    assert ft_readers.count() == 11_470
    broadsheet_readers = people["peNews"] == [
        "Financial Times",
        "The Times",
        "Daily Telegraph",
        "The Guardian",
        "Independent",
    ]
    assert broadsheet_readers.count() == 531_936
    cant_email = people["peContac"] != "EPS"
    assert cant_email.count() == 1_062_397
    no_activities = bookings["deFacil"] != ["Entertainment", "Kidsclub", "Trips"]
    assert no_activities.count() == 75_774


def test_numeric_operator(policies, bookings, web_visits):
    thirty_days_to_travel = policies["PoDaysUn"] == 30
    assert thirty_days_to_travel.count() == 2_647
    multiple_of_100 = bookings["boCost"] == (i * 100 for i in range(285))
    assert multiple_of_100.count() == 3_123
    profit_not_33_33 = bookings["boProfit"] != decimal.Decimal("33.33")
    assert profit_not_33_33.count() == 2_129_833
    more_than_5_days_until_travel = policies["PoDaysUn"] != [0, 1, 2, 3, 4, 5]
    assert more_than_5_days_until_travel.count() == 172_044
    low_profit = bookings["boProfit"] <= 25
    assert low_profit.count() == 211_328
    cost_at_least_2k = bookings["boCost"] >= 2000
    assert cost_at_least_2k.count() == 53_267
    less_than_minute = web_visits["wvDuratn"] < 60
    assert less_than_minute.count() == 44_399
    more_than_8_weeks = policies["PoDaysSi"] > 56
    assert more_than_8_weeks.count() == 23_950


def test_text_operator(people, households):
    smith = people["peSName"] == "Smith"
    assert smith.count() == 13_302
    vowel_initial = people["peInit"] == list("AEIOU")
    assert vowel_initial.count() == 168_548
    not_t_initial = people["peInit"] != "T"
    assert not_t_initial.count() == 1_051_815
    outside_top_5_surnames = people["peSName"] != ["Smith", "Brown", "Jones", "Taylor", "Patel"]
    assert outside_top_5_surnames.count() == 1_113_731
    early_postcode = households["hoPCode"] <= "E"
    assert early_postcode.count() == 208_569
    further_down_street = households["hoAddr"] >= "9"
    assert further_down_street.count() == 31_197


def test_date_operator(bookings, policies):
    valentines_day_2018 = bookings["boTrav"] == date(2018, 2, 14)
    assert valentines_day_2018.count() == 625
    bank_holidays_2020 = bookings["boDate"] == [
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
    not_easter_2017 = policies["PoTrave1"] != date(2017, 4, 16)
    assert not_easter_2017.count() == 213_442  # all - 125
    exclude_solstices_and_equinoxes_2021 = policies["PoPolic1"] != [
        date(2021, 3, 20),
        date(2021, 6, 21),
        date(2021, 9, 22),
        date(2021, 12, 21),
    ]
    assert exclude_solstices_and_equinoxes_2021.count() == 213_109  # all - 458
    before_tax_year_end_2018_19 = policies["PoBooki1"] <= date(2019, 4, 5)
    assert before_tax_year_end_2018_19.count() == 185_601
    after_christmas_2016 = bookings["boDate"] >= date(2016, 12, 26)
    assert after_christmas_2016.count() == 1_915_257


def test_datetime_operator(web_visits, communications):
    before_4pm_halloween_2019 = web_visits["wvTime"] <= datetime(2019, 10, 31, 15, 59, 59)
    assert before_4pm_halloween_2019.count() == 169_019
    after_juy_2016 = communications["cmCommDt"] >= datetime(2016, 8, 1, 0, 0, 0)
    assert after_juy_2016.count() == 3_926


@pytest.mark.xfail(reason="Not yet implemented.")
def test_reference_operators():
    raise NotImplementedError