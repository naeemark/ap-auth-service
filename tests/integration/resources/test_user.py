"""
    A file to containe all integration tests of
    UserResource
"""


def test_sum(test_client, test_database):
    """
        A sample test to demostrate the availability of test_client and test_dataabase
    """
    # for mock purpose
    # pylint: disable=unused-argument
    assert 1 + 1 == 2
