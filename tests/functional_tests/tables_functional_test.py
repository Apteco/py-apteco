from datetime import datetime

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
def web_visits_after_lockdown(chy_datetime_var):
    lockdown_announcement = datetime(2020, 3, 23, 20, 6, 17)
    web_visits_after_lockdown = chy_datetime_var >= lockdown_announcement
    return web_visits_after_lockdown


class TestTableOperators:
    def test_mul(
        self,
        web_visits_after_lockdown,
        chy_supporters_table,
        chy_campaigns_table,
        chy_donations_table,
    ):
        assert web_visits_after_lockdown.table_name == "WebVisits"

        supporters_web_visits = chy_supporters_table * web_visits_after_lockdown
        assert supporters_web_visits.table_name == "Supporters"

        campaigns_web_visits = chy_campaigns_table * web_visits_after_lockdown
        assert campaigns_web_visits.table_name == "Campaigns"

        donations_web_visits = chy_donations_table * web_visits_after_lockdown
        assert donations_web_visits.table_name == "Donations"
