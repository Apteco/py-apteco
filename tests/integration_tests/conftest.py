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


def load_reference_dataframe(path, str_cols=None, date_cols=None, datetime_cols=None):
    """Load reference DataFrame, optionally converting column types.

    Args:
        path (path-like): path to CSV with reference data
        str_cols (list): column names to covert to string
        date_cols (dict): mapping from column name to date format
            for columns to convert to date
        datetime_cols (dict): mapping from column name to datetime format
            for columns to convert to datetime

    Returns:
        pd.DataFrame: DataFrame with loaded reference data

    """
    str_cols = str_cols or []
    date_cols = date_cols or {}
    datetime_cols = datetime_cols or {}

    df = pd.read_csv(path)

    for col in str_cols:
        df.loc[:, col] = df.loc[:, col].astype(str)

    for col, fmt in date_cols.items():
        df.loc[:, col] = pd.to_datetime(df.loc[:, col], format=fmt).dt.date

    for col, fmt in datetime_cols.items():
        df.loc[:, col] = pd.to_datetime(df.loc[:, col], format=fmt)

    return df


@pytest.fixture()
def datagrid_001_bookings_various_columns(data_dir):
    """DataGrid with columns from same table.

    Table: Bookings
    Columns: Bookings
    Selection: [none]
    Rows limit: [none]

    """
    return load_reference_dataframe(
        data_dir / "datagrid_001_bookings_various_columns.csv",
        str_cols=["Booking URN"],
        date_cols={"Booking Date": "%d/%m/%Y"},
    )


@pytest.fixture()
def datagrid_002_policies_2000_rows_various_columns(data_dir):
    """DataGrid with columns from same table and rows limit.

    Table: Policies
    Columns: Policies
    Selection: [none]
    Rows limit: 2000

    """
    return load_reference_dataframe(
        data_dir / "datagrid_002_policies_2000_rows_various_columns.csv",
        str_cols=["Policy Number"],
        date_cols={"Policy Date": "%d/%m/%Y"},
    )


@pytest.fixture()
def datagrid_003_web_visits_mobile_social_media_1500_rows_all_columns(data_dir):
    """DataGrid with columns from same table, selection from same table and rows limit.

    Table: WebVisits
    Columns: WebVisits
    Selection: WebVisits (social media source & mobile device)
    Rows limit: 1500

    """
    return load_reference_dataframe(
        data_dir / "datagrid_003_web_visits_mobile_social_media_1500_rows_all_columns.csv",
        str_cols=["Web URN"],
        datetime_cols={"Web Visit Time": "%d/%m/%Y %H:%M:%S"},
    )


@pytest.fixture()
def datagrid_004_bookings_with_households_selection(data_dir):
    """DataGrid with columns from same table, selection from different table.

    Table: Bookings
    Columns: Bookings
    Selection: Households
    Rows limit: [none]

    """
    return load_reference_dataframe(
        data_dir / "datagrid_004_bookings_with_households_selection.csv",
        str_cols=["Booking URN"],
        date_cols={"Travel Date": "%d/%m/%Y"},
    )


@pytest.fixture()
def cube_001_people_various_dimensions(data_dir):
    """Cube with dimensions from same table.

    Table: People
    Dimensions: People
    Measures: [none]
    Selection: [none]

    """
    df = pd.read_csv(data_dir / "cube_001_people_various_dimensions.csv")
    return df.set_index(["Income", "Occupation", "Source"])


@pytest.fixture()
def cube_002_bookings_before_2020_cost_less_than_500(data_dir):
    """Cube with dimensions and selection from same table.

    Table: Bookings
    Dimensions: Bookings
    Measures: [none]
    Selection: Bookings (cost less than £500, booking date up to 31/12/2019)

    """
    df = pd.read_csv(data_dir / "cube_002_bookings_before_2020_cost_less_than_500.csv")
    return df.set_index(["Destination", "Product", "Response Code"])


@pytest.fixture()
def cube_003_people_dimensions_bookings_table(data_dir):
    """Cube with dimensions from different table.

    Table: Bookings
    Dimensions: People
    Measures: [none]
    Selection: [none]

    """
    df = pd.read_csv(data_dir / "cube_003_people_dimensions_bookings_table.csv")
    return df.set_index(["Source", "Occupation"])


@pytest.fixture()
def cube_004_bookings_dimensions_households_selection_people_table(data_dir):
    """Cube with dimensions and selection from different tables.

    Table: People
    Dimensions: Bookings
    Measures: [none]
    Selection: Households (North West incl. Manchester or has Ferrari, Fiat or Ford)

    """
    df = pd.read_csv(
        data_dir / "cube_004_bookings_dimensions_households_selection_people_table.csv"
    )
    return df.set_index(["Product", "Continent"])
