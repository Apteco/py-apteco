from datetime import datetime

import pandas as pd
import pytest

from apteco.query import (
    ArrayClause,
    BooleanClause,
    DateListClause,
    DateRangeClause,
    DateTimeRangeClause,
    FlagArrayClause,
    NumericClause,
    SelectorClause,
    TableClause,
    TextClause,
)
from tests.integration_tests.cube_integration_test import assert_cube_dataframes_match


class TestSelectorClause:
    def test_selector_clause(self, holidays, bookings, people, households):
        sweden = SelectorClause(bookings["boDest"], ["29"], session=holidays)
        assert sweden.count() == 25207

        high_earners = SelectorClause(
            people["peIncome"], [f"{i:02}" for i in range(7, 12)], session=holidays
        )
        assert high_earners.count() == 7114

        not_student = SelectorClause(
            people["peOccu"], ["4"], include=False, session=holidays
        )
        assert not_student.count() == 1_029_708

        england = SelectorClause(
            households["hoRegion"],
            ["10", "11", "12", "14"],
            include=False,
            session=holidays,
        )
        assert england.count() == 627_550


class TestCombinedCategoriesClause:
    @pytest.mark.xfail(reason="Not yet implemented.")
    def test_combined_categories_clause(self):
        raise NotImplementedError


class TestNumericClause:
    def test_array_clause(self, holidays, households):
        mazda = ArrayClause(households["HHCarmak"], ["MAZ"], session=holidays)
        assert mazda.count() == 3587

        any_v = ArrayClause(
            households["HHCarmak"], ["VAU", "VLK", "VOL"], session=holidays
        )
        assert any_v.count() == 12418

        anything_but_ford = ArrayClause(
            households["HHCarmak"], ["FOR"], include=False, session=holidays
        )
        assert anything_but_ford.count() == 690_951

        exclude_top_6 = ArrayClause(
            households["HHCarmak"],
            ["FIA", "KIA", "  !", "CHE", "SUZ", "DAI"],
            include=False,
            session=holidays,
        )
        assert exclude_top_6.count() == 236_798

        mazda_and = ArrayClause(
            households["HHCarmak"], ["MAZ"], "AND", session=holidays
        )
        assert mazda_and.count() == 3587  # should be same as with OR

        all_aud_toy_vau = ArrayClause(
            households["HHCarmak"], ["AUD", "TOY", "VAU"], "AND", session=holidays
        )
        assert all_aud_toy_vau.count() == 34

        anything_but_ford_and = ArrayClause(
            households["HHCarmak"], ["FOR"], "AND", include=False, session=holidays
        )
        assert anything_but_ford_and.count() == 690_951  # should be same as with OR

        exclude_both_fiat_kia = ArrayClause(
            households["HHCarmak"],
            ["FIA", "KIA"],
            "AND",
            include=False,
            session=holidays,
        )
        assert exclude_both_fiat_kia.count() == 742_265


class TestTextClause:
    def test_flag_array_clause(self, holidays, people, bookings):
        ft_readers = FlagArrayClause(
            people["peNews"], ["Financial Times"], session=holidays
        )
        assert ft_readers.count() == 11470

        broadsheet_readers = FlagArrayClause(
            people["peNews"],
            [
                "Financial Times",
                "The Times",
                "Daily Telegraph",
                "The Guardian",
                "Independent",
            ],
            session=holidays,
        )
        assert broadsheet_readers.count() == 531_936

        cant_email = FlagArrayClause(
            people["peContac"], ["EPS"], include=False, session=holidays
        )
        assert cant_email.count() == 1_062_397

        no_activities = FlagArrayClause(
            bookings["deFacil"],
            ["Entertainment", "Kidsclub", "Trips"],
            include=False,
            session=holidays,
        )
        assert no_activities.count() == 75774

        ft_readers_and = FlagArrayClause(
            people["peNews"], ["Financial Times"], "AND", session=holidays
        )
        assert ft_readers_and.count() == 11470  # should be same as with OR

        trips_and_ents = FlagArrayClause(
            bookings["deFacil"], ["Trips", "Entertainment"], "AND", session=holidays
        )
        assert trips_and_ents.count() == 674_890

        cant_email_and = FlagArrayClause(
            people["peContac"], ["EPS"], "AND", include=False, session=holidays
        )
        assert cant_email_and.count() == 1_062_397  # should be same as with OR

        not_both_m = FlagArrayClause(
            people["peNews"],
            ["Daily Mail", "Daily Mirror"],
            "AND",
            include=False,
            session=holidays,
        )
        assert not_both_m.count() == 1_148_318


