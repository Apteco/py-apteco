from datetime import datetime


def test_session(holidays):
    assert len(holidays.tables) == 9
    assert len([v for v in holidays.variables if not v.is_virtual]) == 77
    assert holidays.master_table.name == "Households"


def test_user(holidays):
    user = holidays.user
    assert user.first_name == "Admin"
    assert user.surname == "User"
    assert user.username == "Administrator"
    assert user.email_address == "support@apteco.com"


def test_system_info(holidays):
    system_info = holidays.system_info
    assert system_info.name == "holidays"
    assert system_info.description == "Holidays Demo Database"
    assert system_info.build_date == datetime(2019, 11, 27, 15, 57, 24)
    assert system_info.view_name == "Holidays"
