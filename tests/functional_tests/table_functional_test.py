class TestTableRelations:
    def test_eq(self, chy_supporters_table, chy_campaigns_table, chy_donations_table, chy_website_visits_table):
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

    def test_lt(self, chy_supporters_table, chy_campaigns_table, chy_donations_table, chy_website_visits_table):
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

    def test_le(self, chy_supporters_table, chy_campaigns_table, chy_donations_table, chy_website_visits_table):
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

    def test_gt(self, chy_supporters_table, chy_campaigns_table, chy_donations_table, chy_website_visits_table):
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
        
    def test_ge(self, chy_supporters_table, chy_campaigns_table, chy_donations_table, chy_website_visits_table):
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

    def test_ne(self, chy_supporters_table, chy_campaigns_table, chy_donations_table, chy_website_visits_table):
        assert chy_campaigns_table != chy_donations_table
        assert not chy_campaigns_table != chy_campaigns_table

    """def test_is_related(self, chy_supporters_table, chy_campaigns_table, chy_donations_table, chy_website_visits_table):
        assert not chy_supporters_table.is_related(chy_supporters_table)
        assert chy_supporters_table.is_related(chy_campaigns_table)
        assert chy_supporters_table.is_related(chy_donations_table)
        assert chy_supporters_table.is_related(chy_website_visits_table)
        assert chy_supporters_table.is_related(chy_supporters_table, allow_same=True)
        assert chy_supporters_table.is_related(chy_campaigns_table, allow_same=True)
        assert chy_supporters_table.is_related(chy_donations_table, allow_same=True)
        assert chy_supporters_table.is_related(chy_website_visits_table, allow_same=True)

        assert chy_campaigns_table.is_related(chy_supporters_table)
        assert not chy_campaigns_table.is_related(chy_campaigns_table)
        assert chy_campaigns_table.is_related(chy_donations_table)
        assert chy_campaigns_table.is_related(chy_website_visits_table)
        assert chy_campaigns_table.is_related(chy_supporters_table, allow_same=True)
        assert chy_campaigns_table.is_related(chy_campaigns_table, allow_same=True)
        assert chy_campaigns_table.is_related(chy_donations_table, allow_same=True)
        assert chy_campaigns_table.is_related(chy_website_visits_table, allow_same=True)

        assert chy_donations_table.is_related(chy_supporters_table)
        assert chy_donations_table.is_related(chy_campaigns_table)
        assert not chy_donations_table.is_related(chy_donations_table)
        assert not chy_donations_table.is_related(chy_website_visits_table)
        assert chy_donations_table.is_related(chy_supporters_table, allow_same=True)
        assert chy_donations_table.is_related(chy_campaigns_table, allow_same=True)
        assert chy_donations_table.is_related(chy_donations_table, allow_same=True)
        assert not chy_donations_table.is_related(chy_website_visits_table, allow_same=True)

        assert chy_website_visits_table.is_related(chy_supporters_table)
        assert chy_website_visits_table.is_related(chy_campaigns_table)
        assert not chy_website_visits_table.is_related(chy_donations_table)
        assert not chy_website_visits_table.is_related(chy_website_visits_table)
        assert chy_website_visits_table.is_related(chy_supporters_table, allow_same=True)
        assert chy_website_visits_table.is_related(chy_campaigns_table, allow_same=True)
        assert not chy_website_visits_table.is_related(chy_donations_table, allow_same=True)
        assert chy_website_visits_table.is_related(chy_website_visits_table, allow_same=True)"""
