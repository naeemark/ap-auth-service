"""
    Validator: User Register
"""
from email_validator import validate_email
from src.utils.constant.response_messages import PASSWORD_POLICY
from src.utils.constant.rules import password_policy


def validate_register_user_data(data=None):
    """Validates data provided for new user register"""
    validate_email(data["email"])
    validate_password_data_param(password_param=data["password"])


def validate_password_data_param(password_param=None):
    """Validates Password"""
    password_rules = password_policy.password(password_param)
    rules_ignored = [str(rule) for rule in password_rules.test()]
    if rules_ignored:
        raise ValueError(PASSWORD_POLICY.format(policy=rules_ignored))
