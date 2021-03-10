from datetime import datetime
from unittest.mock import MagicMock

import pytest


class TestTableRelations:
    def test_eq(
        self,
        chy_supporters_table,
        chy_campaigns_table,
        chy_donations_table,
        chy_website_visits_table,
    ):
        assert chy_supporters_table == chy_supporters_table
        assert not chy_supporters_table == chy_campaigns_table
        assert not chy_supporters_table == chy_donations_table
        assert not chy_supporters_table == chy_website_visits_table

        assert not chy_campaigns_table == chy_supporters_table
        assert chy_campaigns_table == chy_campaigns_table
        assert not chy_campaigns_table == chy_donations_table
        assert not chy_campaigns_table == chy_website_visits_table

        assert not chy_donations_table == chy_supporters_table
        assert not chy_donations_table == chy_campaigns_table
        assert chy_donations_table == chy_donations_table
        assert not chy_donations_table == chy_website_visits_table

        assert not chy_website_visits_table == chy_supporters_table
        assert not chy_website_visits_table == chy_campaigns_table
        assert not chy_website_visits_table == chy_donations_table
        assert chy_website_visits_table == chy_website_visits_table

    def test_lt(
        self,
        chy_supporters_table,
        chy_campaigns_table,
        chy_donations_table,
        chy_website_visits_table,
    ):
        assert not chy_supporters_table < chy_supporters_table
        assert chy_supporters_table < chy_campaigns_table
        assert chy_supporters_table < chy_donations_table
        assert chy_supporters_table < chy_website_visits_table

        assert not chy_campaigns_table < chy_supporters_table
        assert not chy_campaigns_table < chy_campaigns_table
        assert chy_campaigns_table < chy_donations_table
        assert not chy_campaigns_table < chy_website_visits_table

        assert not chy_donations_table < chy_supporters_table
        assert not chy_donations_table < chy_campaigns_table
        assert not chy_donations_table < chy_donations_table
        assert not chy_donations_table < chy_website_visits_table

        assert not chy_website_visits_table < chy_supporters_table
        assert not chy_website_visits_table < chy_campaigns_table
        assert not chy_website_visits_table < chy_donations_table
        assert not chy_website_visits_table < chy_website_visits_table

    def test_le(
        self,
        chy_supporters_table,
        chy_campaigns_table,
        chy_donations_table,
        chy_website_visits_table,
    ):
        assert chy_supporters_table <= chy_supporters_table
        assert chy_supporters_table <= chy_campaigns_table
        assert chy_supporters_table <= chy_donations_table
        assert chy_supporters_table <= chy_website_visits_table

        assert not chy_campaigns_table <= chy_supporters_table
        assert chy_campaigns_table <= chy_campaigns_table
        assert chy_campaigns_table <= chy_donations_table
        assert not chy_campaigns_table <= chy_website_visits_table

        assert not chy_donations_table <= chy_supporters_table
        assert not chy_donations_table <= chy_campaigns_table
        assert chy_donations_table <= chy_donations_table
        assert not chy_donations_table <= chy_website_visits_table

        assert not chy_website_visits_table <= chy_supporters_table
        assert not chy_website_visits_table <= chy_campaigns_table
        assert not chy_website_visits_table <= chy_donations_table
        assert chy_website_visits_table <= chy_website_visits_table

    def test_gt(
        self,
        chy_supporters_table,
        chy_campaigns_table,
        chy_donations_table,
        chy_website_visits_table,
    ):
        assert not chy_supporters_table > chy_supporters_table
        assert not chy_supporters_table > chy_campaigns_table
        assert not chy_supporters_table > chy_donations_table
        assert not chy_supporters_table > chy_website_visits_table

        assert chy_campaigns_table > chy_supporters_table
        assert not chy_campaigns_table > chy_campaigns_table
        assert not chy_campaigns_table > chy_donations_table
        assert not chy_campaigns_table > chy_website_visits_table

        assert chy_donations_table > chy_supporters_table
        assert chy_donations_table > chy_campaigns_table
        assert not chy_donations_table > chy_donations_table
        assert not chy_donations_table > chy_website_visits_table

        assert chy_website_visits_table > chy_supporters_table
        assert not chy_website_visits_table > chy_campaigns_table
        assert not chy_website_visits_table > chy_donations_table
        assert not chy_website_visits_table > chy_website_visits_table

    def test_ge(
        self,
        chy_supporters_table,
        chy_campaigns_table,
        chy_donations_table,
        chy_website_visits_table,
    ):
        assert chy_supporters_table >= chy_supporters_table
        assert not chy_supporters_table >= chy_campaigns_table
        assert not chy_supporters_table >= chy_donations_table
        assert not chy_supporters_table >= chy_website_visits_table

        assert chy_campaigns_table >= chy_supporters_table
        assert chy_campaigns_table >= chy_campaigns_table
        assert not chy_campaigns_table >= chy_donations_table
        assert not chy_campaigns_table >= chy_website_visits_table

        assert chy_donations_table >= chy_supporters_table
        assert chy_donations_table >= chy_campaigns_table
        assert chy_donations_table >= chy_donations_table
        assert not chy_donations_table >= chy_website_visits_table

        assert chy_website_visits_table >= chy_supporters_table
        assert not chy_website_visits_table >= chy_campaigns_table
        assert not chy_website_visits_table >= chy_donations_table
        assert chy_website_visits_table >= chy_website_visits_table

    def test_ne(
        self,
        chy_supporters_table,
        chy_campaigns_table,
        chy_donations_table,
        chy_website_visits_table,
    ):
        assert not chy_supporters_table != chy_supporters_table
        assert chy_supporters_table != chy_campaigns_table
        assert chy_supporters_table != chy_donations_table
        assert chy_supporters_table != chy_website_visits_table

        assert chy_campaigns_table != chy_supporters_table
        assert not chy_campaigns_table != chy_campaigns_table
        assert chy_campaigns_table != chy_donations_table
        assert chy_campaigns_table != chy_website_visits_table

        assert chy_donations_table != chy_supporters_table
        assert chy_donations_table != chy_campaigns_table
        assert not chy_donations_table != chy_donations_table
        assert chy_donations_table != chy_website_visits_table

        assert chy_website_visits_table != chy_supporters_table
        assert chy_website_visits_table != chy_campaigns_table
        assert chy_website_visits_table != chy_donations_table
        assert not chy_website_visits_table != chy_website_visits_table


