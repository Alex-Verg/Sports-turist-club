from controllers.interface import Interface

if __name__ == "__main__":
    cursor, connection = Interface.connect_to_db()
    Interface.clean()
    cursor.close()
    connection.close()
