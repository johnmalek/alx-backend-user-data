#!/usr/bin/env python3
"""A python module
"""
from api.v1.auth.auth import Auth
from models.user import User
from uuid import uuid4


class SessionAuth(Auth):
    """implement session authorization protocol
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a session ID for a user with id user_id
        """
        if user_id is None or type(user_id) != str:
            return None
        some_id = uuid4()
        self.user_id_by_session_id[str(id)] = user_id
        return str(id)

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ that returns a User ID based on a Session ID
        """
        if session_id is None:
            return None
        if type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ returns a User instance based on a cookie value
        """
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_cookie)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """ deletes the user session / logout
        """
        if request is None:
            return None
        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return False
        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_cookie]
        return True
