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
def content(holidays):
    return holidays.tables["Content"]


@pytest.fixture(scope="session")
def responses(holidays):
    return holidays.tables["Responses Attributed"]


@pytest.fixture(scope="session")
def journeys(holidays):
    return holidays.tables["Journey History"]


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
        df.loc[:, col] = pd.to_datetime(
            df.loc[:, col], format=fmt, errors="coerce"
        ).dt.date

    for col, fmt in datetime_cols.items():
        df.loc[:, col] = pd.to_datetime(df.loc[:, col], format=fmt, errors="coerce")

    return df


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
def datagrid_003_web_visits_mobile_social_media_1500_rows_all_columns(data_dir):
    """DataGrid with columns from same table, selection from same table and rows limit.

    Table: WebVisits
    Columns: WebVisits
    Selection: WebVisits (social media source & mobile device)
    Rows limit: 1500

    """
    return load_reference_dataframe(
        data_dir
        / "datagrid_003_web_visits_mobile_social_media_1500_rows_all_columns.csv",
        str_cols=["Web URN"],
        datetime_cols={"Web Visit Time": "%d/%m/%Y %H:%M:%S"},
    )


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
def datagrid_005_bookings_with_mixed_columns(data_dir):
    """DataGrid with columns from different tables, selection from same table.

    Table: Bookings
    Columns: Bookings, People, Households
    Selection: [none]
    Rows limit: [none]

    """
    return load_reference_dataframe(
        data_dir / "datagrid_005_bookings_with_mixed_columns.csv",
        str_cols=["Booking URN"],
        date_cols={"DOB": "%d-%m-%Y"},
    )


@pytest.fixture(scope="session")
def cube_001_people_various_dimensions(data_dir):
    """Cube with dimensions from same table.

    Table: People
    Dimensions: People
    Measures: [none]
    Selection: [none]

    """
    df = pd.read_csv(data_dir / "cube_001_people_various_dimensions.csv")
    return df.set_index(["Income", "Occupation", "Source"])


@pytest.fixture(scope="session")
def cube_002_bookings_before_2020_cost_less_than_500(data_dir):
    """Cube with dimensions and selection from same table.

    Table: Bookings
    Dimensions: Bookings
    Measures: [none]
    Selection: Bookings (cost less than £500, booking date up to 31/12/2019)

    """
    df = pd.read_csv(data_dir / "cube_002_bookings_before_2020_cost_less_than_500.csv")
    return df.set_index(["Destination", "Product", "Response Code"])


@pytest.fixture(scope="session")
def cube_003_people_dimensions_bookings_table(data_dir):
    """Cube with dimensions from different table.

    Table: Bookings
    Dimensions: People
    Measures: [none]
    Selection: [none]

    """
    df = pd.read_csv(data_dir / "cube_003_people_dimensions_bookings_table.csv")
    return df.set_index(["Source", "Occupation"])


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
def cube_005_mixed_households_people_dimensions_households_table(data_dir):
    """Cube with dimensions from mixed tables.

    Table: Households
    Dimensions: Households, People
    Measures: [none]
    Selection: [none]

    """
    df = pd.read_csv(
        data_dir / "cube_005_mixed_households_people_dimensions_households_table.csv"
    )
    return df.set_index(["Income", "Gender", "Region"])


@pytest.fixture(scope="session")
def cube_006_mixed_hhds_jnys_ppl_dimensions_people_selection_journeys_table(data_dir):
    """Cube with dimensions from mixed tables, selection and table are different.

    Table: Journeys
    Dimensions: Households, Journeys, People
    Measures: [none]
    Selection: People (surname contains int/str/bool or been to Americas/Australasia)

    """
    df = pd.read_csv(
        data_dir
        / "cube_006_mixed_hhds_jnys_ppl_dimensions_people_selection_journeys_table.csv"
    )
    return df.set_index(["Region", "Pool", "Gender"])


@pytest.fixture(scope="session")
def cube_007_bookings_single_dimension_default_count_measure(data_dir):
    """Cube with single dimension and single non-default measure.

    Table: Bookings
    Dimensions: Destination
    Measures: [none]
    Selection: [none]

    """
    df = pd.read_csv(
        data_dir / "cube_007_bookings_single_dimension_default_count_measure.csv"
    )
    return df.set_index("Destination")


@pytest.fixture(scope="session")
def cube_008_bookings_dimension_destination_measure_sum_profit(data_dir):
    """Cube with single dimension and single non-default measure.

    Table: Bookings
    Dimensions: Destination
    Measures: Sum(Profit)
    Selection: [none]

    """
    df = pd.read_csv(
        data_dir / "cube_008_bookings_dimension_destination_measure_sum_profit.csv"
    )
    return df.set_index("Destination")


@pytest.fixture(scope="session")
def cube_009_bookings_multiple_measures(data_dir):
    """Cube with single dimension and multiple measures from same table.

    Table: Bookings
    Dimensions: Destination
    Measures: Bookings, Sum(Profit), Mean(Cost)
    Selection: [none]

    """
    df = pd.read_csv(data_dir / "cube_009_bookings_multiple_measures.csv")
    return df.set_index("Destination")


@pytest.fixture(scope="session")
def cube_010_bookings_measures_smorgasbord(data_dir):
    """Cube with single dimension and all measures, some from different tables.

    Table: Bookings
    Dimensions: Destination
    Measures: Bookings, Sum(Profit), Mean(Cost), Maximum(Cost), Minimum(Profit),
        Variance(Cost), Standard Deviation(Profit), Lower Quartile(Cost),
        Upper Quartile(Cost), Inter Quartile Range(Profit), 80 Percentile(Cost),
        Populated(DOB), Mode(Source), Count Mode(Product), Count Distinct(Source),
        People, Households
    Selection: [none]

    """
    df = pd.read_csv(data_dir / "cube_010_bookings_measures_smorgasbord.csv")
    return df.set_index("Destination")


def load_cube_reference_dataframe(path, date_indexes=None):
    """Load reference DataFrame, optionally converting column types.

    Args:
        path (path-like): path to CSV with reference data
        date_indexes (dict): mapping from index name
            to dictionary of conversion options:
            format, errors, output, no_trans

    Returns:
        pd.DataFrame: DataFrame with loaded reference data

    """
    date_indexes = date_indexes or {}

    df = pd.read_csv(path)

    for col, options in date_indexes.items():
        fmt = options.get("format", None)
        errors = options.get("errors", "raise")
        output = options.get("output", None)
        end = -2 if options.get("no_trans", False) else -1
        converted = pd.to_datetime(
            df.iloc[1:end].loc[:, col], format=fmt, errors=errors
        )
        if output is not None:
            converted = converted.dt.strftime(output)
        df.iloc[1:end].loc[:, col] = converted

    return df


@pytest.fixture(
    params=[
        ("day", dict(format="%d-%m-%Y", output="%Y-%m-%d")),
        ("month", dict(format="%Y%m", output="%Y-%m")),
        ("quarter", dict()),
        ("year", dict(format="%Y", output="%Y")),
    ],
    ids=["day", "month", "quarter", "year"],
    scope="session",
)
def cube_011_bookings_banded_date(request, data_dir):
    banding, options = request.param
    index_col_name = f"Booking Date ({banding.title()})"
    df = load_cube_reference_dataframe(
        data_dir / f"cube_011_bookings_banded_date_{banding}.csv",
        date_indexes={index_col_name: options},
    )
    return banding, df.set_index(index_col_name)
