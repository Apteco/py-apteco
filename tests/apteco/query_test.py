from unittest.mock import Mock

import apteco_api as aa

from apteco.query import (
    ArrayClause,
    BooleanClause,
    CombinedCategoriesClause,
    FlagArrayClause,
    NumericClause,
    SelectorClause,
    SubSelectionClause,
    TableClause,
    TextClause,
)


class TestSelectorClause:
    def test_selector_clause_init(self):
        bookings_fr_de_us = SelectorClause(
            "Bookings",
            "boDest",
            ["06", "07", "38"],
            label="Bookings to France, Germany or USA",
        )
        assert bookings_fr_de_us.table_name == "Bookings"
        assert bookings_fr_de_us.variable_name == "boDest"
        assert bookings_fr_de_us.values == ["06", "07", "38"]
        assert bookings_fr_de_us.label == "Bookings to France, Germany or USA"

    def test_selector_clause_to_model(self):
        fake_bookings_fr_de_us = Mock(
            table_name="Bookings",
            variable_name="boDest",
            values=["06", "07", "38"],
            label="Bookings to France, Germany or USA",
            include=True,
            session=None,
        )
        expected_selector_clause_model = aa.Clause(
            criteria=aa.Criteria(
                variable_name="boDest",
                include=True,
                logic="OR",
                ignore_case=False,
                text_match_type="Is",
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(list="06\t07\t38", variable_name="boDest")
                    )
                ],
                table_name="Bookings",
                name="Bookings to France, Germany or USA",
            )
        )
        assert (
            SelectorClause._to_model(fake_bookings_fr_de_us)
            == expected_selector_clause_model
        )


class TestCombinedCategoriesClause:
    def test_combined_categories_clause_init(self):
        bookings_contains_u = CombinedCategoriesClause(
            "Bookings",
            "boCont",
            {"boDest": ["28", "38", "12"], "boCont": ["! ", "AU", "EU"]},
            label="Location contains 'u'",
        )
        assert bookings_contains_u.table_name == "Bookings"
        assert bookings_contains_u.variable_name == "boCont"
        assert bookings_contains_u.value_sets == {
            "boDest": ["28", "38", "12"],
            "boCont": ["! ", "AU", "EU"],
        }
        assert bookings_contains_u.label == "Location contains 'u'"

    def test_combined_categories_clause_to_model(self):
        fake_bookings_contains_u = Mock(
            table_name="Bookings",
            variable_name="boCont",
            value_sets={"boDest": ["28", "38", "12"], "boCont": ["! ", "AU", "EU"]},
            label="Location contains 'u'",
            include=True,
            session=None,
        )
        expected_combined_categories_model = aa.Clause(
            criteria=aa.Criteria(
                variable_name="boCont",
                include=True,
                logic="OR",
                ignore_case=False,
                text_match_type="Is",
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(list="28\t38\t12", variable_name="boDest")
                    ),
                    aa.ValueRule(
                        list_rule=aa.ListRule(list="! \tAU\tEU", variable_name="boCont")
                    ),
                ],
                table_name="Bookings",
                name="Location contains 'u'",
            )
        )
        assert (
            CombinedCategoriesClause._to_model(fake_bookings_contains_u)
            == expected_combined_categories_model
        )


class TestNumericClause:
    def test_numeric_clause_init(self):
        example_numeric_clause = NumericClause(
            "People",
            "peTotalS",
            ["<1066", ">=1558 - <=1603", "=1936", ">1952"],
            include=False,
            label="Exclude total spend matching monarch dates",
        )
        assert example_numeric_clause.table_name == "People"
        assert example_numeric_clause.variable_name == "peTotalS"
        assert example_numeric_clause.values == [
            "<1066",
            ">=1558 - <=1603",
            "=1936",
            ">1952",
        ]
        assert example_numeric_clause.include is False
        assert (
            example_numeric_clause.label == "Exclude total spend matching monarch dates"
        )

    def test_numeric_clause_to_model(self):
        fake_numeric_clause = Mock(
            table_name="People",
            variable_name="peTotalS",
            values=["<1066", ">=1558 - <=1603", "=1936", ">1952"],
            include=False,
            label="Exclude total spend matching monarch dates",
            session=None,
        )
        expected_numeric_clause_model = aa.Clause(
            criteria=aa.Criteria(
                variable_name="peTotalS",
                include=False,
                logic="OR",
                ignore_case=False,
                text_match_type="Is",
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(
                            list="<1066\t>=1558 - <=1603\t=1936\t>1952",
                            variable_name="peTotalS",
                        )
                    )
                ],
                table_name="People",
                name="Exclude total spend matching monarch dates",
            )
        )
        assert (
            NumericClause._to_model(fake_numeric_clause)
            == expected_numeric_clause_model
        )


