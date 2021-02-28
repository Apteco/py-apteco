import getpass
import json
import logging
from json import JSONDecodeError

import apteco_api as aa
import pytest

import apteco.session
from apteco.exceptions import (
    ApiResultsError,
    DeserializeError,
    TablesError,
    VariablesError,
)
from apteco.session import (
    NOT_ASSIGNED,
    InitializeTablesAlgorithm,
    InitializeVariablesAlgorithm,
    Session,
    SimpleLoginAlgorithm,
    User,
    _get_password,
    login,
    login_with_password,
)
from apteco.variables import (
    SelectorVariable,
    NumericVariable,
    TextVariable,
    ArrayVariable,
    FlagArrayVariable,
    DateVariable,
    DateTimeVariable,
    ReferenceVariable,
)


@pytest.fixture()
def patch_unpack_credentials(mocker):
    return mocker.patch.object(apteco.session.Session, "_unpack_credentials")


@pytest.fixture()
def patch_create_client(mocker):
    return mocker.patch.object(apteco.session.Session, "_create_client")


@pytest.fixture()
def patch_fetch_system_info(mocker):
    return mocker.patch.object(apteco.session.Session, "_fetch_system_info")


@pytest.fixture()
def fake_tables_with_master_table(mocker):
    fake = mocker.MagicMock()
    fake.__getitem__.return_value = "fake master table"
    return fake


@pytest.fixture()
def patch_initialize_tables_algo(mocker):
    fake = mocker.Mock()
    fake.run.return_value = ["fake tables no vars", "fake master table name"]
    return mocker.patch("apteco.session.InitializeTablesAlgorithm", return_value=fake)


@pytest.fixture()
def patch_initialize_variables_algo(mocker):
    fake = mocker.Mock()
    fake.run.return_value = ["fake variables", "fake tables"]
    return mocker.patch(
        "apteco.session.InitializeVariablesAlgorithm", return_value=fake
    )


@pytest.fixture()
def patch_tables_accessor(mocker, fake_tables_with_master_table):
    return mocker.patch(
        "apteco.session.TablesAccessor", return_value=fake_tables_with_master_table
    )


@pytest.fixture()
def patch_variables_accessor(mocker):
    return mocker.patch(
        "apteco.session.VariablesAccessor", return_value="fake variables accessor"
    )


@pytest.fixture()
def fake_credentials_with_attrs(mocker):
    return mocker.Mock(
        base_url="baseless assumptions",
        data_view="a room with a view",
        session_id="0246813579",
        access_token="token of my gratitude",
        user="use, er, something else",
    )


@pytest.fixture()
def fake_user_with_asdict(mocker):
    fake_user = mocker.Mock()
    fake_user._asdict.return_value = {"username": "user-per to the throne"}
    return fake_user


@pytest.fixture()
def fake_client(mocker):
    return mocker.Mock()


@pytest.fixture()
def patch_client(mocker, fake_client):
    return mocker.patch("apteco_api.ApiClient", return_value=fake_client)


@pytest.fixture()
def fake_config(mocker):
    return mocker.Mock()


@pytest.fixture()
def patch_config(mocker, fake_config):
    return mocker.patch.object(aa, "Configuration", return_value=fake_config)


@pytest.fixture()
def fake_session_with_attrs(mocker, fake_user_with_asdict):
    return mocker.Mock(
        base_url="baseless assumptions",
        data_view="a room with a view",
        session_id="0246813579",
        access_token="token of my gratitude",
        user=fake_user_with_asdict,
        system="solar system",
    )


@pytest.fixture()
def serialized_session():
    return {
        "base_url": "baseless assumptions",
        "data_view": "a room with a view",
        "session_id": "0246813579",
        "access_token": "token of my gratitude",
        "user": {"username": "user-per to the throne"},
        "system": "solar system",
    }


@pytest.fixture()
def patch_credentials(mocker):
    return mocker.patch.object(
        apteco.session, "Credentials", return_value="here are your creds"
    )


@pytest.fixture()
def patch_user_from_dict(mocker):
    return mocker.patch.object(
        apteco.session.User, "_from_dict", return_value="user your skill and judgement"
    )


@pytest.fixture()
def patch_user_raise_type_error_missing_surname(mocker):
    return mocker.patch.object(
        apteco.session,
        "User",
        side_effect=TypeError(
            "__new__() missing 1 required positional argument: 'surname'"
        ),
    )


@pytest.fixture()
def fake_session_empty(mocker):
    return mocker.Mock()


@pytest.fixture()
def patch_session(mocker, fake_session_empty):
    return mocker.patch.object(
        apteco.session, "Session", return_value=fake_session_empty
    )


@pytest.fixture()
def fake_session_with_to_dict(mocker):
    fake_session = mocker.Mock()
    fake_session._to_dict.return_value = "I'm a session dictionary"
    return fake_session


@pytest.fixture()
def patch_json_dumps(mocker):
    return mocker.patch.object(json, "dumps", return_value="Jason and the Argonauts")


@pytest.fixture()
def patch_json_loads(mocker):
    return mocker.patch.object(json, "loads", return_value="Loads of Jason")


@pytest.fixture()
def patch_session_from_dict(mocker):
    return mocker.patch.object(
        apteco.session.Session, "_from_dict", return_value="Court of Session"
    )


@pytest.fixture()
def patch_json_loads_raise_json_decode_error(mocker):
    doc = mocker.Mock()
    doc.count.return_value = 17
    doc.rfind.return_value = 23
    pos = 29
    return mocker.patch.object(
        json, "loads", side_effect=JSONDecodeError("This was not proper JSON", doc, pos)
    )


def test_create_session_with_credentials(
    fake_credentials_with_attrs,
    fake_tables_with_master_table,
    patch_fetch_system_info,
    patch_initialize_variables_algo,
    patch_initialize_tables_algo,
    patch_tables_accessor,
    patch_variables_accessor,
):
    session_example = Session(fake_credentials_with_attrs, "solar system")
    assert session_example.system == "solar system"
    assert session_example.variables == "fake variables accessor"
    assert session_example.tables is fake_tables_with_master_table
    assert session_example.master_table == "fake master table"
    patch_fetch_system_info.assert_called_once_with()
    patch_initialize_tables_algo.assert_called_once_with(session_example)
    patch_initialize_variables_algo.assert_called_once_with(
        session_example, "fake tables no vars"
    )
    patch_tables_accessor.assert_called_once_with("fake tables")
    patch_variables_accessor.assert_called_once_with("fake variables")
    assert session_example.base_url == "baseless assumptions"
    assert session_example.data_view == "a room with a view"
    assert session_example.session_id == "0246813579"
    assert session_example.access_token == "token of my gratitude"
    assert session_example.user == "use, er, something else"
    assert session_example._config.host == "baseless assumptions"
    assert session_example._config.api_key == {"Authorization": "token of my gratitude"}
    assert session_example._config.api_key_prefix == {"Authorization": "Bearer"}
    assert session_example.api_client.configuration is session_example._config


