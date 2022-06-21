import mysql.connector
from mysql.connector import Error
import os
import hashlib


def hash_password(salt, password):
    hash_pass = hashlib.pbkdf2_hmac('sha256',
                                    password.encode('utf-8'),
                                    salt,
                                    100000,
                                    dklen=255)

    return hash_pass


def insert_new_user(cursor, connection, login, password, first_name, last_name, birth_date, email, phone):
    try:
        insert_query = "INSERT INTO users (login, password, first_name, last_name, birth_date, email, phone) VALUES" \
                       " (%s, %s, %s, %s, %s, %s, %s)"
        salt = os.urandom(32)
        hash_pass = hash_password(salt, password)
        params = (login, hash_pass, first_name, last_name, birth_date, email, phone)
        cursor.execute(insert_query, params)

        select_query = "SELECT id FROM users WHERE login = %s"
        cursor.execute(select_query, (login,))
        user_id = cursor.fetchall()[0][0]

        select_query = "SELECT id FROM role WHERE login = 'User'"
        cursor.execute(select_query)
        role_id = cursor.fetchall()[0][0]

        insert_query = "INSERT INTO user_role (user, role) VALUES (%s, %s)"
        cursor.execute(insert_query, (user_id, role_id))
        connection.commit()
        return False

    except Error as err:
        return err
