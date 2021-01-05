from decimal import Decimal
from fractions import Fraction
from numbers import Integral, Rational, Real
from unittest.mock import Mock

import apteco_api as aa
import pandas as pd
import pytest

from apteco.query import (
    LimitClause,
    NPerVariableClause,
    SelectorClause,
    TopNClause,
    ensure_single_or_range,
)


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


@pytest.fixture()
def clothing(rtl_var_purchase_department):
    clothing_clause = SelectorClause(rtl_var_purchase_department, ["Clothing"])
    clothing_clause._to_model_clause = Mock(
        return_value="Clothing clause model goes here"
    )
    return clothing_clause


@pytest.fixture()
def domestic(rtl_var_purchase_department):
    domestic_clause = SelectorClause(rtl_var_purchase_department, ["Home", "Garden"])
    domestic_clause._to_model_clause = Mock(
        return_value="Domestic clause model goes here"
    )
    return domestic_clause


class TestLimitClause:
    def test_limit_clause_total_correct_type(
        self, electronics, rtl_table_purchases, rtl_session
    ):
        limit_2500 = LimitClause(electronics, 2500, session=rtl_session)
        assert limit_2500.kind == "Total"
        assert limit_2500.total == 2500
        assert limit_2500.percent is None
        assert limit_2500.fraction is None
        assert limit_2500.sample_type == "First"
        assert limit_2500.skip_first == 0
        assert limit_2500.clause is electronics
        assert limit_2500.table is rtl_table_purchases
        assert limit_2500.label is None
        assert limit_2500.session is rtl_session

    def test_limit_clause_total_needs_converting(
        self, electronics, rtl_table_purchases, rtl_session
    ):
        s = pd.Series([654]).astype("int32")
        limit_654_from_pd_series = LimitClause(electronics, s[0], session=rtl_session)
        assert limit_654_from_pd_series.kind == "Total"
        assert limit_654_from_pd_series.total == 654
        assert limit_654_from_pd_series.percent is None
        assert limit_654_from_pd_series.fraction is None
        assert limit_654_from_pd_series.sample_type == "First"
        assert limit_654_from_pd_series.skip_first == 0
        assert limit_654_from_pd_series.clause is electronics
        assert limit_654_from_pd_series.table is rtl_table_purchases
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

    def test_limit_clause_percent_correct_type(
        self, electronics, rtl_table_purchases, rtl_session
    ):
        limit_0_6_pct = LimitClause(electronics, percent=0.6, session=rtl_session)
        assert limit_0_6_pct.kind == "Percent"
        assert limit_0_6_pct.total is None
        assert limit_0_6_pct.percent == 0.6
        assert limit_0_6_pct.fraction is None
        assert limit_0_6_pct.sample_type == "First"
        assert limit_0_6_pct.skip_first == 0
        assert limit_0_6_pct.clause is electronics
        assert limit_0_6_pct.table is rtl_table_purchases
        assert limit_0_6_pct.label is None
        assert limit_0_6_pct.session is rtl_session

    def test_limit_clause_percent_needs_converting(
        self, electronics, rtl_table_purchases, rtl_session
    ):
        limit_127_2000_pct = LimitClause(
            electronics, percent=Fraction("127/20"), session=rtl_session
        )
        assert limit_127_2000_pct.kind == "Percent"
        assert limit_127_2000_pct.total is None
        assert limit_127_2000_pct.percent == 6.35
        assert limit_127_2000_pct.fraction is None
        assert limit_127_2000_pct.sample_type == "First"
        assert limit_127_2000_pct.skip_first == 0
        assert limit_127_2000_pct.clause is electronics
        assert limit_127_2000_pct.table is rtl_table_purchases
        assert limit_127_2000_pct.label is None
        assert limit_127_2000_pct.session is rtl_session

    def test_limit_clause_percent_not_real(self, electronics, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            limit_percent_as_complex = LimitClause(
                electronics, percent=13.87 + 951.84j, session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`percent` must be a number between 0–100 (exclusive)"
        )

        with pytest.raises(ValueError) as exc_info:
            limit_percent_as_str = LimitClause(
                electronics, percent="7.25", session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`percent` must be a number between 0–100 (exclusive)"
        )

    def test_limit_clause_percent_out_of_range(self, electronics, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            limit_percent_is_0 = LimitClause(
                electronics, percent=0, session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`percent` must be a number between 0–100 (exclusive)"
        )

        with pytest.raises(ValueError) as exc_info:
            limit_percent_too_small = LimitClause(
                electronics, percent=-1.5, session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`percent` must be a number between 0–100 (exclusive)"
        )

        with pytest.raises(ValueError) as exc_info:
            limit_percent_is_100 = LimitClause(
                electronics, percent=100, session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`percent` must be a number between 0–100 (exclusive)"
        )

        with pytest.raises(ValueError) as exc_info:
            limit_percent_too_big = LimitClause(
                electronics, percent=144.1, session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`percent` must be a number between 0–100 (exclusive)"
        )

    def test_limit_clause_fraction_correct_type(
        self, electronics, rtl_table_purchases, rtl_session
    ):
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
        assert limit_2_9_frac.clause is electronics
        assert limit_2_9_frac.table is rtl_table_purchases
        assert limit_2_9_frac.label is None
        assert limit_2_9_frac.session is rtl_session

    def test_limit_clause_fraction_needs_converting(
        self, electronics, rtl_table_purchases, rtl_session
    ):
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
        assert limit_custom_rational_class.clause is electronics
        assert limit_custom_rational_class.table is rtl_table_purchases
        assert limit_custom_rational_class.label is None
        assert limit_custom_rational_class.session is rtl_session

    def test_limit_clause_fraction_not_rational(self, electronics, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            limit_fraction_as_float = LimitClause(
                electronics, fraction=0.3333, session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`fraction` must be a rational number between 0 and 1 (exclusive)"
        )

        with pytest.raises(ValueError) as exc_info:
            limit_fraction_as_str = LimitClause(
                electronics, fraction="2/17", session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`fraction` must be a rational number between 0 and 1 (exclusive)"
        )

    def test_limit_clause_fraction_out_of_range(self, electronics, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            limit_fraction_is_0 = LimitClause(
                electronics, fraction=0, session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`fraction` must be a rational number between 0 and 1 (exclusive)"
        )

        with pytest.raises(ValueError) as exc_info:
            limit_fraction_too_small = LimitClause(
                electronics, fraction=Fraction(-4, 100), session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`fraction` must be a rational number between 0 and 1 (exclusive)"
        )

        with pytest.raises(ValueError) as exc_info:
            limit_fraction_is_1 = LimitClause(
                electronics, fraction=1, session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`fraction` must be a rational number between 0 and 1 (exclusive)"
        )

        with pytest.raises(ValueError) as exc_info:
            limit_fraction_too_big = LimitClause(
                electronics, fraction=Fraction(4, 3), session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`fraction` must be a rational number between 0 and 1 (exclusive)"
        )

    def test_limit_clause_skip_first_correct_type(
        self, electronics, rtl_table_purchases, rtl_session
    ):
        limit_skip_82 = LimitClause(
            electronics, 55000, skip_first=82, session=rtl_session
        )
        assert limit_skip_82.kind == "Total"
        assert limit_skip_82.total == 55000
        assert limit_skip_82.percent is None
        assert limit_skip_82.fraction is None
        assert limit_skip_82.sample_type == "First"
        assert limit_skip_82.skip_first == 82
        assert limit_skip_82.clause is electronics
        assert limit_skip_82.table is rtl_table_purchases
        assert limit_skip_82.label is None
        assert limit_skip_82.session is rtl_session

    def test_limit_clause_skip_first_needs_converting(
        self, electronics, rtl_table_purchases, rtl_session
    ):
        limit_skip_1_as_true = LimitClause(
            electronics, percent=64.2, skip_first=True, session=rtl_session
        )
        assert limit_skip_1_as_true.kind == "Percent"
        assert limit_skip_1_as_true.total is None
        assert limit_skip_1_as_true.percent == 64.2
        assert limit_skip_1_as_true.fraction is None
        assert limit_skip_1_as_true.sample_type == "First"
        assert limit_skip_1_as_true.skip_first == 1
        assert limit_skip_1_as_true.clause is electronics
        assert limit_skip_1_as_true.table is rtl_table_purchases
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
        assert exc_info.value.args[0] == (
            "Must specify exactly one of `total`, `percent` or `fraction`"
        )

    def test_limit_clause_two_values_given(self, electronics, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            electronics_2_values = LimitClause(
                clause=electronics, total=10, percent=0, session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "Must specify exactly one of `total`, `percent` or `fraction`"
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
        assert exc_info.value.args[0] == (
            "Must specify exactly one of `total`, `percent` or `fraction`"
        )

    def test_limit_clause_sample_invalid_type(self, electronics, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            electronics_regular_sample = LimitClause(
                clause=electronics, total=10, sample_type="Regular", session=rtl_session
            )
        assert exc_info.value.args[0] == "Regular is not a valid sample type"

    def test_limit_clause_init(self, electronics, rtl_table_purchases, rtl_session):
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
        assert electronics_2_thirds_random_skip_first_5.sample_type == "Random"
        assert electronics_2_thirds_random_skip_first_5.skip_first == 5
        assert electronics_2_thirds_random_skip_first_5.clause is electronics
        assert electronics_2_thirds_random_skip_first_5.table is rtl_table_purchases
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


class TestTopNClause:
    def test_topn_clause_total_single_correct_type(
        self, clothing, rtl_var_purchase_profit, rtl_table_purchases, rtl_session
    ):
        top_43210 = TopNClause(
            clothing, 43210, by=rtl_var_purchase_profit, session=rtl_session
        )
        assert top_43210.kind == ("single", "total")
        assert top_43210.total == 43210
        assert top_43210.percent is None
        assert top_43210.by is rtl_var_purchase_profit
        assert top_43210.ascending is False
        assert top_43210.clause is clothing
        assert top_43210.table is rtl_table_purchases
        assert top_43210.label is None
        assert top_43210.session is rtl_session

    def test_topn_clause_total_single_needs_converting(
        self, clothing, rtl_var_purchase_profit, rtl_table_purchases, rtl_session
    ):
        s = pd.Series([123]).astype("int8")
        top_123 = TopNClause(
            clothing, s[0], by=rtl_var_purchase_profit, session=rtl_session
        )
        assert top_123.kind == ("single", "total")
        assert top_123.total == 123
        assert top_123.percent is None
        assert top_123.by is rtl_var_purchase_profit
        assert top_123.ascending is False
        assert top_123.clause is clothing
        assert top_123.table is rtl_table_purchases
        assert top_123.label is None
        assert top_123.session is rtl_session

    def test_topn_clause_total_single_not_integral(self, clothing, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            top_total_as_float = TopNClause(clothing, 428.06, session=rtl_session)
        assert exc_info.value.args[0] == (
            "`total` must be an integer"
            " or a tuple of two integers (to indicate a range)"
        )

    def test_topn_clause_total_single_less_than_1(self, clothing, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            top_total_betw_0_1 = TopNClause(clothing, 0.23, session=rtl_session)
        assert exc_info.value.args[0] == (
            "`total` must be an integer"
            " or a tuple of two integers (to indicate a range)"
        )

        with pytest.raises(ValueError) as exc_info:
            top_total_is_0 = TopNClause(clothing, 0, session=rtl_session)
        assert exc_info.value.args[0] == (
            "`total` must be an integer"
            " or a tuple of two integers (to indicate a range)"
        )

        with pytest.raises(ValueError) as exc_info:
            top_total_is_negative = TopNClause(clothing, -8100, session=rtl_session)
        assert exc_info.value.args[0] == (
            "`total` must be an integer"
            " or a tuple of two integers (to indicate a range)"
        )

    def test_topn_clause_percent_single_correct_type(
        self, clothing, rtl_var_purchase_profit, rtl_table_purchases, rtl_session
    ):
        top_4_615_percent = TopNClause(
            clothing, percent=4.615, by=rtl_var_purchase_profit, session=rtl_session
        )
        assert top_4_615_percent.kind == ("single", "percent")
        assert top_4_615_percent.total is None
        assert top_4_615_percent.percent == 4.615
        assert top_4_615_percent.by is rtl_var_purchase_profit
        assert top_4_615_percent.ascending is False
        assert top_4_615_percent.clause is clothing
        assert top_4_615_percent.table is rtl_table_purchases
        assert top_4_615_percent.label is None
        assert top_4_615_percent.session is rtl_session

        top_0_332_percent = TopNClause(
            clothing, percent=0.332, by=rtl_var_purchase_profit, session=rtl_session
        )
        assert top_0_332_percent.kind == ("single", "percent")
        assert top_0_332_percent.total is None
        assert top_0_332_percent.percent == 0.332
        assert top_0_332_percent.by is rtl_var_purchase_profit
        assert top_0_332_percent.ascending is False
        assert top_0_332_percent.clause is clothing
        assert top_0_332_percent.table is rtl_table_purchases
        assert top_0_332_percent.label is None
        assert top_0_332_percent.session is rtl_session

    def test_topn_clause_percent_single_needs_converting(
        self, clothing, rtl_var_purchase_profit, rtl_table_purchases, rtl_session
    ):
        top_19_782_percent = TopNClause(
            clothing,
            percent=Fraction(9891 / 500),
            by=rtl_var_purchase_profit,
            session=rtl_session,
        )
        assert top_19_782_percent.kind == ("single", "percent")
        assert top_19_782_percent.total is None
        assert top_19_782_percent.percent == 19.782
        assert top_19_782_percent.by is rtl_var_purchase_profit
        assert top_19_782_percent.ascending is False
        assert top_19_782_percent.clause is clothing
        assert top_19_782_percent.table is rtl_table_purchases
        assert top_19_782_percent.label is None
        assert top_19_782_percent.session is rtl_session

    def test_topn_clause_percent_single_not_real(self, clothing, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            top_percent_as_str = TopNClause(
                clothing, percent="22.33", session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`percent` must be a number or a tuple of two numbers (to indicate a range)"
        )

    def test_topn_clause_percent_single_out_of_range(self, clothing, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            top_percent_is_too_big = TopNClause(
                clothing, percent=110, session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`percent` must be a number or a tuple of two numbers (to indicate a range)"
        )

        with pytest.raises(ValueError) as exc_info:
            top_percent_is_negative = TopNClause(
                clothing, percent=-54.32, session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`percent` must be a number or a tuple of two numbers (to indicate a range)"
        )

        with pytest.raises(ValueError) as exc_info:
            top_percent_is_0 = TopNClause(clothing, percent=0, session=rtl_session)
        assert exc_info.value.args[0] == (
            "`percent` must be a number or a tuple of two numbers (to indicate a range)"
        )

        with pytest.raises(ValueError) as exc_info:
            top_percent_is_100 = TopNClause(clothing, percent=100, session=rtl_session)
        assert exc_info.value.args[0] == (
            "`percent` must be a number or a tuple of two numbers (to indicate a range)"
        )

    def test_topn_clause_total_range_correct_type(
        self, clothing, rtl_var_purchase_profit, rtl_table_purchases, rtl_session
    ):
        top_1234_5678 = TopNClause(
            clothing, (1234, 5678), by=rtl_var_purchase_profit, session=rtl_session
        )
        assert top_1234_5678.kind == ("range", "total")
        assert top_1234_5678.total == (1234, 5678)
        assert top_1234_5678.percent is None
        assert top_1234_5678.by is rtl_var_purchase_profit
        assert top_1234_5678.ascending is False
        assert top_1234_5678.clause is clothing
        assert top_1234_5678.table is rtl_table_purchases
        assert top_1234_5678.label is None
        assert top_1234_5678.session is rtl_session

    def test_topn_clause_total_range_needs_converting(
        self, clothing, rtl_var_purchase_profit, rtl_table_purchases, rtl_session
    ):
        top_1_6_start_needs_converting = TopNClause(
            clothing, (True, 6), by=rtl_var_purchase_profit, session=rtl_session
        )
        assert top_1_6_start_needs_converting.kind == ("range", "total")
        assert top_1_6_start_needs_converting.total == (1, 6)
        assert top_1_6_start_needs_converting.percent is None
        assert top_1_6_start_needs_converting.by is rtl_var_purchase_profit
        assert top_1_6_start_needs_converting.ascending is False
        assert top_1_6_start_needs_converting.clause is clothing
        assert top_1_6_start_needs_converting.table is rtl_table_purchases
        assert top_1_6_start_needs_converting.label is None
        assert top_1_6_start_needs_converting.session is rtl_session

        s = pd.Series([2, 5]).astype("int16")
        top_2k_to_5k_both_need_converting = TopNClause(
            clothing, tuple(s * 1000), by=rtl_var_purchase_profit, session=rtl_session
        )
        assert top_2k_to_5k_both_need_converting.kind == ("range", "total")
        assert top_2k_to_5k_both_need_converting.total == (2000, 5000)
        assert top_2k_to_5k_both_need_converting.percent is None
        assert top_2k_to_5k_both_need_converting.by is rtl_var_purchase_profit
        assert top_2k_to_5k_both_need_converting.ascending is False
        assert top_2k_to_5k_both_need_converting.clause is clothing
        assert top_2k_to_5k_both_need_converting.table is rtl_table_purchases
        assert top_2k_to_5k_both_need_converting.label is None
        assert top_2k_to_5k_both_need_converting.session is rtl_session

    def test_topn_clause_total_range_not_integral(self, clothing, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            top_total_range_end_as_float = TopNClause(
                clothing, (4, 54.0), session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`total` must be an integer"
            " or a tuple of two integers (to indicate a range)"
        )

    def test_topn_clause_total_range_start_less_than_1(self, clothing, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            top_total_range_start_less_than_1 = TopNClause(
                clothing, (-3, 6), session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`total` must be an integer"
            " or a tuple of two integers (to indicate a range)"
        )

    def test_topn_clause_total_range_start_greater_than_end(
        self, clothing, rtl_session
    ):
        with pytest.raises(ValueError) as exc_info:
            top_total_range_end_as_float = TopNClause(
                clothing, (70, 34), session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`total` must be an integer"
            " or a tuple of two integers (to indicate a range)"
        )

    def test_topn_clause_total_range_list_not_tuple(self, clothing, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            top_total_range_end_as_float = TopNClause(
                clothing, [500, 2000], session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`total` must be an integer"
            " or a tuple of two integers (to indicate a range)"
        )

    def test_topn_clause_total_range_tuple_of_3(self, clothing, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            top_total_range_end_as_float = TopNClause(
                clothing, (111, 222, 333), session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`total` must be an integer"
            " or a tuple of two integers (to indicate a range)"
        )

    def test_topn_clause_percent_range_correct_type(
        self, clothing, rtl_var_purchase_profit, rtl_table_purchases, rtl_session
    ):
        top_5_31_to_9_753_percent = TopNClause(
            clothing,
            percent=(5.31, 9.753),
            by=rtl_var_purchase_profit,
            session=rtl_session,
        )
        assert top_5_31_to_9_753_percent.kind == ("range", "percent")
        assert top_5_31_to_9_753_percent.total is None
        assert top_5_31_to_9_753_percent.percent == (5.31, 9.753)
        assert top_5_31_to_9_753_percent.by is rtl_var_purchase_profit
        assert top_5_31_to_9_753_percent.ascending is False
        assert top_5_31_to_9_753_percent.clause is clothing
        assert top_5_31_to_9_753_percent.table is rtl_table_purchases
        assert top_5_31_to_9_753_percent.label is None
        assert top_5_31_to_9_753_percent.session is rtl_session

    def test_topn_clause_percent_range_needs_converting(
        self, clothing, rtl_var_purchase_profit, rtl_table_purchases, rtl_session
    ):
        s = pd.Series([14.2856]).astype("float64")
        top_7_2163_to_14_2856_end_needs_converting = TopNClause(
            clothing,
            percent=(7.2163, s[0]),
            by=rtl_var_purchase_profit,
            session=rtl_session,
        )
        assert top_7_2163_to_14_2856_end_needs_converting.kind == ("range", "percent")
        assert top_7_2163_to_14_2856_end_needs_converting.total is None
        assert top_7_2163_to_14_2856_end_needs_converting.percent == (7.2163, 14.2856)
        assert top_7_2163_to_14_2856_end_needs_converting.by is rtl_var_purchase_profit
        assert top_7_2163_to_14_2856_end_needs_converting.ascending is False
        assert top_7_2163_to_14_2856_end_needs_converting.clause is clothing
        assert top_7_2163_to_14_2856_end_needs_converting.table is rtl_table_purchases
        assert top_7_2163_to_14_2856_end_needs_converting.label is None
        assert top_7_2163_to_14_2856_end_needs_converting.session is rtl_session

        top_65_432_to_76_54_end_needs_converting = TopNClause(
            clothing,
            percent=(Fraction(8179, 125), Fraction(3827, 50)),
            by=rtl_var_purchase_profit,
            session=rtl_session,
        )
        assert top_65_432_to_76_54_end_needs_converting.kind == ("range", "percent")
        assert top_65_432_to_76_54_end_needs_converting.total is None
        assert top_65_432_to_76_54_end_needs_converting.percent == (65.432, 76.54)
        assert top_65_432_to_76_54_end_needs_converting.by is rtl_var_purchase_profit
        assert top_65_432_to_76_54_end_needs_converting.ascending is False
        assert top_65_432_to_76_54_end_needs_converting.clause is clothing
        assert top_65_432_to_76_54_end_needs_converting.table is rtl_table_purchases
        assert top_65_432_to_76_54_end_needs_converting.label is None
        assert top_65_432_to_76_54_end_needs_converting.session is rtl_session

    def test_topn_clause_percent_range_not_real(self, clothing, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            top_percent_range_start_as_complex = TopNClause(
                clothing, percent=(1 + 2j, 3.4), session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`percent` must be a number or a tuple of two numbers (to indicate a range)"
        )

    def test_topn_clause_percent_range_out_of_bounds(self, clothing, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            top_percent_range_start_too_small = TopNClause(
                clothing, percent=(-25, 46.8), session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`percent` must be a number or a tuple of two numbers (to indicate a range)"
        )

        with pytest.raises(ValueError) as exc_info:
            top_percent_range_end_too_big = TopNClause(
                clothing, percent=(15.5, 240.25), session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`percent` must be a number or a tuple of two numbers (to indicate a range)"
        )

        with pytest.raises(ValueError) as exc_info:
            top_percent_range_both_out_of_range = TopNClause(
                clothing, percent=(-123.45, 123.45), session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`percent` must be a number or a tuple of two numbers (to indicate a range)"
        )

    def test_topn_clause_percent_range_start_greater_than_end(
        self, clothing, rtl_session
    ):
        with pytest.raises(ValueError) as exc_info:
            top_percent_range_start_greater_than_end = TopNClause(
                clothing, percent=(3.1, 2.0), session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`percent` must be a number or a tuple of two numbers (to indicate a range)"
        )

    def test_topn_clause_percent_range_list_not_tuple(self, clothing, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            top_percent_range_list_not_tuple = TopNClause(
                clothing, percent=[4.6, 5.7], session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`percent` must be a number or a tuple of two numbers (to indicate a range)"
        )

    def test_topn_clause_percent_range_tuple_of_4(self, clothing, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            top_percent_range_tuple_of_4 = TopNClause(
                clothing, percent=(1.1, 2.2, 3.3, 4.4), session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`percent` must be a number or a tuple of two numbers (to indicate a range)"
        )

    def test_topn_clause_no_value_given(self, clothing, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            topn_no_value_given = TopNClause(clothing, session=rtl_session)
        assert exc_info.value.args[0] == "Must specify one of `total` or `percent`"

    def test_topn_clause_both_values_given(self, clothing, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            topn_both_values_given = TopNClause(clothing, 10, 20.3, session=rtl_session)
        assert exc_info.value.args[0] == (
            "Must specify either `total` or `percent`, but not both"
        )

    def test_topn_clause_by_is_none(self, clothing, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            top_n_by_is_none = TopNClause(clothing, 100, session=rtl_session)
        assert exc_info.value.args[0] == "`by` must be an ordered variable"

    def test_topn_clause_by_not_variable(self, clothing, electronics, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            top_n_by_is_selection = TopNClause(
                clothing, 100, by=electronics, session=rtl_session
            )
        assert exc_info.value.args[0] == "`by` must be an ordered variable"

    def test_topn_clause_ascending_correct_type(
        self, clothing, rtl_var_purchase_profit, rtl_table_purchases, rtl_session
    ):
        bottom_500 = TopNClause(
            clothing,
            500,
            by=rtl_var_purchase_profit,
            ascending=True,
            session=rtl_session,
        )
        assert bottom_500.kind == ("single", "total")
        assert bottom_500.total == 500
        assert bottom_500.percent is None
        assert bottom_500.by is rtl_var_purchase_profit
        assert bottom_500.ascending is True
        assert bottom_500.clause is clothing
        assert bottom_500.table is rtl_table_purchases
        assert bottom_500.label is None
        assert bottom_500.session is rtl_session

    def test_topn_clause_ascending_not_boolean(
        self, clothing, rtl_var_purchase_profit, rtl_session
    ):
        with pytest.raises(ValueError) as exc_info:
            top_n_ascending_is_str = TopNClause(
                clothing,
                100,
                by=rtl_var_purchase_profit,
                ascending="bottom",
                session=rtl_session,
            )
        assert exc_info.value.args[0] == "`ascending` must be a boolean (True or False)"

    def test_topn_clause_to_model_selection_single_total(
        self, clothing, rtl_var_purchase_profit, rtl_table_purchases, rtl_session
    ):
        fake_topn_clause = Mock(
            kind=("single", "total"),
            total=8787,
            percent=None,
            by=rtl_var_purchase_profit,
            ascending=False,
            clause=clothing,
            table=rtl_table_purchases,
            label="Top 8787 clothing purchases by profit",
            session=rtl_session,
        )
        expected_topn_selection_model = aa.Selection(
            rule=aa.Rule(clause="Clothing clause model goes here"),
            top_n=aa.TopN(
                variable_name="puProfit",
                direction="Top",
                value=8787,
                percent="NaN",
                min_value="NaN",
                max_value="NaN",
            ),
            table_name="Purchases",
            name="Top 8787 clothing purchases by profit",
        )
        assert (
            TopNClause._to_model_selection(fake_topn_clause)
            == expected_topn_selection_model
        )
        clothing._to_model_clause.assert_called_once_with()

    def test_topn_clause_to_model_selection_single_percent(
        self, clothing, rtl_var_purchase_profit, rtl_table_purchases, rtl_session
    ):
        fake_topn_clause = Mock(
            kind=("single", "percent"),
            total=None,
            percent=3.45,
            by=rtl_var_purchase_profit,
            ascending=False,
            clause=clothing,
            table=rtl_table_purchases,
            label="Top 3.45% of clothing purchases by profit",
            session=rtl_session,
        )
        expected_topn_selection_model = aa.Selection(
            rule=aa.Rule(clause="Clothing clause model goes here"),
            top_n=aa.TopN(
                variable_name="puProfit",
                direction="Top",
                value=0,
                percent=3.45,
                min_value="NaN",
                max_value="NaN",
            ),
            table_name="Purchases",
            name="Top 3.45% of clothing purchases by profit",
        )
        assert (
            TopNClause._to_model_selection(fake_topn_clause)
            == expected_topn_selection_model
        )
        clothing._to_model_clause.assert_called_once_with()

    def test_topn_clause_to_model_selection_range_total(
        self, clothing, rtl_var_purchase_profit, rtl_table_purchases, rtl_session
    ):
        fake_topn_clause = Mock(
            kind=("range", "total"),
            total=(5000, 10000),
            percent=None,
            by=rtl_var_purchase_profit,
            ascending=False,
            clause=clothing,
            table=rtl_table_purchases,
            label="Between top 5-10k clothing purchases by profit",
            session=rtl_session,
        )
        expected_topn_selection_model = aa.Selection(
            rule=aa.Rule(clause="Clothing clause model goes here"),
            top_n=aa.TopN(
                variable_name="puProfit",
                direction="RangeTopDown",
                value=0,
                percent="NaN",
                min_value=5000.0,
                max_value=10000.0,
            ),
            table_name="Purchases",
            name="Between top 5-10k clothing purchases by profit",
        )
        assert (
            TopNClause._to_model_selection(fake_topn_clause)
            == expected_topn_selection_model
        )
        clothing._to_model_clause.assert_called_once_with()

    def test_topn_clause_to_model_selection_range_percent(
        self, clothing, rtl_var_purchase_profit, rtl_table_purchases, rtl_session
    ):
        fake_topn_clause = Mock(
            kind=("range", "percent"),
            total=None,
            percent=(12.5, 17.5),
            by=rtl_var_purchase_profit,
            ascending=True,
            clause=clothing,
            table=rtl_table_purchases,
            label="Between bottom 12.5-17.5% clothing purchases by profit",
            session=rtl_session,
        )
        expected_topn_selection_model = aa.Selection(
            rule=aa.Rule(clause="Clothing clause model goes here"),
            top_n=aa.TopN(
                variable_name="puProfit",
                direction="PercentRangeBottomUp",
                value=0,
                percent="NaN",
                min_value=12.5,
                max_value=17.5,
            ),
            table_name="Purchases",
            name="Between bottom 12.5-17.5% clothing purchases by profit",
        )
        assert (
            TopNClause._to_model_selection(fake_topn_clause)
            == expected_topn_selection_model
        )
        clothing._to_model_clause.assert_called_once_with()

    def test_topn_clause_to_model_selection_invalid_kind_single(
        self, clothing, rtl_var_purchase_profit, rtl_table_purchases, rtl_session
    ):
        fake_topn_clause = Mock(
            kind=("single", "fraction"),
            total=None,
            percent=3.4,
            by=rtl_var_purchase_profit,
            ascending=False,
            clause=clothing,
            table=rtl_table_purchases,
            label="Top 17/5 clothing purchases by profit",
            session=rtl_session,
        )
        with pytest.raises(ValueError) as exc_info:
            TopNClause._to_model_selection(fake_topn_clause)
        assert exc_info.value.args[0] == "Invalid kind: ('single', 'fraction')"
        clothing._to_model_clause.assert_not_called()

    def test_topn_clause_to_model_selection_invalid_kind_range(
        self, clothing, rtl_var_purchase_profit, rtl_table_purchases, rtl_session
    ):
        fake_topn_clause = Mock(
            kind=("range", "decimal"),
            total=None,
            percent=(12.3456789, 23.4567891),
            by=rtl_var_purchase_profit,
            ascending=False,
            clause=clothing,
            table=rtl_table_purchases,
            label="Top 12.3456789-23.4567891% clothing purchases by profit",
            session=rtl_session,
        )
        with pytest.raises(ValueError) as exc_info:
            TopNClause._to_model_selection(fake_topn_clause)
        assert exc_info.value.args[0] == "Invalid kind: ('range', 'decimal')"
        clothing._to_model_clause.assert_not_called()

    def test_topn_clause_to_model_selection_invalid_kind_total(
        self, clothing, rtl_var_purchase_profit, rtl_table_purchases, rtl_session
    ):
        fake_topn_clause = Mock(
            kind=("sample", "total"),
            total=1111,
            percent=None,
            by=rtl_var_purchase_profit,
            ascending=False,
            clause=clothing,
            table=rtl_table_purchases,
            label="Top sample 1111 clothing purchases by profit",
            session=rtl_session,
        )
        with pytest.raises(ValueError) as exc_info:
            TopNClause._to_model_selection(fake_topn_clause)
        assert exc_info.value.args[0] == "Invalid kind: ('sample', 'total')"
        clothing._to_model_clause.assert_not_called()


class TestNPerVariableClause:
    def test_nper_variable_clause_n_correct_type(
        self, domestic, rtl_var_purchase_store, rtl_table_purchases, rtl_session
    ):
        n_1000_per_store = NPerVariableClause(
            domestic, 1000, rtl_var_purchase_store, session=rtl_session
        )
        assert n_1000_per_store.n == 1000
        assert n_1000_per_store.per is rtl_var_purchase_store
        assert n_1000_per_store.by is None
        assert n_1000_per_store.ascending is False
        assert n_1000_per_store.clause is domestic
        assert n_1000_per_store.table is rtl_table_purchases
        assert n_1000_per_store.label is None
        assert n_1000_per_store.session is rtl_session

    def test_nper_variable_clause_n_needs_converting(
        self, domestic, rtl_var_purchase_store, rtl_table_purchases, rtl_session
    ):
        s = pd.Series([5]).astype("int8")
        n_5_per_store_from_pd_series = NPerVariableClause(
            domestic, s[0], rtl_var_purchase_store, session=rtl_session
        )
        assert n_5_per_store_from_pd_series.n == 5
        assert n_5_per_store_from_pd_series.per is rtl_var_purchase_store
        assert n_5_per_store_from_pd_series.by is None
        assert n_5_per_store_from_pd_series.ascending is False
        assert n_5_per_store_from_pd_series.clause is domestic
        assert n_5_per_store_from_pd_series.table is rtl_table_purchases
        assert n_5_per_store_from_pd_series.label is None
        assert n_5_per_store_from_pd_series.session is rtl_session

    def test_nper_variable_clause_n_not_integral(
        self, domestic, rtl_var_purchase_store, rtl_session
    ):
        with pytest.raises(ValueError) as exc_info:
            n_as_float = NPerVariableClause(
                domestic, 8.4, rtl_var_purchase_store, session=rtl_session
            )
        assert exc_info.value.args[0] == "`n` must be an integer greater than 0"

        with pytest.raises(ValueError) as exc_info:
            n_as_float_no_fractional_part = NPerVariableClause(
                domestic, 80.0, rtl_var_purchase_store, session=rtl_session
            )
        assert exc_info.value.args[0] == "`n` must be an integer greater than 0"

        with pytest.raises(ValueError) as exc_info:
            n_is_none = NPerVariableClause(
                domestic, None, rtl_var_purchase_store, session=rtl_session
            )
        assert exc_info.value.args[0] == "`n` must be an integer greater than 0"

    def test_nper_variable_clause_n_less_than_1(
        self, domestic, rtl_var_purchase_store, rtl_session
    ):
        with pytest.raises(ValueError) as exc_info:
            n_is_0 = NPerVariableClause(
                domestic, 0, rtl_var_purchase_store, session=rtl_session
            )
        assert exc_info.value.args[0] == "`n` must be an integer greater than 0"

        with pytest.raises(ValueError) as exc_info:
            n_negative = NPerVariableClause(
                domestic, -150, rtl_var_purchase_store, session=rtl_session
            )
        assert exc_info.value.args[0] == "`n` must be an integer greater than 0"

        with pytest.raises(ValueError) as exc_info:
            n_too_small_and_not_int = NPerVariableClause(
                domestic, 0.4444, rtl_var_purchase_store, session=rtl_session
            )
        assert exc_info.value.args[0] == "`n` must be an integer greater than 0"

    def test_nper_variable_clause_per_is_none(self, domestic, rtl_session):
        with pytest.raises(ValueError) as exc_info:
            per_is_none = NPerVariableClause(domestic, 10, None, session=rtl_session)
        assert exc_info.value.args[0] == "`per` must be a variable"

    def test_nper_variable_clause_per_not_variable(
        self, domestic, rtl_table_customers, rtl_session
    ):
        with pytest.raises(ValueError) as exc_info:
            per_is_string = NPerVariableClause(
                domestic, 10, "Store", session=rtl_session
            )
        assert exc_info.value.args[0] == "`per` must be a variable"

        with pytest.raises(ValueError) as exc_info:
            per_is_table = NPerVariableClause(
                domestic, 10, rtl_table_customers, session=rtl_session
            )
        assert exc_info.value.args[0] == "`per` must be a variable"

    def test_nper_variable_clause_per_array_variable(
        self, domestic, rtl_var_customer_contact_pref, rtl_session
    ):
        with pytest.raises(ValueError) as exc_info:
            per_is_flag_array_var = NPerVariableClause(
                domestic, 10, rtl_var_customer_contact_pref, session=rtl_session
            )
        assert exc_info.value.args[0] == (
            "`per` cannot be an Array or Flag Array variable"
        )

    def test_nper_variable_clause_by_correct_type(
        self,
        domestic,
        rtl_var_purchase_store,
        rtl_var_purchase_date,
        rtl_table_purchases,
        rtl_session,
    ):
        n_400_domestic_most_recent_by_store = NPerVariableClause(
            domestic,
            400,
            rtl_var_purchase_store,
            rtl_var_purchase_date,
            session=rtl_session,
        )
        assert n_400_domestic_most_recent_by_store.n == 400
        assert n_400_domestic_most_recent_by_store.per is rtl_var_purchase_store
        assert n_400_domestic_most_recent_by_store.by is rtl_var_purchase_date
        assert n_400_domestic_most_recent_by_store.ascending is False
        assert n_400_domestic_most_recent_by_store.clause is domestic
        assert n_400_domestic_most_recent_by_store.table is rtl_table_purchases
        assert n_400_domestic_most_recent_by_store.label is None
        assert n_400_domestic_most_recent_by_store.session is rtl_session

    def test_nper_variable_clause_by_not_variable(
        self, domestic, rtl_var_purchase_store, rtl_table_customers, rtl_session
    ):
        with pytest.raises(ValueError) as exc_info:
            by_is_string = NPerVariableClause(
                domestic, 2500, rtl_var_purchase_store, "Cost", session=rtl_session
            )
        assert exc_info.value.args[0] == "`by` must be an ordered variable"

        with pytest.raises(ValueError) as exc_info:
            by_is_table = NPerVariableClause(
                domestic,
                750,
                rtl_var_purchase_store,
                rtl_table_customers,
                session=rtl_session,
            )
        assert exc_info.value.args[0] == "`by` must be an ordered variable"

    @pytest.mark.xfail(reason="Cannot identify unordered variables")
    def test_nper_variable_clause_by_variable_not_ordered(
        self,
        domestic,
        rtl_var_purchase_store,
        rtl_var_purchase_payment_method,
        rtl_var_customer_contact_pref,
        rtl_session,
    ):
        with pytest.raises(ValueError) as exc_info:
            by_is_unordered_selector_var = NPerVariableClause(
                domestic,
                10,
                rtl_var_purchase_store,
                rtl_var_purchase_payment_method,
                session=rtl_session,
            )
        assert exc_info.value.args[0] == "`by` must be an ordered variable"

        with pytest.raises(ValueError) as exc_info:
            by_is_array_var = NPerVariableClause(
                domestic,
                10,
                rtl_var_purchase_store,
                rtl_var_customer_contact_pref,
                session=rtl_session,
            )
        assert exc_info.value.args[0] == "`by` must be an ordered variable"

    def test_nper_variable_clause_ascending_correct_type(
        self,
        domestic,
        rtl_var_purchase_store,
        rtl_var_purchase_profit,
        rtl_table_purchases,
        rtl_session,
    ):
        lowest_300_profit_per_store = NPerVariableClause(
            domestic,
            300,
            rtl_var_purchase_store,
            rtl_var_purchase_profit,
            ascending=True,
            session=rtl_session,
        )
        assert lowest_300_profit_per_store.n == 300
        assert lowest_300_profit_per_store.per is rtl_var_purchase_store
        assert lowest_300_profit_per_store.by is rtl_var_purchase_profit
        assert lowest_300_profit_per_store.ascending is True
        assert lowest_300_profit_per_store.clause is domestic
        assert lowest_300_profit_per_store.table is rtl_table_purchases
        assert lowest_300_profit_per_store.label is None
        assert lowest_300_profit_per_store.session is rtl_session

    def test_nper_variable_clause_ascending_not_boolean(
        self, domestic, rtl_var_purchase_store, rtl_var_purchase_date, rtl_session
    ):
        with pytest.raises(ValueError) as exc_info:
            n_per_var_direction_is_string = NPerVariableClause(
                domestic,
                1234,
                rtl_var_purchase_store,
                rtl_var_purchase_date,
                ascending="latest",
                session=rtl_session,
            )
        assert exc_info.value.args[0] == "`ascending` must be a boolean (True or False)"

    def test_nper_variable_clause_to_model_selection_by_is_none(
        self, domestic, rtl_var_purchase_store, rtl_table_purchases, rtl_session
    ):
        fake_nper_clause = Mock(
            n=654,
            per=rtl_var_purchase_store,
            by=None,
            ascending=False,
            clause=domestic,
            table=rtl_table_purchases,
            label="654 domestic purchases per store",
            session=rtl_session,
        )
        expected_nper_selection_model = aa.Selection(
            rule=aa.Rule(clause="Domestic clause model goes here"),
            top_n=aa.TopN(
                grouping_variable_name="puStore",
                grouping_sequence_variable_name=None,
                group_max=654,
            ),
            table_name="Purchases",
            name="654 domestic purchases per store",
        )
        assert (
            NPerVariableClause._to_model_selection(fake_nper_clause)
            == expected_nper_selection_model
        )
        domestic._to_model_clause.assert_called_once_with()

    def test_nper_variable_clause_to_model_selection_by_not_none(
        self,
        domestic,
        rtl_var_purchase_store,
        rtl_var_purchase_date,
        rtl_table_purchases,
        rtl_session,
    ):
        fake_nper_clause = Mock(
            n=789,
            per=rtl_var_purchase_store,
            by=rtl_var_purchase_date,
            ascending=False,
            clause=domestic,
            table=rtl_table_purchases,
            label="789 most recent domestic purchases per store",
            session=rtl_session,
        )
        expected_nper_selection_model = aa.Selection(
            rule=aa.Rule(clause="Domestic clause model goes here"),
            top_n=aa.TopN(
                grouping_variable_name="puStore",
                grouping_sequence_variable_name="puDate",
                grouping_ascending=False,
                group_max=789,
            ),
            table_name="Purchases",
            name="789 most recent domestic purchases per store",
        )
        assert (
            NPerVariableClause._to_model_selection(fake_nper_clause)
            == expected_nper_selection_model
        )
        domestic._to_model_clause.assert_called_once_with()
