from pathlib import Path

import pytest
import toml

from apteco import login_with_password

credentials = toml.load(Path(__file__).parent / "credentials.toml")["local"]


@pytest.fixture(scope="session", autouse=True)
def holidays():
    return login_with_password(
        credentials["base_url"],
        credentials["data_view"],
        credentials["system"],
        credentials["user"],
        credentials["password"],
    )


@pytest.fixture(scope="session")
def people(holidays):
    return holidays.tables["People"]


@pytest.fixture(scope="session")
def bookings(holidays):
    return holidays.tables["Bookings"]


@pytest.fixture(scope="session")
def households(holidays):
    return holidays.tables["Households"]


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
