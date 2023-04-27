#!/usr/bin/env python3
"""
A python module
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """
     expects one string argument name password
     and returns a salted, hashed password, which
     is a byte string.
    """
    encoded_passwd = password.encode()
    hashed_password = bcrypt.hashpw(encoded_passwd, bcrypt.gensalt())
    return hashed_password


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
     function that expects 2 arguments and returns a boolean.
    """
    if bcrypt.checkpw(password.encode(), hashed_password):
        return True
    return False


if __name__ == "__main__":
    main()
