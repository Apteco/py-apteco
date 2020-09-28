from unittest.mock import Mock, patch

import pytest

from apteco.exceptions import DeserializeError
from apteco.session import FastStatsSystem, Session, User


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


@pytest.fixture()
def fake_session_with_client():
    return Mock(
        data_view="dataView for the session",
        system="system for the session",
        api_client="API client for the session",
    )


class TestSession:
    @patch("apteco.session.aa.FastStatsSystemsApi")
    def test_fetch_system_info(
        self, patch_aa_faststats_systems_api, fake_session_with_client
    ):
        fake_faststats_system_response = Mock()
        fake_faststats_system_response.configure_mock(
            name="ecosystem",
            description="wasn't in the job description",
            fast_stats_build_date="best-before date",
            view_name="rear view mirror",
        )
        fake_get_system = Mock(return_value=fake_faststats_system_response)
        fake_systems_controller = Mock(
            fast_stats_systems_get_fast_stats_system=fake_get_system
        )
        patch_aa_faststats_systems_api.return_value = fake_systems_controller

        Session._fetch_system_info(fake_session_with_client)
        example_system_info = fake_session_with_client.system_info
        assert type(example_system_info) == FastStatsSystem
        assert example_system_info.name == "ecosystem"
        assert example_system_info.description == "wasn't in the job description"
        assert example_system_info.build_date == "best-before date"
        assert example_system_info.view_name == "rear view mirror"

        patch_aa_faststats_systems_api.assert_called_once_with(
            "API client for the session"
        )
        fake_get_system.assert_called_once_with(
            "dataView for the session", "system for the session"
        )

    def test_serialize_session(
        self, fake_session_for_serialize_test, fake_serialized_session
    ):
        example_serialized_session = fake_session_for_serialize_test.serialize()
        assert example_serialized_session == fake_serialized_session

    @patch("apteco.session.Session.__init__")
    @patch("apteco.session.Credentials")
    @patch("apteco.session.User")
    def test_deserialize_session(
        self,
        patched_user,
        patched_credentials,
        patched_session,
        fake_serialized_session,
    ):
        patched_user.return_value = "my_user_object"
        patched_credentials.return_value = "my_credentials_object"
        patched_session.return_value = None  # error if __init__ returns something
        deserialized_session = Session.deserialize(fake_serialized_session)
        patched_user.assert_called_once_with(
            username="my_fake_user",
            first_name="Jane",
            surname="Doe",
            email_address="jane.doe@mysite.com",
        )
        patched_credentials.assert_called_once_with(
            "https://fake.base/URL/OrbitAPI",
            "fake_data_view",
            "fake_session_ID_04bd678ef",
            "fake_access_token_o87q4bwvf9pac",
            "my_user_object",
        )
        patched_session.assert_called_once_with(
            "my_credentials_object", "fake_system_name"
        )

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
