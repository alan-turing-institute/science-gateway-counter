# project/server/models.py

import jwt
import datetime
from flask import current_app
from service.database import db, bcrypt
from uuid import uuid4


class Organisation(db.Model):
    """Organisation data"""
    __tablename__ = "organisation"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    credit = db.Column(db.Integer())  # remaining simulation credit
    tally = db.Column(db.Integer())  # tally of simulations run

    users = db.relationship("User", back_populates="organisation", lazy="joined")

    def __init__(self, credit=0, tally=0):
        self.credit = credit
        self.tally = tally

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class User(db.Model):
    """User data"""
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uuid = db.Column(db.String)

    tally = db.Column(db.Integer())
    credit = db.Column(db.Integer())

    organisation_id = db.Column(db.Integer, db.ForeignKey('organisation.id'))
    organisation = db.relationship("Organisation", back_populates="users")

    def __init__(self, tally=0, credit=0, organisation=None):
        self.uuid = str(uuid4())
        self.tally = tally
        self.credit = credit
        self.organisation = organisation
