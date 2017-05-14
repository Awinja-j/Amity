class Room(object):
        def __init__(self, room_name):
            self.room_name = room_name
            self.occupants =[]


class Livingspace(Room):
        def __init__(self, room_name):
            Room.__init__(self, room_name)
            self.max_no_occupants = 6
            self.room_type = 'livingspace'

        def __repr__(self):
            return self.room_name, self.occupants

            
class Office(Room):
        def __init__(self, room_name):
           Room.__init__(self, room_name)
           self.max_no_occupants = 4
           self.room_type = 'office'

        def __repr__(self):
            return self.room_name, self.occupants
    