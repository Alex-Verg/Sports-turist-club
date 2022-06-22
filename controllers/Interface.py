import mysql.connector
from mysql.connector import Error
from configs import db_connection
import os


class Interface:

    @staticmethod
    def connect_to_db():
        try:
            print(db_connection.database)
            connection = mysql.connector.connect(host=db_connection.host,
                                                 database=db_connection.database,
                                                 user=db_connection.user,
                                                 password=db_connection.password)
            if connection.is_connected():
                db_info = connection.get_server_info()
                # print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor(dictionary=True)
                cursor.execute("select database();")
                record = cursor.fetchone()
                # print("You're connected to database: ", record)
            return cursor, connection
        except Error as e:
            print("Error while connecting to MySQL", e)

    @staticmethod
    def clean():
        os.system('cls' if os.name == 'nt' else 'clear')
