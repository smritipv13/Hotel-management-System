import os
from contextlib import contextmanager

import mysql.connector
from mysql.connector import Error


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "user": os.getenv("DB_USER", "root"),
    "password": os.getenv("DB_PASSWORD", ""),
    "port": int(os.getenv("DB_PORT", "3307")),
    "database": os.getenv("DB_NAME", "hotel_management"),
}


def get_connection():
    return mysql.connector.connect(**DB_CONFIG)


@contextmanager
def db_cursor(dictionary=True):
    connection = get_connection()
    cursor = connection.cursor(dictionary=dictionary)
    try:
        yield cursor
        connection.commit()
    except Error:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


def fetch_all(query, params=None):
    with db_cursor() as cursor:
        cursor.execute(query, params or ())
        return cursor.fetchall()


def fetch_one(query, params=None):
    with db_cursor() as cursor:
        cursor.execute(query, params or ())
        return cursor.fetchone()


def execute(query, params=None):
    with db_cursor() as cursor:
        cursor.execute(query, params or ())
        return cursor.lastrowid
