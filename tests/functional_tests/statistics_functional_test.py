import apteco_api as aa

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


class TestSum:
    def test_sum_to_model_measure(self, chy_numeric_var_cost, chy_campaigns_table):
        sum_statistic = Sum(chy_numeric_var_cost)
        expected_sum_measure_model = aa.Measure(
            id="Sum(Cost)",
            resolve_table_name="Campaigns",
            function="Sum",
            variable_name="caCost",
        )
        assert (
            sum_statistic._to_model_measure(chy_campaigns_table)
            == expected_sum_measure_model
        )

    def test_sum_to_model_measure_custom_name_different_table(
        self, chy_numeric_var_cost, chy_supporters_table
    ):
        sum_statistic = Sum(chy_numeric_var_cost, label="Total cost")
        expected_sum_measure_model = aa.Measure(
            id="Total cost",
            resolve_table_name="Supporters",
            function="Sum",
            variable_name="caCost",
        )
        assert (
            sum_statistic._to_model_measure(chy_supporters_table)
            == expected_sum_measure_model
        )


class TestMean:
    def test_mean_to_model_measure(self, chy_numeric_var_amount, chy_donations_table):
        mean_statistic = Mean(chy_numeric_var_amount)
        expected_mean_measure_model = aa.Measure(
            id="Mean(Amount)",
            resolve_table_name="Donations",
            function="Mean",
            variable_name="doAmount",
        )
        assert (
            mean_statistic._to_model_measure(chy_donations_table)
            == expected_mean_measure_model
        )

    def test_mean_to_model_measure_custom_name_different_table(
        self, chy_numeric_var_amount, chy_campaigns_table
    ):
        mean_statistic = Mean(chy_numeric_var_amount, label="Average donated")
        expected_mean_measure_model = aa.Measure(
            id="Average donated",
            resolve_table_name="Campaigns",
            function="Mean",
            variable_name="doAmount",
        )
        assert (
            mean_statistic._to_model_measure(chy_campaigns_table)
            == expected_mean_measure_model
        )


class TestPopulated:
    def test_populated_to_model_measure(
        self, chy_numeric_var_age, chy_supporters_table
    ):
        populated_statistic = Populated(chy_numeric_var_age)
        expected_populated_measure_model = aa.Measure(
            id="Populated(Age)",
            resolve_table_name="Supporters",
            function="VariableCount",
            variable_name="suAge",
        )
        assert (
            populated_statistic._to_model_measure(chy_supporters_table)
            == expected_populated_measure_model
        )

    def test_populated_to_model_measure_custom_name_different_table(
        self, chy_numeric_var_age, chy_donations_table
    ):
        populated_statistic = Populated(chy_numeric_var_age, label="Number age known")
        expected_populated_measure_model = aa.Measure(
            id="Number age known",
            resolve_table_name="Donations",
            function="VariableCount",
            variable_name="suAge",
        )
        assert (
            populated_statistic._to_model_measure(chy_donations_table)
            == expected_populated_measure_model
        )


class TestMin:
    def test_min_to_model_measure(self, chy_numeric_var_cost, chy_campaigns_table):
        min_statistic = Min(chy_numeric_var_cost)
        expected_min_measure_model = aa.Measure(
            id="Min(Cost)",
            resolve_table_name="Campaigns",
            function="Minimum",
            variable_name="caCost",
        )
        assert (
            min_statistic._to_model_measure(chy_campaigns_table)
            == expected_min_measure_model
        )

    def test_min_to_model_measure_custom_name_different_table(
        self, chy_numeric_var_cost, chy_website_visits_table
    ):
        min_statistic = Min(chy_numeric_var_cost, label="Smallest donation")
        expected_min_measure_model = aa.Measure(
            id="Smallest donation",
            resolve_table_name="WebsiteVisits",
            function="Minimum",
            variable_name="caCost",
        )
        assert (
            min_statistic._to_model_measure(chy_website_visits_table)
            == expected_min_measure_model
        )


