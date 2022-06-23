import datetime
import os
from controllers.Interface import Interface
from controllers import UserController
from models.User import User
from models.Role import Role


if __name__ == "__main__":
    cursor, connection = Interface.connect_to_db()
    print(UserController.insert_new_user(cursor, connection, 'MainAdmin', '12345',
                    'Main', 'Admin', '2022-06-23', 'mainadmin@gmail.com', '+380000000000'))
    current_user = UserController.authentication(cursor, connection, 'MainAdmin', '12345')
    answ = UserController.update_user(cursor, connection, current_user, current_user, Role({'id': 3, 'name': 'Manager'}))
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