class TestSession:
    def test_session_init(
        self,
        fake_credentials_with_attrs,
        patch_unpack_credentials,
        patch_create_client,
        patch_fetch_system_info,
        fake_tables_with_master_table,
        patch_initialize_tables_algo,
        patch_initialize_variables_algo,
        patch_tables_accessor,
        patch_variables_accessor,
    ):
        session_example = Session(fake_credentials_with_attrs, "solar system")
        patch_unpack_credentials.assert_called_once_with(fake_credentials_with_attrs)
        patch_create_client.assert_called_once_with()
        assert session_example.system == "solar system"
        patch_fetch_system_info.assert_called_once_with()
        patch_initialize_tables_algo.assert_called_once_with(session_example)
        patch_initialize_variables_algo.assert_called_once_with(
            session_example, "fake tables no vars"
        )
        patch_tables_accessor.assert_called_once_with("fake tables")
        patch_variables_accessor.assert_called_once_with("fake variables")
        assert session_example.tables is fake_tables_with_master_table
        assert session_example.variables == "fake variables accessor"
        assert session_example.master_table == "fake master table"

    def test_unpack_credentials(self, mocker, fake_credentials_with_attrs):
        session_example = mocker.Mock()
        Session._unpack_credentials(session_example, fake_credentials_with_attrs)
        assert session_example.base_url == "baseless assumptions"
        assert session_example.data_view == "a room with a view"
        assert session_example.session_id == "0246813579"
        assert session_example.access_token == "token of my gratitude"
        assert session_example.user == "use, er, something else"

    def test_create_client(
        self, mocker, fake_config, patch_config, fake_client, patch_client
    ):
        session_example = mocker.Mock(
            base_url="back to base", access_token="token gesture"
        )
        Session._create_client(session_example)
        patch_config.assert_called_once_with()
        assert fake_config.host == "back to base"
        assert fake_config.api_key == {"Authorization": "token gesture"}
        assert fake_config.api_key_prefix == {"Authorization": "Bearer"}
        assert session_example._config == fake_config
        patch_client.assert_called_once_with(configuration=fake_config)
        assert session_example.api_client == fake_client

    def test_fetch_system_info(self, mocker, fake_session_with_client):
        fake_faststats_system_response = mocker.Mock(
            view_name="rear view mirror",
            description="wasn't in the job description",
            fast_stats_build_date="best-before date",
        )
        fake_faststats_system_response.name = "ecosystem"
        fake_get_system = mocker.Mock(return_value=fake_faststats_system_response)
        fake_systems_controller = mocker.Mock(
            fast_stats_systems_get_fast_stats_system=fake_get_system
        )
        patch_aa_faststats_systems_api = mocker.patch(
            "apteco.session.aa.FastStatsSystemsApi",
            return_value=fake_systems_controller,
        )
        patch_faststats_system = mocker.patch(
            "apteco.session.FastStatsSystem", return_value="Here's your FS system info."
        )
        Session._fetch_system_info(fake_session_with_client)
        patch_aa_faststats_systems_api.assert_called_once_with(
            "API client for the session"
        )
        fake_get_system.assert_called_once_with(
            "dataView for the session", "system for the session"
        )
        patch_faststats_system.assert_called_once_with(
            name="ecosystem",
            description="wasn't in the job description",
            build_date="best-before date",
            view_name="rear view mirror",
        )
        assert fake_session_with_client.system_info == "Here's your FS system info."

    def test_to_dict(
        self, fake_session_with_attrs, serialized_session, fake_user_with_asdict
    ):
        dict_example = Session._to_dict(fake_session_with_attrs)
        assert dict_example == serialized_session
        fake_user_with_asdict._asdict.assert_called_once_with()

    def test_from_dict(
        self,
        serialized_session,
        patch_credentials,
        patch_user,
        patch_session,
        fake_session_empty,
    ):
        result = Session._from_dict(serialized_session)
        patch_user.assert_called_once_with(username="user-per to the throne")
        patch_credentials.assert_called_once_with(
            "baseless assumptions",
            "a room with a view",
            "0246813579",
            "token of my gratitude",
            "you created the user",
        )
        patch_session.assert_called_once_with("here are your creds", "solar system")
        assert result is fake_session_empty

    def test_from_dict_with_bad_creds_dict(self, serialized_session, patch_credentials):
        serialized_session_no_session_id = dict(serialized_session)
        del serialized_session_no_session_id["session_id"]
        with pytest.raises(DeserializeError) as exc_info:
            Session._from_dict(serialized_session_no_session_id)
        exception_msg = exc_info.value.args[0]
        assert exception_msg == (
            "Data missing from 'Session' object: no 'session_id' found."
        )

    def test_from_dict_with_bad_user_dict(
        self,
        serialized_session,
        patch_credentials,
        patch_user_raise_type_error_missing_surname,
    ):
        with pytest.raises(DeserializeError) as excinfo:
            Session._from_dict(serialized_session)
        exception_msg = excinfo.value.args[0]
        assert exception_msg == (
            "The following parameter(s) were missing from 'User' object: 'surname'"
        )

    def test_serialize(self, fake_session_with_to_dict, patch_json_dumps):
        result = Session.serialize(fake_session_with_to_dict)
        patch_json_dumps.assert_called_once_with("I'm a session dictionary")
        assert result == "Jason and the Argonauts"

    def test_deserialize(self, patch_json_loads, patch_session_from_dict):
        result = Session.deserialize("cereal eyes-d session")
        patch_json_loads.assert_called_once_with("cereal eyes-d session")
        patch_session_from_dict.assert_called_once_with("Loads of Jason")
        assert result == "Court of Session"

    def test_deserialize_with_bad_json(self, patch_json_loads_raise_json_decode_error):
        with pytest.raises(DeserializeError) as excinfo:
            Session.deserialize("badly serialized session")
        exception_msg = excinfo.value.args[0]
        patch_json_loads_raise_json_decode_error.assert_called_once_with(
            "badly serialized session"
        )
        assert exception_msg == "The given input could not be deserialized."


@pytest.fixture()
def fake_user_with_attrs(mocker):
    return mocker.Mock(
        username="ewes urn aim",
        first_name="thirst for knowledge",
        surname="Sir Name of Spamalot",
        email_address="he male a trousers",
    )


@pytest.fixture()
def serialized_user():
    return {
        "username": "ewes urn aim",
        "first_name": "thirst for knowledge",
        "surname": "Sir Name of Spamalot",
        "email_address": "he male a trousers",
    }


@pytest.fixture()
def patch_user(mocker):
    return mocker.patch("apteco.session.User", return_value="you created the user")


class TestUser:
    def test_user_init(self):
        user_example = User("JDoe", "Jane", "Doe", "jane.doe@example.com")
        assert user_example.username == "JDoe"
        assert user_example.first_name == "Jane"
        assert user_example.surname == "Doe"
        assert user_example.email_address == "jane.doe@example.com"

    def test_user_asdict(self, fake_user_with_attrs, serialized_user):
        user_example = User(
            "ewes urn aim",
            "thirst for knowledge",
            "Sir Name of Spamalot",
            "he male a trousers",
        )
        dict_example = User._asdict(user_example)
        assert dict(dict_example) == serialized_user


class TestCredentials:
    def test_credentials_init(self, mocker):
        fake_user = mocker.Mock()
        credentials_example = apteco.session.Credentials(
            "https://marketing.example.com/OrbitAPI/",
            "room_with_a_view",
            "31415926",
            "e.g.123abc987zyx",
            fake_user,
        )
        assert credentials_example.base_url == "https://marketing.example.com/OrbitAPI/"
        assert credentials_example.data_view == "room_with_a_view"
        assert credentials_example.session_id == "31415926"
        assert credentials_example.access_token == "e.g.123abc987zyx"
        assert credentials_example.user is fake_user


@pytest.fixture()
def patch_get_password(mocker):
    return mocker.patch.object(
        apteco.session, "_get_password", return_value="something very secret"
    )


@pytest.fixture()
def patch_login_with_password(mocker):
    return mocker.patch.object(
        apteco.session, "login_with_password", return_value="Here is your session!"
    )


@pytest.fixture()
def fake_simple_login_algo(mocker):
    fake = mocker.Mock()
    fake.run.return_value = "fake credentials"
    return fake


@pytest.fixture()
def patch_simple_login_algo(mocker, fake_simple_login_algo):
    return mocker.patch(
        "apteco.session.SimpleLoginAlgorithm", return_value=fake_simple_login_algo
    )