class TestArrayClause:
    def test_numeric_clause(self, holidays, policies, bookings, web_visits):
        thirty_days_to_travel = NumericClause(
            policies["PoDaysUn"], ["30"], session=holidays
        )
        assert thirty_days_to_travel.count() == 2647

        multiple_of_100 = NumericClause(
            bookings["boCost"], [str(i * 100) for i in range(285)], session=holidays
        )
        assert multiple_of_100.count() == 3123

        profit_not_33_33 = NumericClause(
            bookings["boProfit"], ["33.33"], include=False, session=holidays
        )
        assert profit_not_33_33.count() == 2_129_833

        more_than_5_days_until_travel = NumericClause(
            policies["PoDaysUn"],
            ["0", "1", "2", "3", "4", "5"],
            include=False,
            session=holidays,
        )
        assert more_than_5_days_until_travel.count() == 172_044

        low_profit = NumericClause(bookings["boProfit"], ["<=25"], session=holidays)
        assert low_profit.count() == 211_328

        cost_at_least_2k = NumericClause(
            bookings["boCost"], [">=2000"], session=holidays
        )
        assert cost_at_least_2k.count() == 53267

        less_than_minute = NumericClause(
            web_visits["wvDuratn"], ["<60"], session=holidays
        )
        assert less_than_minute.count() == 44399

        more_than_8_weeks = NumericClause(
            policies["PoDaysSi"], [">56"], session=holidays
        )
        assert more_than_8_weeks.count() == 23950

        not_le_8_weeks = NumericClause(
            policies["PoDaysSi"], ["<=56"], include=False, session=holidays
        )
        assert not_le_8_weeks.count() == 23950  # should be same as > with include

        not_ge_minute = NumericClause(
            web_visits["wvDuratn"], [">=60"], include=False, session=holidays
        )
        # should be same as < with include... but there are missing values
        assert not_ge_minute.count() == 44399 + 8673

        cost_not_less_than_2k = NumericClause(
            bookings["boCost"], ["<2000"], include=False, session=holidays
        )
        assert cost_not_less_than_2k.count() == 53267

        not_high_profit = NumericClause(
            bookings["boProfit"], [">25"], include=False, session=holidays
        )
        # should be same as > with include... but there are missing values
        assert not_high_profit.count() == 211_328 + 67012


