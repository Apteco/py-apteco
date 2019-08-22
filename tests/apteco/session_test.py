import pytest

import apteco.session


@pytest.fixture()
def fake_initialize_tables_algo(mocker):
    fake = mocker.Mock()
    fake.run.return_value = ["fake tables", "fake master table"]
    return mocker.patch("apteco.session.InitializeTablesAlgorithm", return_value=fake)


@pytest.fixture()
def fake_initialize_variables_algo(mocker):
    fake = mocker.Mock()
    fake.run.return_value = "fake variables"
    return mocker.patch("apteco.session.InitializeVariablesAlgorithm", return_value=fake)


@pytest.fixture()
def fake_client(mocker):
    fake_client = mocker.Mock(configuration="con-fig leaves")
    return fake_client


@pytest.fixture()
def fake_credentials(mocker):
    fake_credentials = mocker.Mock(
        base_url="baseless assumptions",
        data_view="a room with a view",
        session_id="0246813579",
        access_token="token of my gratitude",
        user="use, er, something else",
    )
    return fake_credentials


def test_session(fake_initialize_variables_algo, fake_initialize_tables_algo, fake_credentials, fake_client, mocker):
    # fake_unpack_credentials = mocker.patch.object(apteco.session.Session, "_unpack_credentials")
    # fake_create_client = mocker.patch.object(apteco.session.Session, "_create_client")
    session_example = apteco.session.Session(fake_credentials, "solar_system")
    assert session_example.system == "solar_system"
    assert session_example.variables == "fake variables"
    assert session_example.tables == "fake tables"
    assert session_example.master_table == "fake master table"
    fake_initialize_variables_algo.assert_called_once_with(session_example)
    fake_initialize_tables_algo.assert_called_once_with(session_example)
    # fake_unpack_credentials.assert_called_once_with(fake_credentials)
    # fake_create_client.assert_called_once()
    assert session_example.base_url == "baseless assumptions"
    assert session_example.data_view == "a room with a view"
    assert session_example.session_id == "0246813579"
    assert session_example.access_token == "token of my gratitude"
    assert session_example.user == "use, er, something else"


# TODO: write test
@pytest.mark.xfail(reason="Test not written")
def test_table():
    raise NotImplementedError


def test_user():
    user_example = apteco.session.User("JDoe", "Jane", "Doe", "jane.doe@example.com")
    assert user_example.username == "JDoe"
    assert user_example.first_name == "Jane"
    assert user_example.surname == "Doe"
    assert user_example.email_address == "jane.doe@example.com"


def test_credentials(mocker):
    fake_user = mocker.Mock()
    credentials_example = apteco.session.Credentials(
        "https://marketing.example.com/AptecoAPI/",
        "room_with_a_view",
        "31415926",
        "e.g.123abc987zyx",
        fake_user,
    )
    assert credentials_example.base_url == "https://marketing.example.com/AptecoAPI/"
    assert credentials_example.data_view == "room_with_a_view"
    assert credentials_example.session_id == "31415926"
    assert credentials_example.access_token == "e.g.123abc987zyx"
    assert credentials_example.user == fake_user


@pytest.fixture()
def fake_get_pw(mocker):
    return mocker.patch.object(
        apteco.session, "_get_password", return_value="something very secret"
    )


@pytest.fixture()
def fake_login_with_pw(mocker):
    return mocker.patch.object(
        apteco.session, "login_with_password", return_value="Here are your credentials!"
    )


def test_login(fake_get_pw, fake_login_with_pw):
    credentials = apteco.session.login(
        "https://marketing.example.com/AptecoAPI/", "a_room_with_a_view", "JDoe"
    )
    assert credentials == "Here are your credentials!"
    fake_get_pw.assert_called_once_with()
    fake_login_with_pw.assert_called_once_with(
        "https://marketing.example.com/AptecoAPI/",
        "a_room_with_a_view",
        "JDoe",
        password="something very secret",
    )


# TODO: write test
@pytest.mark.xfail(reason="Test not written")
def test_login_with_password():
    raise NotImplementedError


# TODO: write test
@pytest.mark.xfail(reason="Test not written")
def test_get_password():
    raise NotImplementedError


# TODO: write test
@pytest.mark.xfail(reason="Test not written")
def test_login_with_password():
    raise NotImplementedError


# TODO: write tests for class and methods
@pytest.mark.xfail(reason="Tests not written")
def test_simple_login_algorithm():
    raise NotImplementedError


# TODO: write tests for class and methods
@pytest.mark.xfail(reason="Tests not written")
def test_initialize_tables_algorithm():
    raise NotImplementedError


# TODO: write tests for class and methods
@pytest.mark.xfail(reason="Tests not written")
def test_initialize_variables_algorithm():
    raise NotImplementedError
