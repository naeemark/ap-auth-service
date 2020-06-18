"""
    User Model
"""
from sqlalchemy.exc import ObjectNotExecutableError
from sqlalchemy.exc import OperationalError
from src import db
from src.utils.constant.response_messages import DATABASE_CONNECTION
from src.utils.constant.response_messages import DUPLICATE_USER


class UserModel(db.Model):
    """
        Provides an instance of UserModel
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.LargeBinary())

    def __init__(self, email, password):
        self.email = email
        self.password = password

    def save_to_db(self):
        """
            Saves to Database
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """
            Deletes from Database
        """
        db.session.delete(self)
        db.session.commit()

    def json(self):
        """
            Returns a json of self
        """
        return {"username": self.email, "password": self.password}

    @classmethod
    def find_by_email(cls, email, already_exist_check=False):
        """
            Finds by email
        """

        try:
            user_instance = cls.query.filter_by(email=email).first()
            if user_instance and already_exist_check:
                raise ObjectNotExecutableError(DUPLICATE_USER)
            return user_instance

        except OperationalError:
            raise OperationalError("server error", 503, DATABASE_CONNECTION)

    @classmethod
    def find_by_id(cls, _id):
        """
            Finds by id
        """
        return cls.query.filter_by(id=_id).first()
