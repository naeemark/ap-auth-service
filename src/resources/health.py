"""
A module to check App Health
"""
from flask_restful import Resource


class Health(Resource):
    """
        Resource Health
    """

    def get(self):
        """
            Returns health
        """
        return {"health": "Ok"}, 200