@pytest.fixture()
def patch_getpass_getpass(mocker):
    return mocker.patch("getpass.getpass", return_value="password typed into console")


@pytest.fixture()
def patch_getpass_getpass_raise_warning(mocker):
    return mocker.patch("getpass.getpass", side_effect=getpass.GetPassWarning)


@pytest.fixture()
def patch_apteco_logo(mocker):
    return mocker.patch("apteco.session.APTECO_LOGO", new="here's the logo")


@pytest.fixture()
def patch_pysimplegui_popupgettext(mocker):
    return mocker.patch(
        "PySimpleGUI.PopupGetText", return_value="password typed into popup box"
    )


class TestLogin:
    """Tests for login functions and related functions."""

    def test_login(self, patch_get_password, patch_login_with_password):
        session = login(
            "https://marketing.example.com/AptecoAPI/",
            "a_room_with_a_view",
            "systemic_change",
            "JDoe",
        )
        assert session == "Here is your session!"
        patch_get_password.assert_called_once_with()
        patch_login_with_password.assert_called_once_with(
            "https://marketing.example.com/AptecoAPI/",
            "a_room_with_a_view",
            "systemic_change",
            "JDoe",
            password="something very secret",
        )

    def test_login_with_password(
        self,
        patch_simple_login_algo,
        patch_session,
        fake_simple_login_algo,
        fake_session_empty,
    ):
        session = login_with_password(
            "https://marketing.example.com/AptecoAPI/",
            "a_room_with_a_view",
            "systemic_change",
            "JDoe",
            "my s3cr3t pa55w0rd",
        )
        assert session is fake_session_empty
        patch_simple_login_algo.assert_called_once_with(
            "https://marketing.example.com/AptecoAPI/", "a_room_with_a_view"
        )
        fake_simple_login_algo.run.assert_called_once_with("JDoe", "my s3cr3t pa55w0rd")
        patch_session.assert_called_once_with("fake credentials", "systemic_change")

    def test_get_password(self, patch_getpass_getpass):
        result = _get_password("This should appear on the console")
        assert result == "password typed into console"
        patch_getpass_getpass.assert_called_once_with(
            "This should appear on the console"
        )

    def test_get_password_from_popup(
        self,
        patch_getpass_getpass_raise_warning,
        patch_pysimplegui_popupgettext,
        patch_apteco_logo,
    ):
        result = _get_password("A different prompt from default")
        assert result == "password typed into popup box"
        patch_getpass_getpass_raise_warning.assert_called_once_with(
            "A different prompt from default"
        )
        patch_pysimplegui_popupgettext.assert_called_once_with(
            "A different prompt from default",
            password_char="*",
            title="Apteco API",
            button_color=("#ffffff", "#004964"),
            icon="here's the logo",
        )


@pytest.fixture()
def fake_create_unauthorized_client(mocker):
    return mocker.Mock()


@pytest.fixture()
def fake_simple_login(mocker):
    return mocker.Mock()


@pytest.fixture()
def fake_create_credentials(mocker):
    return mocker.Mock()


@pytest.fixture()
def fake_simple_login_algo_with_credentials(
    mocker, fake_create_unauthorized_client, fake_simple_login, fake_create_credentials
):
    return mocker.Mock(
        _create_unauthorized_client=fake_create_unauthorized_client,
        _simple_login=fake_simple_login,
        _create_credentials=fake_create_credentials,
        credentials="I made you some credentials!",
    )


@pytest.fixture()
def fake_simple_login_algo_with_base_url(mocker):
    return mocker.Mock(base_url="basic instinct")


@pytest.fixture()
def fake_config_from_aa_configuration(mocker):
    return mocker.Mock()


@pytest.fixture()
def patch_aa_configuration(mocker, fake_config_from_aa_configuration):
    return mocker.patch(
        "apteco.session.aa.Configuration",
        return_value=fake_config_from_aa_configuration,
    )


@pytest.fixture()
def patch_aa_api_client(mocker):
    return mocker.patch(
        "apteco.session.aa.ApiClient", return_value="you've made the API client"
    )


@pytest.fixture()
def fake_aa_user_with_attrs(mocker):
    return mocker.Mock(
        username="my_fake_username1",
        firstname="probably John",
        surname="probably Smith",
        email_address="firstname.surname@company.biz",
    )


@pytest.fixture()
def fake_login_response(mocker, fake_aa_user_with_attrs):
    return mocker.Mock(
        session_id="Bourne Identity",
        access_token="access all areas",
        user=fake_aa_user_with_attrs,
    )


@pytest.fixture()
def fake_sessions_controller(mocker, fake_login_response):
    fake = mocker.Mock()
    fake.sessions_create_session_simple.return_value = fake_login_response
    return fake


@pytest.fixture()
def fake_simple_login_algo_with_bu_dv_ac(mocker):
    """Mock with base_url, data_view and api_client attributes."""
    return mocker.Mock(
        base_url="basic instinct",
        data_view="a point of view",
        api_client="in a meeting with a client",
    )


@pytest.fixture()
def patch_aa_sessions_api(mocker, fake_sessions_controller):
    return mocker.patch(
        "apteco.session.aa.SessionsApi", return_value=fake_sessions_controller
    )


@pytest.fixture()
def fake_simple_login_algo_with_attrs(mocker):
    return mocker.Mock(
        base_url="buttery biscuit base",
        data_view="don't view my data without permission!",
        session_id="say shun eyed ee",
        access_token="excess toucan",
        user="ewe's hair",
    )


class TestSimpleLoginAlgorithm:
    def test_simple_login_algorithm_init(self):
        simple_login_algo_example = SimpleLoginAlgorithm(
            "https://api-here.example.com", "scenic viewpoint"
        )
        assert simple_login_algo_example.base_url == "https://api-here.example.com"
        assert simple_login_algo_example.data_view == "scenic viewpoint"

    def test_run(
        self,
        fake_simple_login_algo_with_credentials,
        fake_create_unauthorized_client,
        fake_simple_login,
        fake_create_credentials,
    ):
        result = SimpleLoginAlgorithm.run(
            fake_simple_login_algo_with_credentials, "you, sir!", "pa55w0rd 4 me"
        )
        assert result == "I made you some credentials!"
        fake_create_unauthorized_client.assert_called_once_with()
        fake_simple_login.assert_called_once_with("you, sir!", "pa55w0rd 4 me")
        fake_create_credentials.assert_called_once_with()

    def test_create_unauthorized_client(
        self,
        fake_simple_login_algo_with_base_url,
        patch_aa_configuration,
        fake_config_from_aa_configuration,
        patch_aa_api_client,
    ):
        SimpleLoginAlgorithm._create_unauthorized_client(
            fake_simple_login_algo_with_base_url
        )
        patch_aa_configuration.assert_called_once_with()
        assert fake_config_from_aa_configuration.host == "basic instinct"
        assert (
            fake_simple_login_algo_with_base_url._config
            is fake_config_from_aa_configuration
        )
        patch_aa_api_client.assert_called_once_with(
            configuration=fake_config_from_aa_configuration
        )
        assert (
            fake_simple_login_algo_with_base_url.api_client
            == "you've made the API client"
        )

    def test_simple_login(
        self,
        fake_simple_login_algo_with_bu_dv_ac,
        patch_aa_sessions_api,
        fake_sessions_controller,
        patch_user,
    ):
        SimpleLoginAlgorithm._simple_login(
            fake_simple_login_algo_with_bu_dv_ac, "yews are trees", "qwerty123"
        )
        patch_aa_sessions_api.assert_called_once_with("in a meeting with a client")
        fake_sessions_controller.sessions_create_session_simple.assert_called_once_with(
            "a point of view", "yews are trees", "qwerty123"
        )
        assert fake_simple_login_algo_with_bu_dv_ac.session_id == "Bourne Identity"
        assert fake_simple_login_algo_with_bu_dv_ac.access_token == "access all areas"
        assert fake_simple_login_algo_with_bu_dv_ac.user == "you created the user"
        patch_user.assert_called_once_with(
            username="my_fake_username1",
            first_name="probably John",
            surname="probably Smith",
            email_address="firstname.surname@company.biz",
        )

    def test_create_credentials(
        self, fake_simple_login_algo_with_attrs, patch_credentials
    ):
        SimpleLoginAlgorithm._create_credentials(fake_simple_login_algo_with_attrs)
        patch_credentials.assert_called_once_with(
            "buttery biscuit base",
            "don't view my data without permission!",
            "say shun eyed ee",
            "excess toucan",
            "ewe's hair",
        )
        assert fake_simple_login_algo_with_attrs.credentials == "here are your creds"