class TestMax:
    def test_max_to_model_measure(self, chy_numeric_var_cost, chy_campaigns_table):
        max_statistic = Max(chy_numeric_var_cost)
        expected_max_measure_model = aa.Measure(
            id="Max(Cost)",
            resolve_table_name="Campaigns",
            function="Maximum",
            variable_name="caCost",
        )
        assert (
            max_statistic._to_model_measure(chy_campaigns_table)
            == expected_max_measure_model
        )

    def test_max_to_model_measure_custom_name_different_table(
        self, chy_numeric_var_cost, chy_donations_table
    ):
        max_statistic = Max(chy_numeric_var_cost, label="Largest donation")
        expected_max_measure_model = aa.Measure(
            id="Largest donation",
            resolve_table_name="Donations",
            function="Maximum",
            variable_name="caCost",
        )
        assert (
            max_statistic._to_model_measure(chy_donations_table)
            == expected_max_measure_model
        )


class TestMedian:
    def test_median_to_model_measure(self, chy_numeric_var_amount, chy_donations_table):
        median_statistic = Median(chy_numeric_var_amount)
        expected_median_measure_model = aa.Measure(
            id="Median(Amount)",
            resolve_table_name="Donations",
            function="Median",
            variable_name="doAmount",
        )
        assert (
            median_statistic._to_model_measure(chy_donations_table)
            == expected_median_measure_model
        )

    def test_median_to_model_measure_custom_name_different_table(
        self, chy_numeric_var_amount, chy_supporters_table
    ):
        median_statistic = Median(chy_numeric_var_amount, label="Average amount")
        expected_median_measure_model = aa.Measure(
            id="Average amount",
            resolve_table_name="Supporters",
            function="Median",
            variable_name="doAmount",
        )
        assert (
            median_statistic._to_model_measure(chy_supporters_table)
            == expected_median_measure_model
        )


class TestMode:
    def test_mode_to_model_measure(self, chy_numeric_var_amount, chy_donations_table):
        mode_statistic = Mode(chy_numeric_var_amount)
        expected_mode_measure_model = aa.Measure(
            id="Mode(Amount)",
            resolve_table_name="Donations",
            function="Mode",
            variable_name="doAmount",
        )
        assert (
            mode_statistic._to_model_measure(chy_donations_table)
            == expected_mode_measure_model
        )

    def test_mode_to_model_measure_custom_name_different_table(
        self, chy_numeric_var_amount, chy_website_visits_table
    ):
        mode_statistic = Mode(chy_numeric_var_amount, label="Most common amount")
        expected_mode_measure_model = aa.Measure(
            id="Most common amount",
            resolve_table_name="WebsiteVisits",
            function="Mode",
            variable_name="doAmount",
        )
        assert (
            mode_statistic._to_model_measure(chy_website_visits_table)
            == expected_mode_measure_model
        )


class TestVariance:
    def test_variance_to_model_measure(
        self, chy_numeric_var_duration, chy_website_visits_table
    ):
        variance_statistic = Variance(chy_numeric_var_duration)
        expected_variance_measure_model = aa.Measure(
            id="Variance(Duration)",
            resolve_table_name="WebsiteVisits",
            function="Variance",
            variable_name="weDurtn",
        )
        assert (
            variance_statistic._to_model_measure(chy_website_visits_table)
            == expected_variance_measure_model
        )

    def test_variance_to_model_measure_custom_name_different_table(
        self, chy_numeric_var_duration, chy_campaigns_table
    ):
        variance_statistic = Variance(chy_numeric_var_duration, label="Duration var")
        expected_variance_measure_model = aa.Measure(
            id="Duration var",
            resolve_table_name="Campaigns",
            function="Variance",
            variable_name="weDurtn",
        )
        assert (
            variance_statistic._to_model_measure(chy_campaigns_table)
            == expected_variance_measure_model
        )


class TestStdDev:
    def test_std_dev_to_model_measure(
        self, chy_numeric_var_duration, chy_website_visits_table
    ):
        std_dev_statistic = StdDev(chy_numeric_var_duration)
        expected_std_dev_measure_model = aa.Measure(
            id="Std Dev(Duration)",
            resolve_table_name="WebsiteVisits",
            function="StandardDeviation",
            variable_name="weDurtn",
        )
        assert (
            std_dev_statistic._to_model_measure(chy_website_visits_table)
            == expected_std_dev_measure_model
        )

    def test_std_dev_to_model_measure_custom_name_different_table(
        self, chy_numeric_var_duration, chy_supporters_table
    ):
        std_dev_statistic = StdDev(chy_numeric_var_duration, label="Duration st dev")
        expected_std_dev_measure_model = aa.Measure(
            id="Duration st dev",
            resolve_table_name="Supporters",
            function="StandardDeviation",
            variable_name="weDurtn",
        )
        assert (
            std_dev_statistic._to_model_measure(chy_supporters_table)
            == expected_std_dev_measure_model
        )


