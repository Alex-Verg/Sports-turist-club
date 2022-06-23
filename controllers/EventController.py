from mysql.connector import Error
from models.Event import Event
from models.User import User
from exceptions.ErrorUserPermissions import ErrorUserPermissions
from controllers import RoleController


def insert_new_event(cursor, connection, current_user: User, new_event: Event):
    try:
        permission_role = RoleController.role_from_base(cursor, 'Club member')
        if not current_user.has_role(permission_role):
            raise ErrorUserPermissions
        else:
            new_role_query = """INSERT INTO events(name, main_organaizer, type, description, event_date, location, price, restrictions) VALUES 
                                (%s, %s, %s, %s, %s, %s, %s, %s)"""
            params = (new_event.name, current_user.id, new_event.event_type.id, new_event.description, new_event.event_date, new_event.location, new_event.price, new_event.restrictions)
            cursor.execute(new_role_query, params)
            connection.commit()
    except Error as err:
        connection.rollback()
        return err
    except ErrorUserPermissions as err:
        return err
