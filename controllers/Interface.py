import mysql.connector
from mysql.connector import Error
from configs import db_connection
import os
import getpass
import re
import time
from models.User import User
from models.Role import Role
from controllers import UserController
from controllers import RoleController
from controllers import EventController


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
    login_pattern = re.compile("^\w+$")
    login = input("Create your login (only letters, digits and _): ")
    while not (login_pattern.match(login)):
        login = input("Please, enter correct login: ")

    password1 = save_input("Create your password: ")
    password2 = save_input("Input same password: ")
    while password1 != password2:
        print("Please, enter equal password two times!")
        password1 = save_input("Create your password: ")
        password2 = save_input("Input same password: ")

    first_name_pattern = re.compile("^\w+\s?\w+$")
    first_name = input("Enter your first name: ")
    while not (first_name_pattern.match(first_name)):
        first_name = input("Please, enter correct first name: ")

    last_name_pattern = re.compile("^\w+\-?\w+$")
    last_name = input("Enter your last name: ")
    while not (last_name_pattern.match(last_name)):
        last_name = input("Please, enter correct last name: ")

    birth_date = input("Enter your birth_date in format yyyy-mm-dd: ")
    while not is_correct_date(birth_date, 'birth'):
        birth_date = input("Please, enter your birth_date in correct format yyyy-mm-dd: ")

    email_pattern = re.compile("^\w+\@[a-zA-Z]+[\.[a-zA-Z]+]?[a-zA-Z]$")
    email = input("Enter your email: ")
    while not (email_pattern.match(email)):
        last_name = input("Please, enter correct email: ")

    phone_pattern = re.compile("^\+\d{1,3}\d{9}$")
    phone = input("Enter your phone number: ")
    while not (phone_pattern.match(phone)):
        phone = input("Please, enter correct phone number+: ")

    result = UserController.insert_new_user(cursor, connection, login, password1, first_name, last_name, birth_date, email, phone)
    if isinstance(result, bool):
        clean()
        print("You successful create new account!")
        time.sleep(2)
        clean()
        current_user = UserController.authentication(cursor, connection, login, password1)
        role_menu(cursor, connection, current_user)
    else:
        clean()
        print("Oops, what's wrong :(\n")
        print(result)
        print("\nEnter anything to return to main menu.")
        save_input("")
        clean()


def role_menu(cursor, connection, current_user: User):
    while True:
        print("Enter number what you want to do:")
        user_role = RoleController.role_from_base(cursor, 'User')
        if current_user.has_role(user_role):
            print("1. View upcoming event")
            print("2. Take part in event")

        club_member_role = RoleController.role_from_base(cursor, 'Club member')
        if current_user.has_role(club_member_role):
            if not current_user.has_role(user_role):
                print("1. View upcoming event")
            print("3. Create new event")
            print("4. Help organaized event")

        manager_role = RoleController.role_from_base(cursor, 'Manager')
        if current_user.has_role(manager_role):
            print("5. Upgrade event")

        admin_role = RoleController.role_from_base(cursor, 'Admin')
        if current_user.has_role(admin_role):
            print("6. Give new role for user")
        print("7. Log out")

        while True:
            choice = input()
            try:
                choice = int(choice)
            except ValueError:
                print("You enter not number! Please enter correct item:")
                continue
            if choice == 1 and (current_user.has_role(user_role) or current_user.has_role(club_member_role)):
                clean()
                break
            if choice == 2 and current_user.has_role(user_role):
                clean()
                select_event_and_take_part(cursor, connection, current_user)
                break
            if choice == 3 and current_user.has_role(club_member_role):
                clean()
                create_event(cursor, connection, current_user)
                break
            if choice == 4 and current_user.has_role(club_member_role):
                clean()
                help_organaized_event(cursor, connection, current_user)
                break
            if choice == 5 and current_user.has_role(manager_role):
                clean()
                view_and_update_event(cursor, connection, current_user)
                break
            if choice == 6 and current_user.has_role(club_member_role):
                clean()
                view_and_update_user(cursor, connection, current_user)
                break
            if choice == 7:
                clean()
                print("You successful log out")
                time.sleep(2)
                return None
            else:
                print("You enter not correct number! Please enter correct item:")


