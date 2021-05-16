from unittest.mock import Mock

import apteco_api as aa
import pytest

from apteco.statistics import (
    Statistic,
    Sum,
    Mean,
    Populated,
    Min,
    Max,
    Median,
    Mode,
    Variance,
    StdDev,
    LowerQuartile,
    UpperQuartile,
    InterQuartileRange,
    CountDistinct,
    CountMode,
)


VARIABLE_TYPES = [
    "Numeric",  # included for completeness
    "Selector",
    "Text",
    "Array",
    "FlagArray",
    "Date",
    "DateTime",
    "BandedDate",
    "Reference",
]


@pytest.fixture()
def retail_var_lookup(
    rtl_var_customer_gender,
    rtl_var_purchase_profit,
    rtl_var_customer_surname,
    rtl_var_customer_interests,
    rtl_var_customer_contact_pref,
    rtl_var_customer_sign_up,
    rtl_var_purchase_date,
    rtl_var_purchase_id,
):
    var_lookup = {
        "Selector": rtl_var_customer_gender,
        "Numeric": rtl_var_purchase_profit,
        "Text": rtl_var_customer_surname,
        "Array": rtl_var_customer_interests,
        "FlagArray": rtl_var_customer_contact_pref,
        "Date": rtl_var_customer_sign_up,
        "DateTime": rtl_var_purchase_date,
        "BandedDate": rtl_var_customer_sign_up.month,
        "Reference": rtl_var_purchase_id,
    }
    return var_lookup


class TestNumericStatistics:
    @pytest.mark.parametrize(
        ["statistic", "display_name"],
        [
            pytest.param(Sum, "Sum(Profit)", id="Sum"),
            pytest.param(Mean, "Mean(Profit)", id="Mean"),
            pytest.param(Populated, "Populated(Profit)", id="Populated"),
            pytest.param(Min, "Min(Profit)", id="Min"),
            pytest.param(Max, "Max(Profit)", id="Max"),
            pytest.param(Median, "Median(Profit)", id="Median"),
            pytest.param(Mode, "Mode(Profit)", id="Mode"),
            pytest.param(Variance, "Variance(Profit)", id="Variance"),
            pytest.param(StdDev, "Std Dev(Profit)", id="StdDev"),
            pytest.param(LowerQuartile, "Lower Quartile(Profit)", id="LowerQuartile"),
            pytest.param(UpperQuartile, "Upper Quartile(Profit)", id="UpperQuartile"),
            pytest.param(
                InterQuartileRange,
                "Inter Quartile Range(Profit)",
                id="InterQuartileRange",
            ),
        ],
    )
    def test_numeric_statistic(
        self, statistic, display_name, rtl_var_purchase_profit, rtl_table_purchases
    ):
        """Test each numeric statistic with Purchases Profit variable."""
        numeric_statistic = statistic(rtl_var_purchase_profit)
        assert numeric_statistic.table is rtl_table_purchases
        assert numeric_statistic._name == display_name

    @pytest.fixture(params=VARIABLE_TYPES[1:])
    def non_numeric_var(self, request, retail_var_lookup):
        var = retail_var_lookup[request.param]
        return var

    @pytest.fixture(
        params=[
            pytest.param((Sum, "Sum"), id="Sum"),
            pytest.param((Mean, "Mean"), id="Mean"),
            pytest.param((Populated, "Populated"), id="Populated"),
            pytest.param((Min, "Min"), id="Min"),
            pytest.param((Max, "Max"), id="Max"),
            pytest.param((Median, "Median"), id="Median"),
            pytest.param((Mode, "Mode"), id="Mode"),
            pytest.param((Variance, "Variance"), id="Variance"),
            pytest.param((StdDev, "Std Dev"), id="StdDev"),
            pytest.param((LowerQuartile, "Lower Quartile"), id="LowerQuartile"),
            pytest.param((UpperQuartile, "Upper Quartile"), id="UpperQuartile"),
            pytest.param(
                (InterQuartileRange, "Inter Quartile Range"), id="InterQuartileRange"
            ),
        ]
    )
    def numeric_statistic(self, request):
        return request.param

    def test_invalid_numeric_statistic(self, numeric_statistic, non_numeric_var):
        """Test each numeric statistic with each invalid variable type.

        Both input fixtures are parametrised, so produces Cartesian product.
        Error message is independent of inputs, so doesn't need parametrising.

        """
        statistic, display_name = numeric_statistic
        with pytest.raises(ValueError) as exc_info:
            invalid_numeric_statistic = statistic(non_numeric_var)
        assert exc_info.value.args[0] == "The operand must be a Numeric variable"