@pytest.fixture()
def fake_session_with_client(mocker):
    return mocker.Mock(
        data_view="dataView for the session",
        system="system for the session",
        api_client="API client for the session",
    )


@pytest.fixture()
def fake_raw_tables(mocker):
    fake = [
        mocker.Mock(parent_table=""),
        mocker.Mock(parent_table="Customers"),
        mocker.Mock(parent_table="Purchases"),
        mocker.Mock(parent_table="Purchases"),
        mocker.Mock(parent_table="Customers"),
        mocker.Mock(parent_table="Web visits"),
        mocker.Mock(parent_table="Pages viewed"),
        mocker.Mock(parent_table="Customers"),
        mocker.Mock(parent_table="Customers"),
    ]
    fake[0].name = "Customers"
    fake[1].name = "Purchases"
    fake[2].name = "Items"
    fake[3].name = "Vouchers"
    fake[4].name = "Web visits"
    fake[5].name = "Pages viewed"
    fake[6].name = "Links clicked"
    fake[7].name = "Rentals"
    fake[8].name = "Communications"
    return fake


@pytest.fixture()
def correct_children_lookup():
    return {
        "": ["Customers"],
        "Customers": ["Purchases", "Web visits", "Rentals", "Communications"],
        "Purchases": ["Items", "Vouchers"],
        "Web visits": ["Pages viewed"],
        "Pages viewed": ["Links clicked"],
    }


@pytest.fixture()
def fake_tables(mocker):
    fake = {
        "Customers": mocker.Mock(parent_name=""),
        "Purchases": mocker.Mock(parent_name="Customers"),
        "Items": mocker.Mock(parent_name="Purchases"),
        "Vouchers": mocker.Mock(parent_name="Purchases"),
        "Web visits": mocker.Mock(parent_name="Customers"),
        "Pages viewed": mocker.Mock(parent_name="Web visits"),
        "Links clicked": mocker.Mock(parent_name="Pages viewed"),
        "Rentals": mocker.Mock(parent_name="Customers"),
        "Communications": mocker.Mock(parent_name="Customers"),
    }
    fake["Customers"].name = "Customers"
    fake["Purchases"].name = "Purchases"
    fake["Items"].name = "Items"
    fake["Vouchers"].name = "Vouchers"
    fake["Web visits"].name = "Web visits"
    fake["Pages viewed"].name = "Pages viewed"
    fake["Links clicked"].name = "Links clicked"
    fake["Rentals"].name = "Rentals"
    fake["Communications"].name = "Communications"
    return fake


@pytest.fixture()
def correct_tables(fake_tables, correct_children_lookup):
    tables = dict(fake_tables)

    tables["Customers"].parent = None
    tables["Purchases"].parent = tables["Customers"]
    tables["Items"].parent = tables["Purchases"]
    tables["Vouchers"].parent = tables["Purchases"]
    tables["Web visits"].parent = tables["Customers"]
    tables["Pages viewed"].parent = tables["Web visits"]
    tables["Links clicked"].parent = tables["Pages viewed"]
    tables["Rentals"].parent = tables["Customers"]
    tables["Communications"].parent = "Communications"

    tables["Customers"].children = [
        "Purchases",
        "Web visits",
        "Rentals",
        "Communications",
    ]
    tables["Purchases"].children = ["Items", "Vouchers"]
    tables["Items"].children = []
    tables["Vouchers"].children = []
    tables["Web visits"].children = ["Pages viewed"]
    tables["Pages viewed"].children = ["Links clicked"]
    tables["Links clicked"].children = []
    tables["Rentals"].children = []
    tables["Communications"].children = []

    return tables


