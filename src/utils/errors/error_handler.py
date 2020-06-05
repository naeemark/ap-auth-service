"""error codes specifications """
from .error_pattern import AuthError
from .error_pattern import ServerError
from .error_pattern import ValidationError


def exception_factory(error_category="Validate"):
    """build error , validate is set by default"""
    localize = {
        "Auth": AuthError,
        "Server": ServerError,
        "Validate": ValidationError,
    }

    return localize[error_category]()
