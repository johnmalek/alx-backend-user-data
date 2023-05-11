#!/usr/bin/env python3
"""A python module
"""
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
from db import DB
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """a method that takes in a password string
    arguments and returns bytes
    """
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_password


def _generate_uuid() -> str:
    """function to generate uuid
    """
    uuid_key = str(uuid.uuid4())
    return uuid_key


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ take mandatory email and password string arguments and
        return a User object.
        If a user already exist with the passed email, raise a ValueError
        with the message User <user's email> already exists.
        If not, hash the password with _hash_password, save the user to the
        database using self._db and return the User object.
        """
        try:
            user_by_email = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            user = self._db.add_user(email=email, hashed_password=hashed_pwd)
            return user
        raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """validate user login
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode(), user.hashed_password):
                return True
        except NoResultFound:
            return False
