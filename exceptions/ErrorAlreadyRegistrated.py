class ErrorAlreadyRegistrated(Exception):

    def __init__(self, message="You already registrated!"):
        self.message = message
        super().__init__(self.message)
