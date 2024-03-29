import pytest

from apteco.common import VariableType
from apteco.query import NumericClause, TextClause
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
    assert selector_variable.var_code_min_count == 123_456
    assert selector_variable.var_code_max_count == 234_567
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
    def test_numeric_variable_init(
        self, ins_aa_num_var_prem, ins_table_prods, ins_session
    ):
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
    def test_text_variable_init(
        self, ins_aa_text_var_addr, ins_table_clnts, ins_session
    ):
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
        email = rtl_var_customer_email

        specific_donor = TextVariable.equals(email, "donor@domain.com")
        assert type(specific_donor) == TextClause
        assert specific_donor.table_name == "Customers"
        assert specific_donor.variable_name == "cuEmail"
        assert specific_donor.values == ["donor@domain.com"]
        assert specific_donor.match_type == "Is"
        assert specific_donor.match_case is True
        assert specific_donor.include is True
        assert specific_donor.session is rtl_session

        donor_list = [f"donor_{i}@domain.com" for i in range(4)]
        donors_by_email = TextVariable.equals(email, donor_list)
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
            donors_by_number = TextVariable.equals(email, {34, 765, 2930})
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a text variable"
            " must be given as a string or an iterable of strings."
        )

        exclude_them = TextVariable.equals(email, "bad_donor@domain.com", include=False)
        assert type(exclude_them) == TextClause
        assert exclude_them.table_name == "Customers"
        assert exclude_them.variable_name == "cuEmail"
        assert exclude_them.values == ["bad_donor@domain.com"]
        assert exclude_them.match_type == "Is"
        assert exclude_them.match_case is True
        assert exclude_them.include is False
        assert exclude_them.session is rtl_session

        bad_donor_set = {"dont_email_me@domain.com", "unsubscribed@domain.org"}
        not_these_people = TextVariable.equals(email, bad_donor_set, include=False)
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
            donor_not_an_obj = TextVariable.equals(email, object(), include=False)
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
        surname = rtl_var_customer_surname

        starts_with_smith = TextVariable.startswith(surname, "Smith")
        assert type(starts_with_smith) == TextClause
        assert starts_with_smith.table_name == "Customers"
        assert starts_with_smith.variable_name == "cuSName"
        assert starts_with_smith.values == ["Smith"]
        assert starts_with_smith.match_type == "Begins"
        assert starts_with_smith.match_case is True
        assert starts_with_smith.include is True
        assert starts_with_smith.session is rtl_session

        surname_starters = ["Tom", "James", "Dan", "Dav"]
        starts_with_multiple = TextVariable.startswith(surname, surname_starters)
        assert type(starts_with_multiple) == TextClause
        assert starts_with_multiple.table_name == "Customers"
        assert starts_with_multiple.variable_name == "cuSName"
        assert starts_with_multiple.values == ["Tom", "James", "Dan", "Dav"]
        assert starts_with_multiple.match_type == "Begins"
        assert starts_with_multiple.match_case is True
        assert starts_with_multiple.include is True
        assert starts_with_multiple.session is rtl_session

        with pytest.raises(ValueError) as exc_info:
            starts_with_boolean = TextVariable.startswith(surname, True)
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a text variable"
            " must be given as a string or an iterable of strings."
        )

    def test_ends_with(self, rtl_var_customer_surname, rtl_session):
        surname = rtl_var_customer_surname

        ends_with_son = TextVariable.endswith(surname, "son")
        assert type(ends_with_son) == TextClause
        assert ends_with_son.table_name == "Customers"
        assert ends_with_son.variable_name == "cuSName"
        assert ends_with_son.values == ["son"]
        assert ends_with_son.match_type == "Ends"
        assert ends_with_son.match_case is True
        assert ends_with_son.include is True
        assert ends_with_son.session is rtl_session

        ends_with_multiple = TextVariable.endswith(surname, ["son", "ez"])
        assert type(ends_with_multiple) == TextClause
        assert ends_with_multiple.table_name == "Customers"
        assert ends_with_multiple.variable_name == "cuSName"
        assert ends_with_multiple.values == ["son", "ez"]
        assert ends_with_multiple.match_type == "Ends"
        assert ends_with_multiple.match_case is True
        assert ends_with_multiple.include is True
        assert ends_with_multiple.session is rtl_session

        with pytest.raises(ValueError) as exc_info:
            ends_with_float = TextVariable.endswith(surname, [2.8, 9.4])
        assert exc_info.value.args[0] == (
            "Chosen value(s) for a text variable"
            " must be given as a string or an iterable of strings."
        )

    def test_before(self, rtl_var_customer_surname, rtl_session):
        surname = rtl_var_customer_surname

        first_half_alphabet = TextVariable.before(surname, "n")
        assert type(first_half_alphabet) == TextClause
        assert first_half_alphabet.table_name == "Customers"
        assert first_half_alphabet.variable_name == "cuSName"
        assert first_half_alphabet.values == ['<"n"']
        assert first_half_alphabet.match_type == "Ranges"
        assert first_half_alphabet.match_case is False
        assert first_half_alphabet.include is True
        assert first_half_alphabet.session is rtl_session

        up_to_my_neck = TextVariable.before(surname, "My neck", allow_equal=True)
        assert type(up_to_my_neck) == TextClause
        assert up_to_my_neck.table_name == "Customers"
        assert up_to_my_neck.variable_name == "cuSName"
        assert up_to_my_neck.values == ['<="My neck"']
        assert up_to_my_neck.match_type == "Ranges"
        assert up_to_my_neck.match_case is False
        assert up_to_my_neck.include is True
        assert up_to_my_neck.session is rtl_session

        with pytest.raises(ValueError) as exc_info:
            earlier_than_letters = TextVariable.before(surname, list("abcedfgh"))
        assert exc_info.value.args[0] == (
            "Must specify a single string for this type of operation."
        )

        with pytest.raises(ValueError) as exc_info:
            before_int = TextVariable.before(surname, 6)
        assert exc_info.value.args[0] == (
            "Must specify a single string for this type of operation."
        )

    def test_after(self, rtl_var_customer_surname, rtl_session):
        surname = rtl_var_customer_surname

        after_smith = TextVariable.after(surname, "Smith")
        assert type(after_smith) == TextClause
        assert after_smith.table_name == "Customers"
        assert after_smith.variable_name == "cuSName"
        assert after_smith.values == ['>"Smith"']
        assert after_smith.match_type == "Ranges"
        assert after_smith.match_case is False
        assert after_smith.include is True
        assert after_smith.session is rtl_session

        from_now_on = TextVariable.after(surname, "now", allow_equal=True)
        assert type(from_now_on) == TextClause
        assert from_now_on.table_name == "Customers"
        assert from_now_on.variable_name == "cuSName"
        assert from_now_on.values == ['>="now"']
        assert from_now_on.match_type == "Ranges"
        assert from_now_on.match_case is False
        assert from_now_on.include is True
        assert from_now_on.session is rtl_session

        with pytest.raises(ValueError) as exc_info:
            later_than_tuple = TextVariable.after(surname, ("A", "e", "i", "O"))
        assert exc_info.value.args[0] == (
            "Must specify a single string for this type of operation."
        )

        with pytest.raises(ValueError) as exc_info:
            after_boolean = TextVariable.after(surname, False)
        assert exc_info.value.args[0] == (
            "Must specify a single string for this type of operation."
        )

    def test_between(self, rtl_var_customer_surname, rtl_session):
        surname = rtl_var_customer_surname

        rock_and_hardplace = TextVariable.between(surname, "hardplace", "rock")
        assert type(rock_and_hardplace) == TextClause
        assert rock_and_hardplace.table_name == "Customers"
        assert rock_and_hardplace.variable_name == "cuSName"
        assert rock_and_hardplace.values == ['>="hardplace" - <="rock"']
        assert rock_and_hardplace.match_type == "Ranges"
        assert rock_and_hardplace.match_case is False
        assert rock_and_hardplace.include is True
        assert rock_and_hardplace.session is rtl_session

        with pytest.raises(ValueError) as exc_info:
            between_lists = TextVariable.between(surname, ["a", "b"], ["y", "z"])
        assert exc_info.value.args[0] == (
            "Must specify a single string for this type of operation."
        )

        with pytest.raises(ValueError) as exc_info:
            between_ints = TextVariable.between(surname, 1, 100)
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
        assert exc_info.value.args[0] == "`start` must sort before `end`"

    @pytest.mark.parametrize(
        ["start", "end"],
        [
            pytest.param("F", "F", id="same thing twice"),
            pytest.param("H", "h", id="uppercase and lowercase pair"),
        ],
    )
    def test_between_ordering_compare_equal(self, start, end, rtl_var_customer_surname):
        """Check `between()` behaves correctly with inputs that compare equal.

        Testing with pairs of characters which compare equal case-insensitively.
        Should be accepted with `start` and `end` values either way round.

        """
        TextVariable.between(rtl_var_customer_surname, start, end)
        TextVariable.between(rtl_var_customer_surname, end, start)

    @pytest.mark.parametrize(
        ["start", "end", "error_message"],
        [
            pytest.param(
                "N",
                "_",
                "`start` must sort before `end`,"
                " but 'N' sorts after '_' when compared case-insensitively.",
                id="ascii 91-96 symbol & uppercase letter",
            ),
            pytest.param(
                "V",
                "d",
                "`start` must sort before `end`,"
                " but 'V' sorts after 'd' when compared case-insensitively.",
                id="lowercase letter & uppercase letter",
            ),
        ],
    )
    def test_between_ascii_order_but_wrong(
        self, start, end, error_message, rtl_var_customer_surname
    ):
        """Test `between()` checks character order correctly.

        Test `between()` with pairs of characters whose ASCII order is different
        from the order fs32svr sorts in when comparing case-insensitively.

        ASCII characters can be split into 5 ranges, based around the letters:
        *  32 -  64: symbols (incl. space):  !"#$%&'()*+,-./0123456789:;<=>?@
        *  65 -  90: uppercase letters    : ABCDEFGHIJKLMNOPQRSTUVWXYZ
        *  91 -  96: symbols (+ backslash): []^_`
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

        domains = ["*@gmail.com", "*@hotmail.com", "*@apteco.com"]
        multiple_domain_donors = TextVariable.matches(rtl_var_customer_email, domains)
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
    assert flag_array_variable.var_code_max_count == 555_666
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
