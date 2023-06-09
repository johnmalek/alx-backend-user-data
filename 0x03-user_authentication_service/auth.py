#!/usr/bin/env python3
"""A python module
"""
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
from typing import Union
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

    def create_session(self, email: str) -> str:
        """takes an email and returns the session ID as a string
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        user_uuid = _generate_uuid()
        user.session_id = user_uuid
        self._db._session.commit()
        return user_uuid

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Find user by session ID
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """destroy a user's session
        """
        self._db.update_user(user_id, session_id=None)

        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generate reset password token
        """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError()
        user_uuid = str(uuid.uuid4())
        user.reset_token = user_uuid
        self._db._session.commit()
        return user_uuid

    def update_password(self, reset_token: str, password: str) -> None:
        """update password
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()
        hashed_pwd = _hash_password(password)
        user.hashed_password = hashed_pwd
        user.reset_token = None
        self._db._session.commit()
        return None