class TestFlagArrayClause:
    def test_text_clause_is(self, holidays, people):
        smith = TextClause(people["peSName"], ["Smith"], session=holidays)
        assert smith.count() == 13302

        vowel_initial = TextClause(people["peInit"], list("AEIOU"), session=holidays)
        assert vowel_initial.count() == 168_548

        not_t_initial = TextClause(
            people["peInit"], ["T"], include=False, session=holidays
        )
        assert not_t_initial.count() == 1_051_815

        outside_top_5_surnames = TextClause(
            people["peSName"],
            ["Smith", "Brown", "Jones", "Taylor", "Patel"],
            include=False,
            session=holidays,
        )
        assert outside_top_5_surnames.count() == 1_113_731

    def test_text_clause_contains(self, holidays, people, households):
        gmail_emails = TextClause(
            people["peEmail"], ["gmail"], "Contains", session=holidays
        )
        assert gmail_emails.count() == 20787

        address_without_1 = TextClause(
            households["hoAddr"], ["1"], "Contains", include=False, session=holidays
        )
        assert address_without_1.count() == 480_860

        triple_digit_telephone = TextClause(
            households["hoTel"],
            [str(i) * 3 for i in range(10)],
            "Contains",
            session=holidays,
        )
        assert triple_digit_telephone.count() == 53962

        xz_surname = TextClause(
            people["peSName"], ["x", "z"], "Contains", False, session=holidays
        )
        assert xz_surname.count() == 25178

        no_vowel_surname = TextClause(
            people["peSName"],
            list("AEIOU"),
            "Contains",
            False,
            include=False,
            session=holidays,
        )
        assert no_vowel_surname.count() == 2966

    def test_text_clause_begins(self, holidays, people, households, web_visits):
        scottish_surname = TextClause(
            people["peSName"], ["Mc", "Mac"], "Begins", False, session=holidays
        )
        assert scottish_surname.count() == 28303

        coventry_postcode = TextClause(
            households["hoPCode"], ["CV"], "Begins", session=holidays
        )
        assert coventry_postcode.count() == 9267

        not_cheap_domain_visits = TextClause(
            web_visits["wvURL"],
            ["www.onecheapholiday.co.uk", "www.shabbychichotels.co.uk"],
            "Begins",
            include=False,
            session=holidays,
        )
        assert not_cheap_domain_visits.count() == 223_658

        not_t_surname = TextClause(
            people["peSName"], ["t"], "Begins", False, include=False, session=holidays
        )
        assert not_t_surname.count() == 1_108_912

    def test_text_clause_ends(self, holidays, people, households):
        son_surname = TextClause(
            people["peSName"], ["son", "SON"], "Ends", True, session=holidays
        )
        assert son_surname.count() == 62775

        no_dot_com_email = TextClause(
            people["peEmail"], [".com"], "Ends", include=False, session=holidays
        )
        assert no_dot_com_email.count() == 451_433

        not_common_road_type = TextClause(
            households["hoAddr"],
            [" Road", " Close", " Avenue", " Drive", " Street"],
            "Ends",
            False,
            include=False,
            session=holidays,
        )
        assert not_common_road_type.count() == 303_948

        profession_surnames = TextClause(
            people["peSName"], ["er"], "Ends", False, session=holidays
        )
        assert profession_surnames.count() == 89460

    def test_text_clause_ranges(self, holidays, households):
        early_postcode = TextClause(
            households["hoPCode"], ['<="E"'], "Ranges", session=holidays
        )
        assert early_postcode.count() == 208_569

        further_down_street = TextClause(
            households["hoAddr"], ['>="9"'], "Ranges", session=holidays
        )
        assert further_down_street.count() == 31197

    def test_text_clause_wildcards(self, holidays, people, households):
        like_smith = TextClause(
            people["peSName"], ['="Sm?th"'], "Ranges", session=holidays
        )
        assert like_smith.count() == 13653

        like_smith_long = TextClause(
            people["peSName"], ['="Sm?th*"'], "Ranges", session=holidays
        )
        assert like_smith_long.count() == 14172

        no_space_address = TextClause(
            households["hoAddr"], ['="* *"'], "Ranges", include=False, session=holidays
        )
        assert no_space_address.count() == 366

        two_digit_high_street = TextClause(
            households["hoAddr"],
            ['="?? High Street"'],
            "Ranges",
            False,
            session=holidays,
        )
        assert two_digit_high_street.count() == 2187

        not_10_something_road = TextClause(
            households["hoAddr"],
            ['="10 *Road"'],
            "Ranges",
            False,
            include=False,
            session=holidays,
        )
        assert not_10_something_road.count() == 739_313

        surname_5_long_2_4_vowels = TextClause(
            people["peSName"],
            [f'="?{i}?{j}?"' for i in list("aeiou") for j in list("aeiou")],
            "Ranges",
            session=holidays,
        )
        assert surname_5_long_2_4_vowels.count() == 59824

        like_short_middle_long = TextClause(
            people["peSName"],
            ['="Sh?rt"', '="M?ddle*"', '="Lo*ng"'],
            "Ranges",
            session=holidays,
        )
        assert like_short_middle_long.count() == 2121

        not_common_email_domains = TextClause(
            people["peEmail"],
            [
                f'="*@*{i}.{j}"'
                for i in ("Mail", "Post")
                for j in ("com", "uk.com", "co.uk")
            ],
            "Ranges",
            include=False,
            session=holidays,
        )
        assert not_common_email_domains.count() == 948_831

        smith_like_double_barrelled = TextClause(
            people["peSName"],
            ['="Sm?th-*"', '="*-Sm?th"'],
            "Ranges",
            False,
            session=holidays,
        )
        assert smith_like_double_barrelled.count() == 660

        first_2_not_vowel = TextClause(
            people["peSName"],
            [f'="{i}{j}*"' for i in ("", "?") for j in list("aeiou")],
            "Ranges",
            False,
            include=False,
            session=holidays,
        )
        assert first_2_not_vowel.count() == 295_815


