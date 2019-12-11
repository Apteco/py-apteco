from apteco import query
import apteco_api as aa
from unittest.mock import Mock

# TODO: separate __init__() and _to_model() tests


def test_selector_clause():

    bookings_fr_de_us = query.SelectorClause(
        'Bookings',
        'boDest',
        ['06', '07', '38'],
        label="Bookings to France, Germany or USA"
    )
    assert bookings_fr_de_us.table_name == 'Bookings'
    assert bookings_fr_de_us.variable_name == 'boDest'
    assert bookings_fr_de_us.values == ['06', '07', '38']
    assert bookings_fr_de_us.label == "Bookings to France, Germany or USA"

    expected_selector_clause_model = aa.Clause(
            criteria=aa.Criteria(
                variable_name='boDest',
                include=True,
                logic='OR',
                ignore_case=False,
                text_match_type='Is',
                value_rules=[
                    aa.ValueRule(
                        list_rule=aa.ListRule(
                            list='06\t07\t38',
                            variable_name='boDest'
                        )
                    )
                ],
                table_name='Bookings',
                name="Bookings to France, Germany or USA"
            )
        )
    assert bookings_fr_de_us._to_model() == expected_selector_clause_model


def test_combined_categories_clause():

    bookings_contains_u = query.CombinedCategoriesClause(
        'Bookings',
        'boCont',
        {'boDest': ['28', '38', '12'], 'boCont': ['! ', 'AU', 'EU']},
        label="Location contains 'u'"
    )
    assert bookings_contains_u.table_name == 'Bookings'
    assert bookings_contains_u.variable_name == 'boCont'
    assert bookings_contains_u.value_sets == {
        'boDest': ['28', '38', '12'],
        'boCont': ['! ', 'AU', 'EU']
    }
    assert bookings_contains_u.label == "Location contains 'u'"

    expected_combined_categories_model = aa.Clause(
        criteria=aa.Criteria(
            variable_name='boCont',
            include=True,
            logic='OR',
            ignore_case=False,
            text_match_type='Is',
            value_rules=[
                aa.ValueRule(
                    list_rule=aa.ListRule(
                        list='28\t38\t12',
                        variable_name='boDest'
                    )
                ),
                aa.ValueRule(
                    list_rule=aa.ListRule(
                        list='! \tAU\tEU',
                        variable_name='boCont'
                    )
                )
            ],
            table_name='Bookings',
            name="Location contains 'u'"
        )
    )
    assert bookings_contains_u._to_model() == expected_combined_categories_model


def test_numeric_clause():

    example_numeric_clause = query.NumericClause(
        'People',
        'peTotalS',
        ['<1066', '>=1558 - <=1603', '=1936', '>1952'],
        include=False,
        label="Exclude total spend matching monarch dates"
    )
    assert example_numeric_clause.table_name == 'People'
    assert example_numeric_clause.variable_name == 'peTotalS'
    assert example_numeric_clause.values == ['<1066', '>=1558 - <=1603', '=1936', '>1952']
    assert example_numeric_clause.include is False
    assert example_numeric_clause.label == "Exclude total spend matching monarch dates"

    expected_numeric_clause_model = aa.Clause(
        criteria=aa.Criteria(
            variable_name='peTotalS',
            include=False,
            logic='OR',
            ignore_case=False,
            text_match_type='Is',
            value_rules=[
                aa.ValueRule(
                    list_rule=aa.ListRule(
                        list='<1066\t>=1558 - <=1603\t=1936\t>1952',
                        variable_name='peTotalS'
                    )
                )
            ],
            table_name='People',
            name="Exclude total spend matching monarch dates"
        )
    )
    assert example_numeric_clause._to_model() == expected_numeric_clause_model


def test_text_clause():

    # TODO: add tests for other text match types
    example_text_clause = query.TextClause(
        'Households',
        'hoAddr',
        ["Regent", "Oxford", "Bond"],
        'Contains',
        True,
        label="Green Monopoly squares addresses (minus 'Street')"
    )
    assert example_text_clause.table_name == 'Households'
    assert example_text_clause.variable_name == 'hoAddr'
    assert example_text_clause.values == ["Regent", "Oxford", "Bond"]
    assert example_text_clause.match_type == 'Contains'
    assert example_text_clause.match_case is True
    assert example_text_clause.label == "Green Monopoly squares addresses (minus 'Street')"

    expected_text_clause_model = aa.Clause(
        criteria=aa.Criteria(
            variable_name='hoAddr',
            include=True,
            logic='OR',
            ignore_case=False,
            text_match_type='Contains',
            value_rules=[
                aa.ValueRule(
                    list_rule=aa.ListRule(
                        list='Regent\tOxford\tBond',
                        variable_name='hoAddr'
                    )
                )
            ],
            table_name='Households',
            name="Green Monopoly squares addresses (minus 'Street')"
        )
    )
    assert example_text_clause._to_model() == expected_text_clause_model


