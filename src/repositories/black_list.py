"""
  Test
"""
import os
from datetime import datetime

from dynamorm import DynaModel
from marshmallow import fields

SLUG_ENTITY_HASH_KEY = "#AP-AUTH-BLACKLISTED#"


class Blacklist(DynaModel):
    """  Test """

    class Table:
        """  Test """

        name = os.environ.get("DYNAMODB_TABLE_NAME_BLACKLIST")
        hash_key = "entity_hash_key"
        range_key = "token_id"

    class Schema:
        """  Test """

        entity_hash_key = fields.String(default=SLUG_ENTITY_HASH_KEY)
        token_id = fields.String(required=True)
        type = fields.String(default="access")
        time_to_live = fields.Integer(required=True)
        created_at = fields.Integer(default=int(datetime.now().timestamp()))

    def save(self):
        """  Overridden Save """
        super(Blacklist, self).save()
        self.log()

    @classmethod
    def get(cls, token_id=None):
        """  Overridden Get """
        return super(Blacklist, cls).get(entity_hash_key=SLUG_ENTITY_HASH_KEY, token_id=token_id)

    @classmethod
    def exists(cls, token_id=None):
        """  Checks if Token is Blacklisted """
        return cls.get(token_id=token_id) is not None

    def dict(self):
        """  Test """
        return {"token_id": self.token_id, "type": self.type, "time_to_live": self.time_to_live}

    def __repr__(self):
        """  Test """
        return "{}: {}".format(self.__class__.__name__, self.dict())

    def log(self):
        """  Logs Representation """
        print(self)


# if os.environ.get("DYNAMODB_LOCAL_ENDPOINT"):
#     print("Connected: Local DYNAMODB")
#     # pylint: disable=no-member
#     Blacklist.Table.get_resource(endpoint_url=os.environ.get("DYNAMODB_LOCAL_ENDPOINT"))
