import pytest

from apteco import Session
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

Tables
------

Supporters
├── Campaigns
│   └── Donations
└── Website visits

Variables
---------

 Table          |  Name                 |  Type                 |
-----------------------------------------------------------------
Supporters      | Membership            | Selector              |
Supporters      | Region                | CombinedCategories    |
Supporters      | EmailAddress          | Text                  |
Supporters      | Surname               | Text                  |
Supporters      | ContactPreferences    | FlagArray             |
----------------|-----------------------|-----------------------|
Campaigns       | CampaignID            | Reference             |
Campaigns       | Tags                  | Array                 |
----------------|-----------------------|-----------------------|
Donations       | Amount                | Numeric               |
Donations       | DonationDate          | Date                  |
----------------|-----------------------|-----------------------|
Website visits  | BrowsingSessionStart  | DateTime              |

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
    website_visits_table.name = "WebVisits"
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
        "WebVisits": website_visits_table,
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
    return chy_tables["WebVisits"]


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
def fake_selector_variable(chy_session, chy_supporters_table):
    sv_example = SelectorVariable.__new__(SelectorVariable)
    sv_example.type = "Selector"
    sv_example.table = chy_supporters_table
    sv_example.name = "Membership"
    sv_example.session = chy_session
    return sv_example


@pytest.fixture()
def fake_combined_categories_variable(chy_session, chy_supporters_table):
    ccv_example = CombinedCategoriesVariable.__new__(CombinedCategoriesVariable)
    ccv_example.type = "CombinedCategories"
    ccv_example.table = chy_supporters_table
    ccv_example.name = "Region"
    ccv_example.session = chy_session
    return ccv_example


@pytest.fixture()
def fake_numeric_variable(chy_session, chy_donations_table):
    nv_example = NumericVariable.__new__(NumericVariable)
    nv_example.type = "Numeric"
    nv_example.table = chy_donations_table
    nv_example.name = "Amount"
    nv_example.session = chy_session
    return nv_example


@pytest.fixture()
def fake_text_variable_email(chy_session, chy_supporters_table):
    tv_example = TextVariable.__new__(TextVariable)
    tv_example.type = "Text"
    tv_example.table = chy_supporters_table
    tv_example.name = "EmailAddress"
    tv_example.session = chy_session
    return tv_example


@pytest.fixture()
def fake_text_variable_surname(chy_session, chy_supporters_table):
    tv_example = TextVariable.__new__(TextVariable)
    tv_example.type = "Text"
    tv_example.table = chy_supporters_table
    tv_example.name = "Surname"
    tv_example.session = chy_session
    return tv_example


@pytest.fixture()
def fake_array_variable(chy_session, chy_campaigns_table):
    av_example = ArrayVariable.__new__(ArrayVariable)
    av_example.type = "Array"
    av_example.table = chy_campaigns_table
    av_example.name = "Tags"
    av_example.session = chy_session
    return av_example


@pytest.fixture()
def fake_flag_array_variable(chy_session, chy_supporters_table):
    fav_example = FlagArrayVariable.__new__(FlagArrayVariable)
    fav_example.type = "FlagArray"
    fav_example.table = chy_supporters_table
    fav_example.name = "ContactPreferences"
    fav_example.session = chy_session
    return fav_example


@pytest.fixture()
def fake_date_variable(chy_session, chy_donations_table):
    dv_example = DateVariable.__new__(DateVariable)
    dv_example.type = "Date"
    dv_example.table = chy_donations_table
    dv_example.name = "DonationDate"
    dv_example.session = chy_session
    return dv_example


@pytest.fixture()
def fake_datetime_variable(chy_session, chy_website_visits_table):
    dtv_example = DateTimeVariable.__new__(DateTimeVariable)
    dtv_example.type = "DateTime"
    dtv_example.table = chy_website_visits_table
    dtv_example.name = "BrowsingSessionStart"
    dtv_example.session = chy_session
    return dtv_example


@pytest.fixture()
def fake_reference_variable(chy_session, chy_campaigns_table):
    rv_example = ReferenceVariable.__new__(ReferenceVariable)
    rv_example.type = "Reference"
    rv_example.table = chy_campaigns_table
    rv_example.name = "CampaignID"
    rv_example.session = chy_session
    return rv_example
