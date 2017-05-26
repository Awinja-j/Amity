import random

from abc import ABCMeta, abstractmethod


class Room(object):
        __metaclass__ = ABCMeta

        @abstractmethod
        def __init__(self, room_name):
            self.room_name = room_name
            self.occupants =[]
            pin = random.randint(999, 9999)
            self.room_ID = pin


class Livingspace(Room):

        def __init__(self, room_name):
            Room.__init__(self, room_name)
            self.max_no_occupants = 6
            self.room_type = 'livingspace'

        def __repr__(self):
            return str(self.room_name)

            
class Office(Room):

        def __init__(self, room_name):
            Room.__init__(self, room_name)
            self.max_no_occupants = 4
            self.room_type = 'office'

        def __repr__(self):
            return str(self.room_name)
    