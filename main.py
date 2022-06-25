import datetime
import os
import json
from controllers import Interface
from controllers import UserController
from controllers import EventController
from controllers import EventTypeController
from models.User import User
from models.Role import Role
from models.EventType import EventType
from models.Event import Event
from models.Status import Status


if __name__ == "__main__":
    cursor, connection = Interface.connect_to_db()
    Interface.first_menu(cursor, connection)
    cursor.close()
    connection.close()
