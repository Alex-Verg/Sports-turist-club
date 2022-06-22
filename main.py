from controllers.Interface import Interface
from controllers import UserController

if __name__ == "__main__":
    cursor, connection = Interface.connect_to_db()
    # print(UserController.insert_new_user(cursor, connection, "Sasha10", "alex2002", "Oleksandr", "Verg", "2002-03-08",
    #                                      "alexclub1@gmail.com", "+38111111111"))
    print(UserController.autorization(cursor, connection, 'Sasha10', 'alex2002'))
    cursor.close()
    connection.close()