class TestDateListClause:
    def test_date_list_clause(self, holidays, bookings, policies):
        valentines_day_2018 = DateListClause(
            bookings["boTrav"], ["20180214"], session=holidays
        )
        assert valentines_day_2018.count() == 625

        bank_holidays_2020 = DateListClause(
            bookings["boDate"],
            [
                "20200101",
                "20200410",
                "20200413",
                "20200508",
                "20200525",
                "20200831",
                "20201225",
                "20201226",
            ],
            session=holidays,
        )
        assert bank_holidays_2020.count() == 7847

        not_easter_2017 = DateListClause(
            policies["PoTrave1"], ["20170416"], include=False, session=holidays
        )
        assert not_easter_2017.count() == 213_442  # all - 125

        exclude_solstices_and_equinoxes_2021 = DateListClause(
            policies["PoPolic1"],
            ["20210320", "20210621", "20210922", "20211221"],
            include=False,
            session=holidays,
        )
        assert exclude_solstices_and_equinoxes_2021.count() == 213_109  # all - 458


class TestDateRangeClause:
    def test_date_range_clause(self, holidays, bookings, policies):
        olympics_summer_16_to_winter_18 = DateRangeClause(
            bookings["boTrav"], "2016-08-22", "2018-02-08", session=holidays
        )
        assert olympics_summer_16_to_winter_18.count() == 328_733

        before_tax_year_end_2018_19 = DateRangeClause(
            policies["PoBooki1"], "Earliest", "2019-04-05", session=holidays
        )
        assert before_tax_year_end_2018_19.count() == 185_601

        after_christmas_2016 = DateRangeClause(
            bookings["boDate"], "2016-12-26", "Latest", session=holidays
        )
        assert after_christmas_2016.count() == 1_915_257

        earliest_to_latest_policy_date = DateRangeClause(
            policies["PoPolic1"], "Earliest", "Latest", session=holidays
        )
        assert earliest_to_latest_policy_date.count() == 213_567

        not_between_world_cup_18_euro_20 = DateRangeClause(
            policies["PoTrave1"],
            "2018-07-16",
            "2020-06-11",
            include=False,
            session=holidays,
        )
        assert not_between_world_cup_18_euro_20.count() == 151_691

        not_before_christmas_2016 = DateRangeClause(
            bookings["boDate"],
            "Earliest",
            "2016-12-25",
            include=False,
            session=holidays,
        )
        assert not_before_christmas_2016.count() == 1_915_257

        not_after_tax_year_end_2018_19 = DateRangeClause(
            policies["PoBooki1"],
            "2019-04-06",
            "Latest",
            include=False,
            session=holidays,
        )
        assert not_after_tax_year_end_2018_19.count() == 185_601

        not_earliest_to_latest_booking = DateRangeClause(
            bookings["boDate"], "Earliest", "Latest", include=False, session=holidays
        )
        assert not_earliest_to_latest_booking.count() == 0


