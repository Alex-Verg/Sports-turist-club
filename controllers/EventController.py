from mysql.connector import Error
from models.Event import Event
from models.User import User
from models.Status import Status
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

            event_query = """SELECT id FROM events WHERE name = %s"""
            cursor.execute(event_query, (new_event.name, ))
            new_event.id = cursor.fetchall()[0]['id']

            add_organaizer_in_participant_query = """INSERT INTO participants(event, participant, is_helper) VALUES 
                                                     (%s, %s, %s)"""
            cursor.execute(add_organaizer_in_participant_query, (new_event.id, current_user.id, 1))

            select_query = """SELECT * FROM events WHERE id = %s"""
            cursor.execute(select_query, (new_event.id,))
            previous_record = cursor.fetchall()[0]
            add_in_history_query = """INSERT INTO history_events(name, main_organaizer, status, type, description, 
                                                    event_date, location, price, changed_by, date_create, restrictions) VALUES 
                                                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """
            params = (previous_record['name'], previous_record['main_organaizer'], previous_record['status'],
                      previous_record['type'], previous_record['description'], previous_record['event_date'],
                      previous_record['location'], previous_record['price'], current_user.id,
                      previous_record['date_create'],
                      previous_record['restrictions'])
            cursor.execute(add_in_history_query, params)

            connection.commit()
    except Error as err:
        connection.rollback()
        return err
    except ErrorUserPermissions as err:
        return err


def update_event_status(cursor, connection, current_user: User, event: Event, next_status: Status):
    try:
        permission_role = RoleController.role_from_base(cursor, 'Manager')
        if not current_user.has_role(permission_role):
            raise ErrorUserPermissions
        else:
            update_event_query = """UPDATE events 
                              SET events.status = %s, 
                                  events.closed = %s,
                                  events.date_update = current_timestamp()
                              WHERE events.id = %s"""
            params = (next_status.id, next_status.closed, event.id)
            cursor.execute(update_event_query, params)
            event.closed = next_status.closed
            event.status = next_status

            select_query = """SELECT * FROM events WHERE id = %s"""
            cursor.execute(select_query, (event.id, ))
            previous_record = cursor.fetchall()[0]
            add_in_history_query = """INSERT INTO history_events(name, main_organaizer, status, type, description, 
                                        event_date, location, price, changed_by, date_create, restrictions) VALUES 
                                        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            params = (previous_record['name'], previous_record['main_organaizer'], previous_record['status'],
                      previous_record['type'], previous_record['description'], previous_record['event_date'],
                      previous_record['location'], previous_record['price'], current_user.id, previous_record['date_create'],
                      previous_record['restrictions'])
            cursor.execute(add_in_history_query, params)

            connection.commit()
    except Error as err:
        connection.rollback()
        return err
    except ErrorUserPermissions as err:
        return err


def get_events_for_update(cursor, connection, current_user: User):
    pass


def get_upcoming_events(cursor, connection, current_user: User):
    pass
