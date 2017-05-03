class Room(object):
        def __init__(self, room_type, room_name ):
            self.room_type = room_type
            self.room_name = room_name

class Livingspace(Room):
        def __init__(self, room_type, room_name):
            Room.__init__(self, room_type, room_name)
            self.capacity = 6
        def check_availability(self, available_room):
            for lv in self.Livingspace_room:
                if self.capacity < 6:
                    return available_room.append(lv)
            
            
class Office(Room):
        def __init__(self, room_type, room_name):
           Room.__init__(self, room_type, room_name)
           self.capacity = 4
        def check_availability(self):
            for o in self.Offices:
                if self.capacity < 4:
                    return Room.available_room.append(Office)

    