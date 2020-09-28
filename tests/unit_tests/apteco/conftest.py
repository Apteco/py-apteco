from unittest.mock import Mock

import pytest

from apteco.tables import Table
from apteco.variables import (
    SelectorVariable,
    TextVariable,
    FlagArrayVariable,
    DateTimeVariable,
    ReferenceVariable,
)

"""
Fake 'Retail' system
====================

Tables
------

Customers
└── Purchases

Variables
---------

 Table      |  Description                  |  Name     |  Type     |
---------------------------------------------------------------------
Customers   | Customer ID                   | cuID      | Reference |
Customers   | Customer First Name           | cuFName   | Text      |
Customers   | Customer Surname              | cuSName   | Text      |
Customers   | Gender                        | cuGender  | Selector  |
Customers   | Customer Contact Preferences  | cuContac  | FlagArray |
------------|-------------------------------|-----------|-----------|
Purchases   | Purchase ID                   | puID      | Reference |
Purchases   | Department                    | puDept    | Selector  |
Purchases   | Purchase Date                 | puDate    | DateTime  |
Purchases   | Store Type                    | puStType  | Selector  |
Purchases   | Payment Method                | puPayMtd  | Selector  |

"""


@pytest.fixture()
def rtl_table_customers():
    table = Mock(spec=Table)
    table.configure_mock(name="Customers")
    return table


@pytest.fixture()
def rtl_table_purchases():
    table = Mock(spec=Table)
    table.configure_mock(name="Purchases", plural_display_name="purchases")
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
def rtl_var_purchase_department(rtl_table_purchases):
    var = Mock(spec=SelectorVariable)
    var.configure_mock(
        name="puDept",
        description="Department",
        type="Selector",
        table=rtl_table_purchases,
    )
    return var


@pytest.fixture()
def rtl_var_purchase_date(rtl_table_purchases):
    var = Mock(spec=DateTimeVariable)
    var.configure_mock(
        name="puDate",
        description="Purchase Date",
        type="DateTime",
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
def rtl_sel_last_week_customers(rtl_table_customers):
    return Mock(
        table=rtl_table_customers, _to_model=Mock(return_value="selection_model")
    )


@pytest.fixture()
def rtl_session():
    return Mock(data_view="acme_inc", system="retail", api_client="my_api_client")


@pytest.fixture()
def rtl_sel_high_value_purchases(rtl_table_purchases):
    return Mock(
        table=rtl_table_purchases,
        _to_model=Mock(return_value="selection_high_value_purchases_model"),
    )
