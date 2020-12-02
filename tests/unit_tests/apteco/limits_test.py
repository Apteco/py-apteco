from fractions import Fraction

import pytest

from apteco.query import LimitClause, SelectorClause


@pytest.fixture()
def electronics(rtl_var_purchase_department):
    return SelectorClause(rtl_var_purchase_department, "Electronics")


def test_limit_clause(electronics, rtl_session):
    with pytest.raises(ValueError) as exc_info:
        electronics_no_value = LimitClause(clause=electronics, session=rtl_session)
    assert exc_info.value.args[0] == ("Must specify exactly one of `total`, `percent` or `fraction`")

    with pytest.raises(ValueError) as exc_info:
        electronics_2_values = LimitClause(clause=electronics, total=10, percent=0,
            session=rtl_session)
    assert exc_info.value.args[0] == ("Must specify exactly one of `total`, `percent` or `fraction`")

    with pytest.raises(ValueError) as exc_info:
        electronics_3_values = LimitClause(clause=electronics, total=10, percent=0,
            fraction=(2, 3), session=rtl_session)
    assert exc_info.value.args[0] == ("Must specify exactly one of `total`, `percent` or `fraction`")

    with pytest.raises(ValueError) as exc_info:
        electronics_regular_sample = LimitClause(clause=electronics, total=10,
            sample_type="Regular", session=rtl_session)
    assert exc_info.value.args[0] == ("Regular is not a valid sample type")

    electronics_2_thirds_random_skip_first_5 = LimitClause(clause=electronics,
        fraction=Fraction(2, 3), sample_type="Random", skip_first=5, session=rtl_session)
    assert electronics_2_thirds_random_skip_first_5.total == None
    assert electronics_2_thirds_random_skip_first_5.percent == None
    assert electronics_2_thirds_random_skip_first_5.fraction.numerator == 2
    assert electronics_2_thirds_random_skip_first_5.fraction.denominator == 3
    assert electronics_2_thirds_random_skip_first_5.clause == electronics
    assert electronics_2_thirds_random_skip_first_5.sample_type == "Random"
    assert electronics_2_thirds_random_skip_first_5.skip_first == 5
    assert electronics_2_thirds_random_skip_first_5.table == electronics.table
    assert electronics_2_thirds_random_skip_first_5.label == None
    assert electronics_2_thirds_random_skip_first_5.session == rtl_session
