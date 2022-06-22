from mysql.connector import Error
import os
import hashlib
from models.User import User
from models.Role import Role


class ErrorAuthentication(Exception):

    def __init__(self):
        super().__init__("You haven't access to this account!")


def hash_password(salt, password):
    hash_pass = hashlib.pbkdf2_hmac('sha256',
                                    password.encode('utf-8'),
                                    salt,
                                    100000,
                                    dklen=95)

    return hash_pass.hex()


def insert_new_user(cursor, connection, login, password, first_name, last_name, birth_date, email, phone):
    try:
        insert_query = """INSERT INTO users (login, password, first_name, last_name, birth_date, email, phone) VALUES 
                       (%s, %s, %s, %s, %s, %s, %s)"""
        salt = os.urandom(32)
        hash_pass = salt.hex() + hash_password(salt, password)

        params = (login, hash_pass, first_name, last_name, birth_date, email, phone)
        cursor.execute(insert_query, params)

        select_query = "SELECT id FROM users WHERE users.login = %s"
        cursor.execute(select_query, (login,))
        user_id = cursor.fetchall()[0][0]

        select_query = "SELECT id FROM role WHERE name = 'User'"
        cursor.execute(select_query)
        role_id = cursor.fetchall()[0][0]

        insert_query = "INSERT INTO user_role (user, role) VALUES (%s, %s)"
        cursor.execute(insert_query, (user_id, role_id))
        connection.commit()
        return False

    except Error as err:
        return err


def autorization(cursor, connection, login, password):
    try:
        select_login = "SELECT password, enabled FROM users WHERE users.login = %s"
        cursor.execute(select_login, (login,))
        base_password, enabled = cursor.fetchall()[0].values()
        salt = base_password[:64]
        salt = bytes.fromhex(salt)
        if (base_password == salt.hex() + hash_password(salt, password)) and enabled:
            select_login = "SELECT * FROM users WHERE users.login = %s"
            cursor.execute(select_login, (login,))
            record = cursor.fetchall()[0]
            user_id = record['id']
            select_user_roles = """SELECT role, name 
                                   FROM user_role AS u
                                   INNER JOIN role AS r
                                   ON u.role = r.id
                                   WHERE u.user = %s"""
            cursor.execute(select_user_roles, (user_id,))
            roles = cursor.fetchall()
            roles = [Role(i['role'], i['name']) for i in roles]
            return User(record, roles)
        else:
            raise ErrorAuthentication
    except Error as err:
        return err
    except ErrorAuthentication as err:
        return err
