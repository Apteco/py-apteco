from pathlib import Path

import pandas as pd
import pytest
import toml

from apteco import login_with_password

credentials = toml.load(Path(__file__).parent / "credentials.toml")["local"]


@pytest.fixture(scope="session", autouse=True)
def data_dir():
    return Path(__file__).parent / "data"


@pytest.fixture(scope="session", autouse=True)
def holidays():
    return login_with_password(
        credentials["base_url"],
        credentials["data_view"],
        credentials["system"],
        credentials["user"],
        credentials["password"],
    )


"""
Holidays table structure:

Households
└── People
    ├── Bookings
    ├── Policies
    ├── WebVisits
    ├── Communications
    │   ├── Content
    │   └── Responses
    └── Journeys

"""


@pytest.fixture(scope="session")
def households(holidays):
    return holidays.tables["Households"]


@pytest.fixture(scope="session")
def people(holidays):
    return holidays.tables["People"]


@pytest.fixture(scope="session")
def bookings(holidays):
    return holidays.tables["Bookings"]


@pytest.fixture(scope="session")
def policies(holidays):
    return holidays.tables["Policies"]


@pytest.fixture(scope="session")
def web_visits(holidays):
    return holidays.tables["WebVisits"]


@pytest.fixture(scope="session")
def communications(holidays):
    return holidays.tables["Communications"]


@pytest.fixture(scope="session")
def responses(holidays):
    return holidays.tables["Responses Attributed"]


@pytest.fixture()
def datagrid_001_bookings_various_columns(data_dir):
    df = pd.read_csv(data_dir / "datagrid_001_bookings_various_columns.csv")
    df.loc[:, "Booking URN"] = df.loc[:, "Booking URN"].astype(str)
    df.loc[:, "Booking Date"] = pd.to_datetime(
        df.loc[:, "Booking Date"],
        format="%d/%m/%Y",
    ).dt.date
    return df


@pytest.fixture()
def datagrid_002_policies_2000_rows_various_columns(data_dir):
    df = pd.read_csv(
        data_dir / "datagrid_002_policies_2000_rows_various_columns.csv",
    )
    df.loc[:, "Policy Number"] = df.loc[:, "Policy Number"].astype(str)
    df.loc[:, "Policy Date"] = pd.to_datetime(
        df.loc[:, "Policy Date"],
        format="%d/%m/%Y",
    ).dt.date
    return df


@pytest.fixture()
def datagrid_003_web_visits_mobile_social_media_1500_rows_all_columns(data_dir):
    df = pd.read_csv(
        data_dir / "datagrid_003_web_visits_mobile_social_media_1500_rows_all_columns.csv",
    )
    df.loc[:, "Web URN"] = df.loc[:, "Web URN"].astype(str)
    df.loc[:, "Web Visit Time"] = pd.to_datetime(
        df.loc[:, "Web Visit Time"],
        format="%d/%m/%Y %H:%M:%S",
    )
    return df


@pytest.fixture()
def datagrid_004_bookings_with_households_selection(data_dir):
    df = pd.read_csv(
        data_dir / "datagrid_004_bookings_with_households_selection.csv"
    )
    df.loc[:, "Booking URN"] = df.loc[:, "Booking URN"].astype(str)
    df.loc[:, "Travel Date"] = pd.to_datetime(
        df.loc[:, "Travel Date"],
        format="%d/%m/%Y",
    ).dt.date
    return df
