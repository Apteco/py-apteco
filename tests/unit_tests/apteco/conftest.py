from datetime import datetime
from unittest.mock import Mock

import apteco_api as aa
import pytest

from apteco.common import VariableType
from apteco.session import Session
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
* variables have a reference to their table and the session
* selections have a reference to their table, but not the session

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
Customers   | Customer Email                | cuEmail   | Text      | rtl_var_customer_email
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
def rtl_var_customer_id(rtl_table_customers, rtl_session):
    var = Mock(spec=ReferenceVariable)
    var.configure_mock(
        name="cuID",
        description="Customer ID",
        type=VariableType.REFERENCE,
        table=rtl_table_customers,
        table_name=rtl_table_customers.name,
        session=rtl_session,
    )
    return var


@pytest.fixture()
def rtl_var_customer_first_name(rtl_table_customers, rtl_session):
    var = Mock(spec=TextVariable)
    var.configure_mock(
        name="cuFName",
        description="Customer First Name",
        type=VariableType.TEXT,
        table=rtl_table_customers,
        table_name=rtl_table_customers.name,
        session=rtl_session,
    )
    return var


@pytest.fixture()
def rtl_var_customer_surname(rtl_table_customers, rtl_session):
    var = Mock(spec=TextVariable)
    var.configure_mock(
        name="cuSName",
        description="Customer Surname",
        type=VariableType.TEXT,
        table=rtl_table_customers,
        table_name=rtl_table_customers.name,
        session=rtl_session,
    )
    return var


@pytest.fixture()
def rtl_var_customer_email(rtl_table_customers, rtl_session):
    var = Mock(spec=TextVariable)
    var.configure_mock(
        name="cuEmail",
        description="Customer Email",
        type=VariableType.TEXT,
        table=rtl_table_customers,
        table_name=rtl_table_customers.name,
        session=rtl_session,
    )
    return var


@pytest.fixture()
def rtl_var_customer_gender(rtl_table_customers, rtl_session):
    var = Mock(spec=SelectorVariable)
    var.configure_mock(
        name="cuGender",
        description="Gender",
        type=VariableType.SELECTOR,
        table=rtl_table_customers,
        table_name=rtl_table_customers.name,
        session=rtl_session,
    )
    return var


@pytest.fixture()
def rtl_var_customer_contact_pref(rtl_table_customers, rtl_session):
    var = Mock(spec=FlagArrayVariable)
    var.configure_mock(
        name="cuContac",
        description="Customer Contact Preferences",
        type=VariableType.FLAG_ARRAY,
        is_selectable=True,
        table=rtl_table_customers,
        table_name=rtl_table_customers.name,
        session=rtl_session,
    )
    return var


@pytest.fixture()
def rtl_var_purchase_id(rtl_table_purchases, rtl_session):
    var = Mock(spec=ReferenceVariable)
    var.configure_mock(
        name="puID",
        description="Purchase ID",
        type=VariableType.REFERENCE,
        table=rtl_table_purchases,
        table_name=rtl_table_purchases.name,
        session=rtl_session,
    )
    return var


@pytest.fixture()
def rtl_var_purchase_store(rtl_table_purchases, rtl_session):
    var = Mock(spec=SelectorVariable)
    var.configure_mock(
        name="puStore",
        description="Store",
        type=VariableType.SELECTOR,
        is_selectable=True,
        table=rtl_table_purchases,
        table_name=rtl_table_purchases.name,
        session=rtl_session,
    )
    return var


@pytest.fixture()
def rtl_var_purchase_department(rtl_table_purchases, rtl_session):
    var = Mock(spec=SelectorVariable)
    var.configure_mock(
        name="puDept",
        description="Department",
        type=VariableType.SELECTOR,
        _dimension_type="Selector",
        table=rtl_table_purchases,
        table_name=rtl_table_purchases.name,
        session=rtl_session,
    )
    return var


@pytest.fixture()
def rtl_var_purchase_date(rtl_table_purchases, rtl_session):
    var = Mock(spec=DateTimeVariable)
    var.configure_mock(
        name="puDate",
        description="Purchase Date",
        type=VariableType.DATETIME,
        is_selectable=True,
        table=rtl_table_purchases,
        table_name=rtl_table_purchases.name,
        session=rtl_session,
    )
    return var


