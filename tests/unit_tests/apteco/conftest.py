from unittest.mock import Mock

import pytest

from apteco import Session
from apteco.tables import Table
from apteco.variables import (
    DateTimeVariable,
    FlagArrayVariable,
    NumericVariable,
    ReferenceVariable,
    SelectorVariable,
    TextVariable,
)


"""
Fake 'Retail' system
====================

For use in unit tests.

* session, tables, variables & selections are Mock objects
* session, tables & variables have `spec` set to the corresponding py-apteco class
* variables & selections have a reference to their table, but not the session

Tables
------

Customers       | rtl_table_customers
└── Purchases   | rtl_table_purchases

Variables
---------

 Table      |  Description                  |  Name     |  Type     |
---------------------------------------------------------------------
Customers   | Customer ID                   | cuID      | Reference | rtl_var_customer_id
Customers   | Customer First Name           | cuFName   | Text      | rtl_var_customer_first_name
Customers   | Customer Surname              | cuSName   | Text      | rtl_var_customer_surname
Customers   | Gender                        | cuGender  | Selector  | rtl_var_customer_gender
Customers   | Customer Contact Preferences  | cuContac  | FlagArray | rtl_var_customer_contact_pref
------------|-------------------------------|-----------|-----------|
Purchases   | Purchase ID                   | puID      | Reference | rtl_var_purchase_id
Purchases   | Store                         | puStore   | Selector  | rtl_var_purchase_store
Purchases   | Department                    | puDept    | Selector  | rtl_var_purchase_department
Purchases   | Purchase Date                 | puDate    | DateTime  | rtl_var_purchase_date
Purchases   | Store Type                    | puStType  | Selector  | rtl_var_purchase_store_type
Purchases   | Payment Method                | puPayMtd  | Selector  | rtl_var_purchase_payment_method
Purchases   | Profit                        | puProfit  | Numeric   | rtl_var_purchase_profit

"""


@pytest.fixture()
def rtl_session():
    return Mock(
        spec=Session, data_view="acme_inc", system="retail", api_client="my_api_client"
    )


@pytest.fixture()
def rtl_table_customers():
    table = Mock(spec=Table)
    table.configure_mock(name="Customers", is_people=True)
    return table


@pytest.fixture()
def rtl_table_purchases():
    table = Mock(spec=Table)
    table.configure_mock(
        name="Purchases", plural="purchases", _name="Purchases", table=table
    )
    return table


@pytest.fixture()
def rtl_var_customer_id(rtl_table_customers):
    var = Mock(spec=ReferenceVariable)
    var.configure_mock(
        name="cuID",
        description="Customer ID",
        type="Reference",
        table=rtl_table_customers,
    )
    return var


@pytest.fixture()
def rtl_var_customer_first_name(rtl_table_customers):
    var = Mock(spec=TextVariable)
    var.configure_mock(
        name="cuFName",
        description="Customer First Name",
        type="Text",
        table=rtl_table_customers,
    )
    return var


@pytest.fixture()
def rtl_var_customer_surname(rtl_table_customers):
    var = Mock(spec=TextVariable)
    var.configure_mock(
        name="cuSName",
        description="Customer Surname",
        type="Text",
        table=rtl_table_customers,
    )
    return var


@pytest.fixture()
def rtl_var_customer_gender(rtl_table_customers):
    var = Mock(spec=SelectorVariable)
    var.configure_mock(
        name="cuGender",
        description="Gender",
        type="Selector",
        table=rtl_table_customers,
    )
    return var


@pytest.fixture()
def rtl_var_customer_contact_pref(rtl_table_customers):
    var = Mock(spec=FlagArrayVariable)
    var.configure_mock(
        name="cuContac",
        description="Customer Contact Preferences",
        type="FlagArray",
        is_selectable=True,
        table=rtl_table_customers,
    )
    return var


@pytest.fixture()
def rtl_var_purchase_id(rtl_table_purchases):
    var = Mock(spec=ReferenceVariable)
    var.configure_mock(
        name="puID",
        description="Purchase ID",
        type="Reference",
        table=rtl_table_purchases,
    )
    return var


@pytest.fixture()
def rtl_var_purchase_store(rtl_table_purchases):
    var = Mock(spec=SelectorVariable)
    var.configure_mock(
        name="puStore",
        description="Store",
        type="Selector",
        is_selectable=True,
        table=rtl_table_purchases,
    )
    return var


@pytest.fixture()
def rtl_var_purchase_department(rtl_table_purchases):
    var = Mock(spec=SelectorVariable)
    var.configure_mock(
        name="puDept",
        description="Department",
        type="Selector",
        table=rtl_table_purchases,
        table_name=rtl_table_purchases.name,
    )
    return var


@pytest.fixture()
def rtl_var_purchase_date(rtl_table_purchases):
    var = Mock(spec=DateTimeVariable)
    var.configure_mock(
        name="puDate",
        description="Purchase Date",
        type="DateTime",
        is_selectable=True,
        table=rtl_table_purchases,
    )
    return var


@pytest.fixture()
def rtl_var_purchase_store_type(rtl_table_purchases):
    var = Mock(spec=SelectorVariable)
    var.configure_mock(
        name="puStType",
        description="Store Type",
        type="Selector",
        table=rtl_table_purchases,
    )
    return var


@pytest.fixture()
def rtl_var_purchase_payment_method(rtl_table_purchases):
    var = Mock(spec=SelectorVariable)
    var.configure_mock(
        name="puPayMtd",
        description="Payment Method",
        type="Selector",
        table=rtl_table_purchases,
    )
    return var


@pytest.fixture()
def rtl_var_purchase_profit(rtl_table_purchases):
    var = Mock(spec=NumericVariable)
    var.configure_mock(
        name="puProfit",
        description="Profit",
        type="Numeric",
        is_selectable=True,
        table=rtl_table_purchases,
    )
    return var


@pytest.fixture()
def rtl_sel_last_week_customers(rtl_table_customers):
    return Mock(
        table=rtl_table_customers,
        _to_model_selection=Mock(return_value="selection_model"),
    )


@pytest.fixture()
def rtl_sel_high_value_purchases(rtl_table_purchases):
    return Mock(
        table=rtl_table_purchases,
        _to_model_selection=Mock(return_value="selection_high_value_purchases_model"),
    )
