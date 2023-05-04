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
        elif excluded_paths is None or excluded_paths == []:
            return True
        elif path in excluded_paths:
            return False
        else:
            for i in excluded_paths:
                if i.startswith(path):
                    return False
                if path.startswith(i):
                    return False
                if i[-1] == "*":
                    if path.startswith(i[:-1]):
                        return False
        return False

    def authorization_header(self, request=None) -> str:
        """a public method
        Returns:
          - None
        """
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """a public method
        Return:
          - None
        """
        return None