class TestTextClause:
    def test_text_clause_init(self):
        # TODO: add tests for other text match types
        example_text_clause = TextClause(
            "Households",
            "hoAddr",
            ["Regent", "Oxford", "Bond"],
            "Contains",
            True,
            label="Green Monopoly squares addresses (minus 'Street')",
        )
        assert example_text_clause.table_name == "Households"
        assert example_text_clause.variable_name == "hoAddr"
        assert example_text_clause.values == ["Regent", "Oxford", "Bond"]
        assert example_text_clause.match_type == "Contains"
        assert example_text_clause.match_case is True
        assert (
            example_text_clause.label
            == "Green Monopoly squares addresses (minus 'Street')"
        )

    def test_text_clause_to_model(self):
        fake_text_clause = Mock(
            table_name="Households",
            variable_name="hoAddr",
            values=["Regent", "Oxford", "Bond"],
            match_type="Contains",
            match_case=True,
            label="Green Monopoly squares addresses (minus 'Street')",
            include=True,
            session=None,
        )
        expected_text_clause_model = aa.Clause(
            criteria=aa.Criteria(
                variable_name="hoAddr",
                include=True,
                logic="OR",
                ignore_case=False,
                text_match_type="Contains",
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(
                            list="Regent\tOxford\tBond", variable_name="hoAddr"
                        )
                    )
                ],
                table_name="Households",
                name="Green Monopoly squares addresses (minus 'Street')",
            )
        )
        assert TextClause._to_model(fake_text_clause) == expected_text_clause_model


class TestArrayClause:
    def test_array_clause_init(self):
        example_array_clause = ArrayClause(
            "Households",
            "HHCarmak",
            ["FOR", "PEU", "VOL"],
            "AND",
            label="House has Ford, Peugeot & Volvo",
        )
        assert example_array_clause.table_name == "Households"
        assert example_array_clause.variable_name == "HHCarmak"
        assert example_array_clause.values == ["FOR", "PEU", "VOL"]
        assert example_array_clause.logic == "AND"
        assert example_array_clause.label == "House has Ford, Peugeot & Volvo"

    def test_array_clause_to_model(self):
        fake_array_clause = Mock(
            table_name="Households",
            variable_name="HHCarmak",
            values=["FOR", "PEU", "VOL"],
            logic="AND",
            label="House has Ford, Peugeot & Volvo",
            include=True,
            Session=None,
        )
        expected_array_clause_model = aa.Clause(
            criteria=aa.Criteria(
                variable_name="HHCarmak",
                include=True,
                logic="AND",
                ignore_case=False,
                text_match_type="Is",
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(
                            list="FOR\tPEU\tVOL", variable_name="HHCarmak"
                        )
                    )
                ],
                table_name="Households",
                name="House has Ford, Peugeot & Volvo",
            )
        )
        assert ArrayClause._to_model(fake_array_clause) == expected_array_clause_model


