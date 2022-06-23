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


if __name__ == "__main__":
    cursor, connection = Interface.connect_to_db()
    # print(UserController.insert_new_user(cursor, connection, 'MainAdmin', '12345',
    #                 'Main', 'Admin', '2022-06-23', 'mainadmin@gmail.com', '+380000000000'))
    current_user = UserController.authentication(cursor, connection, 'Sasha10', 'alex2002')
    # up_user = UserController.authentication(cursor, connection, 'Sasha10', 'alex2002')
    rest = {'age': '18+',
            'hiking experience': '1st category'}
    rest = json.dumps(rest)
    main_info = {
        'id': None,
        'name': '3nd Category Hiking in Carpathians',
        'description': 'Cool event!',
        'event_date': datetime.datetime(2023, 8, 1, 0, 0, 0, 0),
        'location': "Carpathian mountains",
        'price': 3000,
        'closed': 0
    }
    new_event = Event(main_info, EventType({"id": 1, "name": 'Hiking'}))
    answ = EventController.insert_new_event(cursor, connection, current_user, new_event)
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
