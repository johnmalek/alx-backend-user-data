#!/usr/bin/env python3
"""A python module
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    """a method that takes in a password string
    arguments and returns bytes
    """
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_password