@pytest.fixture()
def rtl_var_purchase_store_type(rtl_table_purchases, rtl_session):
    var = Mock(spec=SelectorVariable)
    var.configure_mock(
        name="puStType",
        description="Store Type",
        type=VariableType.SELECTOR,
        _dimension_type="Selector",
        table=rtl_table_purchases,
        table_name=rtl_table_purchases.name,
        session=rtl_session,
    )
    return var


@pytest.fixture()
def rtl_var_purchase_payment_method(rtl_table_purchases, rtl_session):
    var = Mock(spec=SelectorVariable)
    var.configure_mock(
        name="puPayMtd",
        description="Payment Method",
        type=VariableType.SELECTOR,
        _dimension_type="Selector",
        table=rtl_table_purchases,
        table_name=rtl_table_purchases.name,
        session=rtl_session,
    )
    return var


@pytest.fixture()
def rtl_var_purchase_profit(rtl_table_purchases, rtl_session):
    var = Mock(spec=NumericVariable)
    var.configure_mock(
        name="puProfit",
        description="Profit",
        type=VariableType.NUMERIC,
        is_selectable=True,
        table=rtl_table_purchases,
        table_name=rtl_table_purchases.name,
        session=rtl_session,
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


"""
Fake 'Insurance' system
=======================

For use in unit tests interfacing with apteco_api.

* variables are apteco_api instances
* session & table are Mock objects
  and have `spec` set to the corresponding py-apteco class

Tables
------

Clients             | ins_table_clnts
├── Products        | ins_table_prods
│   └── Payments    | ins_table_pmnts
└── Communications  | ins_table_comms

Variables
---------

 Table          |  Description              |  Name     |  Type     |
---------------------------------------------------------------------
Clients         | Gender                    | clGender  | Selector  | ins_aa_sel_var_gender
Clients         | Address                   | clAddr    | Text      | ins_aa_text_var_addr
Clients         | Pre-existing conditions   | clPrExCo  | Array     | ins_aa_arr_var_prexco
----------------|---------------------------|-----------|-----------|
Products        | Premium                   | prPrem    | Numeric   | ins_aa_num_var_prem
Products        | Product tags              | prTags    | FlagArray | ins_aa_flarr_var_tags
----------------|---------------------------|-----------|-----------|
Payments        | Payment ID                | pmID      | Reference | ins_aa_ref_var_payid
Payments        | Payment received          | pmDate    | Date      | ins_aa_dat_var_payrcvd
----------------|---------------------------|-----------|-----------|
Communications  | Time sent                 | coSent    | DateTime  | ins_aa_dtme_var_timesnt

"""


@pytest.fixture()
def ins_aa_sel_var_gender():
    var = aa.Variable(
        name="clGender",
        description="Gender",
        type="Selector",
        folder_name="Client details",
        table_name="Clients",
        is_selectable=True,
        is_browsable=False,
        is_exportable=True,
        is_virtual=False,
        selector_info=aa.SelectorVariableInfo(
            selector_type="SingleValue",
            sub_type="Categorical",
            var_code_order="Nominal",
            number_of_codes=4,
            code_length=2,
            minimum_var_code_count=123_456,
            maximum_var_code_count=234_567,
            minimum_date=None,
            maximum_date=None,
            combined_from_variable_name=None,
        ),
        numeric_info=None,
        text_info=None,
        reference_info=None,
    )
    return var


@pytest.fixture()
def ins_aa_num_var_prem():
    var = aa.Variable(
        name="prPrem",
        description="Premium",
        type="Numeric",
        folder_name="Products",
        table_name="Products",
        is_selectable=True,
        is_browsable=True,
        is_exportable=True,
        is_virtual=False,
        selector_info=None,
        numeric_info=aa.NumericVariableInfo(
            minimum=1.00,
            maximum=3044.21,
            is_currency=True,
            currency_locale="en-GB",
            currency_symbol="£",
        ),
        text_info=None,
        reference_info=None,
    )
    return var


@pytest.fixture()
def ins_aa_text_var_addr():
    var = aa.Variable(
        name="clAddr",
        description="Address",
        type="Text",
        folder_name="Client details",
        table_name="Clients",
        is_selectable=True,
        is_browsable=False,
        is_exportable=True,
        is_virtual=False,
        selector_info=None,
        numeric_info=None,
        text_info=aa.TextVariableInfo(maximum_text_length=80),
        reference_info=None,
    )
    return var


@pytest.fixture()
def ins_aa_arr_var_prexco():
    var = aa.Variable(
        name="clPrExCo",
        description="Pre-existing conditions",
        type="Selector",
        folder_name="Client health info",
        table_name="Clients",
        is_selectable=True,
        is_browsable=False,
        is_exportable=False,
        is_virtual=False,
        selector_info=aa.SelectorVariableInfo(
            selector_type="OrArray",
            sub_type="Categorical",
            var_code_order="Nominal",
            number_of_codes=678,
            code_length=10,
            minimum_var_code_count=0,
            maximum_var_code_count=23456,
            minimum_date=None,
            maximum_date=None,
            combined_from_variable_name=None,
        ),
        numeric_info=None,
        text_info=None,
        reference_info=None,
    )
    return var


@pytest.fixture()
def ins_aa_flarr_var_tags():
    var = aa.Variable(
        name="prTags",
        description="Product tags",
        type="Selector",
        folder_name="Product info",
        table_name="Products",
        is_selectable=True,
        is_browsable=True,
        is_exportable=True,
        is_virtual=False,
        selector_info=aa.SelectorVariableInfo(
            selector_type="OrBitArray",
            sub_type="Categorical",
            var_code_order="Nominal",
            number_of_codes=58,
            code_length=6,
            minimum_var_code_count=56,
            maximum_var_code_count=555_666,
            minimum_date=None,
            maximum_date=None,
            combined_from_variable_name=None,
        ),
        numeric_info=None,
        text_info=None,
        reference_info=None,
    )
    return var


@pytest.fixture()
def ins_aa_dat_var_payrcvd():
    var = aa.Variable(
        name="pmDate",
        description="Payment received",
        type="Selector",
        folder_name="Payments",
        table_name="Payments",
        is_selectable=True,
        is_browsable=True,
        is_exportable=True,
        is_virtual=False,
        selector_info=aa.SelectorVariableInfo(
            selector_type="SingleValue",
            sub_type="Date",
            var_code_order="Ascending",
            number_of_codes=5678,
            code_length=13,
            minimum_var_code_count=0,
            maximum_var_code_count=9876,
            minimum_date=datetime(2008, 1, 1),
            maximum_date=datetime(2023, 7, 22),
            combined_from_variable_name=None,
        ),
        numeric_info=None,
        text_info=None,
        reference_info=None,
    )
    return var


@pytest.fixture()
def ins_aa_dtme_var_timesnt():
    var = aa.Variable(
        name="coSent",
        description="Time sent",
        type="Selector",
        folder_name="Communications",
        table_name="Communications",
        is_selectable=True,
        is_browsable=True,
        is_exportable=True,
        is_virtual=False,
        selector_info=aa.SelectorVariableInfo(
            selector_type="SingleValue",
            sub_type="DateTime",
            var_code_order="Ascending",
            number_of_codes=2468,
            code_length=12,
            minimum_var_code_count=0,
            maximum_var_code_count=87654,
            minimum_date=datetime(2012, 5, 13),
            maximum_date=datetime(2020, 10, 18),
            combined_from_variable_name=None,
        ),
        numeric_info=None,
        text_info=None,
        reference_info=None,
    )
    return var


@pytest.fixture()
def ins_aa_ref_var_payid():
    var = aa.Variable(
        name="pmID",
        description="Payment ID",
        type="Reference",
        folder_name="Payments",
        table_name="Payments",
        is_selectable=True,
        is_browsable=True,
        is_exportable=True,
        is_virtual=False,
        selector_info=None,
        numeric_info=None,
        text_info=None,
        reference_info=dict(),
    )
    return var


@pytest.fixture()
def ins_session():
    session = Mock(spec=Session)
    return session


@pytest.fixture()
def ins_table_clnts():
    table = Mock(spec=Table)
    table.configure_mock(name="clients")
    return table


@pytest.fixture()
def ins_table_prods():
    table = Mock(spec=Table)
    table.configure_mock(name="products")
    return table


@pytest.fixture()
def ins_table_pmnts():
    table = Mock(spec=Table)
    table.configure_mock(name="payments")
    return table


@pytest.fixture()
def ins_table_comms():
    table = Mock(spec=Table)
    table.configure_mock(name="communications")
    return table
