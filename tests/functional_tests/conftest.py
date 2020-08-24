from unittest.mock import Mock

import pytest

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
def chy_supporters_table():
    fake = Mock()
    fake.configure_mock(name="Supporters")
    return fake


@pytest.fixture()
def chy_donations_table():
    fake = Mock()
    fake.configure_mock(name="Donations")
    return fake


@pytest.fixture()
def chy_campaigns_table():
    fake = Mock()
    fake.configure_mock(name="Campaigns")
    return fake


@pytest.fixture()
def chy_website_visits_table():
    fake = Mock()
    fake.configure_mock(name="WebVisits")
    return fake


@pytest.fixture()
def fake_selector_variable(chy_supporters_table):
    sv_example = SelectorVariable.__new__(SelectorVariable)
    sv_example.type = "Selector"
    sv_example.table = chy_supporters_table
    sv_example.name = "Membership"
    sv_example.session = "CharityDataViewSession"
    return sv_example


@pytest.fixture()
def fake_combined_categories_variable(chy_supporters_table):
    ccv_example = CombinedCategoriesVariable.__new__(CombinedCategoriesVariable)
    ccv_example.type = "CombinedCategories"
    ccv_example.table = chy_supporters_table
    ccv_example.name = "Region"
    ccv_example.session = "CharityDataViewSession"
    return ccv_example


@pytest.fixture()
def fake_numeric_variable(chy_donations_table):
    nv_example = NumericVariable.__new__(NumericVariable)
    nv_example.type = "Numeric"
    nv_example.table = chy_donations_table
    nv_example.name = "Amount"
    nv_example.session = "CharityDataViewSession"
    return nv_example


@pytest.fixture()
def fake_text_variable_email(chy_supporters_table):
    tv_example = TextVariable.__new__(TextVariable)
    tv_example.type = "Text"
    tv_example.table = chy_supporters_table
    tv_example.name = "EmailAddress"
    tv_example.session = "CharityDataViewSession"
    return tv_example


@pytest.fixture()
def fake_text_variable_surname(chy_supporters_table):
    tv_example = TextVariable.__new__(TextVariable)
    tv_example.type = "Text"
    tv_example.table = chy_supporters_table
    tv_example.name = "Surname"
    tv_example.session = "CharityDataViewSession"
    return tv_example


@pytest.fixture()
def fake_array_variable(chy_campaigns_table):
    av_example = ArrayVariable.__new__(ArrayVariable)
    av_example.type = "Array"
    av_example.table = chy_campaigns_table
    av_example.name = "Tags"
    av_example.session = "CharityDataViewSession"
    return av_example


@pytest.fixture()
def fake_flag_array_variable(chy_supporters_table):
    fav_example = FlagArrayVariable.__new__(FlagArrayVariable)
    fav_example.type = "FlagArray"
    fav_example.table = chy_supporters_table
    fav_example.name = "ContactPreferences"
    fav_example.session = "CharityDataViewSession"
    return fav_example


@pytest.fixture()
def fake_date_variable(chy_donations_table):
    dv_example = DateVariable.__new__(DateVariable)
    dv_example.type = "Date"
    dv_example.table = chy_donations_table
    dv_example.name = "DonationDate"
    dv_example.session = "CharityDataViewSession"
    return dv_example


@pytest.fixture()
def fake_datetime_variable(chy_website_visits_table):
    dtv_example = DateTimeVariable.__new__(DateTimeVariable)
    dtv_example.type = "DateTime"
    dtv_example.table = chy_website_visits_table
    dtv_example.name = "BrowsingSessionStart"
    dtv_example.session = "CharityDataViewSession"
    return dtv_example


@pytest.fixture()
def fake_reference_variable(chy_campaigns_table):
    rv_example = ReferenceVariable.__new__(ReferenceVariable)
    rv_example.type = "Reference"
    rv_example.table = chy_campaigns_table
    rv_example.name = "CampaignID"
    rv_example.session = "CharityDataViewSession"
    return rv_example
