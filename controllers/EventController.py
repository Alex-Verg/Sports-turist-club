import datetime
from mysql.connector import Error
from models.Event import Event
from models.User import User
from models.Status import Status
from exceptions.ErrorUserPermissions import ErrorUserPermissions
from exceptions.ErrorNotPastEvent import ErrorNotPastEvent
from controllers import RoleController


def insert_new_event(cursor, connection, current_user: User, new_event: Event):
    try:
        permission_role = RoleController.role_from_base(cursor, 'Club member')
        if not current_user.has_role(permission_role):
            raise ErrorUserPermissions
        else:
            new_event_query = """INSERT INTO events(name, main_organaizer, type, description, event_date, location, price, restrictions) VALUES 
                                (%s, %s, %s, %s, %s, %s, %s, %s)"""
            params = (new_event.name, current_user.id, new_event.event_type.id, new_event.description, new_event.event_date, new_event.location, new_event.price, new_event.restrictions)
            cursor.execute(new_event_query, params)

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

            return True
    except Error as err:
        connection.rollback()
        return err
    except ErrorUserPermissions as err:
        return err


def update_event_status(cursor, connection, current_user: User, event_id, next_status: Status):
    try:
        permission_role = RoleController.role_from_base(cursor, 'Manager')
        if not current_user.has_role(permission_role):
            raise ErrorUserPermissions
        else:
            if next_status.name == 'Past':
                date_event_query = """SELECT event_date FROM events WHERE id = %s"""
                cursor.execute(date_event_query, (event_id,))
                date_event = cursor.fetchall()[0]['event_date']
                if date_event > datetime.datetime.now():
                    raise ErrorNotPastEvent

            update_event_query = """UPDATE events 
                                              SET events.status = %s, 
                                                  events.closed = %s,
                                                  events.date_update = current_timestamp()
                                              WHERE events.id = %s"""
            params = (next_status.id, next_status.closed, event_id)
            cursor.execute(update_event_query, params)

            select_query = """SELECT * FROM events WHERE id = %s"""
            cursor.execute(select_query, (event_id,))
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
    except (ErrorUserPermissions, ErrorNotPastEvent) as err:
        return err


def get_events_for_update(cursor, connection, current_user: User):
    try:
        permission_role = RoleController.role_from_base(cursor, 'Manager')
        if not current_user.has_role(permission_role):
            raise ErrorUserPermissions
        else:
            select_query = """SELECT e.id, e.name, concat(u.first_name, ' ', u.last_name) AS organaizer, s.status, t.name AS type,
                                e.description, e.event_date, e.location, e.price, e.restrictions
                                FROM events AS e
                                LEFT JOIN users AS u
                                ON e.main_organaizer = u.id
                                LEFT JOIN type AS t
                                ON e.type = t.id
                                LEFT JOIN status AS s
                                ON e.status = s.id
                                WHERE (e.closed = 0) AND ((e.status != (SELECT id FROM status WHERE status = 'Upcoming')
                                OR (e.event_date < current_timestamp ())))"""
            cursor.execute(select_query)
            records = cursor.fetchall()

            return records
    except Error as err:
        return err
    except ErrorUserPermissions as err:
        return err


def get_upcoming_events(cursor, connection, current_user: User):
    try:
        permission_role = RoleController.role_from_base(cursor, 'User')
        if not current_user.has_role(permission_role):
            raise ErrorUserPermissions
        else:
            select_query = """SELECT e.id, e.name, concat(u.first_name, ' ', u.last_name) AS organaizer, t.name AS type,
                                e.description, e.event_date, e.location, e.price, e.restrictions
                                FROM events AS e
                                LEFT JOIN users AS u
                                ON e.main_organaizer = u.id
                                LEFT JOIN type AS t
                                ON e.type = t.id
                                WHERE e.status = (SELECT id from status WHERE status = 'Upcoming')
                                ORDER BY e.id"""
            cursor.execute(select_query)
            records = cursor.fetchall()

            return records
    except Error as err:
        return err
    except ErrorUserPermissions as err:
        return ErrorUserPermissions


def view_my_organaize_upcoming_event(cursor, connection, current_user: User):
    try:
        permission_role = RoleController.role_from_base(cursor, 'Club member')
        if not current_user.has_role(permission_role):
            raise ErrorUserPermissions
        else:
            main_organaizer_query = """SELECT e.id, e.name, t.name AS type,
                                        e.description, e.event_date, e.location, e.price, e.restrictions
                                        FROM events AS e
                                        LEFT JOIN type AS t
                                        ON e.type = t.id
                                        WHERE e.status = (SELECT id from status WHERE status = 'Upcoming') AND e.main_organaizer = %s
                                        ORDER BY e.id"""
            cursor.execute(main_organaizer_query, (current_user.id, ))
            records = cursor.fetchall()

            return records
    except Error as err:
        return err
    except ErrorUserPermissions as err:
        return err