class TestTimeRangeClause:
    @pytest.mark.xfail(reason="Not yet implemented.")
    def test_time_range_clause(self):
        raise NotImplementedError


class TestDateTimeRangeClause:
    def test_datetime_range_clause(self, holidays, communications, web_visits):
        during_week_29_2016 = DateTimeRangeClause(
            communications["cmCommDt"],
            "2016-07-18T08:00:00",
            "2016-07-22T17:59:59",
            session=holidays,
        )
        assert during_week_29_2016.count() == 19298

        before_4pm_halloween_2019 = DateTimeRangeClause(
            web_visits["wvTime"], "Earliest", "2019-10-31T15:59:59", session=holidays
        )
        assert before_4pm_halloween_2019.count() == 169_019

        after_juy_2016 = DateTimeRangeClause(
            communications["cmCommDt"],
            "2016-08-01T00:00:00",
            "Latest",
            session=holidays,
        )
        assert after_juy_2016.count() == 3926

        all_web_visits = DateTimeRangeClause(
            web_visits["wvTime"], "Earliest", "Latest", session=holidays
        )
        assert all_web_visits.count() == 279_538

        not_during_lent_2021 = DateTimeRangeClause(
            web_visits["wvTime"],
            "2021-02-17T07:18:00",
            "2021-04-03T19:44:00",
            include=False,
            session=holidays,
        )
        assert not_during_lent_2021.count() == 270_245  # all - 9293

        not_before_july_2016 = DateTimeRangeClause(
            communications["cmCommDt"],
            "Earliest",
            "2016-07-31T23:59:59",
            include=False,
            session=holidays,
        )
        assert not_before_july_2016.count() == 3926

        not_after_4pm_halloween_2019 = DateTimeRangeClause(
            web_visits["wvTime"],
            "2019-10-31T16:00:00",
            "Latest",
            include=False,
            session=holidays,
        )
        assert not_after_4pm_halloween_2019.count() == 169_019

        not_all_communications = DateTimeRangeClause(
            communications["cmCommDt"],
            "Earliest",
            "Latest",
            include=False,
            session=holidays,
        )
        assert not_all_communications.count() == 0


class TestReferenceClause:
    @pytest.mark.xfail(reason="Not yet implemented.")
    def test_reference_clause(self):
        raise NotImplementedError


@pytest.fixture()
def sweden(holidays, bookings):
    return SelectorClause(bookings["boDest"], ["29"], session=holidays)


@pytest.fixture()
def single_product(holidays, bookings):
    return SelectorClause(bookings["boProd"], ["0", "2"], session=holidays)


@pytest.fixture()
def high_earners(holidays, people):
    return SelectorClause(
        people["peIncome"], [f"{i:02}" for i in range(7, 12)], session=holidays
    )


@pytest.fixture()
def white_collar_jobs(holidays, people):
    return SelectorClause(people["peOccu"], ["1", "2", "3"], session=holidays)


@pytest.fixture()
def london_south_east(holidays, households):
    return SelectorClause(households["hoRegion"], ["03", "09"], session=holidays)


@pytest.fixture()
def unclassified_response(holidays, bookings):
    return SelectorClause(bookings["boKeyCd"], ["       !"], session=holidays)


@pytest.fixture()
def various_sources(holidays, people):
    return SelectorClause(
        people["peSource"], ["05", "09", "10", "12", "27"], session=holidays
    )


@pytest.fixture()
def suggested_booking(holidays, responses):
    return SelectorClause(responses["raRspTyp"], ["6", "8", "10"], session=holidays)


@pytest.fixture()
def mazda(holidays, households):
    return ArrayClause(households["HHCarmak"], ["MAZ"], session=holidays)