class TestInitializeTablesAlgorithm:
    def test_initialize_tables_algo_init(self, fake_session_with_client):
        initialize_tables_algo_example = InitializeTablesAlgorithm(
            fake_session_with_client
        )
        assert initialize_tables_algo_example.data_view == "dataView for the session"
        assert initialize_tables_algo_example.system == "system for the session"
        assert initialize_tables_algo_example.api_client == "API client for the session"
        assert initialize_tables_algo_example.session is fake_session_with_client

    def test_initialize_tables_algo_run(self, mocker):
        fake_get_raw_tables = mocker.Mock()
        fake_identify_children = mocker.Mock()
        fake_create_tables = mocker.Mock()
        fake_assign_parent_and_children = mocker.Mock()
        fake_find_master_table = mocker.Mock()
        fake_assign_ancestors_and_descendants = mocker.Mock(
            return_value="forest of tables"
        )
        fake_check_all_tables_in_tree = mocker.Mock()
        fake_check_all_relations_assigned = mocker.Mock()
        fake_master_table = mocker.Mock()
        fake_master_table.configure_mock(name="jack of all tables master of none")
        fake_initialize_tables_algo = mocker.Mock(
            master_table=fake_master_table,
            tables_lookup="the tables have turned",
            _get_raw_tables=fake_get_raw_tables,
            _identify_children=fake_identify_children,
            _create_tables=fake_create_tables,
            _assign_parent_and_children=fake_assign_parent_and_children,
            _find_master_table=fake_find_master_table,
            _assign_ancestors_and_descendants=fake_assign_ancestors_and_descendants,
            _check_all_tables_in_tree=fake_check_all_tables_in_tree,
            _check_all_relations_assigned=fake_check_all_relations_assigned,
        )
        result = InitializeTablesAlgorithm.run(fake_initialize_tables_algo)
        fake_get_raw_tables.assert_called_once_with()
        fake_identify_children.assert_called_once_with()
        fake_create_tables.assert_called_once_with()
        fake_assign_parent_and_children.assert_called_once_with()
        fake_find_master_table.assert_called_once_with()
        fake_assign_ancestors_and_descendants.assert_called_once_with(
            fake_master_table, []
        )
        fake_check_all_tables_in_tree.assert_called_once_with("forest of tables")
        fake_check_all_relations_assigned.assert_called_once_with()
        assert result == ("the tables have turned", "jack of all tables master of none")

    def test_get_raw_tables(self, mocker):
        fake_initialize_tables_algo = mocker.Mock(
            api_client="a potential client",
            data_view="data centre",
            system="System Of A Down",
        )
        table1 = mocker.Mock()
        table2 = mocker.Mock()
        table3 = mocker.Mock()
        fake_tables_response = mocker.Mock(list=[table1, table2, table3])
        fake_get_tables = mocker.Mock(return_value=fake_tables_response)
        fake_systems_controller = mocker.Mock(
            fast_stats_systems_get_fast_stats_tables=fake_get_tables
        )
        patch_aa_faststats_systems_api = mocker.patch(
            "apteco.session.aa.FastStatsSystemsApi",
            return_value=fake_systems_controller,
        )
        InitializeTablesAlgorithm._get_raw_tables(fake_initialize_tables_algo)
        patch_aa_faststats_systems_api.assert_called_once_with("a potential client")
        fake_get_tables.assert_called_once_with(
            "data centre", "System Of A Down", count=1000
        )
        ctrc = fake_initialize_tables_algo._check_table_results_consistency
        ctrc.assert_called_once_with(fake_tables_response)
        assert fake_initialize_tables_algo.raw_tables == [table1, table2, table3]

    def test_check_table_results_consistency(self, mocker):
        fake_results = mocker.Mock(count=3, list=[1, 2, 3])
        InitializeTablesAlgorithm._check_table_results_consistency(fake_results)

    def test_check_table_results_consistency_with_wrong_count(self, mocker):
        fake_results = mocker.Mock(count=2, list=[1, 2, 3])
        with pytest.raises(ApiResultsError) as exc_info:
            InitializeTablesAlgorithm._check_table_results_consistency(fake_results)
        exception_msg = exc_info.value.args[0]
        assert exception_msg == "API stated 2 tables were returned but 3 were found."

    def test_identify_children(self, mocker, fake_raw_tables, correct_children_lookup):
        fake_initialize_tables_algo = mocker.Mock(raw_tables=fake_raw_tables)
        InitializeTablesAlgorithm._identify_children(fake_initialize_tables_algo)
        assert fake_initialize_tables_algo.children_lookup == correct_children_lookup
        assert fake_initialize_tables_algo.children_lookup.default_factory is list

    def test_create_tables(self, mocker, fake_raw_tables):
        raw_table_attrs = [
            "singular_display_name",
            "plural_display_name",
            "is_default_table",
            "is_people_table",
            "total_records",
            "child_relationship_name",
            "parent_relationship_name",
            "has_child_tables",
        ]
        attrs_list1 = ["customer", "customers", True, True, 123, "has", "having", True]
        attrs_list2 = [
            "purchase",
            "purchases",
            False,
            False,
            456,
            "has made",
            "having been made",
            True,
        ]
        attrs_list3 = [
            "item",
            "items",
            False,
            False,
            789,
            "includes",
            "including",
            False,
        ]
        attrs1 = dict(zip(raw_table_attrs, attrs_list1))
        attrs2 = dict(zip(raw_table_attrs, attrs_list2))
        attrs3 = dict(zip(raw_table_attrs, attrs_list3))
        fake_raw_tables_with_all_attrs = [
            fake_raw_tables[0],
            fake_raw_tables[1],
            fake_raw_tables[2],
        ]
        fake_raw_tables_with_all_attrs[0].configure_mock(**attrs1)
        fake_raw_tables_with_all_attrs[1].configure_mock(**attrs2)
        fake_raw_tables_with_all_attrs[2].configure_mock(**attrs3)
        patch_table = mocker.patch(
            "apteco.session.Table", side_effect=[f"Table{i}" for i in (1, 2, 3)]
        )
        fake_initialize_tables_algo = mocker.Mock(
            raw_tables=fake_raw_tables_with_all_attrs, session="jam session"
        )
        InitializeTablesAlgorithm._create_tables(fake_initialize_tables_algo)
        correct_tables = {
            "Customers": "Table1",
            "Purchases": "Table2",
            "Items": "Table3",
        }
        args1 = ["Customers"] + attrs_list1 + [""] + [NOT_ASSIGNED] * 5
        args2 = ["Purchases"] + attrs_list2 + ["Customers"] + [NOT_ASSIGNED] * 5
        args3 = ["Items"] + attrs_list3 + ["Purchases"] + [NOT_ASSIGNED] * 5
        table_calls = [
            mocker.call(*args1, session="jam session"),
            mocker.call(*args2, session="jam session"),
            mocker.call(*args3, session="jam session"),
        ]
        assert fake_initialize_tables_algo.tables_lookup == correct_tables
        patch_table.assert_has_calls(table_calls)

    def test_assign_parent_and_children(
        self, mocker, fake_tables, correct_children_lookup, correct_tables
    ):
        patch_cctc = mocker.patch(
            "apteco.session.InitializeTablesAlgorithm._check_child_tables_consistency"
        )
        fake_children_lookup = mocker.MagicMock(default_factory="This should change")

        def getitem_helper(x):
            return correct_children_lookup.get(x, [])

        fake_children_lookup.__getitem__.side_effect = getitem_helper
        fake_initialize_tables_algo = mocker.Mock(
            tables_lookup=fake_tables,
            children_lookup=fake_children_lookup,
            _check_child_tables_consistency=patch_cctc,
        )
        InitializeTablesAlgorithm._assign_parent_and_children(
            fake_initialize_tables_algo
        )
        patch_cctc.assert_has_calls([mocker.call(t) for t in correct_tables.values()])
        assert fake_initialize_tables_algo.tables_lookup == correct_tables
        assert fake_children_lookup.default_factory is None

    def test_check_child_tables_consistency(self, mocker):
        table_has_children = mocker.Mock(has_children=True, children=["Ben", "Emma"])
        table_has_children.name = "Ross"
        table_has_no_children = mocker.Mock(has_children=False, children=[])
        table_has_no_children.name = "Joey"
        table_should_have_children = mocker.Mock(has_children=True, children=[])
        table_should_have_children.name = "Monica"
        table_shouldnt_have_children = mocker.Mock(
            has_children=False, children=["Frank Jr. Jr.", "Leslie Jr.", "Chandler"]
        )
        table_shouldnt_have_children.name = "Phoebe"

        InitializeTablesAlgorithm._check_child_tables_consistency(table_has_children)
        InitializeTablesAlgorithm._check_child_tables_consistency(table_has_no_children)
        with pytest.raises(TablesError) as exc_info:
            InitializeTablesAlgorithm._check_child_tables_consistency(
                table_should_have_children
            )
        exception_msg = exc_info.value.args[0]
        assert exception_msg == (
            "API stated 'Monica' table has child tables but none were found."
        )
        with pytest.raises(TablesError) as exc_info:
            InitializeTablesAlgorithm._check_child_tables_consistency(
                table_shouldnt_have_children
            )
        exception_msg = exc_info.value.args[0]
        assert exception_msg == (
            "API stated 'Phoebe' table has no child tables but 3 were found."
        )

    def test_find_master_table(self, mocker):
        fake_initialize_tables_algo = mocker.Mock(
            children_lookup={"": ["Master of the Universe"]},
            tables_lookup={"Master of the Universe": "My master table"},
        )
        InitializeTablesAlgorithm._find_master_table(fake_initialize_tables_algo)
        assert fake_initialize_tables_algo.master_table == "My master table"

    find_master_table_bad_cases_parameters = [
        # first KeyError path
        pytest.param(
            {"key for master is wrong": ["Masterfully done"]},
            {"Masterfully done": "But you won't be able to fetch me :("},
            "No master table found.",
            id="no master key",
        ),
        # ValueError path
        pytest.param(
            {"": []},
            {"Quartermaster": "But I'm not in the list :/"},
            "Found 0 master tables, there should be 1.",
            id="no master tables",
        ),
        # ValueError path
        pytest.param(
            {"": ["Master of Arts", "Master of Science"]},
            {
                "Master of Arts": "There are two of us :'(",
                "Master of Science": "But we can't both be master :'(",
            },
            "Found 2 master tables, there should be 1.",
            id="multiple master tables",
        ),
        # second KeyError path
        pytest.param(
            {"": ["Mastermind"]},
            {"Should be Master": "But my key here is wrong! >:("},
            "The master table 'Mastermind' could not be found.",
            id="master table named but missing",
        ),
    ]

    @pytest.mark.parametrize(
        "children_lookup, tables_lookup, expected_exc_msg",
        find_master_table_bad_cases_parameters,
    )
    def test_find_master_table_bad_cases(
        self, children_lookup, tables_lookup, expected_exc_msg, mocker
    ):
        fake_initialize_tables_algo = mocker.Mock(
            children_lookup=children_lookup, tables_lookup=tables_lookup
        )
        with pytest.raises(TablesError) as exc_info:
            InitializeTablesAlgorithm._find_master_table(fake_initialize_tables_algo)
        exception_msg = exc_info.value.args[0]
        assert exception_msg == expected_exc_msg

    def test_assign_ancestors_and_descendants(self, mocker):
        ancestor1 = mocker.Mock(description="Customers")
        ancestor2 = mocker.Mock(description="Households")
        child1 = mocker.Mock(description="Purchases")
        child2 = mocker.Mock(description="Web visits")
        child3 = mocker.Mock(description="Rentals")
        child4 = mocker.Mock(description="Communications")
        grandchild1a = mocker.Mock(description="Items")
        grandchild1b = mocker.Mock(description="Vouchers")
        grandchild2a = mocker.Mock(description="Pages viewed")
        fake_table = mocker.Mock(
            description="Customers", children=[child1, child2, child3, child4]
        )
        fake_initialize_tables_algo = mocker.Mock()
        fake_initialize_tables_algo._assign_ancestors_and_descendants.side_effect = [
            [child1, grandchild1a, grandchild1b],
            [child2, grandchild2a],
            [child3],
            [child4],
        ]
        result = InitializeTablesAlgorithm._assign_ancestors_and_descendants(
            fake_initialize_tables_algo, fake_table, [ancestor1, ancestor2]
        )
        table_calls = [
            mocker.call(child1, [fake_table, ancestor1, ancestor2]),
            mocker.call(child2, [fake_table, ancestor1, ancestor2]),
            mocker.call(child3, [fake_table, ancestor1, ancestor2]),
            mocker.call(child4, [fake_table, ancestor1, ancestor2]),
        ]
        fake_initialize_tables_algo._assign_ancestors_and_descendants.assert_has_calls(
            table_calls
        )
        assert result == [
            fake_table,
            child1,
            grandchild1a,
            grandchild1b,
            child2,
            grandchild2a,
            child3,
            child4,
        ]
        assert fake_table.ancestors == [ancestor1, ancestor2]
        assert fake_table.descendants == [
            child1,
            grandchild1a,
            grandchild1b,
            child2,
            grandchild2a,
            child3,
            child4,
        ]

    """
    Table tree for these tests:
    customers
        purchases
            items
            vouchers
        web visits
            pages viewed
        rentals
        communications
    """

    def test_check_all_tables_in_tree(self, mocker, fake_tables, fake_raw_tables):
        patch_counter = mocker.patch(
            "apteco.session.Counter", side_effect=["I counted my tables"] * 2
        )
        fake_initialize_tables_algo = mocker.Mock(raw_tables=fake_raw_tables)
        fake_tree_tables = fake_tables.items()
        InitializeTablesAlgorithm._check_all_tables_in_tree(
            fake_initialize_tables_algo, fake_tree_tables
        )
        patch_counter.assert_called()
        assert len(patch_counter.mock_calls) == 2

    def test_check_all_tables_in_tree_with_bad_counts(
        self, mocker, fake_tables, fake_raw_tables
    ):
        fake_diff = mocker.MagicMock()
        fake_diff.__pos__.return_value = {"Items": 3, "Customers": 1}
        fake_diff.__neg__.return_value = {
            "Web visits": -1,
            "Pages viewed": -1,
            "Communications": -2,
        }
        patch_counter = mocker.patch(
            "apteco.session.Counter",
            side_effect=["tree counts", "raw counts", fake_diff],
        )
        fake_initialize_tables_algo = mocker.Mock(raw_tables=fake_raw_tables)
        fake_tree_tables = fake_tables.items()
        with pytest.raises(TablesError) as exc_info:
            InitializeTablesAlgorithm._check_all_tables_in_tree(
                fake_initialize_tables_algo, fake_tree_tables
            )
        exception_msg = exc_info.value.args[0]
        patch_counter.assert_called()
        assert len(patch_counter.mock_calls) == 3
        fake_diff.subtract.assert_called_once_with("raw counts")
        assert exception_msg == (
            "Error constructing table tree:"
            " 2 table(s) occurred more than once in tree"
            " and 3 table(s) did not occur at all."
        )

    def test_check_all_relations_assigned(self, mocker):
        fake_initialize_tables_algo = mocker.Mock()
        fake_table1 = mocker.Mock()
        fake_table1.configure_mock(
            name="Charles",
            parent="Elizabeth",
            children=["William", "Henry"],
            ancestors=["Elizabeth", "George", "George"],
            descendants=["William", "George", "Charlotte", "Louis", "Henry", "Archie"],
        )
        fake_table2 = mocker.Mock()
        fake_table2.mocker.Mock(
            name="William",
            parent="Charles",
            children=["George", "Charlotte", "Louis"],
            ancestors=["Charles", "Elizabeth", "George", "George"],
            descendants=["George", "Charlotte", "Louis"],
        )
        fake_table3 = mocker.Mock()
        fake_table3.configure_mock(
            name="George",
            parent="William",
            children=[],
            ancestors=["William", "Charles", "Elizabeth", "George", "George"],
            descendants=[],
        )
        fake_initialize_tables_algo.tables_lookup.values.return_value = [
            fake_table1,
            fake_table2,
            fake_table3,
        ]
        InitializeTablesAlgorithm._check_all_relations_assigned(
            fake_initialize_tables_algo
        )

    def test_check_all_relations_assigned_with_missing_assignments(self, mocker):
        fake_initialize_tables_algo = mocker.Mock()
        fake_table1 = mocker.Mock()
        fake_table1.configure_mock(
            name="Ron",
            parent="Molly",
            children=["Rose", "Hugo"],
            ancestors=NOT_ASSIGNED,
            descendants=NOT_ASSIGNED,
        )
        fake_table2 = mocker.Mock()
        fake_table2.configure_mock(
            name="Tom",
            parent="Merope",
            children=NOT_ASSIGNED,
            ancestors=["Thomas", "Marvolo", "Salazar"],
            descendants=[],
        )
        fake_table3 = mocker.Mock()
        fake_table3.mocker.Mock(
            name="Narcissa",
            parent="Cygnus",
            children=["Draco"],
            ancestors=["Cygnus", "Pollux"],
            descendants=["Draco", "Scorpio"],
        )
        fake_table4 = mocker.Mock()
        fake_table4.configure_mock(
            name="Harry",
            parent="James",
            children=["James", "Albus", "Lily"],
            ancestors=["Ignotus"],
            descendants=NOT_ASSIGNED,
        )
        fake_initialize_tables_algo.tables_lookup.values.return_value = [
            fake_table1,
            fake_table2,
            fake_table3,
            fake_table4,
        ]
        with pytest.raises(TablesError) as exc_info:
            InitializeTablesAlgorithm._check_all_relations_assigned(
                fake_initialize_tables_algo
            )
        exception_msg = exc_info.value.args[0]
        assert exception_msg == (
            "Error constructing table tree:"
            "\n1 table(s) had no children assigned."
            " First example: 'Tom' table"
            "\n1 table(s) had no ancestors assigned."
            " First example: 'Ron' table"
            "\n2 table(s) had no descendants assigned."
            " First example: 'Ron' table"
        )


