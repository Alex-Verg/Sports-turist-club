import mysql.connector
from mysql.connector import Error
from configs import db_connection
import os
import getpass
import re
import time
from models.User import User
from controllers import UserController


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


def clean():
    os.system('cls' if os.name == 'nt' else 'clear')


def first_menu(cursor, connection):
    clean()
    print("Hello! This is application with database of events in sport tourist club!")
    while True:
        print("Enter number what you want to do:")
        print("1. Log in")
        print("2. Sign up")
        print("3. Exit")
        while True:
            choice = input()
            try:
                choice = int(choice)
            except ValueError:
                print("You enter not number! Please enter correct item:")
                continue
            if choice == 1:
                clean()
                log_in(cursor, connection)
                break
            if choice == 2:
                clean()
                sign_up(cursor, connection)
                break
            if choice == 3:
                clean()
                print("Goodbye!")
                return None
            else:
                print("You enter not correct number! Please enter correct item:")


def log_in(cursor, connection):
    pattern = re.compile("^\w+$")
    login = input("Enter your login (only letters, digits and _): ")
    while not (pattern.match(login)):
        login = input("Please, enter correct login: ")
    password = save_input("Enter your password: ")
    current_user = UserController.authentication(cursor, connection, login, password)
    if isinstance(current_user, User):
        clean()
        print("You successful log in in your account!")
        time.sleep(2)
        clean()
        role_menu(cursor, connection, current_user)
    else:
        clean()
        print("Oops, what's wrong :(\n")
        print(current_user)
        print("\nEnter anything to return to main menu.")
        save_input("")
        clean()


def sign_up(cursor, connection):
    pass


def role_menu(cursor, connection, current_user: User):
    pass


def view_and_update_user(cursor, connection, current_user: User):
    pass


def upcoming_events(cursor, connection, current_user: User):
    pass


def select_event_and_take_part(cursor, connection, current_user: User):
    pass


def create_event(cursor, connection, current_user: User):
    pass


def help_organaized_event(cursor, connection, current_user: User):
    pass


def view_and_update_event(cursor, connection, current_user: User):
    pass


def print_list_of_dictionary(cursor, connection, current_user: User):
    pass


def save_input(message):
    if os.name == 'nt':
        password = getpass.getpass(prompt=message)
    else:
        print(message)
        os.system("stty -echo")
        password = input()
        os.system("stty echo")

    return password
