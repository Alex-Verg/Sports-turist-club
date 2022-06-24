class ErrorNotPastEvent(Exception):

    def __init__(self, message="This event has not yet taken place!"):
        self.message = message
        super().__init__(self.message)
