import decimal
from datetime import date, datetime

import pytest


def test_selector_operators(bookings, people, households):
    sweden = bookings["boDest"] == "29"
    assert sweden.count() == 25207
    high_earners = people["peIncome"] == (f"{i:02}" for i in range(7, 12))
    assert high_earners.count() == 7114
    not_student = people["peOccu"] != "4"
    assert not_student.count() == 1_029_708
    england = households["hoRegion"] != ["10", "11", "12", "14"]
    assert england.count() == 627_550


@pytest.mark.xfail(reason="Not yet implemented.")
def test_combined_categories_operators():
    raise NotImplementedError


def test_array_operators(households):
    mazda = households["HHCarmak"] == "MAZ"
    assert mazda.count() == 3587
    any_v = households["HHCarmak"] == ["VAU", "VLK", "VOL"]
    assert any_v.count() == 12418
    anything_but_ford = households["HHCarmak"] != "FOR"
    assert anything_but_ford.count() == 690_951
    exclude_top_6 = households["HHCarmak"] != ["FIA", "KIA", "  !", "CHE", "SUZ", "DAI"]
    assert exclude_top_6.count() == 236_798


def test_flag_array_operators(people, bookings):
    ft_readers = people["peNews"] == "Financial Times"
    assert ft_readers.count() == 11470
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
    assert no_activities.count() == 75774


class TestNumericVariable:
    def test_numeric_operator(self, policies, bookings, web_visits):
        thirty_days_to_travel = policies["PoDaysUn"] == 30
        assert thirty_days_to_travel.count() == 2647
        multiple_of_100 = bookings["boCost"] == (i * 100 for i in range(285))
        assert multiple_of_100.count() == 3123
        profit_not_33_33 = bookings["boProfit"] != decimal.Decimal("33.33")
        assert profit_not_33_33.count() == 2_129_833
        more_than_5_days_until_travel = policies["PoDaysUn"] != [0, 1, 2, 3, 4, 5]
        assert more_than_5_days_until_travel.count() == 172_044
        low_profit = bookings["boProfit"] <= 25
        assert low_profit.count() == 211_328
        cost_at_least_2k = bookings["boCost"] >= 2000
        assert cost_at_least_2k.count() == 53267
        less_than_minute = web_visits["wvDuratn"] < 60
        assert less_than_minute.count() == 44399
        more_than_8_weeks = policies["PoDaysSi"] > 56
        assert more_than_8_weeks.count() == 23950

    def test_numeric_missing(self, bookings, policies):
        missing_profit = bookings["Profit"].missing()
        assert missing_profit.count() == 67012

        not_missing_premium = policies["Premium"].missing(include=False)
        assert not_missing_premium.count() == 213567


class TestTextVariable:
    def test_text_operator(self, people, households):
        smith = people["peSName"] == "Smith"
        assert smith.count() == 13302
        vowel_initial = people["peInit"] == list("AEIOU")
        assert vowel_initial.count() == 168_548
        not_t_initial = people["peInit"] != "T"
        assert not_t_initial.count() == 1_051_815
        outside_top_5_surnames = people["peSName"] != [
            "Smith",
            "Brown",
            "Jones",
            "Taylor",
            "Patel",
        ]
        assert outside_top_5_surnames.count() == 1_113_731
        early_postcode = households["hoPCode"] <= "E"
        assert early_postcode.count() == 208_569
        further_down_street = households["hoAddr"] >= "9"
        assert further_down_street.count() == 31197

    def test_text_equals(self, people):
        morse = people["Surname"].equals("Morse")
        assert morse.count() == 143

        sherlock = people["Surname"].equals(["Holmes", "Watson", "Moriarty"], match_case=False)
        assert sherlock.count() == 2953

    def test_text_contains(self, households):
        no_lower_case_e = households["Address"].contains("e", include=False)
        assert no_lower_case_e.count() == 139337

        holy_address = households["Address"].contains(["church", "chapel", "cathedral", "temple"], match_case=False)
        assert holy_address.count() == 8111

    def test_text_startswith(self, people):
        x_surname = people["Surname"].startswith("X")
        assert x_surname.count() == 47

        apteco_initial = people["Surname"].startswith(list("apteco"), match_case=False)
        assert apteco_initial.count() == 288014

    def test_text_endswith(self, people, households):
        hotmail_co_uk = people["Email Address"].endswith("@hotmail.co.uk")
        assert hotmail_co_uk.count() == 6880

        not_common_road_type = households["Address"].endswith([" Road", " Street", " Close", " Avenue", " Drive", " Lane"], match_case=False, include=False)
        assert not_common_road_type.count() == 269893

    def test_text_between(self, people):
        green_to_grey = people["Surname"].between("Green", "Grey")
        assert green_to_grey.count() == 7549

        brown_to_brown = people["Surname"].between("Brown", "Brown")
        assert brown_to_brown.count() == 7618

        lower_to_upper = people["Surname"].between("taupe", "TEAL")
        assert lower_to_upper.count() == 6910

        upper_to_lower = people["Surname"].between("Pink", "purple")
        assert upper_to_lower.count() == 22760

        with pytest.raises(ValueError) as exc_info:
            empty_range = people["Surname"].between("W", "S")
        assert exc_info.value.args[0] == "`start` must come before `end`"

        with pytest.raises(ValueError) as exc_info:
            wrong_way_round = people["Surname"].between("W", "s")
        assert exc_info.value.args[0] == (
            "`start` must come before `end`, but 'W'"
            " comes after 's' when compared case-insensitively."
        )

    def test_text_matches(self, people):
        no_wildcards = people["Surname"].matches("Brown")
        assert no_wildcards.count() == 6847

        single_char_wildcard = people["Surname"].matches("Brown?")
        assert single_char_wildcard.count() == 265

        star_wildcard = people["Surname"].matches("Brown*", match_case=False)
        assert star_wildcard.count() == 7618

        both_wildcards = people["Surname"].matches("B?r*", match_case=False)
        assert both_wildcards.count() == 25770


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
    assert bank_holidays_2020.count() == 7847
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
    before_4pm_halloween_2019 = web_visits["wvTime"] <= datetime(
        2019, 10, 31, 15, 59, 59
    )
    assert before_4pm_halloween_2019.count() == 169_019
    after_juy_2016 = communications["cmCommDt"] >= datetime(2016, 8, 1, 0, 0, 0)
    assert after_juy_2016.count() == 3926


