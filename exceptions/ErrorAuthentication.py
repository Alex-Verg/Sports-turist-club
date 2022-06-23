class ErrorAuthentication(Exception):

    def __init__(self, message="You haven't access to this account!"):
        self.message = message
        super().__init__(self.message)
