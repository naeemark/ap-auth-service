"""
  Test
"""
import datetime
import os

import boto3
from dynamorm import DynaModel
from email_validator import validate_email
from marshmallow import fields
from marshmallow import validates


os.environ["AWS_PROFILE"] = "aletheadev"

dynamodb = boto3.resource("dynamodb", endpoint_url="http://localhost:8000")
list_tables = list(dynamodb.tables.all())
print(list_tables)


# def create_user(name=None, email=None, password=None):
#     print(name, email, password)
#     user = User(email=email, name=name, password=password)
#     user.save()
#     # user.say_hello()
#     print(user)
#     return user.json()


class User(DynaModel):
    """  Test """

    class Table:
        """  Test """

        name = "ap-users-{}".format(os.environ.get("STAGE", "dev"))
        hash_key = "entity_hash_key"
        range_key = "email"

    class Schema:
        """  Test """

        entity_hash_key = fields.String(default="#AP-USER#")
        email = fields.String(required=True, validate=validate_email)
        name = fields.String()
        password = fields.String()
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

    def json(self):
        """  Test """
        return {"name": self.name, "email": self.email}

    def __repr__(self):
        """  Test """
        return "<User(name={}, email={})>".format(self.name, self.email)

    # def say_hello(self):
    #     print(
    #         "Hello.  {name} here.  My ID is {email} and I'm colored {password}".format(
    #             name=self.name, email=self.email, password=self.password
    #         )
    #     )


# User.Table.get_resource(
#     aws_access_key_id="anything",
#     aws_secret_access_key="anything",
#     region_name="us-west-2",
#     endpoint_url="http://localhost:8000",
# )
