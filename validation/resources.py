class UserRegisterValidate():
    __slots__ = ['password_policy']

    def __init__(self, password_policy):
        self.password_policy = password_policy

    def validate_password(self, password):
        password_rules = self.password_policy.test(password)
        rules_ignored = [str(rule) for rule in password_rules]
        return rules_ignored
