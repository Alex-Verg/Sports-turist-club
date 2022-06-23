class ErrorUserPermissions(Exception):

    def __init__(self, message="You haven't permissions to do this action!"):
        self.message = message
        super().__init__(self.message)