@pytest.mark.xfail(reason="Not yet implemented.")
def test_reference_operators():
    raise NotImplementedError


class TestVariablesAccessor:
    def test_variables_getitem_by_name(self, bookings):
        destination = bookings.variables["boDest"]
        assert destination.description == "Destination"

    def test_variables_getitem_by_desc(self, bookings):
        destination = bookings.variables["Destination"]
        assert destination.name == "boDest"

    def test_variables_getitem_bad_key(self, bookings):
        with pytest.raises(KeyError) as exc_info:
            not_a_var = bookings.variables["notAKey"]
        assert exc_info.value.args[0] == (
            "Lookup key 'notAKey' did not match a variable name or description."
        )

    def test_variables_getitem_duplicate_key(self, bookings):
        grade_var_for_setup = bookings.variables._variables_by_name["deGrade"]
        bookings.variables._variables_by_desc["deGrade"] = grade_var_for_setup
        grade = bookings.variables["deGrade"]
        assert grade.description == "Grade"
        del bookings.variables._variables_by_desc["deGrade"]

    def test_variables_getitem_ambiguous_key(self, bookings):
        product = bookings.variables._variables_by_name["boProd"]
        bookings.variables._variables_by_desc["boCost"] = product
        with pytest.raises(KeyError) as exc_info:
            ambiguous_var = bookings.variables["boCost"]
        assert exc_info.value.args[0] == "Lookup key 'boCost' was ambiguous."
        del bookings.variables._variables_by_desc["boCost"]

    def test_variables_iter(self, bookings):
        all_vars = [var.name for var in bookings.variables if not var.is_virtual]
        assert sorted(all_vars) == [
            "boCont",
            "boCost",
            "boDate",
            "boDest",
            "boKeyCd",
            "boProd",
            "boProfit",
            "boTrav",
            "boURN",
            "deFacil",
            "deGrade",
            "deMgr",
            "deType",
        ]

    def test_variables_len(self, web_visits):
        assert len(web_visits.variables) == 6


class TestVariableNamesAccessor:
    def test_variable_names_getitem(self, households):
        region = households.variables.names["hoRegion"]
        assert region.description == "Region"

    def test_variable_names_getitem_try_desc(self, households):
        with pytest.raises(KeyError) as exc_info:
            region_will_fail = households.variables.names["Region"]
        assert exc_info.value.args[0] == (
            "Lookup key 'Region' did not match a variable name."
        )

    def test_variable_names_iter(self, households):
        household_vars = [
            name
            for name in households.variables.names
            if not households.variables.names[name].is_virtual
        ]
        assert sorted(household_vars) == [
            "HHCarmak",
            "fs$PSS",
            "hoAddr",
            "hoJustAC",
            "hoPCode",
            "hoPSect",
            "hoRegion",
            "hoTel",
            "hoTown",
            "hoURN",
        ]


class TestVariableDescsAccessor:
    def test_variable_descs_getitem(self, people):
        surname = people.variables.descs["Surname"]
        assert surname.name == "peSName"

    def test_variable_descs_getitem_try_name(self, people):
        with pytest.raises(KeyError) as exc_info:
            peoccu_will_fail = people.variables.descs["peOccu"]
        assert exc_info.value.args[0] == (
            "Lookup key 'peOccu' did not match a variable description."
        )

    def test_variable_descs_iter(self, people):
        people_vars = [
            desc
            for desc in people.variables.descs
            if not people.variables.descs[desc].is_virtual
        ]
        assert sorted(people_vars) == [
            "Contact Permission",
            "DOB",
            "Email Address",
            "Income",
            "Initial",
            "Newspapers",
            "Occupation",
            "Person URN",
            "Source",
            "Surname",
            "Title",
        ]

    def test_variables_descriptions_alias(self, people):
        income = people.variables.descriptions["Income"]
        assert income.name == "peIncome"
