from models.Role import Role
from models.User import User
from mysql.connector import Error
from exceptions.ErrorUserPermissions import ErrorUserPermissions


def role_from_base(cursor, needed_role):
    select_role = """SELECT *
                     FROM role
                     WHERE name = %s"""
    cursor.execute(select_role, (needed_role,))
    return Role(cursor.fetchall()[0])


def get_role_list(cursor, connection, current_user: User):
    try:
        permission_role = role_from_base(cursor, 'Admin')
        if not current_user.has_role(permission_role):
            raise ErrorUserPermissions
        else:
            select_query = """SELECT * FROM role ORDER BY id"""
            cursor.execute(select_query)
            records = cursor.fetchall()

            return records
    except Error as err:
        return err
    except ErrorUserPermissions as err:
        return err
