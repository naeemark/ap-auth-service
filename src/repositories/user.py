"""
  Test
"""
import datetime
import os

from dynamorm import DynaModel
from email_validator import validate_email
from marshmallow import fields
from marshmallow import validates


class User(DynaModel):
    """  Test """

    class Table:
        """  Test """

        name = os.environ.get("DYNAMODB_TABLE_NAME_USERS")
        hash_key = "entity_hash_key"
        range_key = "email"

    class Schema:
        """  Test """

        entity_hash_key = fields.String(default="#AP-USER#")
        email = fields.String(required=True, validate=validate_email)
        name = fields.String()
        password = fields.String()
        is_admin = fields.Boolean(default=False)
        is_active = fields.Boolean(default=False)
        is_approved = fields.Boolean(default=False)
        created_at = fields.DateTime(default=datetime.datetime.utcnow())
        updated_at = fields.DateTime(default=datetime.datetime.utcnow())

        @validates("name")
        def validate_name(self, name):
            """Validates Name"""
            name_string = name.replace(" ", "")
            if not name_string.isalpha() or not len(name_string) > 2:
                raise ValueError("`name` is not valid")

    def save(self):
        """  Overridden Save """
        super(User, self).save(unique=True)

    @classmethod
    def get(cls, email=None):
        """  Overridden Get """
        entity_hash_key = "#AP-USER#"
        return super(User, cls).get(entity_hash_key=entity_hash_key, email=email)

    def json(self):
        """  Test """
        return {"name": self.name, "email": self.email}

    def __repr__(self):
        """  Test """
        return "<User(name={}, email={})>".format(self.name, self.email)

    def log(self):
        """  Logs Representation """
        print(self)


if os.environ.get("DYNAMODB_LOCAL_ENDPOINT"):
    print("Connected: Local DYNAMODB")
    # pylint: disable=no-member
    User.Table.get_resource(endpoint_url=os.environ.get("DYNAMODB_LOCAL_ENDPOINT"),)
