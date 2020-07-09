"""
  Test
"""
import os
from datetime import datetime

from dynamorm import DynaModel
from email_validator import validate_email
from marshmallow import fields
from marshmallow import validates

SLUG_ENTITY_HASH_KEY = "#AP-USER#"
SLUG_ENTITY_SORT_KEY = "#USR#{}#"


# pylint: disable=too-many-instance-attributes
class User(DynaModel):
    """  Test """

    # for partial updates
    _validated_data = {}

    class Table:
        """  Test """

        name = os.environ.get("DYNAMODB_TABLE_NAME_USERS")
        hash_key = "entity_hash_key"
        range_key = "entity_sort_key"

    def __init__(self, **kwargs):
        self.entity_hash_key = SLUG_ENTITY_HASH_KEY
        self.entity_sort_key = SLUG_ENTITY_SORT_KEY.format(kwargs.get("email"))
        self.email = kwargs.get("email")
        self.name = kwargs.get("name")
        self.password = kwargs.get("password")
        self.is_admin = kwargs.get("is_admin", False)
        self.is_active = kwargs.get("is_active", False)
        self.is_approved = kwargs.get("is_approved", False)
        self.created_at = int(kwargs.get("created_at", datetime.now().timestamp()))
        self.updated_at = int(kwargs.get("updated_at", datetime.now().timestamp()))
        self.log()

    class Schema:
        """  Test """

        entity_hash_key = fields.String(required=True)
        entity_sort_key = fields.String(required=True)
        email = fields.String(required=True, validate=validate_email)
        name = fields.String()
        password = fields.String()
        is_admin = fields.Boolean(default=False)
        is_active = fields.Boolean(default=False)
        is_approved = fields.Boolean(default=False)
        created_at = fields.Integer()
        updated_at = fields.Integer()

        @validates("name")
        def validate_name(self, name):
            """Validates Name"""
            name_string = name.replace(" ", "")
            if not name_string.isalpha() or not len(name_string) > 2:
                raise ValueError("`name` is not valid")

    def save(self):
        """  Overridden Save """
        self.log()
        super(User, self).save(unique=True)

    @classmethod
    def get(cls, email=None):
        """  Overridden Get """
        return super(User, cls).get(entity_hash_key=SLUG_ENTITY_HASH_KEY, entity_sort_key=SLUG_ENTITY_SORT_KEY.format(email))

    def dict(self):
        """  Test """
        return {
            "name": self.name,
            "email": self.email,
            "isAdmin": self.is_admin,
            "isActive": self.is_active,
            "isApproved": self.is_approved,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
        }

    def __repr__(self):
        """  Test """
        return "{}: {}".format(self.__class__.__name__, self.dict())

    def log(self):
        """  Logs Representation """
        print(self)


if os.environ.get("DYNAMODB_LOCAL_ENDPOINT"):
    print("Connected: Local DYNAMODB")
    # pylint: disable=no-member
    User.Table.get_resource(endpoint_url=os.environ.get("DYNAMODB_LOCAL_ENDPOINT"),)
