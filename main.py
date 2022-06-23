import datetime
import os
import json
from controllers.Interface import Interface
from controllers import UserController
from controllers import EventController
from models.User import User
from models.Role import Role
from models.EventType import EventType
from models.Event import Event
from models.Status import Status


if __name__ == "__main__":
    cursor, connection = Interface.connect_to_db()
    # print(UserController.insert_new_user(cursor, connection, 'MainAdmin', '12345',
    #                 'Main', 'Admin', '2022-06-23', 'mainadmin@gmail.com', '+380000000000'))
    current_user = UserController.authentication(cursor, connection, 'Sasha10', 'alex2002')
    # up_user = UserController.authentication(cursor, connection, 'Sasha10', 'alex2002')

    new_status = Status({
        "id": 4,
        "name": "Past",
        "closed": 0
    }, [])
    cursor.execute('SELECT id, name, description, event_date, location, price, closed FROM events WHERE id = 3')
    event = Event(cursor.fetchall()[0], EventType({'id': 1, 'name': 'Hiking'}))
    answ = EventController.update_event_status(cursor, connection, current_user, event, new_status)
    if isinstance(answ, Exception):
        print(answ)
    # select = "SELECT * FROM user_role"
    # cursor.execute(select)
    # rec = cursor.fetchall()
    # for i in rec:
    #     user, role = i.values()
    #     print("{:<10} {:<10}".format(user, role))
    cursor.close()
    connection.close()
