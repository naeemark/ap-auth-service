from email_validator import validate_email, EmailNotValidError

from constant.rules import password_policy
from constant.exception import Exception


class UserRegisterValidate():
    __slots__ = ['password', 'email']

    def __init__(self, data):
        self.password = data['password']
        self.email = data['email']

    def validate_password(self):
        password_rules = password_policy.test(self.password)
        rules_ignored = [str(rule) for rule in password_rules]
        return rules_ignored

    def validate_email(self):
        try:
            valid = validate_email(self.email)

            email = valid.email
            return False
        except EmailNotValidError as error_message:
            return str(error_message)

    def validate_login(self):
        password_check = self.validate_password()
        email_check = self.validate_email()
        if password_check:
            return {"message": Exception.PASSWORD_CONDITION,
                    "pre_condition": password_check}, 412
        elif email_check:
            return {"message": Exception.EMAIL_CONDITION,
                    "pre_condition": email_check}, 406
