#!/usr/bin/env python3
"""
A python module
"""
from typing import List
import re

def filter_datum(fields: List[str], redaction: str,
        message: str, separator: str) -> str:
    """
    function called filter_datum that returns
    the log message obfuscated
    """
    for field in fields:
        message = re.sub(field+'=.*?'+separator,
                field+'='+redaction+separator, message)
    return message

if __name__ == "__main__":
    main()
