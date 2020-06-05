"""error codes specifications """
from src.constant.rules import AuthError
from src.constant.rules import ServerError
from src.constant.rules import ValidationError


def factory(error_category="Validate"):
    """build error """
    localize = {
        "Auth": AuthError,
        "Server": ServerError,
        "Validate": ValidationError,
    }

    return localize[error_category]()


if __name__ == "__main__":
    f1 = factory()
    f2 = factory("Auth")

    f1.get_response("Invalid Credential")
    f2.get_response("Token Revoked", status_code=422)
