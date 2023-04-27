#!/usr/bin/env python3
"""
A python module
"""
from typing import List
import re
import logging
import os

PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str) -> str:
    """
    function called filter_datum that returns
    the log message obfuscated
    """
    for field in fields:
        message = re.sub(
                field+'=.*?'+separator,
                field+'='+redaction+separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
         filter values in incoming log records using filter_datum
        """
        message = super(RedactingFormatter, self).format(record)
        redact = filter_datum(
                self.fields,
                self.REDACTION,
                message,
                self.SEPARATOR)
        return redact


def get_logger() -> logging.Logger:
    """
    Returns the logging.Logging object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()

    formatter = RedactingFormatter(PII_FIELDS)

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    connect to a secure holberton database to read a users table.
    The database is protected by a username and password that are
    set as environment variables on the server named PERSONAL_DATA_DB_USERNAME
    (set the default as “root”), PERSONAL_DATA_DB_PASSWORD (set the default
    as an empty string) and PERSONAL_DATA_DB_HOST (set the default as
    “localhost”).
    """
    user = os.getenv('PERSONAL_DATA_DB_USERNAME') or 'root'
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ''
    host = os.getenv('PERSONAL_DATA_DB_HOST') or 'localhost'
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')
    con = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            database=db_name)
    return con


def main():
    """
    main function that takes no arguments and returns nothing.

    The function will obtain a database connection using get_db
    and retrieve all rows in the users table and display each
    row under a filtered format like this:
    """
    db = get_db()
    logger = get_logger()
    cursor = db.cursor()
    query = "SELECT * FROM users;"
    cursor.execute(query)
    fields = cursor.column_names
    for row in cursor:
        message = "".join("{}={}; ".format(k,v) for k, v in zip(fields, row))
        logger.info(message.strip())
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
