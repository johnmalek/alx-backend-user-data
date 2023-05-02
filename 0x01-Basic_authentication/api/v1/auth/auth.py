#!/usr/bin/env python3
"""A python module
"""
from flask import request
from typing import List


class Auth:
    """Class to manage API Authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """a public method
        Return:
          - False
        """
        return False

    def authorization_header(self, request=None) -> str:
        """a public method
        Returns:
          - None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """a public method
        Return:
          - None
        """
        return None
