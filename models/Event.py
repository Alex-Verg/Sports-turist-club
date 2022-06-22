import json
from Status import Status
from EventType import EventType
import datetime


class Event:

    def __init__(self, main_info, status, event_type, restrictions):
        self.__id = main_info['id']
        self.__name = main_info['name']

        self.__status = status
        self.__event_type = event_type
        self.__description = main_info['description']
        self.__event_date = main_info['event_date']
        self.__location = main_info['location']
        self.__price = main_info['price']
        self.__closed = main_info['closed']
        self.__restrictions = restrictions

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
    def status(self):
        return self.__status

    @status.setter
    def status(self, new_status):
        if not isinstance(new_status, Status):
            ValueError('Not Status type for event status!')
        else:
            self.__status = new_status

    @property
    def event_type(self):
        return self.__event_type

    @event_type.setter
    def event_type(self, new_type):
        if not isinstance(new_type, EventType):
            ValueError('Not EventType type for event type!')
        else:
            self.__event_type = new_type

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, new_description):
        self.__description = new_description

    @property
    def event_date(self):
        return self.__event_date

    @event_date.setter
    def event_date(self, new_event_date):
        if not isinstance(new_event_date, datetime.datetime):
            raise ValueError('Not datetime type for birth date!')
        else:
            self.__event_date = new_event_date

    @property
    def location(self):
        return self.__location

    @location.setter
    def location(self, new_location):
        self.__location = new_location

    @property
    def price(self):
        return self.__price

    @price.setter
    def price(self, new_price):
        if not isinstance(new_price, (int, float)):
            ValueError('Not int or float type for price!')
        else:
            self.__price = round(new_price, 2)

    @property
    def closed(self):
        return self.__closed

    @closed.setter
    def closed(self, new_closed):
        self.__closed = bool(new_closed)

    @property
    def restriction(self):
        return self.__restrictions

    @restriction.setter
    def restriction(self, new_restriction):
        self.__restrictions = json.dumps(new_restriction)

    def is_type(self, needed_type):
        return self.event_type == needed_type.name