def test_array_clause():

    example_array_clause = query.ArrayClause(
        'Households',
        'HHCarmak',
        ['FOR', 'PEU', 'VOL'],
        'AND',
        label="House has Ford, Peugeot & Volvo"
    )
    assert example_array_clause.table_name == 'Households'
    assert example_array_clause.variable_name == 'HHCarmak'
    assert example_array_clause.values == ['FOR', 'PEU', 'VOL']
    assert example_array_clause.logic == 'AND'
    assert example_array_clause.label == "House has Ford, Peugeot & Volvo"

    expected_array_clause_model = aa.Clause(
        criteria=aa.Criteria(
            variable_name='HHCarmak',
            include=True,
            logic='AND',
            ignore_case=False,
            text_match_type='Is',
            value_rules=[
                aa.ValueRule(
                    list_rule=aa.ListRule(
                        list='FOR\tPEU\tVOL',
                        variable_name='HHCarmak'
                    )
                )
            ],
            table_name='Households',
            name="House has Ford, Peugeot & Volvo"
        )
    )
    assert example_array_clause._to_model() == expected_array_clause_model


def test_flag_array_clause():

    example_flag_array_clause = query.FlagArrayClause(
        'People',
        'peNews',
        [
            'Daily Express  ',
            'The Sun        ',
            'Daily Mirror   ',
            'Daily Mail     ',
            'Record         '
        ],
        'OR',
        label="Tabloid newspaper readers"
    )
    assert example_flag_array_clause.table_name == 'People'
    assert example_flag_array_clause.variable_name == 'peNews'
    assert example_flag_array_clause.values == [
        'Daily Express  ',
        'The Sun        ',
        'Daily Mirror   ',
        'Daily Mail     ',
        'Record         '
    ]
    assert example_flag_array_clause.logic == 'OR'
    assert example_flag_array_clause.label == "Tabloid newspaper readers"

    expected_flag_array_clause_model = aa.Clause(
        criteria=aa.Criteria(
            variable_name='peNews',
            include=True,
            logic='OR',
            ignore_case=False,
            text_match_type='Is',
            value_rules=[
                aa.ValueRule(
                    list_rule=aa.ListRule(
                        list=(
                            'Daily Express  '
                            '\tThe Sun        '
                            '\tDaily Mirror   '
                            '\tDaily Mail     '
                            '\tRecord         '
                        ),
                        variable_name='peNews'
                    )
                )
            ],
            table_name='People',
            name="Tabloid newspaper readers"
        )
    )
    assert example_flag_array_clause._to_model() == expected_flag_array_clause_model


def test_boolean_clause():

    clause1 = Mock()
    clause2 = Mock()
    example_boolean_clause = query.BooleanClause(
        'Bookings',
        'AND',
        [clause1, clause2],
        label="Both of these please!"
    )
    assert example_boolean_clause.table_name == 'Bookings'
    assert example_boolean_clause.operation == 'AND'
    assert example_boolean_clause.operands == [clause1, clause2]
    assert example_boolean_clause.label == "Both of these please!"

    clause1._to_model.return_value = 'Clause1 model goes here'
    clause2._to_model.return_value = 'Clause2 model goes here'
    expected_boolean_clause_model = aa.Clause(
        logic=aa.Logic(
            operation='AND',
            operands=['Clause1 model goes here', 'Clause2 model goes here'],
            table_name='Bookings',
            name="Both of these please!"
        )
    )
    assert example_boolean_clause._to_model() == expected_boolean_clause_model
    clause1._to_model.assert_called_once_with()
    clause2._to_model.assert_called_once_with()


def test_table_clause():

    subclause = Mock()
    example_table_clause = query.TableClause(
        'People',
        'THE',
        subclause,
        label="People who live at these houses"
    )
    assert example_table_clause.table_name == 'People'
    assert example_table_clause.operation == 'THE'
    assert example_table_clause.operand == subclause
    assert example_table_clause.label == 'People who live at these houses'

    subclause._to_model.return_value = 'Subclause model goes here'
    expected_table_clause_model = aa.Clause(
        logic=aa.Logic(
            operation='THE',
            operands=['Subclause model goes here'],
            table_name='People',
            name="People who live at these houses"
        )
    )
    assert example_table_clause._to_model() == expected_table_clause_model
    subclause._to_model.assert_called_once_with()


def test_sub_selection_clause():

    fake_selection = Mock()
    example_subselection_clause = query.SubSelectionClause(fake_selection)
    assert example_subselection_clause.selection == fake_selection

    fake_selection._to_model.return_value = 'Selection model goes here'
    expected_subselection_clause_model = aa.Clause(
        sub_selection='Selection model goes here'
    )
    assert example_subselection_clause._to_model() == expected_subselection_clause_model
    fake_selection._to_model.assert_called_once_with()
