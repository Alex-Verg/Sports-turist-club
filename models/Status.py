class Status:

    def __init__(self, main_info, next_statuses):
        self.__id = main_info['id']
        self.__name = main_info['name']
        self.__closed = main_info['closed']
        self.__next_statuses = next_statuses

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, new_id):
        if not isinstance(new_id, int):
            raise ValueError('Non correct index type!')

        self.__id = new_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name

    @property
    def closed(self):
        return self.__closed

    @closed.setter
    def closed(self, new_closed):
        closed = new_closed

    @property
    def next_statuses(self):
        return self.__next_statuses

    @next_statuses.setter
    def next_statuses(self, new_next_statuses):
        self.__next_statuses = new_next_statuses
