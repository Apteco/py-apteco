from datetime import datetime
from unittest.mock import Mock

import apteco_api as aa
import pytest

from apteco import Session
from apteco.common import VariableType
from apteco.query import NumericClause, TextClause
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


class TestNumericVariable:
    def test_numeric_variable_init(self, ins_aa_num_var_prem, ins_table_prods, ins_session):
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

    def test_missing(self, rtl_var_purchase_profit, rtl_table_purchases, rtl_session):
        missing_value = NumericVariable.missing(rtl_var_purchase_profit)
        assert type(missing_value) == NumericClause
        assert missing_value.table is rtl_table_purchases
        assert missing_value.variable_name == "puProfit"
        assert missing_value.values == ["><"]
        assert missing_value.include is True
        assert missing_value.session is rtl_session


class TestTextVariable:
    def test_text_variable_init(self, ins_aa_text_var_addr, ins_table_clnts, ins_session):
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

    def test_equals(self, rtl_var_customer_email, rtl_session):
        specific_donor = TextVariable.equals(rtl_var_customer_email, "donor@domain.com")
        assert type(specific_donor) == TextClause
        assert specific_donor.table_name == "Customers"
        assert specific_donor.variable_name == "cuEmail"
        assert specific_donor.values == ["donor@domain.com"]
        assert specific_donor.match_type == "Is"
        assert specific_donor.match_case is True
        assert specific_donor.include is True
        assert specific_donor.session is rtl_session

        donors_by_email = TextVariable.equals(rtl_var_customer_email,
            [f"donor_{i}@domain.com" for i in range(4)]
        )
        assert type(donors_by_email) == TextClause
        assert donors_by_email.table_name == "Customers"
        assert donors_by_email.variable_name == "cuEmail"
        assert donors_by_email.values == [
            "donor_0@domain.com",
            "donor_1@domain.com",
            "donor_2@domain.com",
            "donor_3@domain.com",
        ]
        assert donors_by_email.match_type == "Is"
        assert donors_by_email.match_case is True
        assert donors_by_email.include is True
        assert donors_by_email.session is rtl_session

        with pytest.raises(ValueError) as exc_info:
            donors_by_number = TextVariable.equals(rtl_var_customer_email, {34, 765, 2930})
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a text variable"
            " must be given as a string or an iterable of strings."
        )

        dont_want_this_person = TextVariable.equals(rtl_var_customer_email,
            "bad_donor@domain.com", include=False
        )
        assert type(dont_want_this_person) == TextClause
        assert dont_want_this_person.table_name == "Customers"
        assert dont_want_this_person.variable_name == "cuEmail"
        assert dont_want_this_person.values == ["bad_donor@domain.com"]
        assert dont_want_this_person.match_type == "Is"
        assert dont_want_this_person.match_case is True
        assert dont_want_this_person.include is False
        assert dont_want_this_person.session is rtl_session

        not_these_people = TextVariable.equals(rtl_var_customer_email,
            {"dont_email_me@domain.com", "unsubscribed@domain.org"}, include=False
        )
        assert type(not_these_people) == TextClause
        assert not_these_people.table_name == "Customers"
        assert not_these_people.variable_name == "cuEmail"
        assert sorted(not_these_people.values) == [
            "dont_email_me@domain.com",
            "unsubscribed@domain.org",
        ]
        assert not_these_people.match_type == "Is"
        assert not_these_people.match_case is True
        assert not_these_people.include is False
        assert not_these_people.session is rtl_session

        with pytest.raises(ValueError) as exc_info:
            donor_not_an_obj = TextVariable.equals(rtl_var_customer_email, object(), include=False)
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a text variable"
            " must be given as a string or an iterable of strings."
        )

    def test_contains(self, rtl_var_customer_surname, rtl_session):
        contains_nuts = TextVariable.contains(rtl_var_customer_surname, "nuts")
        assert type(contains_nuts) == TextClause
        assert contains_nuts.table_name == "Customers"
        assert contains_nuts.variable_name == "cuSName"
        assert contains_nuts.values == ["nuts"]
        assert contains_nuts.match_type == "Contains"
        assert contains_nuts.match_case is True
        assert contains_nuts.include is True
        assert contains_nuts.session is rtl_session

        contains_multiple = TextVariable.contains(rtl_var_customer_surname, ["a", "b"])
        assert type(contains_multiple) == TextClause
        assert contains_multiple.table_name == "Customers"
        assert contains_multiple.variable_name == "cuSName"
        assert contains_multiple.values == ["a", "b"]
        assert contains_multiple.match_type == "Contains"
        assert contains_multiple.match_case is True
        assert contains_multiple.include is True
        assert contains_multiple.session is rtl_session

        with pytest.raises(ValueError) as exc_info:
            contains_ints = TextVariable.contains(rtl_var_customer_surname, [1, 2, 3])
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a text variable"
            " must be given as a string or an iterable of strings."
        )

    def test_starts_with(self, rtl_var_customer_surname, rtl_session):
        starts_with_smith = TextVariable.startswith(rtl_var_customer_surname, "Smith")
        assert type(starts_with_smith) == TextClause
        assert starts_with_smith.table_name == "Customers"
        assert starts_with_smith.variable_name == "cuSName"
        assert starts_with_smith.values == ["Smith"]
        assert starts_with_smith.match_type == "Begins"
        assert starts_with_smith.match_case is True
        assert starts_with_smith.include is True
        assert starts_with_smith.session is rtl_session

        starts_with_multiple = TextVariable.startswith(rtl_var_customer_surname,
            ["Tom", "James", "Dan", "Dav"]
        )
        assert type(starts_with_multiple) == TextClause
        assert starts_with_multiple.table_name == "Customers"
        assert starts_with_multiple.variable_name == "cuSName"
        assert starts_with_multiple.values == ["Tom", "James", "Dan", "Dav"]
        assert starts_with_multiple.match_type == "Begins"
        assert starts_with_multiple.match_case is True
        assert starts_with_multiple.include is True
        assert starts_with_multiple.session is rtl_session

        with pytest.raises(ValueError) as exc_info:
            starts_with_boolean = TextVariable.startswith(rtl_var_customer_surname, True)
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a text variable"
            " must be given as a string or an iterable of strings."
        )

    def test_ends_with(self, rtl_var_customer_surname, rtl_session):
        ends_with_son = TextVariable.endswith(rtl_var_customer_surname, "son")
        assert type(ends_with_son) == TextClause
        assert ends_with_son.table_name == "Customers"
        assert ends_with_son.variable_name == "cuSName"
        assert ends_with_son.values == ["son"]
        assert ends_with_son.match_type == "Ends"
        assert ends_with_son.match_case is True
        assert ends_with_son.include is True
        assert ends_with_son.session is rtl_session

        ends_with_multiple = TextVariable.endswith(rtl_var_customer_surname, ["son", "ez"])
        assert type(ends_with_multiple) == TextClause
        assert ends_with_multiple.table_name == "Customers"
        assert ends_with_multiple.variable_name == "cuSName"
        assert ends_with_multiple.values == ["son", "ez"]
        assert ends_with_multiple.match_type == "Ends"
        assert ends_with_multiple.match_case is True
        assert ends_with_multiple.include is True
        assert ends_with_multiple.session is rtl_session

        with pytest.raises(ValueError) as exc_info:
            ends_with_float = TextVariable.endswith(rtl_var_customer_surname, [2.8, 9.4])
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a text variable"
            " must be given as a string or an iterable of strings."
        )

    @pytest.mark.xfail(
        reason="Feature-switched off before/after TextVariable methods",
        raises=AttributeError,
    )
    def test_before(self, rtl_var_customer_surname, rtl_session):
        first_half_alphabet = TextVariable.before(rtl_var_customer_surname, "n")
        assert type(first_half_alphabet) == TextClause
        assert first_half_alphabet.table_name == "Customers"
        assert first_half_alphabet.variable_name == "cuSName"
        assert first_half_alphabet.values == ['<="n"']
        assert first_half_alphabet.match_type == "Ranges"
        assert first_half_alphabet.match_case is True
        assert first_half_alphabet.include is True
        assert first_half_alphabet.session is rtl_session

        with pytest.raises(ValueError) as exc_info:
            earlier_than_letters = TextVariable.before(rtl_var_customer_surname, list("abcedfgh"))
        assert exc_info.value.args[0] == (
            "Must specify a single string for this type of operation."
        )

        with pytest.raises(ValueError) as exc_info:
            before_int = TextVariable.before(rtl_var_customer_surname, 6)
        assert exc_info.value.args[0] == (
            "Must specify a single string for this type of operation."
        )

    @pytest.mark.xfail(
        reason="Feature-switched off before/after TextVariable methods",
        raises=AttributeError,
    )
    def test_after(self, rtl_var_customer_surname, rtl_session):
        smith_or_later = TextVariable.after(rtl_var_customer_surname, "Smith")
        assert type(smith_or_later) == TextClause
        assert smith_or_later.table_name == "Customers"
        assert smith_or_later.variable_name == "cuSName"
        assert smith_or_later.values == ['>="Smith"']
        assert smith_or_later.match_type == "Ranges"
        assert smith_or_later.match_case is True
        assert smith_or_later.include is True
        assert smith_or_later.session is rtl_session

        with pytest.raises(ValueError) as exc_info:
            later_than_tuple = TextVariable.after(rtl_var_customer_surname, ("A", "e", "i", "O"))
        assert exc_info.value.args[0] == (
            "Must specify a single string for this type of operation."
        )

        with pytest.raises(ValueError) as exc_info:
            after_boolean = TextVariable.after(rtl_var_customer_surname, False)
        assert exc_info.value.args[0] == (
            "Must specify a single string for this type of operation."
        )

    def test_between(self, rtl_var_customer_surname, rtl_session):
        rock_and_hardplace = TextVariable.between(rtl_var_customer_surname, "hardplace", "rock")
        assert type(rock_and_hardplace) == TextClause
        assert rock_and_hardplace.table_name == "Customers"
        assert rock_and_hardplace.variable_name == "cuSName"
        assert rock_and_hardplace.values == ['>="hardplace" - <="rock"']
        assert rock_and_hardplace.match_type == "Ranges"
        assert rock_and_hardplace.match_case is False
        assert rock_and_hardplace.include is True
        assert rock_and_hardplace.session is rtl_session

        with pytest.raises(ValueError) as exc_info:
            between_lists = TextVariable.between(rtl_var_customer_surname, ["a", "b"], ["y", "z"])
        assert exc_info.value.args[0] == (
            "Must specify a single string for this type of operation."
        )

        with pytest.raises(ValueError) as exc_info:
            between_ints = TextVariable.between(rtl_var_customer_surname, 1, 100)
        assert exc_info.value.args[0] == (
            "Must specify a single string for this type of operation."
        )

    @pytest.mark.parametrize(
        ["start", "end"],
        [
            pytest.param("-", "C", id="ascii 32-64 symbol & uppercase letter"),
            pytest.param("'", "y", id="ascii 32-64 symbol & lowercase letter"),
            pytest.param("^", "s", id="ascii 91-96 symbol & lowercase letter"),
            pytest.param("G", "|", id="ascii 123-126 symbol & uppercase letter"),
            pytest.param("t", "~", id="ascii 123-126 symbol & lowercase letter"),
            pytest.param("J", "X", id="uppercase letter & uppercase letter"),
            pytest.param("B", "k", id="uppercase letter & lowercase letter"),
            pytest.param("m", "x", id="lowercase letter & lowercase letter"),

        ],
    )
    def test_between_ordering(self, start, end, rtl_var_customer_surname):
        """Check `between()` behaves correctly with different pairs of characters.

        Testing with pairs of characters whose ASCII order is the same as
        the order fs32svr uses when comparing case-insensitively.

        """
        TextVariable.between(rtl_var_customer_surname, start, end)

        with pytest.raises(ValueError) as exc_info:
            TextVariable.between(rtl_var_customer_surname, end, start)
        assert exc_info.value.args[0] == "`start` must come before `end`"

    @pytest.mark.parametrize(
        ["start", "end", "error_message"],
        [
            pytest.param(
                "N",
                "_",
                "`start` must come before `end`,"
                " but 'N' comes after '_' when compared case-insensitively.",
                id="ascii 91-96 symbol & uppercase letter",
            ),
            pytest.param(
                "V",
                "d",
                "`start` must come before `end`,"
                " but 'V' comes after 'd' when compared case-insensitively.",
                id="lowercase letter & uppercase letter",
            ),
            pytest.param(
                "H",
                "f",
                "`start` must come before `end`,"
                " but 'H' comes after 'f' when compared case-insensitively.",
                id="uppercase letter & lowercase letter",
            ),
        ],
    )
    def test_between_ascii_order_but_wrong(self, start, end, error_message, rtl_var_customer_surname):
        """Test `between()` checks character order correctly.

        Test `between()` with pairs of characters whose ASCII order is different
        from the order fs32svr sorts in when comparing case-insensitively.

        ASCII characters can be split into 5 ranges, based around the letters:
        *  32 -  64: symbols (incl. space):  !"#$%&'()*+,-./0123456789:;<=>?@
        *  65 -  90: uppercase letters    : ABCDEFGHIJKLMNOPQRSTUVWXYZ
        *  91 -  96: symbols              : [\]^_`
        *  97 - 122: lowercase letters    : abcdefghijklmnopqrstuvwxyz
        * 123 - 126: symbols              : {|}~

        When matching case, fs32svr follows ASCII order exactly,
        but when ignoring case the symbols occurring between uppercase and lowercase
        letters sort as if they came before the uppercase letters,
        i.e. between '@' and 'A'.

        The parameters for this test are passed with `start` & `end` in ASCII order,
        but these are cases where this is the *incorrect* order,
        on basis of the fs32svr rules outlined above and the fact that
        `between()` always ignores case (on the principle of least surprise).

        """
        with pytest.raises(ValueError) as exc_info:
            TextVariable.between(rtl_var_customer_surname, start, end)
        assert exc_info.value.args[0] == error_message

        TextVariable.between(rtl_var_customer_surname, end, start)

    def test_matches(self, rtl_var_customer_email, rtl_session):
        gmail_donor = TextVariable.matches(rtl_var_customer_email, "*@gmail.com")
        assert type(gmail_donor) == TextClause
        assert gmail_donor.table_name == "Customers"
        assert gmail_donor.variable_name == "cuEmail"
        assert gmail_donor.values == ['="*@gmail.com"']
        assert gmail_donor.match_type == "Ranges"
        assert gmail_donor.match_case is True
        assert gmail_donor.include is True
        assert gmail_donor.session is rtl_session

        multiple_domain_donors = TextVariable.matches(rtl_var_customer_email,
            ["*@gmail.com", "*@hotmail.com", "*@apteco.com"]
        )
        assert type(multiple_domain_donors) == TextClause
        assert multiple_domain_donors.table_name == "Customers"
        assert multiple_domain_donors.variable_name == "cuEmail"
        assert multiple_domain_donors.values == [
            '="*@gmail.com"',
            '="*@hotmail.com"',
            '="*@apteco.com"',
        ]
        assert multiple_domain_donors.match_type == "Ranges"
        assert multiple_domain_donors.match_case is True
        assert multiple_domain_donors.include is True
        assert multiple_domain_donors.session is rtl_session

        with pytest.raises(ValueError) as exc_info:
            matches_int = TextVariable.matches(rtl_var_customer_email, 30)
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a text variable"
            " must be given as a string or an iterable of strings."
        )


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
