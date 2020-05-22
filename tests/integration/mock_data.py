"""
content data handling
"""
content_data = {
    "register_user_1": {
        "data": {"email": "john1223@gmail.com", "password": "123!!@@AB"}
    },
    "TestRepeatedCases": {
        "login": {"data": {"email": "john12211a3@gmail.com", "password": "123!!@@AB"}},
        "user_register": {
            "data": {"email": "john12211a3@gmail.com", "password": "123!!@@AB"}
        },
        "start_session": {
            "headers": {
                "Client-App-Token": "0b0069c752ec18172c5f782\
                08f1863d7ad6755a6fae6fe76ec2c80d13be41e42",
                "Timestamp": "1311231",
                "Device-ID": "1322a31x121za",
            }
        },
    },
    "TestUserBehaviour": {
        "login": {"data": {"email": "john1223@gmail.com", "password": "123!!@@AB"}},
        "changePassword_precondition": {"data": {"new_password": "1212312"}},
        "changePassword_no_fresh_token": {"data": {"new_password": "7897!!@@AB"}},
        "register_without_token": {
            "data": {"email": "john12@gmail.com", "password": "123!!@@AB"}
        },
        "register_precondition_password": {
            "data": {"email": "john1234@gmail.com", "password": "12378"},
            "url": "{prefix}/user/register",
        },
        "password_change": {"data": {"new_password": "7897!!@@AB"}},
    },
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
