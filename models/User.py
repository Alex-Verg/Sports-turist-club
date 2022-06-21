class User:

    def __init__(self):
        pass

    def login(self):
        pass

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
