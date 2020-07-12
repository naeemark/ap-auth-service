"""
A module to check App Health
"""
from flask_restful import Resource
from src.utils.response_builder import get_success_response


class Health(Resource):
    """
        Resource Health
    """

    def get(self):
        """
            Returns health
        """
        return get_success_response(data={"health": "Ok"})
