"""
    Validator: User Register
"""
from email_validator import EmailNotValidError
from email_validator import validate_email
from src.utils.constant.response_messages import PASSWORD_POLICIY
from src.utils.constant.rules import password_policy


class ValidateRegisterUser:
    """
        Validator Class
    """

    __slots__ = ["password", "email"]

    def __init__(self, data):
        self.password = data["password"]
        self.email = data["email"]

    def validate_password(self):
        """
            Validates Password
        """
        password_rules = password_policy.test(self.password)
        rules_ignored = [str(rule) for rule in password_rules]
        return rules_ignored

    def validate_email(self):
        """
            Validates Email
        """
        try:
            valid = validate_email(self.email)
            email = valid.email
            return not email
        except EmailNotValidError as error_message:
            raise NameError(error_message)

    def validate_login(self):
        """
            Validates Login
        """
        password_check = self.validate_password()
        self.validate_email()
        if password_check:
            raise ValueError(PASSWORD_POLICIY.format(policy=password_check))


class ChangePasswordValidate:
    """
      Change Password Validation
    """

    __slots__ = ["new_password"]

    def __init__(self, data):
        self.new_password = data["new_password"]

    def validate_password(self):
        """
        Validates Password
        """
        respone = {}
        password_rules = password_policy.password(self.new_password)
        password_strength = round(password_rules.strength() * 100, 2)
        rules_ignored = [str(rule) for rule in password_rules.test()]
        respone.update({"password_strength": password_strength})
        if rules_ignored:
            raise ValueError(PASSWORD_POLICIY.format(policy=rules_ignored))
        return respone, 200
