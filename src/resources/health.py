"""
A module to check App Health
"""
from flask_restful import Resource
from src.utils.logger import info


class Health(Resource):
    """
        Resource Health
    """

    def get(self):
        """
            Returns health
        """
        info("Hello from HealthCheck")
        return {"health": "Ok"}, 200
