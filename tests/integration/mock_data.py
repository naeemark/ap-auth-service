"""
content data handling
"""
content_data = {
    "register_user_1": {"data": {"email": "john1223@gmail.com", "password": "123!!@@AB"}},
    "base_startSession": {
        "headers": {
            "Client-App-Token": "Lv4Apvf6zX3mnRRKRNid3z500JtAfYx9kIqsjuSaoCk=",
            "Timestamp": "1591028817",
            "Device-ID": "this is unique device id",
        }
    },
    "TestSuccessScenario": {
        "login": {"data": {"email": "john12211a3@gmail.com", "password": "123!!@@AB"}},
        "user_register": {"data": {"email": "john12211a3@gmail.com", "password": "123!!@@AB"}},
        "start_session": {
            "headers": {
                "Client-App-Token": "Lv4Apvf6zX3mnRRKRNid3z500JtAfYx9kIqsjuSaoCk=",
                "Timestamp": "1591028817",
                "Device-ID": "this is unique device id",
            }
        },
    },
    "TestFailureScenario": {
        "login": {"data": {"email": "john12211a3@gmail.com", "password": "123!!qq"}},
        "user_register_email": {"data": {"email": "john12211a3.com", "password": "123!!@@AB"}},
        "login_missing_email": {"data": {"password": "123!!@@AB"}},
        "user_register_password": {"data": {"email": "john525@gmail.com", "password": "1231"}},
        "user_register_bad_req": {"data": {"email": "john525@gmail.com"}},
        "start_session": {
            "headers": {
                "Client-App-Token": "Lv4Apvf6zX3mnRRKRNid3z500JtAfYx9kIqsju",
                "Timestamp": "1591028817",
                "Device-ID": "this is unique device id",
            },
            "incomplete_headers": {"Client-App-Token": "Lv4Apvf6zX3mnRRKRNid3z500JtAfYx9kIqsju", "Timestamp": "1591028817"},
        },
    },
    "TestUserBehaviour": {
        "login": {"data": {"email": "john1223@gmail.com", "password": "123!!@@AB"}},
        "changePassword_precondition": {"data": {"new_password": "1212312"}},
        "changePassword_no_fresh_token": {"data": {"new_password": "7897!!@@AB"}},
        "register_without_token": {"data": {"email": "john12@gmail.com", "password": "123!!@@AB"}},
        "register_precondition_password": {"data": {"email": "john1234@gmail.com", "password": "12378"}, "url": "{prefix}/user/register"},
        "password_change": {"data": {"new_password": "7897!!@@AB"}},
    },
    "TestBlackListManager": {"JWT_ACCESS_TOKEN_EXPIRES_SECONDS": 1800, "key": "121", "value": "113123131"},
}


class MockData:
    """content access class"""

    def content(self):
        """content type access method"""


class MockDataManager:
    """content data handler"""

    def __init__(self, data):
        self.data = data

    def get_content(self):
        """returns the content"""
        content_required = self.data.content()
        data = content_data
        return data[content_required]