@pytest.fixture
def recurring_campaigns(chy_array_var):
    recurring_campaigns = chy_array_var == "recurring"
    return recurring_campaigns


@pytest.fixture
def web_visits_after_lockdown(chy_datetime_var):
    lockdown_announcement = datetime(2020, 3, 23, 20, 6, 17)
    web_visits_after_lockdown = chy_datetime_var >= lockdown_announcement
    return web_visits_after_lockdown


class TestTableOperators:
    def test_getitem(self, chy_campaigns_table):
        # Test that __getitem__ is connected to .variables
        # Not designed to test VariablesAccessor
        # - that is covered in variables_integration_test.py::TestVariablesAccessor
        fake_variables_accessor = MagicMock()
        fake_variables_accessor.__getitem__.side_effect = ["var1", "var2", "var3"]
        chy_campaigns_table.variables = fake_variables_accessor

        first = chy_campaigns_table["one"]
        second = chy_campaigns_table["two"]
        third = chy_campaigns_table["three"]

        assert first == "var1"
        assert second == "var2"
        assert third == "var3"

    def test_mul_related_tables(
        self,
        recurring_campaigns,
        chy_supporters_table,
        chy_campaigns_table,
        chy_donations_table,
        chy_website_visits_table,
    ):
        assert recurring_campaigns.table_name == "Campaigns"

        supporters_recurring_campaigns = chy_supporters_table * recurring_campaigns
        assert supporters_recurring_campaigns.table_name == "Supporters"

        # check 'changing' to itself
        campaigns_recurring_campaigns = chy_campaigns_table * recurring_campaigns
        assert campaigns_recurring_campaigns.table_name == "Campaigns"
        assert campaigns_recurring_campaigns is recurring_campaigns

        donations_recurring_campaigns = chy_donations_table * recurring_campaigns
        assert donations_recurring_campaigns.table_name == "Donations"

        # this table isn't related but is included for completeness
        web_visits_recurring_campaigns = chy_website_visits_table * recurring_campaigns
        assert web_visits_recurring_campaigns.table_name == "WebVisits"

    def test_mul_unrelated_tables(
        self,
        web_visits_after_lockdown,
        chy_supporters_table,
        chy_campaigns_table,
        chy_donations_table,
        chy_website_visits_table,
    ):
        assert web_visits_after_lockdown.table_name == "WebVisits"

        # this table *is* related (master table) but is included for completeness
        supporters_web_visits = chy_supporters_table * web_visits_after_lockdown
        assert supporters_web_visits.table_name == "Supporters"

        campaigns_web_visits = chy_campaigns_table * web_visits_after_lockdown
        assert campaigns_web_visits.table_name == "Campaigns"

        donations_web_visits = chy_donations_table * web_visits_after_lockdown
        assert donations_web_visits.table_name == "Donations"

        # check 'changing' to itself
        website_visits_web_visits = chy_website_visits_table * web_visits_after_lockdown
        assert website_visits_web_visits.table_name == "WebVisits"
        assert website_visits_web_visits is web_visits_after_lockdown
