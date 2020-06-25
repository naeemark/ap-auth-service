"""
    Validator: User Register
"""
from email_validator import validate_email
from src.utils.constant.response_messages import PASSWORD_POLICY
from src.utils.constant.rules import password_policy


def validate_register_user_data(data=None):
    """Validates data provided for new user register"""
    validate_email(data["email"])
    password_rules = password_policy.test(data["password"])
    rules_ignored = [str(rule) for rule in password_rules]
    if rules_ignored:
        raise ValueError(PASSWORD_POLICY.format(policy=rules_ignored))


def validate_change_password(data):
    """
    Validates Password
    """

    password_rules = password_policy.password(data["new_password"])
    password_strength = round(password_rules.strength() * 100, 2)
    rules_ignored = [str(rule) for rule in password_rules.test()]

    if rules_ignored:
        raise ValueError(PASSWORD_POLICY.format(policy=rules_ignored))
    return password_strength