def view_and_update_user(cursor, connection, current_user: User):
    result = UserController.get_user_list(cursor, connection, current_user)
    if isinstance(result, list):
        clean()
        print_list_of_dictionary(result, 'birth_date')
        needed_user_id = input("Enter id user for who you want give role: ")
        roles = RoleController.get_role_list(cursor, connection, current_user)
        print_list_of_dictionary(roles)
        needed_role_id = input("Enter id role what you want give: ")
        try:
            needed_user_id = int(needed_user_id)
            needed_role_id = int(needed_role_id)
            needed_user = search_attributes_in_list_by_id(result, needed_user_id)
            needed_role = search_attributes_in_list_by_id(roles, needed_role_id)
            new_role = Role(needed_role)
            UserController.update_user(cursor, connection, current_user, needed_user_id, new_role)
            clean()
            print("You successful add role {0} to user {1}".format(new_role.name, needed_user['login']))
            time.sleep(2)
        except Exception as err:
            clean()
            print("Oops, what's wrong :(\n")
            print(err)
            print("\nEnter anything to return to main menu.")
            save_input("")
            clean()
        clean()
    else:
        clean()
        print("Oops, what's wrong :(\n")
        print(result)
        print("\nEnter anything to return to main menu.")
        save_input("")
        clean()


def select_event_and_take_part(cursor, connection, current_user: User):
    result = EventController.get_upcoming_events(cursor, connection, current_user)
    if isinstance(result, list):
        print("Upcoming events: ")
        print_list_of_dictionary(result, 'event_date')
        needed_event_id = input("Enter id event in what you want take a part: ")
        try:
            needed_event_id = int(needed_event_id)
            UserController.take_part_in_event(cursor, connection, current_user, needed_event_id)
            clean()
            needed_event = search_attributes_in_list_by_id(result, needed_event_id)
            print("You successful registration to event {0}".format(needed_event['name']))
            time.sleep(5)
        except Exception as err:
            clean()
            print("Oops, what's wrong :(\n")
            print(err)
            print("\nEnter anything to return to main menu.")
            save_input("")
            clean()
        clean()
    else:
        clean()
        print("Oops, what's wrong :(\n")
        print(result)
        print("\nEnter anything to return to main menu.")
        save_input("")
        clean()


def create_event(cursor, connection, current_user: User):
    pass


def help_organaized_event(cursor, connection, current_user: User):
    result = EventController.get_upcoming_events(cursor, connection, current_user)
    if isinstance(result, list):
        print("Upcoming events: ")
        print_list_of_dictionary(result, 'event_date')
        needed_event_id = input("Enter id event what you want help organaize: ")
        try:
            needed_event_id = int(needed_event_id)
            UserController.help_organaize_event(cursor, connection, current_user, needed_event_id)
            clean()
            needed_event = search_attributes_in_list_by_id(result, needed_event_id)
            print("You successful registration to help organaize event {0}".format(needed_event['name']))
            time.sleep(5)
        except Exception as err:
            clean()
            print("Oops, what's wrong :(\n")
            print(err)
            print("\nEnter anything to return to main menu.")
            save_input("")
            clean()
        clean()
    else:
        clean()
        print("Oops, what's wrong :(\n")
        print(result)
        print("\nEnter anything to return to main menu.")
        save_input("")
        clean()


def view_and_update_event(cursor, connection, current_user: User):
    pass


def print_list_of_dictionary(records, date_field=None):
    names = records[0].keys()
    n = len(names)
    print(("{: <20}| "*n).format(*names))
    print("-"*22*n)
    for i in records:
        if 'restrictions' in names:
            i['restrictions'] = str(i['restrictions'] or '')
        if date_field is not None:
            i[date_field] = i[date_field].strftime("%m/%d/%Y, %H:%M:%S")
        rec = i.values()
        print(("{: <20}| "*n).format(*rec))


def search_attributes_in_list_by_id(records, need_id):
    for i in records:
        if i['id'] == need_id:
            return i


def save_input(message):
    if os.name == 'nt':
        password = getpass.getpass(prompt=message)
    else:
        print(message)
        os.system("stty -echo")
        password = input()
        os.system("stty echo")

    return password


def is_correct_date(date, date_type):
    return True