@pytest.fixture()
def vowel_initial(holidays, people):
    return TextClause(people["peInit"], list("AEIOU"), session=holidays)


class TestClause:
    def test_boolean_operator(
        self, sweden, single_product, high_earners, white_collar_jobs, london_south_east
    ):
        single_sweden = sweden & single_product
        assert single_sweden.count() == 2541

        high_potential = high_earners | white_collar_jobs
        assert high_potential.count() == 114_621

        not_london_south_east = ~london_south_east
        assert not_london_south_east.count() == 504_029

    @pytest.mark.xfail(
        reason="Inserting more clauses into existing boolean clause not implemented."
    )
    def test_boolean_operator_multiple(
        self,
        sweden,
        single_product,
        unclassified_response,
        high_earners,
        white_collar_jobs,
        various_sources,
    ):
        triple_and = sweden & single_product & unclassified_response
        assert len(triple_and.operands) == 3
        assert sweden in triple_and.operands
        assert single_product in triple_and.operands
        assert unclassified_response in triple_and.operands
        assert triple_and.count() == 1989

        triple_or = high_earners | white_collar_jobs | various_sources
        assert len(triple_or.operands) == 3
        assert high_earners in triple_or.operands
        assert white_collar_jobs in triple_or.operands
        assert various_sources in triple_or.operands
        assert triple_or.count() == 129_655

    def test_table_operator(
        self,
        households,
        people,
        responses,
        sweden,
        suggested_booking,
        mazda,
        vowel_initial,
    ):
        been_to_sweden = people * sweden
        assert been_to_sweden.count() == 25175

        house_suggested_booking = suggested_booking * households
        assert house_suggested_booking.count() == 695

        mazda_drivers = mazda * people
        assert mazda_drivers.count() == 6959

        responses_by_vowels = responses * vowel_initial
        assert responses_by_vowels.count() == 216


class TestBooleanClause:
    def test_boolean_clause(
        self,
        holidays,
        bookings,
        people,
        households,
        sweden,
        single_product,
        unclassified_response,
        high_earners,
        white_collar_jobs,
        various_sources,
        london_south_east,
    ):
        single_sweden = BooleanClause(
            bookings, "AND", [sweden, single_product], session=holidays
        )
        assert single_sweden.count() == 2541

        triple_and = BooleanClause(
            bookings,
            "AND",
            [sweden, single_product, unclassified_response],
            session=holidays,
        )
        assert triple_and.count() == 1989

        high_potential = BooleanClause(
            people, "OR", [high_earners, white_collar_jobs], session=holidays
        )
        assert high_potential.count() == 114_621

        triple_or = BooleanClause(
            people,
            "OR",
            [high_earners, white_collar_jobs, various_sources],
            session=holidays,
        )
        assert triple_or.count() == 129_655

        not_london_south_east = BooleanClause(
            households, "NOT", [london_south_east], session=holidays
        )
        assert not_london_south_east.count() == 504_029


class TestTableClause:
    def test_table_clause(
        self,
        holidays,
        people,
        responses,
        households,
        communications,
        sweden,
        suggested_booking,
        mazda,
        vowel_initial,
    ):
        been_to_sweden = TableClause(people, "ANY", sweden, session=holidays)
        assert been_to_sweden.count() == 25175

        house_suggested_booking = TableClause(
            households,
            "ANY",
            TableClause(
                people,
                "ANY",
                TableClause(communications, "ANY", suggested_booking, session=holidays),
                session=holidays,
            ),
            session=holidays,
        )
        assert house_suggested_booking.count() == 695

        mazda_drivers = TableClause(people, "THE", mazda, session=holidays)
        assert mazda_drivers.count() == 6959

        responses_by_vowels = TableClause(
            responses,
            "THE",
            TableClause(communications, "THE", vowel_initial, session=holidays),
            session=holidays,
        )
        assert responses_by_vowels.count() == 216


