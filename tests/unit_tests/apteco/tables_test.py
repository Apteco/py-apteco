from unittest.mock import Mock

import apteco_api as aa
import pytest

from apteco.tables import Table


@pytest.fixture()
def fake_parent_table():
    return Mock()


@pytest.fixture()
def fake_child_tables():
    child1 = Mock()
    child2 = Mock()
    return [child1, child2]


# unused
@pytest.fixture()
def fake_parent_tables():
    parent1 = Mock()
    parent2 = Mock()
    return [parent1, parent2]


@pytest.fixture()
def fake_ancestor_tables():
    ancestor1 = Mock()
    ancestor2 = Mock()
    return [ancestor1, ancestor2]


@pytest.fixture()
def fake_descendant_tables():
    descendant1 = Mock()
    descendant2 = Mock()
    return [descendant1, descendant2]


@pytest.fixture()
def fake_variables():
    variable1 = Mock()
    variable2 = Mock()
    return {"var1": variable1, "var2": variable2}


class TestTable:
    def test_table_init(
        self,
        fake_parent_table,
        fake_child_tables,
        fake_ancestor_tables,
        fake_descendant_tables,
        fake_variables,
    ):
        table_example = Table(
            "what's in a name",
            "the singularity",
            "first person plural",
            False,
            True,
            123_456_789,
            "sweet child of mine",
            "the parent trap",
            True,
            "mother nature",
            fake_parent_table,
            fake_child_tables,
            fake_ancestor_tables,
            fake_descendant_tables,
            fake_variables,
            session="court of session",
        )
        assert table_example.name == "what's in a name"
        assert table_example.singular == "the singularity"
        assert table_example.plural == "first person plural"
        assert table_example.is_default is False
        assert table_example.is_people is True
        assert table_example.total_records == 123_456_789
        assert table_example.child_relationship == "sweet child of mine"
        assert table_example.parent_relationship == "the parent trap"
        assert table_example.has_children is True
        assert table_example.parent_name == "mother nature"
        assert table_example.parent is fake_parent_table
        assert table_example.children is fake_child_tables
        assert table_example.ancestors is fake_ancestor_tables
        assert table_example.descendants is fake_descendant_tables
        assert table_example.variables is fake_variables
        assert table_example.session == "court of session"

    def test_to_model_measure(self, rtl_table_purchases, rtl_table_customers):
        expected_measures_model = aa.Measure(
            id="Purchases",
            resolve_table_name="Purchases",
            function="Count",
            variable_name=None,
        )

        assert (
            Table._to_model_measure(rtl_table_purchases, rtl_table_customers)
            == expected_measures_model
        )
