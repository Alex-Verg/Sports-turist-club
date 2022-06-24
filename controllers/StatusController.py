from models.User import User
from mysql.connector import Error
from exceptions.ErrorUserPermissions import ErrorUserPermissions
from controllers import RoleController


def get_status_list(cursor, connection, current_user: User, current_status):
    try:
        permission_role = RoleController.role_from_base(cursor, 'Club member')
        if not current_user.has_role(permission_role):
            raise ErrorUserPermissions
        else:
            select_query = """SELECT n.next_status AS id, s2.status, s2.closed
                                FROM status AS s1
                                LEFT JOIN next_statuses AS n
                                ON s1.id = n.status
                                LEFT JOIN status AS s2
                                ON n.next_status = s2.id
                                WHERE s1.status = %s
                                ORDER BY s2.id;"""
            cursor.execute(select_query, (current_status, ))
            records = cursor.fetchall()

            return records
    except Error as err:
        return err
    except ErrorUserPermissions as err:
        return err
