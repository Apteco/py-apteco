import pytest

from apteco import Session
from apteco.common import VariableType
from apteco.tables import Table, TablesAccessor
from apteco.variables import (
    ArrayVariable,
    CombinedCategoriesVariable,
    DateTimeVariable,
    DateVariable,
    FlagArrayVariable,
    NumericVariable,
    ReferenceVariable,
    SelectorVariable,
    TextVariable,
)


"""
Fake 'Charity' system
=====================

For use in functional tests.

* variables, tables & session are instances of py-apteco Variable, Table & Session classes
* tables have references to their table relations
* variables & session have reference to tables

Tables
------

Supporters          | chy_supporters_table
├── Campaigns       | chy_campaigns_table
│   └── Donations   | chy_donations_table
└── WebsiteVisits   | chy_website_visits_table

Variables
---------

 Table          |  Name     |  Description          |  Type                 |
-----------------------------------------------------------------------------
Supporters      | suMember  | Membership            | Selector              | chy_selector_var
Supporters      | suRegion  | Region                | CombinedCategories    | chy_combined_categories_var
Supporters      | suEmail   | Email Address         | Text                  | chy_text_var_email
Supporters      | suSrName  | Surname               | Text                  | chy_text_var_surname
Supporters      | suAge     | Age                   | Numeric               | chy_numeric_var_age
Supporters      | suCtcPrf  | Contact Preferences   | FlagArray             | chy_flag_array_var
----------------|-----------|-----------------------|-----------------------|
Campaigns       | caID      | Campaign ID           | Reference             | chy_reference_var
Campaigns       | caCost    | Cost                  | Numeric               | chy_numeric_var_cost
Campaigns       | caTags    | Tags                  | Array                 | chy_array_var
----------------|-----------|-----------------------|-----------------------|
Donations       | doAmount  | Amount                | Numeric               | chy_numeric_var_amount
Donations       | doDate    | Donation Date         | Date                  | chy_date_var
----------------|-----------|-----------------------|-----------------------|
WebsiteVisits   | weSessSt  | Session Start         | DateTime              | chy_datetime_var
WebsiteVisits   | weDurtn   | Duration              | Numeric               | chy_numeric_var_duration

"""


@pytest.fixture()
def chy_tables():
    supporters_table = Table.__new__(Table)
    supporters_table.name = "Supporters"
    supporters_table.parent = None
    supporters_table.ancestors = []

    campaigns_table = Table.__new__(Table)
    campaigns_table.name = "Campaigns"
    campaigns_table.parent = supporters_table
    campaigns_table.ancestors = [supporters_table]

    donations_table = Table.__new__(Table)
    donations_table.name = "Donations"
    donations_table.parent = campaigns_table
    donations_table.ancestors = [campaigns_table, supporters_table]

    website_visits_table = Table.__new__(Table)
    website_visits_table.name = "WebsiteVisits"
    website_visits_table.parent = supporters_table
    website_visits_table.ancestors = [supporters_table]

    supporters_table.children = [campaigns_table]
    supporters_table.descendants = [
        campaigns_table,
        donations_table,
        website_visits_table,
    ]

    campaigns_table.children = [donations_table]
    campaigns_table.descendants = [donations_table]

    donations_table.children = []
    donations_table.descendants = []

    website_visits_table.children = []
    website_visits_table.descendants = []

    return {
        "Supporters": supporters_table,
        "Campaigns": campaigns_table,
        "Donations": donations_table,
        "WebsiteVisits": website_visits_table,
    }


@pytest.fixture()
def chy_supporters_table(chy_tables):
    return chy_tables["Supporters"]


@pytest.fixture()
def chy_campaigns_table(chy_tables):
    return chy_tables["Campaigns"]


@pytest.fixture()
def chy_donations_table(chy_tables):
    return chy_tables["Donations"]


@pytest.fixture()
def chy_website_visits_table(chy_tables):
    return chy_tables["WebsiteVisits"]


@pytest.fixture()
def chy_session(
    chy_supporters_table,
    chy_campaigns_table,
    chy_donations_table,
    chy_website_visits_table,
):
    charity_session = Session.__new__(Session)
    charity_session.system = "CharitySystem"
    charity_session.data_view = "CharityDataView"
    charity_session.tables = TablesAccessor(
        [
            chy_supporters_table,
            chy_campaigns_table,
            chy_donations_table,
            chy_website_visits_table,
        ]
    )
    charity_session.master_table = chy_supporters_table
    charity_session.variables = "CharityVariables"

    return charity_session


@pytest.fixture()
def chy_selector_var(chy_session, chy_supporters_table):
    sv_example = SelectorVariable.__new__(SelectorVariable)
    sv_example.type = VariableType.SELECTOR
    sv_example.table = chy_supporters_table
    sv_example.name = "suMember"
    sv_example.description = "Membership"
    sv_example.session = chy_session
    return sv_example


