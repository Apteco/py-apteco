import pytest

from apteco.tables import Table


@pytest.fixture()
def fake_parent_table(mocker):
    return mocker.Mock()


@pytest.fixture()
def fake_child_tables(mocker):
    child1 = mocker.Mock()
    child2 = mocker.Mock()
    return [child1, child2]


# unused
@pytest.fixture()
def fake_parent_tables(mocker):
    parent1 = mocker.Mock()
    parent2 = mocker.Mock()
    return [parent1, parent2]


@pytest.fixture()
def fake_ancestor_tables(mocker):
    ancestor1 = mocker.Mock()
    ancestor2 = mocker.Mock()
    return [ancestor1, ancestor2]


@pytest.fixture()
def fake_descendant_tables(mocker):
    descendant1 = mocker.Mock()
    descendant2 = mocker.Mock()
    return [descendant1, descendant2]


@pytest.fixture()
def fake_variables(mocker):
    variable1 = mocker.Mock()
    variable2 = mocker.Mock()
    return {"var1": variable1, "var2": variable2}


@pytest.fixture()
def fake_table_with_variables():
    table = Table(*[None] * 14, {"var1": "my first variable"})
    return table


@pytest.fixture()
def fake_customers_table():
    customers = Table("Customers", *[None] * 14)
    return customers


@pytest.fixture()
def fake_products_table():
    products = Table("Products", *[None] * 14)
    return products


@pytest.fixture()
def fake_purchases_table(fake_customers_table, fake_products_table):
    purchases = Table(
        "Purchases",
        *[None] * 7,
        True,
        None,
        fake_customers_table,
        fake_products_table,
        [fake_customers_table],
        [fake_products_table],
        None,
    )
    return purchases


@pytest.fixture()
def fake_web_visits_table():
    web_visits = Table("Web Visits", *[None] * 14)
    return web_visits


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
        assert table_example.singular_display_name == "the singularity"
        assert table_example.plural_display_name == "first person plural"
        assert table_example.is_default_table is False
        assert table_example.is_people_table is True
        assert table_example.total_records == 123_456_789
        assert table_example.child_relationship_name == "sweet child of mine"
        assert table_example.parent_relationship_name == "the parent trap"
        assert table_example.has_child_tables is True
        assert table_example.parent_name == "mother nature"
        assert table_example.parent is fake_parent_table
        assert table_example.children is fake_child_tables
        assert table_example.ancestors is fake_ancestor_tables
        assert table_example.descendants is fake_descendant_tables
        assert table_example.variables is fake_variables
        assert table_example.session == "court of session"

    def test_table_eq(self):
        fake_people_table1 = Table("People", "person", *[None] * 13)
        fake_people_table2 = Table("People", "human", *[None] * 13)
        fake_purchases_table = Table("Purchases", "purchase", *[None] * 13)
        assert fake_people_table1 == fake_people_table2
        assert fake_people_table1 != fake_purchases_table

    def test_table_lt(
        self, fake_customers_table, fake_purchases_table, fake_web_visits_table
    ):
        assert fake_customers_table < fake_purchases_table
        assert not fake_web_visits_table < fake_purchases_table

    def test_table_gt(
        self,
        fake_customers_table,
        fake_purchases_table,
        fake_products_table,
        fake_web_visits_table,
    ):
        assert fake_products_table > fake_purchases_table
        assert not fake_web_visits_table > fake_purchases_table

    def test_table_getitem(self, fake_table_with_variables):
        assert fake_table_with_variables["var1"] == "my first variable"
        with pytest.raises(KeyError) as excinfo:
            my_second_variable = fake_table_with_variables["var2"]
        exception_msg = excinfo.value.args[0]
        assert exception_msg == "var2"
