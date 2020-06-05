"""error codes specifications """
from src.constant.rules import AuthError
from src.constant.rules import ServerError
from src.constant.rules import ValidationError


def factory(language="English"):
    """Factory Method"""
    localizers = {
        "French": AuthError,
        "English": ServerError,
        "Spanish": ValidationError,
    }

    return localizers[language]()


if __name__ == "__main__":

    f = factory("French")
    e = factory("English")
    s = factory("Spanish")

    message = ["car", "bike", "cycle"]

    for msg in message:
        print(f.localize(msg))
        print(e.localize(msg))
        print(s.localize(msg))
