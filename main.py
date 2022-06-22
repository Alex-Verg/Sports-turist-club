import datetime

from controllers.Interface import Interface
from controllers import UserController
from models.User import User
from models.Role import Role

if __name__ == "__main__":
    cursor, connection = Interface.connect_to_db()
    # print(UserController.insert_new_user(cursor, connection, "Sasha10", "alex2002", "Oleksandr", "Verg", "2002-03-08",
    #                                      "alexclub1@gmail.com", "+38111111111"))
    current_user = UserController.authentication(cursor, connection, 'Sasha10', 'alex2002')
    if isinstance(current_user, User):
        print(current_user.has_role('Admin'))
    cursor.close()
    connection.close()

    print(datetime)