class TestClauseDataGrid:
    def test_clause_datagrid_to_df_web_visits_mobile_social_media_1500_rows_all_columns(
        self,
        web_visits,
        datagrid_003_web_visits_mobile_social_media_1500_rows_all_columns,
    ):
        web_visits_mobile_social_media = (web_visits["wvSource"] == "S") & (
            web_visits["wvDevice"] == "3"
        )

        web_visits_dg = web_visits_mobile_social_media.datagrid(
            [
                web_visits[var]
                for var in (
                    "Web URN",  # Reference (Numeric)
                    "URL",  # Text
                    "Web Visit Time",  # DateTime
                    "Device Type",  # Selector
                    "Duration",  # Numeric (0 dp, with missing)
                    "Original Source",  # Selector
                )
            ],
            max_rows=1500,
        )
        web_visits_df = web_visits_dg.to_df()

        pd.testing.assert_frame_equal(
            web_visits_df,
            datagrid_003_web_visits_mobile_social_media_1500_rows_all_columns,
        )

    def test_clause_datagrid_to_df_bookings_500_rows_households_selection(
        self, households, bookings, datagrid_004_bookings_with_households_selection
    ):
        north_west_streets = (households["Region"] == "02") & households[
            "Address"
        ].contains("street", match_case=False)

        bookings_dg = north_west_streets.datagrid(
            [
                bookings[var]
                for var in (
                    "Booking URN",  # Reference (Numeric)
                    "Destination",  # Selector
                    "Travel Date",  # Date
                    "Type",  # Selector
                    "Profit",  # Currency (2 dp)
                )
            ],
            table=bookings,
        )
        bookings_df = bookings_dg.to_df()

        pd.testing.assert_frame_equal(
            bookings_df,
            datagrid_004_bookings_with_households_selection,
            check_dtype=False,
        )


class TestClauseCube:
    def test_cube_to_df_bookings_before_2020_cost_less_than_500(
        self, bookings, cube_002_bookings_before_2020_cost_less_than_500
    ):
        before_2020_cost_less_than_500 = (bookings["Cost"] < 500) & (
            bookings["boDate"] <= datetime(2019, 12, 31)
        )

        cube = before_2020_cost_less_than_500.cube(
            [bookings[var] for var in ("Destination", "Product", "Response Code")]
        )
        df = cube.to_df()

        assert_cube_dataframes_match(
            df, cube_002_bookings_before_2020_cost_less_than_500
        )

    def test_cube_to_df_bookings_dimensions_households_selection_people_table(
        self,
        households,
        people,
        bookings,
        cube_004_bookings_dimensions_households_selection_people_table,
    ):
        north_west_or_f_car = (households["Region"] == ("02", "13")) | (
            households["HHCarmak"] == ("FER", "FIA", "FOR")
        )

        cube = north_west_or_f_car.cube(
            [bookings[var] for var in ("Product", "Continent")], table=people
        )
        df = cube.to_df()

        assert_cube_dataframes_match(
            df, cube_004_bookings_dimensions_households_selection_people_table
        )

    def test_cube_to_df_mixed_hhds_jnys_ppl_dimensions_people_selection_journeys_table(
        self,
        households,
        people,
        bookings,
        journeys,
        cube_006_mixed_hhds_jnys_ppl_dimensions_people_selection_journeys_table,
    ):

        surname_contains_python_type_or_distant_trip = (
            people["Surname"].contains(["int", "str", "bool"], match_case=False)
        ) | (bookings["Continent"] == ("AM", "AU"))

        cube = surname_contains_python_type_or_distant_trip.cube(
            [households["Region"], journeys["Pool"], people["Gender"]], table=journeys
        )
        df = cube.to_df()

        assert_cube_dataframes_match(
            df, cube_006_mixed_hhds_jnys_ppl_dimensions_people_selection_journeys_table
        )
