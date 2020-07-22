from unittest.mock import Mock

import pytest

from apteco.session import Table, SelectorVariable, DateTimeVariable, TextVariable, \
    ReferenceVariable, FlagArrayVariable

"""
Fake system table structure:

Customers
└── Purchases

"""


@pytest.fixture()
def fake_table_customers():
    table = Mock(spec=Table)
    table.configure_mock(name="Customers")
    return table


@pytest.fixture()
def fake_table_purchases():
    table = Mock(spec=Table)
    table.configure_mock(name="Purchases", plural_display_name="purchases")
    return table


@pytest.fixture()
def fake_var_customer_id(fake_table_customers):
    var = Mock(spec=ReferenceVariable)
    var.configure_mock(
        name="cuID",
        description="Customer ID",
        type="Reference",
        table=fake_table_customers,
    )
    return var


@pytest.fixture()
def fake_var_customer_first_name(fake_table_customers):
    var = Mock(spec=TextVariable)
    var.configure_mock(
        name="cuFName",
        description="Customer First Name",
        type="Text",
        table=fake_table_customers,
    )
    return var


@pytest.fixture()
def fake_var_customer_surname(fake_table_customers):
    var = Mock(spec=TextVariable)
    var.configure_mock(
        name="cuSName",
        description="Customer Surname",
        type="Text",
        table=fake_table_customers,
    )
    return var


@pytest.fixture()
def fake_var_customer_gender(fake_table_customers):
    var = Mock(spec=SelectorVariable)
    var.configure_mock(
        name="cuGender",
        description="Gender",
        type="Selector",
        table=fake_table_customers,
    )
    return var


@pytest.fixture()
def fake_var_customer_contact_pref(fake_table_customers):
    var = Mock(spec=FlagArrayVariable)
    var.configure_mock(
        name="cuContac",
        description="Customer Contact Preferences",
        type="FlagArray",
        table=fake_table_customers,
    )
    return var


@pytest.fixture()
def fake_var_purchase_id(fake_table_purchases):
    var = Mock(spec=ReferenceVariable)
    var.configure_mock(
        name="puID",
        description="Purchase ID",
        type="Reference",
        table=fake_table_purchases,
    )
    return var


@pytest.fixture()
def fake_var_purchase_department(fake_table_purchases):
    var = Mock(spec=SelectorVariable)
    var.configure_mock(
        name="puDept",
        description="Department",
        type="Selector",
        table=fake_table_purchases,
    )
    return var


@pytest.fixture()
def fake_var_purchase_date(fake_table_purchases):
    var = Mock(spec=DateTimeVariable)
    var.configure_mock(
        name="puDate",
        description="Purchase Date",
        type="DateTime",
        table=fake_table_purchases,
    )
    return var


@pytest.fixture()
def fake_var_purchase_store_type(fake_table_purchases):
    var = Mock(spec=SelectorVariable)
    var.configure_mock(
        name="puStType",
        description="Store Type",
        type="Selector",
        table=fake_table_purchases,
    )
    return var


@pytest.fixture()
def fake_var_purchase_payment_method(fake_table_purchases):
    var = Mock(spec=SelectorVariable)
    var.configure_mock(
        name="puPayMtd",
        description="Payment Method",
        type="Selector",
        table=fake_table_purchases,
    )
    return var


@pytest.fixture()
def fake_sel_last_week_customers(fake_table_customers):
    return Mock(
        table=fake_table_customers,
        _to_model=Mock(return_value="selection_model"),
    )


@pytest.fixture()
def fake_session():
    return Mock(data_view="acme_inc", system="sales", api_client="my_api_client")


@pytest.fixture()
def fake_sel_high_value_purchases(fake_table_purchases):
    return Mock(
        table=fake_table_purchases,
        _to_model=Mock(return_value="selection_high_value_purchases_model"),
    )
