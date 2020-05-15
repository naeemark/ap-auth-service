from email_validator import EmailNotValidError
from email_validator import validate_email
from src.constant.exception import ValidationException
from src.constant.rules import password_policy


class UserRegisterValidate:
    __slots__ = ["password", "email"]

    def __init__(self, data):
        self.password = data["password"]
        self.email = data["email"]

    def validate_password(self):
        password_rules = password_policy.test(self.password)
        rules_ignored = [str(rule) for rule in password_rules]
        return rules_ignored

    def validate_email(self):
        try:
            valid = validate_email(self.email)
            email = valid.email
            return not email
        except EmailNotValidError as error_message:
            return str(error_message)

    def validate_login(self):
        password_check = self.validate_password()
        email_check = self.validate_email()
        if password_check:
            return (
                {
                    "message": ValidationException.PASSWORD_CONDITION,
                    "pre_condition": password_check,
                },
                412,
            )
        elif email_check:
            return (
                {
                    "message": ValidationException.EMAIL_CONDITION,
                    "pre_condition": email_check,
                },
                406,
            )


class ChangePasswordValidate:
    __slots__ = ["new_password"]

    def __init__(self, data):
        self.new_password = data["new_password"]

    def validate_password(self):
        respone = {}
        password_rules = password_policy.password(self.new_password)
        password_strength = round(password_rules.strength() * 100, 2)
        rules_ignored = [str(rule) for rule in password_rules.test()]
        respone.update({"password_strength": password_strength})
        if rules_ignored:
            respone.update(
                {
                    "message": ValidationException.PASSWORD_CONDITION,
                    "pre_condition": rules_ignored,
                }
            )
            return respone, 412
        return respone, 200
