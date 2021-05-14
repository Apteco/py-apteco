import pytest

from apteco.statistics import (
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


variable_type_params = [
    pytest.param("Cost", id="Numeric"),  # included for completeness
    pytest.param("Response Type", id="Selector"),
    pytest.param("URL", id="Text"),
    pytest.param("Car Make Code", id="Array"),
    pytest.param("Newspapers", id="FlagArray"),
    pytest.param("Travel Date", id="Date"),
    pytest.param("Communication Time", id="DateTime"),
    pytest.param("Policy Number", id="Reference"),
]


class TestNumericStatistics:
    @pytest.mark.parametrize(
        ["statistic", "var", "display_name", "table"],
        # sorry Black!
        # fmt: off
        [
            pytest.param(Sum, "boCost", "Sum(Cost)", "Bookings", id="Sum"),  # noqa
            pytest.param(Mean, "boProfit", "Mean(Profit)", "Bookings", id="Mean"),  # noqa
            pytest.param(Populated, "PoPremiu", "Populated(Premium)", "Policies", id="Populated"),  # noqa
            pytest.param(Min, "ctCost", "Min(Cost of Content)", "Content", id="Min"),  # noqa
            pytest.param(Max, "PoDaysUn", "Max(Days Until Travel)", "Policies", id="Max"),  # noqa
            pytest.param(Median, "wvDuratn", "Median(Duration)", "WebVisits", id="Median"),  # noqa
            pytest.param(Mode, "cmRun", "Mode(Run)", "Communications", id="Mode"),  # noqa
            pytest.param(Variance, "raRspRev", "Variance(Revenue)", "Responses Attributed", id="Variance"),  # noqa
            pytest.param(StdDev, "raPercen", "Std Dev(Percentage Attributed)", "Responses Attributed", id="StdDev"),  # noqa
            pytest.param(LowerQuartile, "boCost", "Lower Quartile(Cost)", "Bookings", id="LowerQuartile"),  # noqa
            pytest.param(UpperQuartile, "boProfit", "Upper Quartile(Profit)", "Bookings", id="UpperQuartile"),  # noqa
            pytest.param(InterQuartileRange, "PoPremiu", "Inter Quartile Range(Premium)", "Policies", id="InterQuartileRange"),  # noqa
        ]
        # fmt: on
    )
    def test_numeric_statistic(self, statistic, var, display_name, table, holidays):
        """Test each numeric statistic with individualised numeric variable input."""
        numeric_statistic = statistic(holidays.variables[var])
        assert numeric_statistic.table is holidays.tables[table]
        assert numeric_statistic._name == display_name

    @pytest.fixture(params=variable_type_params[1:], scope="session")
    def non_numeric_var(self, request, holidays):
        var = holidays.variables[request.param]
        return var

    @pytest.fixture(
        # sorry Black!
        # fmt: off
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
            pytest.param((InterQuartileRange, "Inter Quartile Range"), id="InterQuartileRange"),  # noqa
        ],
        scope="session",
        # fmt: on
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
        ["statistic", "var", "display_name", "table"],
        # sorry Black!
        # fmt: off
        [
            pytest.param(CountDistinct, "boKeyCd", "Count Distinct(Response Code)", "Bookings", id="CountDistinct-Selector"), # noqa
            pytest.param(CountMode, "hoTown", "Count Mode(Town)", "Households", id="CountMode-Selector"), # noqa
            pytest.param(CountDistinct, "fWaitDay", "Count Distinct(Days Waiting)", "Journey History", id="CountDistinct-Numeric"), # noqa
            pytest.param(CountMode, "wvDuratn", "Count Mode(Duration)", "WebVisits", id="CountMode-Numeric"), # noqa
        ]
        # fmt: on
    )
    def test_num_or_sel_statistic(self, statistic, var, display_name, table, holidays):
        """Test each numeric/selector statistic with individualised variable input."""
        num_or_sel_statistic = statistic(holidays.variables[var])
        assert num_or_sel_statistic.table is holidays.tables[table]
        assert num_or_sel_statistic._name == display_name

    @pytest.fixture(params=variable_type_params[2:], scope="session")
    def non_num_or_sel_var(self, request, holidays):
        var = holidays.variables[request.param]
        return var

    @pytest.fixture(
        params=[
            pytest.param((CountDistinct, "Count Distinct"), id="CountDistinct"),
            pytest.param((CountMode, "Count Mode"), id="CountMode"),
        ],
        scope="session",
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
