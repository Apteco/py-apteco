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
