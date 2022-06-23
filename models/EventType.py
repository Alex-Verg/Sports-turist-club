class EventType:

    def __init__(self, main_info):
        self.__id = main_info['id']
        self.__name = main_info['name']

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, new_id):
        if not isinstance(new_id, int):
            raise ValueError('Non correct index type')

        self.__id = new_id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, new_name):
        self.__name = new_name
