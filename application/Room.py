class Room(object):
        def __init__(self, room_name):
            self.room_name = room_name
            self.occupants =[]


class Livingspace(Room):
        def __init__(self, room_name):
            Room.__init__(self, room_name)
            self.max_no_occupants = 6
            self.room_type = 'livingspace'

        # def check_availability(self, available_room):
        #     for lv in self.Livingspace_room:
        #         if self.capacity < 6:
        #             return available_room.append(lv)
            
            
class Office(Room):
        def __init__(self, room_name):
           Room.__init__(self, room_name)
           self.max_no_occupants = 4
           self.room_type = 'office'

        # def check_availability(self):
        #     for o in self.Offices:
        #         if self.capacity < 4:
        #             return Room.available_room.append(Office)

    