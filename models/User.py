import datetime


class User:

    def __init__(self, main_info, roles):
        self.__id = main_info['id']
        self.__login = main_info['login']
        self.__password = main_info['password']
        self.__first_name = main_info['first_name']
        self.__last_name = main_info['last_name']
        self.__birth_date = main_info['birth_date']
        self.__email = main_info['email']
        self.__phone = main_info['phone']
        self.__roles = roles

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, new_id):
        if not isinstance(new_id, int):
            raise ValueError('Not int type for id!')
        else:
            self.__id = new_id

    @property
    def login(self):
        return self.__login

    @login.setter
    def login(self, new_login):
        self.__login = new_login

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, new_password):
        self.__password = new_password

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, new_first_name):
        self.__first_name = new_first_name

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, new_last_name):
        self.__last_name = new_last_name

    @property
    def birth_date(self):
        return self.__birth_date

    @birth_date.setter
    def birth_date(self, new_birth_date):
        if not isinstance(new_birth_date, datetime.datetime):
            raise ValueError('Not datetime type for birth date!')
        else:
            self.__birth_date = new_birth_date

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, new_email):
        self.__email = new_email

    @property
    def phone(self):
        return self.__phone

    @phone.setter
    def phone(self, new_phone):
        self.__phone = new_phone

    @property
    def roles(self):
        return self.__roles

    @roles.setter
    def roles(self, new_roles):
        self.__roles = new_roles

    def has_role(self, needed_role):
        filter_role = [role for role in self.roles if role.name == needed_role]
        return bool(filter_role)

    def view_users(self):
        if 'Admin' in self.roles:
            pass
        else:
            pass

    def add_user_role(self, another_user):
        if 'Admin' in self.roles:
            pass
        else:
            pass

    def view_upcoming_events(self):
        if 'User' in self.roles:
            pass
        else:
            pass

    def participate_in_events(self, event):
        if 'User' in self.roles:
            pass
        else:
            pass

    # additional function
    # def make_feedback_about_event(self, event):
    #     if 'User' in self.roles:
    #         pass
    #     else:
    #         pass

    def create_event(self):
        if 'Club member' in self.roles:
            pass
        else:
            pass

    def help_organize(self, event):
        if 'Club member' in self.roles:
            pass
        else:
            pass

    def update_event_status(self, event):
        if 'Manager' in self.roles:
            pass
        else:
            pass

    def logout(self):
        pass
