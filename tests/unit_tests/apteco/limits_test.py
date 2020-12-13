from decimal import Decimal
from fractions import Fraction
from numbers import Integral, Rational, Real
from unittest.mock import Mock

import apteco_api as aa
import pandas as pd
import pytest

from apteco.query import LimitClause, SelectorClause, ensure_single_or_range


class FractionableDecimal(Decimal, Rational):
    """Class used for testing with LimitClause `fraction` parameter."""

    @property
    def numerator(self):
        return self.as_integer_ratio()[0]

    @property
    def denominator(self):
        return self.as_integer_ratio()[1]


@pytest.fixture()
def electronics(rtl_var_purchase_department):
    return SelectorClause(rtl_var_purchase_department, ["Electronics"])


class TestLimitClause:
    def test_limit_clause_total_correct_type(self, electronics, rtl_session):
        limit_2500 = LimitClause(electronics, 2500, session=rtl_session)
        assert limit_2500.kind == "Total"
        assert limit_2500.total == 2500
        assert limit_2500.percent is None
        assert limit_2500.fraction is None
        assert limit_2500.sample_type == "First"
        assert limit_2500.skip_first == 0
        assert limit_2500.label is None
        assert limit_2500.session is rtl_session

    def test_limit_clause_total_needs_converting(self, electronics, rtl_session):
        s = pd.Series([654]).astype("int32")
        limit_654_from_pd_series = LimitClause(electronics, s[0], session=rtl_session)
        assert limit_654_from_pd_series.kind == "Total"
        assert limit_654_from_pd_series.total == 654
        assert limit_654_from_pd_series.percent is None
        assert limit_654_from_pd_series.fraction is None
        assert limit_654_from_pd_series.sample_type == "First"
        assert limit_654_from_pd_series.skip_first == 0
        assert limit_654_from_pd_series.label is None
        assert limit_654_from_pd_series.session is rtl_session

    def test_limit_clause_total_not_integral(self, electronics, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            limit_total_as_float = LimitClause(electronics, 17.5, session=rtl_session)
        assert exc_info.value.args[0] == "`total` must be an integer greater than 0"

        with pytest.raises(ValueError) as exc_info:
            limit_total_as_float_no_fractional_part = LimitClause(
                electronics, 5.2e5, session=rtl_session
            )
        assert exc_info.value.args[0] == "`total` must be an integer greater than 0"

    def test_limit_clause_total_less_than_1(self, electronics, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            limit_total_is_0 = LimitClause(electronics, 0, session=rtl_session)
        assert exc_info.value.args[0] == "`total` must be an integer greater than 0"

        with pytest.raises(ValueError) as exc_info:
            limit_total_negative = LimitClause(electronics, -300, session=rtl_session)
        assert exc_info.value.args[0] == "`total` must be an integer greater than 0"

        with pytest.raises(ValueError) as exc_info:
            limit_total_too_small_and_not_int = LimitClause(
                electronics, 0.125, session=rtl_session
            )
        assert exc_info.value.args[0] == "`total` must be an integer greater than 0"

    def test_limit_clause_percent_correct_type(self, electronics, rtl_session):
        limit_0_6_pct = LimitClause(electronics, percent=0.6, session=rtl_session)
        assert limit_0_6_pct.kind == "Percent"
        assert limit_0_6_pct.total is None
        assert limit_0_6_pct.percent == 0.6
        assert limit_0_6_pct.fraction is None
        assert limit_0_6_pct.sample_type == "First"
        assert limit_0_6_pct.skip_first == 0
        assert limit_0_6_pct.label is None
        assert limit_0_6_pct.session is rtl_session

    def test_limit_clause_percent_needs_converting(self, electronics, rtl_session):
        limit_127_2000_pct = LimitClause(
            electronics, percent=Fraction("127/20"), session=rtl_session
        )
        assert limit_127_2000_pct.kind == "Percent"
        assert limit_127_2000_pct.total is None
        assert limit_127_2000_pct.percent == 6.35
        assert limit_127_2000_pct.fraction is None
        assert limit_127_2000_pct.sample_type == "First"
        assert limit_127_2000_pct.skip_first == 0
        assert limit_127_2000_pct.label is None
        assert limit_127_2000_pct.session is rtl_session

    def test_limit_clause_percent_not_real(self, electronics, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            limit_percent_as_complex = LimitClause(
                electronics, percent=13.87 + 951.84j, session=rtl_session
            )
        assert (
            exc_info.value.args[0]
            == "`percent` must be a number between 0–100 (exclusive)"
        )

        with pytest.raises(ValueError) as exc_info:
            limit_percent_as_str = LimitClause(
                electronics, percent="7.25", session=rtl_session
            )
        assert (
            exc_info.value.args[0]
            == "`percent` must be a number between 0–100 (exclusive)"
        )

    def test_limit_clause_percent_out_of_range(self, electronics, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            limit_percent_is_0 = LimitClause(
                electronics, percent=0, session=rtl_session
            )
        assert (
            exc_info.value.args[0]
            == "`percent` must be a number between 0–100 (exclusive)"
        )

        with pytest.raises(ValueError) as exc_info:
            limit_percent_too_small = LimitClause(
                electronics, percent=-1.5, session=rtl_session
            )
        assert (
            exc_info.value.args[0]
            == "`percent` must be a number between 0–100 (exclusive)"
        )

        with pytest.raises(ValueError) as exc_info:
            limit_percent_is_100 = LimitClause(
                electronics, percent=100, session=rtl_session
            )
        assert (
            exc_info.value.args[0]
            == "`percent` must be a number between 0–100 (exclusive)"
        )

        with pytest.raises(ValueError) as exc_info:
            limit_percent_too_big = LimitClause(
                electronics, percent=144.1, session=rtl_session
            )
        assert (
            exc_info.value.args[0]
            == "`percent` must be a number between 0–100 (exclusive)"
        )

    def test_limit_clause_fraction_correct_type(self, electronics, rtl_session):
        limit_2_9_frac = LimitClause(
            electronics, fraction=Fraction(2, 9), session=rtl_session
        )
        assert limit_2_9_frac.kind == "Fraction"
        assert limit_2_9_frac.total is None
        assert limit_2_9_frac.percent is None
        assert limit_2_9_frac.fraction.numerator == 2
        assert limit_2_9_frac.fraction.denominator == 9
        assert limit_2_9_frac.sample_type == "First"
        assert limit_2_9_frac.skip_first == 0
        assert limit_2_9_frac.label is None
        assert limit_2_9_frac.session is rtl_session

    def test_limit_clause_fraction_needs_converting(self, electronics, rtl_session):
        limit_custom_rational_class = LimitClause(
            electronics, fraction=FractionableDecimal("0.0265"), session=rtl_session
        )
        assert limit_custom_rational_class.kind == "Fraction"
        assert limit_custom_rational_class.total is None
        assert limit_custom_rational_class.percent is None
        assert limit_custom_rational_class.fraction.numerator == 53
        assert limit_custom_rational_class.fraction.denominator == 2000
        assert limit_custom_rational_class.sample_type == "First"
        assert limit_custom_rational_class.skip_first == 0
        assert limit_custom_rational_class.label is None
        assert limit_custom_rational_class.session is rtl_session

    def test_limit_clause_fraction_not_rational(self, electronics, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            limit_fraction_as_float = LimitClause(
                electronics, fraction=0.3333, session=rtl_session
            )
        assert (
            exc_info.value.args[0]
            == "`fraction` must be a rational number between 0 and 1 (exclusive)"
        )

        with pytest.raises(ValueError) as exc_info:
            limit_fraction_as_str = LimitClause(
                electronics, fraction="2/17", session=rtl_session
            )
        assert (
            exc_info.value.args[0]
            == "`fraction` must be a rational number between 0 and 1 (exclusive)"
        )

    def test_limit_clause_fraction_out_of_range(self, electronics, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            limit_fraction_is_0 = LimitClause(
                electronics, fraction=0, session=rtl_session
            )
        assert (
            exc_info.value.args[0]
            == "`fraction` must be a rational number between 0 and 1 (exclusive)"
        )

        with pytest.raises(ValueError) as exc_info:
            limit_fraction_too_small = LimitClause(
                electronics, fraction=Fraction(-4, 100), session=rtl_session
            )
        assert (
            exc_info.value.args[0]
            == "`fraction` must be a rational number between 0 and 1 (exclusive)"
        )

        with pytest.raises(ValueError) as exc_info:
            limit_fraction_is_1 = LimitClause(
                electronics, fraction=1, session=rtl_session
            )
        assert (
            exc_info.value.args[0]
            == "`fraction` must be a rational number between 0 and 1 (exclusive)"
        )

        with pytest.raises(ValueError) as exc_info:
            limit_fraction_too_big = LimitClause(
                electronics, fraction=Fraction(4, 3), session=rtl_session
            )
        assert (
            exc_info.value.args[0]
            == "`fraction` must be a rational number between 0 and 1 (exclusive)"
        )

    def test_limit_clause_skip_first_correct_type(self, electronics, rtl_session):
        limit_skip_82 = LimitClause(
            electronics, 55000, skip_first=82, session=rtl_session
        )
        assert limit_skip_82.kind == "Total"
        assert limit_skip_82.total == 55000
        assert limit_skip_82.percent is None
        assert limit_skip_82.fraction is None
        assert limit_skip_82.sample_type == "First"
        assert limit_skip_82.skip_first == 82
        assert limit_skip_82.label is None
        assert limit_skip_82.session is rtl_session

    def test_limit_clause_skip_first_needs_converting(self, electronics, rtl_session):
        limit_skip_1_as_true = LimitClause(
            electronics, percent=64.2, skip_first=True, session=rtl_session
        )
        assert limit_skip_1_as_true.kind == "Percent"
        assert limit_skip_1_as_true.total is None
        assert limit_skip_1_as_true.percent == 64.2
        assert limit_skip_1_as_true.fraction is None
        assert limit_skip_1_as_true.sample_type == "First"
        assert limit_skip_1_as_true.skip_first == 1
        assert limit_skip_1_as_true.label is None
        assert limit_skip_1_as_true.session is rtl_session

    def test_limit_clause_skip_first_not_integral(self, electronics, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            limit_skip_first_as_float = LimitClause(
                electronics,
                fraction=Fraction(5 / 18),
                skip_first=0.11,
                session=rtl_session,
            )
        assert exc_info.value.args[0] == "`skip_first` must be a non-negative integer"

    def test_limit_clause_skip_first_less_than_0(self, electronics, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            limit_skip_first_as_float = LimitClause(
                electronics, 42, skip_first=-21, session=rtl_session
            )
        assert exc_info.value.args[0] == "`skip_first` must be a non-negative integer"

    def test_limit_clause_no_value_given(self, electronics, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            electronics_no_value = LimitClause(clause=electronics, session=rtl_session)
        assert (
            exc_info.value.args[0]
            == "Must specify exactly one of `total`, `percent` or `fraction`"
        )

    def test_limit_clause_two_values_given(self, electronics, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            electronics_2_values = LimitClause(
                clause=electronics, total=10, percent=0, session=rtl_session
            )
        assert (
            exc_info.value.args[0]
            == "Must specify exactly one of `total`, `percent` or `fraction`"
        )

    def test_limit_clause_three_values_given(self, electronics, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            electronics_3_values = LimitClause(
                clause=electronics,
                total=10,
                percent=0,
                fraction=Fraction(2, 3),
                session=rtl_session,
            )
        assert (
            exc_info.value.args[0]
            == "Must specify exactly one of `total`, `percent` or `fraction`"
        )

    def test_limit_clause_sample_invalid_type(self, electronics, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            electronics_regular_sample = LimitClause(
                clause=electronics, total=10, sample_type="Regular", session=rtl_session
            )
        assert exc_info.value.args[0] == "Regular is not a valid sample type"

    def test_limit_clause_init(self, electronics, rtl_session):
        electronics_2_thirds_random_skip_first_5 = LimitClause(
            clause=electronics,
            fraction=Fraction(2, 3),
            sample_type="Random",
            skip_first=5,
            session=rtl_session,
        )
        assert electronics_2_thirds_random_skip_first_5.kind == "Fraction"
        assert electronics_2_thirds_random_skip_first_5.total is None
        assert electronics_2_thirds_random_skip_first_5.percent is None
        assert electronics_2_thirds_random_skip_first_5.fraction.numerator == 2
        assert electronics_2_thirds_random_skip_first_5.fraction.denominator == 3
        assert electronics_2_thirds_random_skip_first_5.clause == electronics
        assert electronics_2_thirds_random_skip_first_5.sample_type == "Random"
        assert electronics_2_thirds_random_skip_first_5.skip_first == 5
        assert electronics_2_thirds_random_skip_first_5.table == electronics.table
        assert electronics_2_thirds_random_skip_first_5.label is None
        assert electronics_2_thirds_random_skip_first_5.session == rtl_session

    def test_limit_clause_to_model_selection_frac_is_none(
        self, electronics, rtl_table_purchases, rtl_session
    ):
        electronics._to_model_clause = Mock(
            return_value="Electronics clause model goes here"
        )
        fake_limit_clause = Mock(
            kind="Percent",
            total=None,
            percent=72.96,
            fraction=None,
            sample_type="Stratified",
            skip_first=24,
            clause=electronics,
            table=rtl_table_purchases,
            label="Regular sample of 72.96% of electronics purchases excl. first 24",
            session=rtl_session,
        )
        expected_limit_selection_model = aa.Selection(
            rule=aa.Rule(clause="Electronics clause model goes here"),
            limits=aa.Limits(
                sampling="Stratified",
                total=None,
                type="Percent",
                start_at=24,
                percent=72.96,
                fraction=None,
            ),
            table_name="Purchases",
            name="Regular sample of 72.96% of electronics purchases excl. first 24",
        )
        assert (
            LimitClause._to_model_selection(fake_limit_clause)
            == expected_limit_selection_model
        )
        electronics._to_model_clause.assert_called_once_with()

    def test_limit_clause_to_model_selection_frac_not_none(
        self, electronics, rtl_table_purchases, rtl_session
    ):
        electronics._to_model_clause = Mock(
            return_value="Electronics clause model goes here"
        )
        fake_limit_clause = Mock(
            kind="Fraction",
            total=None,
            percent=None,
            fraction=Fraction(4, 111),
            sample_type="Random",
            skip_first=0,
            clause=electronics,
            table=rtl_table_purchases,
            label="Random 4/111ths of all electronics purchases",
            session=rtl_session,
        )
        expected_limit_selection_model = aa.Selection(
            rule=aa.Rule(clause="Electronics clause model goes here"),
            limits=aa.Limits(
                sampling="Random",
                total=None,
                type="Fraction",
                start_at=0,
                percent=None,
                fraction=aa.Fraction(4, 111),
            ),
            table_name="Purchases",
            name="Random 4/111ths of all electronics purchases",
        )
        assert (
            LimitClause._to_model_selection(fake_limit_clause)
            == expected_limit_selection_model
        )


class TestEnsureSingleOrRangeSingleValueInteger:
    def test_single_value_integer_conversion_superfluous(self):
        kind, output_value = ensure_single_or_range(
            3, Integral, int, "an integer", "the_whole_number"
        )
        assert kind == "single"
        assert output_value == 3

    def test_single_value_integer_needs_converting(self):
        kind, output_value = ensure_single_or_range(
            True, Integral, int, "an integer", "the_whole_number"
        )
        assert kind == "single"
        assert output_value == 1

    def test_single_value_integer_negative_no_range_given(self):
        kind, output_value = ensure_single_or_range(
            -3, Integral, int, "an integer", "the_whole_number"
        )
        assert kind == "single"
        assert output_value == -3

    def test_single_value_integer_bad_type_float_not_int(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                3.0, Integral, int, "an integer", "the_whole_number"
            )
        assert exc_info.value.args[0] == "`the_whole_number` must be an integer"

    def test_single_value_integer_bad_type_str_not_int(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                "3", Integral, int, "an integer", "the_whole_number"
            )
        assert exc_info.value.args[0] == "`the_whole_number` must be an integer"

    def test_single_value_integer_in_range_with_lower_bound(self):
        kind, output_value = ensure_single_or_range(
            4000, Integral, int, "an integer", "the_whole_number", lower_bound=0
        )
        assert kind == "single"
        assert output_value == 4000

    def test_single_value_integer_in_range_with_upper_bound(self):
        kind, output_value = ensure_single_or_range(
            -6789, Integral, int, "an integer", "the_whole_number", upper_bound=54321
        )
        assert kind == "single"
        assert output_value == -6789

    def test_single_value_integer_in_range_with_both_bounds(self):
        kind, output_value = ensure_single_or_range(
            38,
            Integral,
            int,
            "an integer",
            "the_whole_number",
            lower_bound=-273,
            upper_bound=100,
        )
        assert kind == "single"
        assert output_value == 38

    def test_single_value_integer_not_in_range_with_lower_bound(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                2, Integral, int, "an integer", "the_whole_number", lower_bound=5
            )
        assert exc_info.value.args[0] == "`the_whole_number` must be greater than 5"

    def test_single_value_integer_not_in_range_with_upper_bound(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                43, Integral, int, "an integer", "the_whole_number", upper_bound=25
            )
        assert exc_info.value.args[0] == "`the_whole_number` must be less than 25"

    def test_single_value_integer_not_in_range_with_both_bounds_too_big(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                256,
                Integral,
                int,
                "an integer",
                "the_whole_number",
                lower_bound=75,
                upper_bound=100,
            )
        assert exc_info.value.args[0] == "`the_whole_number` must be less than 100"

    def test_single_value_integer_not_in_range_with_both_bounds_too_small(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                -1,
                Integral,
                int,
                "an integer",
                "the_whole_number",
                lower_bound=1,
                upper_bound=20,
            )
        assert exc_info.value.args[0] == "`the_whole_number` must be greater than 1"


class TestEnsureSingleOrRangeSingleValueReal:
    def test_conversion_superfluous(self):
        kind, output_value = ensure_single_or_range(
            4.5, Real, float, "a number", "the_decimal_param"
        )
        assert kind == "single"
        assert output_value == 4.5

    def test_needs_converting(self):
        kind, output_value = ensure_single_or_range(
            Fraction(1357, 25), Real, float, "a number", "the_decimal_param"
        )
        assert kind == "single"
        assert output_value == 54.28

    def test_negative_no_range_given(self):
        kind, output_value = ensure_single_or_range(
            -6.283, Real, float, "a number", "the_decimal_param"
        )
        assert kind == "single"
        assert output_value == -6.283

    def test_bad_type_complex_not_float(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                31.415 + 9.26j, Real, float, "a number", "the_decimal_param"
            )
        assert exc_info.value.args[0] == "`the_decimal_param` must be a number"

    def test_bad_type_str_not_float(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                "2718.28", Real, float, "a number", "the_decimal_param"
            )
        assert exc_info.value.args[0] == "`the_decimal_param` must be a number"

    def test_in_range_with_lower_bound(self):
        kind, output_value = ensure_single_or_range(
            678.678, Real, float, "a number", "the_decimal_param", lower_bound=0
        )
        assert kind == "single"
        assert output_value == 678.678

    def test_in_range_with_upper_bound(self):
        kind, output_value = ensure_single_or_range(
            -67.89, Real, float, "a number", "the_decimal_param", upper_bound=76.76
        )
        assert kind == "single"
        assert output_value == -67.89

    def test_in_range_with_both_bounds(self):
        kind, output_value = ensure_single_or_range(
            200.592,
            Real,
            float,
            "a number",
            "the_number",
            lower_bound=-38.8290,
            upper_bound=356.73,
        )
        assert kind == "single"
        assert output_value == 200.592

    def test_not_in_range_with_lower_bound(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                2.1, Real, float, "a number", "the_decimal_param", lower_bound=5.4
            )
        assert exc_info.value.args[0] == "`the_decimal_param` must be greater than 5.4"

    def test_not_in_range_with_upper_bound(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                43.21, Real, float, "a number", "the_decimal_param", upper_bound=12.34
            )
        assert exc_info.value.args[0] == "`the_decimal_param` must be less than 12.34"

    def test_not_in_range_with_both_bounds_too_big(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                128.256,
                Real,
                float,
                "a number",
                "the_decimal_param",
                lower_bound=0,
                upper_bound=100,
            )
        assert exc_info.value.args[0] == "`the_decimal_param` must be less than 100"

    def test_not_in_range_with_both_bounds_too_small(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                112.223,
                Real,
                float,
                "a number",
                "the_decimal_param",
                lower_bound=554.443,
                upper_bound=6677.7788,
            )
        assert exc_info.value.args[0] == (
            "`the_decimal_param` must be greater than 554.443"
        )


class TestEnsureSingleOrRangeIntegerRange:
    def test_conversion_superfluous(self):
        kind, output_value = ensure_single_or_range(
            (5, 8), Integral, int, "an integer", "the_integral_param"
        )
        assert kind == "range"
        assert output_value == (5, 8)

    def test_one_needs_converting(self):
        kind, output_value = ensure_single_or_range(
            (False, 25), Integral, int, "an integer", "the_integral_param"
        )
        assert kind == "range"
        assert output_value == (0, 25)

    def test_both_need_converting(self):
        s = pd.Series([99]).astype("int64")
        kind, output_value = ensure_single_or_range(
            (True, s[0]), Integral, int, "an integer", "the_integral_param"
        )
        assert kind == "range"
        assert output_value == (1, 99)

    def test_bad_type_float_not_int(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                (0, 100.0), Integral, int, "an integer", "the_integral_param"
            )
        assert exc_info.value.args[0] == (
            "Invalid range given for `the_integral_param`"
            " - end of range must be an integer"
        )

    def test_bad_type_str_not_int(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                ("17.5", 20), Integral, int, "an integer", "the_integral_param"
            )
        assert exc_info.value.args[0] == (
            "Invalid range given for `the_integral_param`"
            " - start of range must be an integer"
        )

    def test_in_range_with_lower_bound(self):
        kind, output_value = ensure_single_or_range(
            (5, 8), Integral, int, "an integer", "the_integral_param", lower_bound=0
        )
        assert kind == "range"
        assert output_value == (5, 8)

    def test_in_range_with_upper_bound(self):
        kind, output_value = ensure_single_or_range(
            (-50, 50), Integral, int, "an integer", "the_integral_param", upper_bound=80
        )
        assert kind == "range"
        assert output_value == (-50, 50)

    def test_in_range_with_both_bounds(self):
        kind, output_value = ensure_single_or_range(
            (True, 16),
            Integral,
            int,
            "an integer",
            "the_integral_param",
            lower_bound=0,
            upper_bound=20,
        )
        assert kind == "range"
        assert output_value == (1, 16)

    def test_not_in_range_with_both_bounds_start_too_small(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                (5, 10),
                Integral,
                int,
                "an integer",
                "the_integral_param",
                lower_bound=10,
                upper_bound=20,
            )
        assert exc_info.value.args[0] == (
            "Invalid range given for `the_integral_param`"
            " - start of range must be greater than 10"
        )

    def test_not_in_range_with_both_bounds_end_too_big(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                (-64, 1024),
                Integral,
                int,
                "an integer",
                "the_integral_param",
                lower_bound=-128,
                upper_bound=512,
            )
        assert exc_info.value.args[0] == (
            "Invalid range given for `the_integral_param`"
            " - end of range must be less than 512"
        )

    def test_bad_range_start_greater_than_end(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                (50, 45), Integral, int, "an integer", "the_integral_param"
            )
        assert exc_info.value.args[0] == (
            "Invalid range given for `the_integral_param`"
            " - start of range must be less than the end."
        )

    def test_bad_type_list_not_tuple(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                [0, 100], Integral, int, "an integer", "the_integral_param"
            )
        assert exc_info.value.args[0] == (
            "Invalid range given for `the_integral_param`"
            " - must be a tuple of two values."
        )

    def test_bad_type_tuple_of_3(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                (9, 25, 49), Integral, int, "an integer", "the_integral_param"
            )
        assert exc_info.value.args[0] == (
            "Invalid range given for `the_integral_param`"
            " - must be a tuple of two values."
        )


class TestEnsureSingleOrRangeRealRange:
    def test_conversion_superfluous(self):
        kind, output_value = ensure_single_or_range(
            (5.6, 8.9), Real, float, "a number", "the_number_param"
        )
        assert kind == "range"
        assert output_value == (5.6, 8.9)

    def test_one_needs_converting(self):
        kind, output_value = ensure_single_or_range(
            (Fraction(617, 50), 23.45), Real, float, "a number", "the_number_param"
        )
        assert kind == "range"
        assert output_value == (12.34, 23.45)

    def test_both_need_converting(self):
        s = pd.Series([99.87]).astype("float64")
        kind, output_value = ensure_single_or_range(
            (10, s[0]), Real, float, "a number", "the_number_param"
        )
        assert kind == "range"
        assert output_value == (10.0, 99.87)

    def test_bad_type_complex_not_float(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                (123 + 456j, 789), Real, float, "a number", "the_number_param"
            )
        assert exc_info.value.args[0] == (
            "Invalid range given for `the_number_param`"
            " - start of range must be a number"
        )

    def test_bad_type_str_not_float(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                (17.5, "20"), Real, float, "a number", "the_number_param"
            )
        assert exc_info.value.args[0] == (
            "Invalid range given for `the_number_param`"
            " - end of range must be a number"
        )

    def test_in_range_with_lower_bound(self):
        kind, output_value = ensure_single_or_range(
            (5, 8.5), Real, float, "a number", "the_number_param", lower_bound=0
        )
        assert kind == "range"
        assert output_value == (5, 8.5)

    def test_in_range_with_upper_bound(self):
        kind, output_value = ensure_single_or_range(
            (-62.5, 12.48), Real, float, "a number", "the_number_param", upper_bound=80
        )
        assert kind == "range"
        assert output_value == (-62.5, 12.48)

    def test_in_range_with_both_bounds(self):
        kind, output_value = ensure_single_or_range(
            (Fraction(169, 40), 16.32),
            Real,
            float,
            "a number",
            "the_number_param",
            lower_bound=0,
            upper_bound=19.9,
        )
        assert kind == "range"
        assert output_value == (4.225, 16.32)

    def test_not_in_range_with_both_bounds_start_too_small(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                (-33.33, 66.67),
                Real,
                float,
                "a number",
                "the_number_param",
                lower_bound=50,
                upper_bound=99.99,
            )
        assert exc_info.value.args[0] == (
            "Invalid range given for `the_number_param`"
            " - start of range must be greater than 50"
        )

    def test_not_in_range_with_both_bounds_end_too_big(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                (64.256, 128.512),
                Real,
                float,
                "a number",
                "the_number_param",
                lower_bound=32.128,
                upper_bound=96.48,
            )
        assert exc_info.value.args[0] == (
            "Invalid range given for `the_number_param`"
            " - end of range must be less than 96.48"
        )

    def test_bad_range_start_greater_than_end(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                (78.34, 56.12), Real, float, "a number", "the_number_param"
            )
        assert exc_info.value.args[0] == (
            "Invalid range given for `the_number_param`"
            " - start of range must be less than the end."
        )

    def test_bad_type_list_not_tuple(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                [5.5, 95.95], Real, float, "a number", "the_number_param"
            )
        assert exc_info.value.args[0] == (
            "Invalid range given for `the_number_param`"
            " - must be a tuple of two values."
        )

    def test_bad_type_tuple_of_3(self):
        with pytest.raises(ValueError) as exc_info:
            kind, output_value = ensure_single_or_range(
                (10.89, 30.25, 59.29), Real, float, "a number", "the_number_param"
            )
        assert exc_info.value.args[0] == (
            "Invalid range given for `the_number_param`"
            " - must be a tuple of two values."
        )