class TestInitializeVariablesAlgorithm:
    def test_initialize_variables_algo_init(self, mocker, fake_session_with_client):
        fake_tables_without_variables = mocker.Mock()  # Mock to avoid type complaints
        initialize_vars_algo_example = InitializeVariablesAlgorithm(
            fake_session_with_client, fake_tables_without_variables
        )
        assert initialize_vars_algo_example.data_view == "dataView for the session"
        assert initialize_vars_algo_example.system == "system for the session"
        assert initialize_vars_algo_example.api_client == "API client for the session"
        assert initialize_vars_algo_example.session is fake_session_with_client
        assert (
            initialize_vars_algo_example.tables_lookup is fake_tables_without_variables
        )

    def test_initialize_variables_algo_run(self, mocker):
        fake_tables_lookup = mocker.Mock()
        fake_tables_lookup.values.return_value = ["table an amendment"]
        fake_get_raw_variables = mocker.Mock()
        fake_create_variables = mocker.Mock()
        fake_identify_variables = mocker.Mock()
        fake_assign_variables = mocker.Mock()
        fake_check_all_variables_assigned = mocker.Mock()
        fake_initialize_vars_algo = mocker.Mock(
            variables="Wind: Variable, mainly east to northeast",
            tables_lookup=fake_tables_lookup,
            _get_raw_variables=fake_get_raw_variables,
            _create_variables=fake_create_variables,
            _identify_variables=fake_identify_variables,
            _assign_variables=fake_assign_variables,
            _check_all_variables_assigned=fake_check_all_variables_assigned,
        )
        result = InitializeVariablesAlgorithm.run(fake_initialize_vars_algo)
        fake_get_raw_variables.assert_called_once_with()
        fake_create_variables.assert_called_once_with()
        fake_identify_variables.assert_called_once_with()
        fake_assign_variables.assert_called_once_with()
        fake_check_all_variables_assigned.assert_called_once_with()
        assert result == (
            "Wind: Variable, mainly east to northeast",
            ["table an amendment"],
        )

    def test_get_raw_variables(self, mocker):
        fake_results1 = mocker.Mock(list=["var0"], offset=0, count=7, total_count=17)
        fake_results2 = mocker.Mock(list=["var7"], offset=7, count=7, total_count=17)
        fake_results3 = mocker.Mock(list=["var14"], offset=14, count=3, total_count=17)
        fake_get_variables = mocker.Mock(
            side_effect=[fake_results1, fake_results2, fake_results3]
        )
        fake_systems_controller = mocker.Mock(
            fast_stats_systems_get_fast_stats_variables=fake_get_variables
        )
        patch_aa_faststats_systems_api = mocker.patch(
            "apteco.session.aa.FastStatsSystemsApi",
            return_value=fake_systems_controller,
        )
        fake_check_variable_results_consistency = mocker.Mock()
        fake_initialize_vars_algo = mocker.Mock(
            api_client="Client Eastwood",
            data_view="Doris Day-ta",
            system="My System's Keeper",
            _check_variable_results_consistency=fake_check_variable_results_consistency,
        )
        InitializeVariablesAlgorithm._get_raw_variables(fake_initialize_vars_algo, 7)
        patch_aa_faststats_systems_api.assert_called_once_with("Client Eastwood")
        get_variables_calls = [
            mocker.call("Doris Day-ta", "My System's Keeper", count=7, offset=0),
            mocker.call("Doris Day-ta", "My System's Keeper", count=7, offset=7),
            mocker.call("Doris Day-ta", "My System's Keeper", count=7, offset=14),
        ]
        fake_get_variables.assert_has_calls(get_variables_calls)
        assert fake_initialize_vars_algo.raw_variables == ["var0", "var7", "var14"]
        fake_check_variable_results_consistency.assert_called_once_with(17)

    def test_check_variable_results_consistency(self, mocker):
        fake_initialize_vars_algo = mocker.MagicMock()
        fake_initialize_vars_algo.raw_variables.__len__.return_value = 12345
        InitializeVariablesAlgorithm._check_variable_results_consistency(
            fake_initialize_vars_algo, 12345
        )

    def test_check_variable_results_consistency_with_bad_total(self, mocker):
        fake_initialize_vars_algo = mocker.MagicMock()
        fake_initialize_vars_algo.raw_variables.__len__.return_value = 12345
        with pytest.raises(ApiResultsError) as exc_info:
            InitializeVariablesAlgorithm._check_variable_results_consistency(
                fake_initialize_vars_algo, 98765
            )
        exception_msg = exc_info.value.args[0]
        assert exception_msg == (
            "API stated there are 98765 variables in the system"
            " but 12345 were returned."
        )

    def test_create_variables(self, mocker):
        args_list = [
            "name",
            "description",
            "type",
            "folder_name",
            "is_selectable",
            "is_browsable",
            "is_exportable",
            "is_virtual",
            "selector_info",
            "numeric_info",
            "text_info",
            "reference_info",
        ]
        attrs_list0 = [
            "cuName",
            "Full Name",
            "Text",
            "Customer PII",
            True,
            False,
            False,
            False,
            "cuNameSelInfo",
            "cuNameNumInfo",
            "cuNameTextInfo",
            "cuNameRefInfo",
        ]
        attrs_list1 = [
            "trCost",
            "Cost",
            "Numeric",
            "Transaction Main",
            True,
            True,
            True,
            True,
            "trCostSelInfo",
            "trCostNumInfo",
            "trCostTextInfo",
            "trCostRefInfo",
        ]
        attrs_list2 = [
            "itCode",
            "Item Code",
            "Selector",
            "Item Data",
            True,
            True,
            True,
            False,
            "itCodeSelInfo",
            "itCodeNumInfo",
            "itCodeTextInfo",
            "itCodeRefInfo",
        ]
        attrs0 = dict(zip(args_list, attrs_list0))
        attrs1 = dict(zip(args_list, attrs_list1))
        attrs2 = dict(zip(args_list, attrs_list2))
        fake_raw_variables = [mocker.Mock() for __ in range(3)]
        fake_raw_variables[0].configure_mock(**attrs0, table_name="Customers")
        fake_raw_variables[1].configure_mock(**attrs1, table_name="Transactions")
        fake_raw_variables[2].configure_mock(**attrs2, table_name="Items")
        fake_chosen_variable_class = mocker.Mock(
            side_effect=["Created 1st var", "Created 2nd var", "Created 3rd var"]
        )
        fake_choose_variable = mocker.Mock(return_value=fake_chosen_variable_class)
        fake_tables = mocker.MagicMock()
        fake_tables.__getitem__.side_effect = [
            "Customers table",
            "Transact. table",
            "Items table",
        ]
        fake_initialize_vars_algo = mocker.Mock(
            _choose_variable=fake_choose_variable,
            tables_lookup=fake_tables,
            session="session musician",
            raw_variables=fake_raw_variables,
        )
        InitializeVariablesAlgorithm._create_variables(fake_initialize_vars_algo)
        choose_variable_calls = [
            mocker.call(fake_raw_variables[0]),
            mocker.call(fake_raw_variables[1]),
            mocker.call(fake_raw_variables[2]),
        ]
        variable_class_calls = [
            mocker.call(**attrs0, table="Customers table", session="session musician"),
            mocker.call(**attrs1, table="Transact. table", session="session musician"),
            mocker.call(**attrs2, table="Items table", session="session musician"),
        ]
        fake_choose_variable.assert_has_calls(choose_variable_calls)
        fake_chosen_variable_class.assert_has_calls(variable_class_calls)
        assert fake_initialize_vars_algo.variables == [
            "Created 1st var",
            "Created 2nd var",
            "Created 3rd var",
        ]

    def test_create_variables_with_bad_raw_variable(self, mocker, caplog):
        bad_raw_var = mocker.Mock(
            type="Numeric",
            selector_info=mocker.Mock(sub_type="Boolean", selector_type=None),
            to_dict=mocker.Mock(
                return_value={
                    "selector_info": {"sub_type": "Boolean", "selector_type": None}
                }
            ),
        )
        bad_raw_var.configure_mock(name="BadVariable")
        fake_initialise_variables_algo = mocker.Mock(
            raw_variables=[bad_raw_var],
            _choose_variable=InitializeVariablesAlgorithm._choose_variable,
        )

        InitializeVariablesAlgorithm._create_variables(fake_initialise_variables_algo)

        warning_msg = (
            "Failed to initialize variable 'BadVariable',"
            " did not recognise the type from determinant:"
            " ('Numeric', 'Boolean', None, False)"
        )
        assert caplog.record_tuples == [("root", logging.WARN, warning_msg)]

    def test_choose_variable_with_selector_var(self, mocker):
        raw_selector_var = mocker.Mock(
            type="Selector",
            selector_info=mocker.Mock(
                sub_type="Categorical",
                selector_type="SingleValue",
                combined_from_variable_name=None,
            ),
            to_dict=mocker.Mock(
                return_value={
                    "selector_info": {
                        "sub_type": "Categorical",
                        "selector_type": "SingleValue",
                        "combined_from_variable_name": None,
                    }
                }
            ),
        )
        assert (
            InitializeVariablesAlgorithm._choose_variable(raw_selector_var)
            == SelectorVariable
        )

    def test_choose_variable_with_combined_categories_var(self, mocker):
        raw_combined_cat_var = mocker.Mock(
            type="Selector",
            selector_info=mocker.Mock(
                sub_type="Categorical",
                selector_type="SingleValue",
                combined_from_variable_name="my_original_variable",
            ),
            to_dict=mocker.Mock(
                return_value={
                    "selector_info": {
                        "sub_type": "Categorical",
                        "selector_type": "SingleValue",
                        "combined_from_variable_name": "my_original_variable",
                    }
                }
            ),
        )
        assert (
            InitializeVariablesAlgorithm._choose_variable(raw_combined_cat_var)
            == SelectorVariable
        )

    def test_choose_variable_with_numeric_var(self, mocker):
        raw_numeric_var = mocker.Mock(
            type="Numeric", to_dict=mocker.Mock(return_value={})
        )
        assert (
            InitializeVariablesAlgorithm._choose_variable(raw_numeric_var)
            == NumericVariable
        )

    def test_choose_variable_with_text_var(self, mocker):
        raw_text_var = mocker.Mock(type="Text", to_dict=mocker.Mock(return_value={}))
        assert (
            InitializeVariablesAlgorithm._choose_variable(raw_text_var) == TextVariable
        )

    def test_choose_variable_with_array_var(self, mocker):
        raw_array_var = mocker.Mock(
            type="Selector",
            selector_info=mocker.Mock(sub_type="Categorical", selector_type="OrArray"),
            to_dict=mocker.Mock(
                return_value={
                    "selector_info": {
                        "sub_type": "Categorical",
                        "selector_type": "OrArray",
                    }
                }
            ),
        )
        assert (
            InitializeVariablesAlgorithm._choose_variable(raw_array_var)
            == ArrayVariable
        )

    def test_choose_variable_with_flag_array_var(self, mocker):
        raw_flag_array_var = mocker.Mock(
            type="Selector",
            selector_info=mocker.Mock(
                sub_type="Categorical", selector_type="OrBitArray"
            ),
            to_dict=mocker.Mock(
                return_value={
                    "selector_info": {
                        "sub_type": "Categorical",
                        "selector_type": "OrBitArray",
                    }
                }
            ),
        )
        assert (
            InitializeVariablesAlgorithm._choose_variable(raw_flag_array_var)
            == FlagArrayVariable
        )

    def test_choose_variable_with_date_var(self, mocker):
        raw_date_var = mocker.Mock(
            type="Selector",
            selector_info=mocker.Mock(sub_type="Date", selector_type="SingleValue"),
            to_dict=mocker.Mock(
                return_value={
                    "selector_info": {
                        "sub_type": "Date",
                        "selector_type": "SingleValue",
                    }
                }
            ),
        )
        assert (
            InitializeVariablesAlgorithm._choose_variable(raw_date_var) == DateVariable
        )

    def test_choose_variable_with_datetime_var(self, mocker):
        raw_datetime_var = mocker.Mock(
            type="Selector",
            selector_info=mocker.Mock(sub_type="DateTime", selector_type="SingleValue"),
            to_dict=mocker.Mock(
                return_value={
                    "selector_info": {
                        "sub_type": "DateTime",
                        "selector_type": "SingleValue",
                    }
                }
            ),
        )
        assert (
            InitializeVariablesAlgorithm._choose_variable(raw_datetime_var)
            == DateTimeVariable
        )

    def test_choose_variable_with_reference_var(self, mocker):
        raw_reference_var = mocker.Mock(
            type="Reference", to_dict=mocker.Mock(return_value={})
        )
        assert (
            InitializeVariablesAlgorithm._choose_variable(raw_reference_var)
            == ReferenceVariable
        )

    def test_choose_variable_with_bad_type(self, mocker):
        bad_raw_var = mocker.Mock(
            type="Numeric",
            selector_info=mocker.Mock(sub_type="Boolean", selector_type=None),
            to_dict=mocker.Mock(
                return_value={
                    "selector_info": {"sub_type": "Boolean", "selector_type": None}
                }
            ),
        )
        bad_raw_var.configure_mock(name="BadVariable")
        with pytest.raises(VariablesError) as exc_info:
            InitializeVariablesAlgorithm._choose_variable(bad_raw_var)
        exception_msg = exc_info.value.args[0]
        assert exception_msg == (
            "Failed to initialize variable 'BadVariable',"
            " did not recognise the type from determinant: "
            "('Numeric', 'Boolean', None, False)"
        )

    def test_identify_variables(self, mocker):
        fake_customers_table = mocker.Mock()
        fake_purchases_table = mocker.Mock()
        fake_items_table = mocker.Mock()
        fake_web_visits_table = mocker.Mock()
        fake_pages_viewed_table = mocker.Mock()
        fake_customers_table.configure_mock(name="Customers")
        fake_purchases_table.configure_mock(name="Purchases")
        fake_items_table.configure_mock(name="Items")
        fake_web_visits_table.configure_mock(name="Web visits")
        fake_pages_viewed_table.configure_mock(name="Pages viewed")
        var1 = mocker.Mock(table_name="Customers", description="Full name")
        var2 = mocker.Mock(table_name="Customers", description="Gender")
        var3 = mocker.Mock(table_name="Customers", description="Customer ID")
        var4 = mocker.Mock(table_name="Purchases", description="Time")
        var5 = mocker.Mock(table_name="Purchases", description="Total cost")
        var6 = mocker.Mock(table_name="Items", description="Product code")
        var7 = mocker.Mock(table_name="Web visits", description="Origin")
        var8 = mocker.Mock(table_name="Pages viewed", description="URL")
        var9 = mocker.Mock(table_name="Pages viewed", description="Time requested")
        var1.configure_mock(name="cuName")
        var2.configure_mock(name="cuGender")
        var3.configure_mock(name="cuID")
        var4.configure_mock(name="puTime")
        var5.configure_mock(name="puCost")
        var6.configure_mock(name="itPCode")
        var7.configure_mock(name="wvOrigin")
        var8.configure_mock(name="pvURL")
        var9.configure_mock(name="pvTime")
        fake_variables = [var1, var2, var3, var4, var5, var6, var7, var8, var9]
        correct_results = {
            "Customers": [var1, var2, var3],
            "Purchases": [var4, var5],
            "Items": [var6],
            "Web visits": [var7],
            "Pages viewed": [var8, var9],
        }
        fake_initialize_variables_algo = mocker.Mock(variables=fake_variables)
        InitializeVariablesAlgorithm._identify_variables(fake_initialize_variables_algo)
        assert fake_initialize_variables_algo.variables_lookup == correct_results
        assert fake_initialize_variables_algo.variables_lookup.default_factory is None
