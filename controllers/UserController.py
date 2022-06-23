from mysql.connector import Error
import os
import hashlib
from models.User import User
from models.Role import Role
from models.Event import Event
from exceptions.ErrorAuthentication import ErrorAuthentication
from exceptions.ErrorUserPermissions import ErrorUserPermissions
from controllers import RoleController


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
        user_id = cursor.fetchall()[0]['id']

        select_query = "SELECT id FROM role WHERE name = 'User'"
        cursor.execute(select_query)
        role_id = cursor.fetchall()[0]['id']

        insert_query = "INSERT INTO user_role (user, role) VALUES (%s, %s)"
        cursor.execute(insert_query, (user_id, role_id))
        connection.commit()
        return True

    except Error as err:
        connection.rollback()
        return err


def authentication(cursor, connection, login, password):
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
            select_user_roles = """SELECT id, name 
                                   FROM user_role AS u
                                   INNER JOIN role AS r
                                   ON u.role = r.id
                                   WHERE u.user = %s"""
            cursor.execute(select_user_roles, (user_id,))
            roles = cursor.fetchall()
            roles = [Role(i) for i in roles]
            return User(record, roles)
        else:
            raise ErrorAuthentication
    except Error as err:
        return err
    except ErrorAuthentication as err:
        return err


def update_user(cursor, connection, current_user: User, update_user: User, new_role: Role):
    try:
        permission_role = RoleController.role_from_base(cursor, 'Admin')
        if not current_user.has_role(permission_role):
            raise ErrorUserPermissions
        else:
            new_role_query = """INSERT INTO user_role(user, role) VALUES (%s, %s)"""
            cursor.execute(new_role_query, (update_user.id, new_role.id))
            update_user.roles.append(new_role)

            date_modified_query = """UPDATE users SET date_modified = current_timestamp() WHERE id = %s"""
            cursor.execute(date_modified_query, (current_user.id, ))

            connection.commit()
    except Error as err:
        connection.rollback()
        return err
    except ErrorUserPermissions as err:
        return err


def help_organaize_event(cursor, connection, current_user: User, event: Event):
    pass


def take_part_in_event(cursor, connection, current_user: User, event: Event):
    pass


def view_event_participant(cursor, connection, current_user: User, event: Event):
    pass


def get_user_list(cursor, connection, current_user: User):
    pass