class TestLowerQuartile:
    def test_lower_quartile_to_model_measure(
        self, chy_numeric_var_age, chy_supporters_table
    ):
        lower_quartile_statistic = LowerQuartile(chy_numeric_var_age)
        expected_lower_quartile_measure_model = aa.Measure(
            id="Lower Quartile(Age)",
            resolve_table_name="Supporters",
            function="LowerQuartile",
            variable_name="suAge",
        )
        assert (
            lower_quartile_statistic._to_model_measure(chy_supporters_table)
            == expected_lower_quartile_measure_model
        )

    def test_lower_quartile_to_model_measure_custom_name_different_table(
        self, chy_numeric_var_age, chy_campaigns_table
    ):
        lower_quartile_statistic = LowerQuartile(chy_numeric_var_age, label="LQ Age")
        expected_lower_quartile_measure_model = aa.Measure(
            id="LQ Age",
            resolve_table_name="Campaigns",
            function="LowerQuartile",
            variable_name="suAge",
        )
        assert (
            lower_quartile_statistic._to_model_measure(chy_campaigns_table)
            == expected_lower_quartile_measure_model
        )


class TestUpperQuartile:
    def test_upper_quartile_to_model_measure(
        self, chy_numeric_var_age, chy_supporters_table
    ):
        upper_quartile_statistic = UpperQuartile(chy_numeric_var_age)
        expected_upper_quartile_measure_model = aa.Measure(
            id="Upper Quartile(Age)",
            resolve_table_name="Supporters",
            function="UpperQuartile",
            variable_name="suAge",
        )
        assert (
            upper_quartile_statistic._to_model_measure(chy_supporters_table)
            == expected_upper_quartile_measure_model
        )

    def test_upper_quartile_to_model_measure_custom_name_different_table(
        self, chy_numeric_var_age, chy_supporters_table
    ):
        upper_quartile_statistic = UpperQuartile(chy_numeric_var_age, label="UQ Age")
        expected_upper_quartile_measure_model = aa.Measure(
            id="UQ Age",
            resolve_table_name="Supporters",
            function="UpperQuartile",
            variable_name="suAge",
        )
        assert (
            upper_quartile_statistic._to_model_measure(chy_supporters_table)
            == expected_upper_quartile_measure_model
        )


class TestInterQuartileRange:
    def test_inter_quartile_range_to_model_measure(
        self, chy_numeric_var_duration, chy_website_visits_table
    ):
        inter_quartile_range_statistic = InterQuartileRange(chy_numeric_var_duration)
        expected_inter_quartile_range_measure_model = aa.Measure(
            id="Inter Quartile Range(Duration)",
            resolve_table_name="WebsiteVisits",
            function="InterQuartileRange",
            variable_name="weDurtn",
        )
        assert (
            inter_quartile_range_statistic._to_model_measure(chy_website_visits_table)
            == expected_inter_quartile_range_measure_model
        )

    def test_inter_quartile_range_to_model_measure_custom_name_different_table(
        self, chy_numeric_var_duration, chy_donations_table
    ):
        inter_quartile_range_statistic = InterQuartileRange(
            chy_numeric_var_duration, label="IQR Duration"
        )
        expected_inter_quartile_range_measure_model = aa.Measure(
            id="IQR Duration",
            resolve_table_name="Donations",
            function="InterQuartileRange",
            variable_name="weDurtn",
        )
        assert (
            inter_quartile_range_statistic._to_model_measure(chy_donations_table)
            == expected_inter_quartile_range_measure_model
        )


