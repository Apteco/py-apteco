from decimal import Decimal
from fractions import Fraction
from numbers import Integral, Rational
from unittest.mock import Mock

import apteco_api as aa
import pandas as pd
import pytest

from apteco.query import LimitClause, SelectorClause


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

