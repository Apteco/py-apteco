import getpass
import json
from json import JSONDecodeError

import apteco_api
import pytest

import apteco.session
from apteco.exceptions import DeserializeError
from apteco.session import (
    Session,
    Table,
    User,
    _get_password,
    login,
    login_with_password,
)


@pytest.fixture()
def patch_unpack_credentials(mocker):
    return mocker.patch.object(apteco.session.Session, "_unpack_credentials")


@pytest.fixture()
def patch_create_client(mocker):
    return mocker.patch.object(apteco.session.Session, "_create_client")


@pytest.fixture()
def patch_initialize_tables_algo(mocker):
    fake = mocker.Mock()
    fake.run.return_value = ["fake tables", "fake master table"]
    return mocker.patch("apteco.session.InitializeTablesAlgorithm", return_value=fake)


@pytest.fixture()
def patch_initialize_variables_algo(mocker):
    fake = mocker.Mock()
    fake.run.return_value = "fake variables"
    return mocker.patch(
        "apteco.session.InitializeVariablesAlgorithm", return_value=fake
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
def fake_user_with_to_dict(mocker):
    fake_user = mocker.Mock()
    fake_user._to_dict.return_value = "user-per to the throne"
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
    return mocker.patch.object(apteco_api, "Configuration", return_value=fake_config)


@pytest.fixture()
def fake_session_with_attrs(mocker, fake_user_with_to_dict):
    return mocker.Mock(
        base_url="baseless assumptions",
        data_view="a room with a view",
        session_id="0246813579",
        access_token="token of my gratitude",
        user=fake_user_with_to_dict,
        system="solar system",
    )


@pytest.fixture()
def serialized_session():
    return {
        "base_url": "baseless assumptions",
        "data_view": "a room with a view",
        "session_id": "0246813579",
        "access_token": "token of my gratitude",
        "user": "user-per to the throne",
        "system": "solar system",
    }


@pytest.fixture()
def fake_credentials_empty(mocker):
    return mocker.Mock()


@pytest.fixture()
def patch_credentials(mocker, fake_credentials_empty):
    return mocker.patch.object(
        apteco.session, "Credentials", return_value=fake_credentials_empty
    )


@pytest.fixture()
def patch_user_from_dict(mocker):
    return mocker.patch.object(
        apteco.session.User, "_from_dict", return_value="user your skill and judgement"
    )


@pytest.fixture()
def patch_user_from_dict_raise_deserialize_error(mocker):
    return mocker.patch.object(
        apteco.session.User,
        "_from_dict",
        side_effect=DeserializeError(
            "Data missing from 'User' object: no 'surname' found."
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
    patch_initialize_variables_algo,
    patch_initialize_tables_algo,
):
    session_example = Session(fake_credentials_with_attrs, "solar system")
    assert session_example.system == "solar system"
    assert session_example.variables == "fake variables"
    assert session_example.tables == "fake tables"
    assert session_example.master_table == "fake master table"
    patch_initialize_variables_algo.assert_called_once_with(session_example)
    patch_initialize_tables_algo.assert_called_once_with(session_example)
    assert session_example.base_url == "baseless assumptions"
    assert session_example.data_view == "a room with a view"
    assert session_example.session_id == "0246813579"
    assert session_example.access_token == "token of my gratitude"
    assert session_example.user == "use, er, something else"


class TestSession:
    def test_session_init(
        self,
        fake_credentials_with_attrs,
        patch_unpack_credentials,
        patch_create_client,
        patch_initialize_variables_algo,
        patch_initialize_tables_algo,
    ):
        session_example = Session(fake_credentials_with_attrs, "solar system")
        patch_unpack_credentials.assert_called_once_with(fake_credentials_with_attrs)
        patch_create_client.assert_called_once_with()
        assert session_example.system == "solar system"
        patch_initialize_variables_algo.assert_called_once_with(session_example)
        assert session_example.variables == "fake variables"
        patch_initialize_tables_algo.assert_called_once_with(session_example)
        assert session_example.tables == "fake tables"
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

    def test_to_dict(
        self, fake_session_with_attrs, serialized_session, fake_user_with_to_dict
    ):
        dict_example = Session._to_dict(fake_session_with_attrs)
        assert dict_example == serialized_session
        fake_user_with_to_dict._to_dict.assert_called_once_with()

    def test_from_dict(
        self,
        serialized_session,
        patch_credentials,
        fake_credentials_empty,
        patch_user_from_dict,
        patch_session,
        fake_session_empty,
    ):
        result = Session._from_dict(serialized_session)
        patch_user_from_dict.assert_called_once_with("user-per to the throne")
        patch_credentials.assert_called_once_with(
            "baseless assumptions",
            "a room with a view",
            "0246813579",
            "token of my gratitude",
            "user your skill and judgement",
        )
        patch_session.assert_called_once_with(fake_credentials_empty, "solar system")
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
        patch_user_from_dict_raise_deserialize_error,
    ):
        with pytest.raises(DeserializeError) as excinfo:
            Session._from_dict(serialized_session)
        exception_msg = excinfo.value.args[0]
        assert exception_msg == "Data missing from 'User' object: no 'surname' found."

    def test_serialize(self, fake_session_with_to_dict, patch_json_dumps):
        result = Session.serialize(fake_session_with_to_dict)
        patch_json_dumps.assert_called_once_with("I'm a session dictionary")
        assert result == "Jason and the Argonauts"

    def test_deserialize(self, patch_json_loads, patch_session_from_dict):
        result = Session.deserialize("cereal eyes-d session")
        patch_json_loads.called_once_with("cereal eyes-d session")
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
def fake_parent_table(mocker):
    return mocker.Mock()


@pytest.fixture()
def fake_child_tables(mocker):
    child1 = mocker.Mock()
    child2 = mocker.Mock()
    return [child1, child2]


@pytest.fixture()
def fake_parent_tables(mocker):
    parent1 = mocker.Mock()
    parent2 = mocker.Mock()
    return [parent1, parent2]


@pytest.fixture()
def fake_ancestor_tables(mocker):
    ancestor1 = mocker.Mock()
    ancestor2 = mocker.Mock()
    return [ancestor1, ancestor2]


@pytest.fixture()
def fake_descendant_tables(mocker):
    descendant1 = mocker.Mock()
    descendant2 = mocker.Mock()
    return [descendant1, descendant2]


@pytest.fixture()
def fake_variables(mocker):
    variable1 = mocker.Mock()
    variable2 = mocker.Mock()
    return {"var1": variable1, "var2": variable2}


@pytest.fixture()
def fake_customers_table():
    customers = Table("Customers", *[None] * 14)
    return customers


@pytest.fixture()
def fake_products_table():
    products = Table("Products", *[None] * 14)
    return products


@pytest.fixture()
def fake_purchases_table(fake_customers_table, fake_products_table):
    purchases = Table(
        "Purchases",
        *[None] * 7,
        True,
        None,
        fake_customers_table,
        fake_products_table,
        [fake_customers_table],
        [fake_products_table],
        None,
    )
    return purchases


@pytest.fixture()
def fake_table_with_variables():
    table = Table(*[None] * 14, {"var1": "my first variable"})
    return table


@pytest.fixture()
def fake_web_visits_table():
    web_visits = Table("Web Visits", *[None] * 14)
    return web_visits


class TestTable:
    def test_table_init(
        self,
        fake_parent_table,
        fake_child_tables,
        fake_ancestor_tables,
        fake_descendant_tables,
        fake_variables,
        fake_session_empty,
    ):
        table_example = Table(
            "what's in a name",
            "the singularity",
            "first person plural",
            False,
            True,
            123_456_789,
            "sweet child of mine",
            "the parent trap",
            True,
            "mother nature",
            fake_parent_table,
            fake_child_tables,
            fake_ancestor_tables,
            fake_descendant_tables,
            fake_variables,
            session=fake_session_empty,
        )
        assert table_example.name == "what's in a name"
        assert table_example.singular_display_name == "the singularity"
        assert table_example.plural_display_name == "first person plural"
        assert table_example.is_default_table is False
        assert table_example.is_people_table is True
        assert table_example.total_records == 123_456_789
        assert table_example.child_relationship_name == "sweet child of mine"
        assert table_example.parent_relationship_name == "the parent trap"
        assert table_example.has_child_tables is True
        assert table_example.parent_name == "mother nature"
        assert table_example.parent is fake_parent_table
        assert table_example.children is fake_child_tables
        assert table_example.ancestors is fake_ancestor_tables
        assert table_example.descendants is fake_descendant_tables
        assert table_example.variables is fake_variables
        assert table_example.session is fake_session_empty

    def test_table_eq(self):
        fake_people_table1 = Table("People", "person", *[None] * 13)
        fake_people_table2 = Table("People", "human", *[None] * 13)
        fake_purchases_table = Table("Purchases", "purchase", *[None] * 13)
        assert fake_people_table1 == fake_people_table2
        assert fake_people_table1 != fake_purchases_table

    def test_table_gt(
        self, fake_customers_table, fake_purchases_table, fake_web_visits_table
    ):
        assert fake_customers_table > fake_purchases_table
        assert not fake_web_visits_table > fake_purchases_table

    def test_table_lt(
        self,
        fake_customers_table,
        fake_purchases_table,
        fake_products_table,
        fake_web_visits_table,
    ):
        assert fake_products_table < fake_purchases_table
        assert not fake_web_visits_table < fake_purchases_table

    def test_table_getitem(self, fake_table_with_variables):
        assert fake_table_with_variables["var1"] == "my first variable"
        with pytest.raises(KeyError) as excinfo:
            my_second_variable = fake_table_with_variables["var2"]
        exception_msg = excinfo.value.args[0]
        assert exception_msg == "var2"


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
def fake_user_empty(mocker):
    return mocker.Mock()


@pytest.fixture()
def patch_user(mocker, fake_user_empty):
    return mocker.patch.object(apteco.session, "User", return_value=fake_user_empty)


class TestUser:
    def test_user_init(self):
        user_example = User("JDoe", "Jane", "Doe", "jane.doe@example.com")
        assert user_example.username == "JDoe"
        assert user_example.first_name == "Jane"
        assert user_example.surname == "Doe"
        assert user_example.email_address == "jane.doe@example.com"

    def test_user_to_dict(self, fake_user_with_attrs, serialized_user):
        dict_example = User._to_dict(fake_user_with_attrs)
        assert dict_example == serialized_user

    def test_user_from_dict(self, serialized_user, patch_user, fake_user_empty):
        result = User._from_dict(serialized_user)
        patch_user.assert_called_once_with(
            "ewes urn aim",
            "thirst for knowledge",
            "Sir Name of Spamalot",
            "he male a trousers",
        )
        assert result is fake_user_empty

    def test_user_from_dict_with_bad_dict(self, serialized_user):
        serialized_user_no_surname = dict(serialized_user)
        del serialized_user_no_surname["surname"]
        with pytest.raises(DeserializeError) as exc_info:
            User._from_dict(serialized_user_no_surname)
        exception_msg = exc_info.value.args[0]
        assert exception_msg == "Data missing from 'User' object: no 'surname' found."


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
        apteco.session, "login_with_password", return_value="Here are your credentials!"
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
        credentials = login(
            "https://marketing.example.com/AptecoAPI/", "a_room_with_a_view", "JDoe"
        )
        assert credentials == "Here are your credentials!"
        patch_get_password.assert_called_once_with()
        patch_login_with_password.assert_called_once_with(
            "https://marketing.example.com/AptecoAPI/",
            "a_room_with_a_view",
            "JDoe",
            password="something very secret",
        )

    def test_login_with_password(self, patch_simple_login_algo, fake_simple_login_algo):
        credentials = login_with_password(
            "https://marketing.example.com/AptecoAPI/",
            "a_room_with_a_view",
            "JDoe",
            "my s3cr3t pa55w0rd",
        )
        assert credentials == "fake credentials"
        patch_simple_login_algo.assert_called_once_with(
            "https://marketing.example.com/AptecoAPI/", "a_room_with_a_view"
        )
        fake_simple_login_algo.run.assert_called_once_with("JDoe", "my s3cr3t pa55w0rd")

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
