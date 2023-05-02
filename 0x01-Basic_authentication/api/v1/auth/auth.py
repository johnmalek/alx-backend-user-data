#!/usr/bin/env python3
"""A python module
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Class to manage API Authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """a public method
        Return:
          - False
        """
        if path is None:
            return True
        elif excluded_paths is None or len(excluded_paths) == 0:
            return True
        elif path in excluded_paths:
            return False
        else:
            return False

    def authorization_header(self, request=None) -> str:
        """a public method
        Returns:
          - None
        """
        if request is None:
            return None
        elif "Authorization" not in request.keys():
            return None
        else:
            return request["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """a public method
        Return:
          - None
        """
        return None