class TestNumericOrSelectorStatistics:
    @pytest.mark.parametrize(
        ["statistic", "var_type", "display_name"],
        # sorry Black!
        # fmt: off
        [
            pytest.param(CountDistinct, "Sel", "Count Distinct(Store)", id="CountDistinct-Selector"), # noqa
            pytest.param(CountMode, "Sel", "Count Mode(Store)", id="CountMode-Selector"), # noqa
            pytest.param(CountDistinct, "Num", "Count Distinct(Profit)", id="CountDistinct-Numeric"), # noqa
            pytest.param(CountMode, "Num", "Count Mode(Profit)", id="CountMode-Numeric"), # noqa
        ]
        # fmt: on
    )
    def test_num_or_sel_statistic(
        self,
        statistic,
        var_type,
        display_name,
        rtl_var_purchase_store,
        rtl_var_purchase_profit,
        rtl_table_purchases,
    ):
        """Test each numeric/selector statistic with per-type variable input."""
        var = {"Sel": rtl_var_purchase_store, "Num": rtl_var_purchase_profit}[var_type]
        num_or_sel_statistic = statistic(var)
        assert num_or_sel_statistic.table is rtl_table_purchases
        assert num_or_sel_statistic._name == display_name

    @pytest.fixture(params=VARIABLE_TYPES[2:])
    def non_num_or_sel_var(self, request, retail_var_lookup):
        var = retail_var_lookup[request.param]
        return var

    @pytest.fixture(
        params=[
            pytest.param((CountDistinct, "Count Distinct"), id="CountDistinct"),
            pytest.param((CountMode, "Count Mode"), id="CountMode"),
        ]
    )
    def num_or_sel_statistic(self, request):
        return request.param

    def test_invalid_num_or_sel_statistic(
        self, num_or_sel_statistic, non_num_or_sel_var
    ):
        """Test each numeric/selector statistic with each invalid variable type.

        Both input fixtures are parametrised, so produces Cartesian product.
        Error message is independent of inputs, so doesn't need parametrising.

        """
        statistic, display_name = num_or_sel_statistic
        with pytest.raises(ValueError) as exc_info:
            invalid_num_or_sel_statistic = statistic(non_num_or_sel_var)
        assert exc_info.value.args[0] == (
            "The operand must be a Numeric or Selector variable"
        )


class TestStatistic:
    def test_statistic_to_model_measure(self, rtl_table_purchases, rtl_var_purchase_department):
        statistic = Mock(
            table=rtl_table_purchases,
            operand=rtl_var_purchase_department,
            label=None,
            _name="Chi Squared Probability(Department)",
            _model_function="ChiSqProb",
        )
        expected_statistic_measure_model = aa.Measure(
            id="Chi Squared Probability(Department)",
            resolve_table_name="Purchases",
            function="ChiSqProb",
            variable_name="puDept",
        )
        assert Statistic._to_model_measure(statistic, rtl_table_purchases) == expected_statistic_measure_model

    def test_statistic_to_model_measure_custom_name(self, rtl_table_customers, rtl_var_customer_email):
        statistic = Mock(
            table=rtl_table_customers,
            operand=rtl_var_customer_email,
            label="Magic email insight",
            _name="Cramér's V(Customer Email)",
            _model_function="CramersV",
        )
        expected_statistic_measure_model = aa.Measure(
            id="Magic email insight",
            resolve_table_name="Customers",
            function="CramersV",
            variable_name="cuEmail",
        )
        assert Statistic._to_model_measure(statistic, rtl_table_customers) == expected_statistic_measure_model

    def test_statistic_to_model_measure_different_table(self, rtl_table_purchases, rtl_var_purchase_profit, rtl_table_customers):
        statistic = Mock(
            table=rtl_table_purchases,
            operand=rtl_var_purchase_profit,
            label=None,
            _name="Max(Profit)",
            _model_function="Maximum",
        )
        expected_statistic_measure_model = aa.Measure(
            id="Max(Profit)",
            resolve_table_name="Customers",
            function="Maximum",
            variable_name="puProfit",
        )
        assert Statistic._to_model_measure(statistic, rtl_table_customers) == expected_statistic_measure_model
