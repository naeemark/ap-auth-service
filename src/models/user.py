"""
    User Model
"""
from src import db


class UserModel(db.Model):
    """
        Provides an instance of UserModel
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80))
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
    def find_by_email(cls, email):
        """
            Finds by email
        """
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, _id):
        """
            Finds by id
        """
        return cls.query.filter_by(id=_id).first()
