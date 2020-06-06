"""common validator utilities """


def check_none(element):
    """filter method"""
    if not element[1]:
        return True
    return False
