from unittest.mock import Mock, patch

import pytest

from apteco.exceptions import DeserializeError
from apteco.session import Session, User


@pytest.fixture()
def fake_session_for_serialize_test():
    session = Session.__new__(Session)
    session.base_url = "https://fake.base/URL/OrbitAPI"
    session.data_view = "fake_data_view"
    session.session_id = "fake_session_ID_04bd678ef"
    session.access_token = "fake_access_token_o87q4bwvf9pac"
    session.user = User("my_fake_user", "Jane", "Doe", "jane.doe@mysite.com")
    session.system = "fake_system_name"
    return session


@pytest.fixture()
def fake_serialized_session():
    return (
        "{"
        '"base_url": "https://fake.base/URL/OrbitAPI", '
        '"data_view": "fake_data_view", '
        '"session_id": "fake_session_ID_04bd678ef", '
        '"access_token": "fake_access_token_o87q4bwvf9pac", '
        '"user": {'
        '"username": "my_fake_user", '
        '"first_name": "Jane", '
        '"surname": "Doe", '
        '"email_address": "jane.doe@mysite.com"'
        "}, "
        '"system": "fake_system_name"'
        "}"
    )


class TestSession:
    def test_serialize_session(
        self, fake_session_for_serialize_test, fake_serialized_session
    ):
        example_serialized_session = fake_session_for_serialize_test.serialize()
        assert example_serialized_session == fake_serialized_session

    @patch("apteco.session.InitializeTablesAlgorithm")
    @patch("apteco.session.InitializeVariablesAlgorithm")
    @patch("apteco.session.Session._fetch_system_info")
    def test_deserialize_session(
        self,
        patched_fetch_system_info,
        patched_initialize_variables_algo,
        patched_initialize_tables_algo,
        fake_serialized_session,
    ):
        patched_initialize_tables_algo.return_value = Mock(
            run=Mock(return_value=("fake_tables", "fake_master_table"))
        )
        expected_user = User("my_fake_user", "Jane", "Doe", "jane.doe@mysite.com")
        deserialized_session = Session.deserialize(fake_serialized_session)
        assert deserialized_session.base_url == "https://fake.base/URL/OrbitAPI"
        assert deserialized_session.data_view == "fake_data_view"
        assert deserialized_session.session_id == "fake_session_ID_04bd678ef"
        assert deserialized_session.access_token == "fake_access_token_o87q4bwvf9pac"
        assert deserialized_session.user == expected_user
        assert deserialized_session.system == "fake_system_name"
        assert deserialized_session.tables == "fake_tables"
        assert deserialized_session.master_table == "fake_master_table"
        patched_fetch_system_info.assert_called_once_with()
        patched_initialize_variables_algo.assert_called_once_with(deserialized_session)
        patched_initialize_tables_algo.assert_called_once_with(deserialized_session)

    def test_deserialize_session_with_bad_credentials_dict(
        self, fake_serialized_session
    ):
        serialized_session_no_session_id = fake_serialized_session.replace(
            '"session_id": "fake_session_ID_04bd678ef", ', ""
        )
        with pytest.raises(DeserializeError) as exc_info:
            Session.deserialize(serialized_session_no_session_id)
        exception_msg = exc_info.value.args[0]
        assert exception_msg == (
            "Data missing from 'Session' object: no 'session_id' found."
        )

    def test_deserialize_session_with_bad_user_dict(self, fake_serialized_session):
        serialized_session_no_user_surname = fake_serialized_session.replace(
            '"surname": "Doe", ', ""
        )
        with pytest.raises(DeserializeError) as excinfo:
            Session.deserialize(serialized_session_no_user_surname)
        exception_msg = excinfo.value.args[0]
        assert exception_msg == (
            "The following parameter(s) were missing from 'User' object: 'surname'"
        )
