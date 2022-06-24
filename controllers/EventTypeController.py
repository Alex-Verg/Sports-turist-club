from models.EventType import EventType
from models.User import User
from mysql.connector import Error
from exceptions.ErrorUserPermissions import ErrorUserPermissions
from controllers import RoleController


def event_type_from_base(cursor, needed_type):
    select_role = """SELECT *
                     FROM type
                     WHERE name = %s"""
    cursor.execute(select_role, (needed_type,))
    return EventType(cursor.fetchall()[0])


def get_event_type_list(cursor, connection, current_user: User):
    try:
        permission_role = RoleController.role_from_base(cursor, 'Club member')
        if not current_user.has_role(permission_role):
            raise ErrorUserPermissions
        else:
            select_query = """SELECT * FROM type"""
            cursor.execute(select_query)
            records = cursor.fetchall()

            return records
    except Error as err:
        return err
    except ErrorUserPermissions as err:
        return err