class TestCountDistinct:
    def test_count_distinct_numeric_to_model_measure(
        self, chy_numeric_var_age, chy_supporters_table
    ):
        count_distinct_statistic = CountDistinct(chy_numeric_var_age)
        expected_count_distinct_measure_model = aa.Measure(
            id="Count Distinct(Age)",
            resolve_table_name="Supporters",
            function="CountDistinct",
            variable_name="suAge",
        )
        assert (
            count_distinct_statistic._to_model_measure(chy_supporters_table)
            == expected_count_distinct_measure_model
        )

    def test_count_distinct_numeric_to_model_measure_custom_name_different_table(
        self, chy_numeric_var_age, chy_donations_table
    ):
        count_distinct_statistic = CountDistinct(
            chy_numeric_var_age, label="No. different ages of supporters"
        )
        expected_count_distinct_measure_model = aa.Measure(
            id="No. different ages of supporters",
            resolve_table_name="Donations",
            function="CountDistinct",
            variable_name="suAge",
        )
        assert (
            count_distinct_statistic._to_model_measure(chy_donations_table)
            == expected_count_distinct_measure_model
        )

    def test_count_distinct_selector_to_model_measure(
        self, chy_selector_var, chy_supporters_table
    ):
        count_distinct_statistic = CountDistinct(chy_selector_var)
        expected_count_distinct_measure_model = aa.Measure(
            id="Count Distinct(Membership)",
            resolve_table_name="Supporters",
            function="CountDistinct",
            variable_name="suMember",
        )
        assert (
            count_distinct_statistic._to_model_measure(chy_supporters_table)
            == expected_count_distinct_measure_model
        )

    def test_count_distinct_selector_to_model_measure_custom_name_different_table(
        self, chy_selector_var, chy_website_visits_table
    ):
        count_distinct_statistic = CountDistinct(
            chy_selector_var, label="No. membership types"
        )
        expected_count_distinct_measure_model = aa.Measure(
            id="No. membership types",
            resolve_table_name="WebsiteVisits",
            function="CountDistinct",
            variable_name="suMember",
        )
        assert (
            count_distinct_statistic._to_model_measure(chy_website_visits_table)
            == expected_count_distinct_measure_model
        )


class TestCountMode:
    def test_count_mode_numeric_to_model_measure(
        self, chy_numeric_var_amount, chy_donations_table
    ):
        count_mode_statistic = CountMode(chy_numeric_var_amount)
        expected_count_mode_measure_model = aa.Measure(
            id="Count Mode(Amount)",
            resolve_table_name="Donations",
            function="MaxDistinctCount",
            variable_name="doAmount",
        )
        assert (
            count_mode_statistic._to_model_measure(chy_donations_table)
            == expected_count_mode_measure_model
        )

    def test_count_mode_numeric_to_model_measure_custom_name_different_table(
        self, chy_numeric_var_amount, chy_website_visits_table
    ):
        count_mode_statistic = CountMode(
            chy_numeric_var_amount, label="No. donations of most common amount"
        )
        expected_count_mode_measure_model = aa.Measure(
            id="No. donations of most common amount",
            resolve_table_name="WebsiteVisits",
            function="MaxDistinctCount",
            variable_name="doAmount",
        )
        assert (
            count_mode_statistic._to_model_measure(chy_website_visits_table)
            == expected_count_mode_measure_model
        )

    def test_count_mode_selector_to_model_measure(
        self, chy_selector_var, chy_supporters_table
    ):
        count_mode_statistic = CountMode(chy_selector_var)
        expected_count_mode_measure_model = aa.Measure(
            id="Count Mode(Membership)",
            resolve_table_name="Supporters",
            function="MaxDistinctCount",
            variable_name="suMember",
        )
        assert (
            count_mode_statistic._to_model_measure(chy_supporters_table)
            == expected_count_mode_measure_model
        )

    def test_count_mode_selector_to_model_measure_custom_name_different_table(
        self, chy_selector_var, chy_campaigns_table
    ):
        count_mode_statistic = CountMode(
            chy_selector_var, label="Size largest membership type"
        )
        expected_count_mode_measure_model = aa.Measure(
            id="Size largest membership type",
            resolve_table_name="Campaigns",
            function="MaxDistinctCount",
            variable_name="suMember",
        )
        assert (
            count_mode_statistic._to_model_measure(chy_campaigns_table)
            == expected_count_mode_measure_model
        )
