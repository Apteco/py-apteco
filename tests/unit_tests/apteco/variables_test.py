from datetime import datetime
from unittest.mock import Mock

import apteco_api as aa
import pytest

from apteco import Session
from apteco.common import VariableType
from apteco.tables import Table
from apteco.variables import (
    ArrayVariable,
    DateTimeVariable,
    DateVariable,
    FlagArrayVariable,
    NumericVariable,
    ReferenceVariable,
    SelectorVariable,
    TextVariable,
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
            minimum_var_code_count=123456,
            maximum_var_code_count=234567,
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
            maximum_var_code_count=555666,
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


def test_selector_variable_init(ins_aa_sel_var_gender, ins_table_clnts, ins_session):
    v = ins_aa_sel_var_gender
    selector_variable = SelectorVariable(
        name=v.name,
        description=v.description,
        type=v.type,
        folder_name=v.folder_name,
        table=ins_table_clnts,
        is_selectable=v.is_selectable,
        is_browsable=v.is_browsable,
        is_exportable=v.is_exportable,
        is_virtual=v.is_virtual,
        selector_info=v.selector_info,
        numeric_info=v.numeric_info,
        text_info=v.text_info,
        reference_info=v.reference_info,
        session=ins_session,
    )
    assert selector_variable.type == VariableType.SELECTOR
    assert selector_variable.code_length == 2
    assert selector_variable.num_codes == 4
    assert selector_variable.var_code_min_count == 123456
    assert selector_variable.var_code_max_count == 234567
    assert selector_variable.var_code_order == "Nominal"
    assert selector_variable.name == "clGender"
    assert selector_variable.description == "Gender"
    assert selector_variable._model_type == "Selector"
    assert selector_variable.folder_name == "Client details"
    assert selector_variable.table is ins_table_clnts
    assert selector_variable.is_selectable is True
    assert selector_variable.is_browsable is False
    assert selector_variable.is_exportable is True
    assert selector_variable.is_virtual is False
    assert selector_variable.session is ins_session


def test_numeric_variable_init(ins_aa_num_var_prem, ins_table_prods, ins_session):
    v = ins_aa_num_var_prem
    numeric_variable = NumericVariable(
        name=v.name,
        description=v.description,
        type=v.type,
        folder_name=v.folder_name,
        table=ins_table_prods,
        is_selectable=v.is_selectable,
        is_browsable=v.is_browsable,
        is_exportable=v.is_exportable,
        is_virtual=v.is_virtual,
        selector_info=v.selector_info,
        numeric_info=v.numeric_info,
        text_info=v.text_info,
        reference_info=v.reference_info,
        session=ins_session,
    )
    assert numeric_variable.type == VariableType.NUMERIC
    assert numeric_variable.min_value == 1.00
    assert numeric_variable.max_value == 3044.21
    assert numeric_variable.is_currency == True
    assert numeric_variable.currency_locale == "en-GB"
    assert numeric_variable.currency_symbol == "£"
    assert numeric_variable.name == "prPrem"
    assert numeric_variable.description == "Premium"
    assert numeric_variable._model_type == "Numeric"
    assert numeric_variable.folder_name == "Products"
    assert numeric_variable.table is ins_table_prods
    assert numeric_variable.is_selectable is True
    assert numeric_variable.is_browsable is True
    assert numeric_variable.is_exportable is True
    assert numeric_variable.is_virtual is False
    assert numeric_variable.session is ins_session


def test_text_variable_init(ins_aa_text_var_addr, ins_table_clnts, ins_session):
    v = ins_aa_text_var_addr
    text_variable = TextVariable(
        name=v.name,
        description=v.description,
        type=v.type,
        folder_name=v.folder_name,
        table=ins_table_clnts,
        is_selectable=v.is_selectable,
        is_browsable=v.is_browsable,
        is_exportable=v.is_exportable,
        is_virtual=v.is_virtual,
        selector_info=v.selector_info,
        numeric_info=v.numeric_info,
        text_info=v.text_info,
        reference_info=v.reference_info,
        session=ins_session,
    )
    assert text_variable.type == VariableType.TEXT
    assert text_variable.max_length == 80
    assert text_variable.name == "clAddr"
    assert text_variable.description == "Address"
    assert text_variable._model_type == "Text"
    assert text_variable.folder_name == "Client details"
    assert text_variable.table is ins_table_clnts
    assert text_variable.is_selectable is True
    assert text_variable.is_browsable is False
    assert text_variable.is_exportable is True
    assert text_variable.is_virtual is False
    assert text_variable.session is ins_session


def test_array_variable_init(ins_aa_arr_var_prexco, ins_table_clnts, ins_session):
    v = ins_aa_arr_var_prexco
    array_variable = ArrayVariable(
        name=v.name,
        description=v.description,
        type=v.type,
        folder_name=v.folder_name,
        table=ins_table_clnts,
        is_selectable=v.is_selectable,
        is_browsable=v.is_browsable,
        is_exportable=v.is_exportable,
        is_virtual=v.is_virtual,
        selector_info=v.selector_info,
        numeric_info=v.numeric_info,
        text_info=v.text_info,
        reference_info=v.reference_info,
        session=ins_session,
    )
    assert array_variable.type == VariableType.ARRAY
    assert array_variable.code_length == 10
    assert array_variable.num_codes == 678
    assert array_variable.var_code_min_count == 0
    assert array_variable.var_code_max_count == 23456
    assert array_variable.var_code_order == "Nominal"
    assert array_variable.name == "clPrExCo"
    assert array_variable.description == "Pre-existing conditions"
    assert array_variable._model_type == "Selector"
    assert array_variable.folder_name == "Client health info"
    assert array_variable.table is ins_table_clnts
    assert array_variable.is_selectable is True
    assert array_variable.is_browsable is False
    assert array_variable.is_exportable is False
    assert array_variable.is_virtual is False
    assert array_variable.session is ins_session


def test_flag_array_variable_init(ins_aa_flarr_var_tags, ins_table_prods, ins_session):
    v = ins_aa_flarr_var_tags
    flag_array_variable = FlagArrayVariable(
        name=v.name,
        description=v.description,
        type=v.type,
        folder_name=v.folder_name,
        table=ins_table_prods,
        is_selectable=v.is_selectable,
        is_browsable=v.is_browsable,
        is_exportable=v.is_exportable,
        is_virtual=v.is_virtual,
        selector_info=v.selector_info,
        numeric_info=v.numeric_info,
        text_info=v.text_info,
        reference_info=v.reference_info,
        session=ins_session,
    )
    assert flag_array_variable.type == VariableType.FLAG_ARRAY
    assert flag_array_variable.code_length == 6
    assert flag_array_variable.num_codes == 58
    assert flag_array_variable.var_code_min_count == 56
    assert flag_array_variable.var_code_max_count == 555666
    assert flag_array_variable.var_code_order == "Nominal"
    assert flag_array_variable.name == "prTags"
    assert flag_array_variable.description == "Product tags"
    assert flag_array_variable._model_type == "Selector"
    assert flag_array_variable.folder_name == "Product info"
    assert flag_array_variable.table is ins_table_prods
    assert flag_array_variable.is_selectable is True
    assert flag_array_variable.is_browsable is True
    assert flag_array_variable.is_exportable is True
    assert flag_array_variable.is_virtual is False
    assert flag_array_variable.session is ins_session


def test_date_variable_init(ins_aa_dat_var_payrcvd, ins_table_pmnts, ins_session):
    v = ins_aa_dat_var_payrcvd
    date_variable = DateVariable(
        name=v.name,
        description=v.description,
        type=v.type,
        folder_name=v.folder_name,
        table=ins_table_pmnts,
        is_selectable=v.is_selectable,
        is_browsable=v.is_browsable,
        is_exportable=v.is_exportable,
        is_virtual=v.is_virtual,
        selector_info=v.selector_info,
        numeric_info=v.numeric_info,
        text_info=v.text_info,
        reference_info=v.reference_info,
        session=ins_session,
    )
    assert date_variable.type == VariableType.DATE
    assert date_variable.code_length == 13
    assert date_variable.num_codes == 5678
    assert date_variable.var_code_min_count == 0
    assert date_variable.var_code_max_count == 9876
    assert date_variable.var_code_order == "Ascending"
    assert date_variable.name == "pmDate"
    assert date_variable.description == "Payment received"
    assert date_variable._model_type == "Selector"
    assert date_variable.folder_name == "Payments"
    assert date_variable.table is ins_table_pmnts
    assert date_variable.is_selectable is True
    assert date_variable.is_browsable is True
    assert date_variable.is_exportable is True
    assert date_variable.is_virtual is False
    assert date_variable.session is ins_session


def test_datetime_variable_init(ins_aa_dtme_var_timesnt, ins_table_comms, ins_session):
    v = ins_aa_dtme_var_timesnt
    datetime_variable = DateTimeVariable(
        name=v.name,
        description=v.description,
        type=v.type,
        folder_name=v.folder_name,
        table=ins_table_comms,
        is_selectable=v.is_selectable,
        is_browsable=v.is_browsable,
        is_exportable=v.is_exportable,
        is_virtual=v.is_virtual,
        selector_info=v.selector_info,
        numeric_info=v.numeric_info,
        text_info=v.text_info,
        reference_info=v.reference_info,
        session=ins_session,
    )
    assert datetime_variable.type == VariableType.DATETIME
    assert datetime_variable.code_length == 12
    assert datetime_variable.num_codes == 2468
    assert datetime_variable.var_code_min_count == 0
    assert datetime_variable.var_code_max_count == 87654
    assert datetime_variable.var_code_order == "Ascending"
    assert datetime_variable.name == "coSent"
    assert datetime_variable.description == "Time sent"
    assert datetime_variable._model_type == "Selector"
    assert datetime_variable.folder_name == "Communications"
    assert datetime_variable.table is ins_table_comms
    assert datetime_variable.is_selectable is True
    assert datetime_variable.is_browsable is True
    assert datetime_variable.is_exportable is True
    assert datetime_variable.is_virtual is False
    assert datetime_variable.session is ins_session


def test_reference_variable_init(ins_aa_ref_var_payid, ins_table_pmnts, ins_session):
    v = ins_aa_ref_var_payid
    reference_variable = ReferenceVariable(
        name=v.name,
        description=v.description,
        type=v.type,
        folder_name=v.folder_name,
        table=ins_table_pmnts,
        is_selectable=v.is_selectable,
        is_browsable=v.is_browsable,
        is_exportable=v.is_exportable,
        is_virtual=v.is_virtual,
        selector_info=v.selector_info,
        numeric_info=v.numeric_info,
        text_info=v.text_info,
        reference_info=v.reference_info,
        session=ins_session,
    )
    assert reference_variable.type == VariableType.REFERENCE
    assert reference_variable.name == "pmID"
    assert reference_variable.description == "Payment ID"
    assert reference_variable._model_type == "Reference"
    assert reference_variable.folder_name == "Payments"
    assert reference_variable.table is ins_table_pmnts
    assert reference_variable.is_selectable is True
    assert reference_variable.is_browsable is True
    assert reference_variable.is_exportable is True
    assert reference_variable.is_virtual is False
    assert reference_variable.session is ins_session