class TestFlagArrayClause:
    def test_flag_array_clause_init(self):
        example_flag_array_clause = FlagArrayClause(
            "People",
            "peNews",
            [
                "Daily Express  ",
                "The Sun        ",
                "Daily Mirror   ",
                "Daily Mail     ",
                "Record         ",
            ],
            "OR",
            label="Tabloid newspaper readers",
        )
        assert example_flag_array_clause.table_name == "People"
        assert example_flag_array_clause.variable_name == "peNews"
        assert example_flag_array_clause.values == [
            "Daily Express  ",
            "The Sun        ",
            "Daily Mirror   ",
            "Daily Mail     ",
            "Record         ",
        ]
        assert example_flag_array_clause.logic == "OR"
        assert example_flag_array_clause.label == "Tabloid newspaper readers"

    def test_flag_array_clause_to_model(self):
        fake_flag_array_clause = Mock(
            table_name="People",
            variable_name="peNews",
            values=[
                "Daily Express  ",
                "The Sun        ",
                "Daily Mirror   ",
                "Daily Mail     ",
                "Record         ",
            ],
            logic="OR",
            label="Tabloid newspaper readers",
            include=True,
            session=None,
        )
        expected_flag_array_clause_model = aa.Clause(
            criteria=aa.Criteria(
                variable_name="peNews",
                include=True,
                logic="OR",
                ignore_case=False,
                text_match_type="Is",
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(
                            list=(
                                "Daily Express  "
                                "\tThe Sun        "
                                "\tDaily Mirror   "
                                "\tDaily Mail     "
                                "\tRecord         "
                            ),
                            variable_name="peNews",
                        )
                    )
                ],
                table_name="People",
                name="Tabloid newspaper readers",
            )
        )
        assert (
            FlagArrayClause._to_model(fake_flag_array_clause)
            == expected_flag_array_clause_model
        )


class TestDateListClause:
    pass


class TestDateRangeClause:
    pass


class TestTimeRangeClause:
    pass


class TestDateTimeRangeClause:
    pass


class TestBooleanClause:
    def test_boolean_clause_init(self):
        clause1 = Mock()
        clause2 = Mock()
        example_boolean_clause = BooleanClause(
            "Bookings", "AND", [clause1, clause2], label="Both of these please!"
        )
        assert example_boolean_clause.table_name == "Bookings"
        assert example_boolean_clause.operation == "AND"
        assert example_boolean_clause.operands == [clause1, clause2]
        assert example_boolean_clause.label == "Both of these please!"

    def test_boolean_clause_to_model(self):
        clause1 = Mock()
        clause2 = Mock()
        clause1._to_model.return_value = "Clause1 model goes here"
        clause2._to_model.return_value = "Clause2 model goes here"
        fake_boolean_clause = Mock(
            table_name="Bookings",
            operation="AND",
            operands=[clause1, clause2],
            label="Both of these please!",
            session=None,
        )
        expected_boolean_clause_model = aa.Clause(
            logic=aa.Logic(
                operation="AND",
                operands=["Clause1 model goes here", "Clause2 model goes here"],
                table_name="Bookings",
                name="Both of these please!",
            )
        )
        assert (
            BooleanClause._to_model(fake_boolean_clause)
            == expected_boolean_clause_model
        )
        clause1._to_model.assert_called_once_with()
        clause2._to_model.assert_called_once_with()


# TODO: unary logic query


class TestTableClause:
    def test_table_clause_init(self):
        subclause = Mock()
        example_table_clause = TableClause(
            "People", "THE", subclause, label="People who live at these houses"
        )
        assert example_table_clause.table_name == "People"
        assert example_table_clause.operation == "THE"
        assert example_table_clause.operand is subclause
        assert example_table_clause.label == "People who live at these houses"

    def test_table_clause_to_model(self):
        subclause = Mock()
        subclause._to_model.return_value = "Subclause model goes here"
        fake_table_clause = Mock(
            table_name="People",
            operation="THE",
            operand=subclause,
            label="People who live at these houses",
            session=None,
        )
        expected_table_clause_model = aa.Clause(
            logic=aa.Logic(
                operation="THE",
                operands=["Subclause model goes here"],
                table_name="People",
                name="People who live at these houses",
            )
        )
        assert TableClause._to_model(fake_table_clause) == expected_table_clause_model
        subclause._to_model.assert_called_once_with()


class TestSubSelectionClause:
    def test_sub_selection_clause_init(self):
        fake_selection = Mock()
        example_subselection_clause = SubSelectionClause(fake_selection)
        assert example_subselection_clause.selection is fake_selection

    def test_sub_selection_clause_to_model(self):
        fake_selection = Mock()
        fake_selection._to_model.return_value = "Selection model goes here"
        fake_subselection_clause = Mock(
            selection=fake_selection, label=None, session=None
        )
        expected_subselection_clause_model = aa.Clause(
            sub_selection="Selection model goes here"
        )
        assert (
            SubSelectionClause._to_model(fake_subselection_clause)
            == expected_subselection_clause_model
        )
        fake_selection._to_model.assert_called_once_with()