@pytest.fixture()
def chy_combined_categories_var(chy_session, chy_supporters_table):
    ccv_example = CombinedCategoriesVariable.__new__(CombinedCategoriesVariable)
    ccv_example.type = VariableType.COMBINED_CATEGORIES
    ccv_example.table = chy_supporters_table
    ccv_example.name = "suRegion"
    ccv_example.description = "Region"
    ccv_example.session = chy_session
    return ccv_example


@pytest.fixture()
def chy_numeric_var_age(chy_session, chy_supporters_table):
    nv_example = NumericVariable.__new__(NumericVariable)
    nv_example.type = VariableType.NUMERIC
    nv_example.table = chy_supporters_table
    nv_example.name = "suAge"
    nv_example.description = "Age"
    nv_example.session = chy_session
    return nv_example


@pytest.fixture()
def chy_numeric_var_cost(chy_session, chy_campaigns_table):
    nv_example = NumericVariable.__new__(NumericVariable)
    nv_example.type = VariableType.NUMERIC
    nv_example.table = chy_campaigns_table
    nv_example.name = "caCost"
    nv_example.description = "Cost"
    nv_example.session = chy_session
    return nv_example


@pytest.fixture()
def chy_numeric_var_amount(chy_session, chy_donations_table):
    nv_example = NumericVariable.__new__(NumericVariable)
    nv_example.type = VariableType.NUMERIC
    nv_example.table = chy_donations_table
    nv_example.name = "doAmount"
    nv_example.description = "Amount"
    nv_example.session = chy_session
    return nv_example


@pytest.fixture()
def chy_numeric_var_duration(chy_session, chy_website_visits_table):
    nv_example = NumericVariable.__new__(NumericVariable)
    nv_example.type = VariableType.NUMERIC
    nv_example.table = chy_website_visits_table
    nv_example.name = "weDurtn"
    nv_example.description = "Duration"
    nv_example.session = chy_session
    return nv_example


@pytest.fixture()
def chy_text_var_email(chy_session, chy_supporters_table):
    tv_example = TextVariable.__new__(TextVariable)
    tv_example.type = VariableType.TEXT
    tv_example.table = chy_supporters_table
    tv_example.name = "suEmail"
    tv_example.description = "Email Address"
    tv_example.session = chy_session
    return tv_example


@pytest.fixture()
def chy_text_var_surname(chy_session, chy_supporters_table):
    tv_example = TextVariable.__new__(TextVariable)
    tv_example.type = VariableType.TEXT
    tv_example.table = chy_supporters_table
    tv_example.name = "suSrName"
    tv_example.description = "Surname"
    tv_example.session = chy_session
    return tv_example


@pytest.fixture()
def chy_array_var(chy_session, chy_campaigns_table):
    av_example = ArrayVariable.__new__(ArrayVariable)
    av_example.type = VariableType.ARRAY
    av_example.table = chy_campaigns_table
    av_example.name = "caTags"
    av_example.description = "Tags"
    av_example.session = chy_session
    return av_example


@pytest.fixture()
def chy_flag_array_var(chy_session, chy_supporters_table):
    fav_example = FlagArrayVariable.__new__(FlagArrayVariable)
    fav_example.type = VariableType.FLAG_ARRAY
    fav_example.table = chy_supporters_table
    fav_example.name = "suCtcPrf"
    fav_example.description = "Contact Preferences"
    fav_example.session = chy_session
    return fav_example


@pytest.fixture()
def chy_date_var(chy_session, chy_donations_table):
    dv_example = DateVariable.__new__(DateVariable)
    dv_example.type = VariableType.DATE
    dv_example.table = chy_donations_table
    dv_example.name = "doDate"
    dv_example.description = "Donation Date"
    dv_example.session = chy_session
    return dv_example


@pytest.fixture()
def chy_datetime_var(chy_session, chy_website_visits_table):
    dtv_example = DateTimeVariable.__new__(DateTimeVariable)
    dtv_example.type = VariableType.DATETIME
    dtv_example.table = chy_website_visits_table
    dtv_example.name = "weSessSt"
    dtv_example.description = "Session Start"
    dtv_example.session = chy_session
    return dtv_example


@pytest.fixture()
def chy_reference_var(chy_session, chy_campaigns_table):
    rv_example = ReferenceVariable.__new__(ReferenceVariable)
    rv_example.type = VariableType.REFERENCE
    rv_example.table = chy_campaigns_table
    rv_example.name = "caID"
    rv_example.description = "Campaign ID"
    rv_example.session = chy_session
    return rv_example
