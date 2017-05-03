from Room import Room, Office, Livingspace
from Person import Person, Staff, Fellow
import random
from twilio.rest import Client

# put your own credentials here
account_sid = 'ACc684e833e5afc573a4cccee306537e95'
auth_token = "8d835935196f549c04527d55adeac603"

class Amity(object):
    ''' this application should be able to be installed using a package '''
    ''' this applicaation should be linked to firebase '''
    ''' on add person,if person has a phone number, the person will be sent a text message with the room they have been allocated '''
    def __init__(self):
        self.all_staff = []
        self.all__fellow = []
        self.all_people = []
        self.lv_allocations = []
        self.office_allocations = []
        self.available_room = []
        self.all_offices = []
        self.all_Livingspace = []
        self.all_rooms = []

    def check_available_rooms(self):
        if not self.available_room:
            return "There are no rooms available, Please use the create command to make Rooms"
        else:
            for room in self.available_room:
                if room.room_type == "Office":
                    return room
                elif room.room_type == "Livingspace":
                    return room


    def create_room(self, room_type, room_name):
            if room_type == 'Office':

                if self.all_offices:
                    for item in self.all_offices:
                        if item.room_name == room_name:
                            return (item.room_name + 'already exists in Amity')
                        else:
                            office = Office(room_type, room_name)
                            self.all_offices.append(office)
                            return 'Room has been added succesfully!!'
                else:
                    office = Office(room_type, room_name)
                    self.all_offices.append(office)
                    return 'Room has been added succesfully!!'
            if room_type == 'Livingspace':
                if self.all_Livingspace:
                    for item in self.all_Livingspace:
                        if item == room_name:
                            return (item.room_name + 'already exists in Amity')
                        else:
                            lv = Livingspace(room_type, room_name)
                            return self.all_Livingspace.append(lv)
                else:
                    lv = Livingspace(room_type, room_name)
                    self.all_Livingspace.append(lv)
                    return 'Room has been added succesfully!!'

    def add_person(self, person_name, person_role, person_accomodation, person_phone):
        if person_role == 'STAFF':
            staff = Staff(person_name, person_role, person_accomodation, person_phone)
            if staff.person_name not in self.all_staff:
                    if staff.person_accomodation == "N" or "":
                        if staff.person_phone == '':
                            self.all_staff.append(staff)
                            return staff.person_name + 'has been succesfully added to Amity'
                        else:
                            self.all_staff.append(staff)
                            client = Client(account_sid, auth_token)
                            client.messages.create(
                                to=person_phone,
                                from_="+14026206866",
                                body='Hello' + staff.person_name + ', ' + 'you have been succesfully added to Amity')
                    else:
                        if staff.person_phone == '':
                            self.all_staff.append(staff)
                            office_all = random.choice(self.available_room)
                            self.office_allocations = office_all.append(staff)
                            return staff.person_name + 'Has been allocated to' + office_all + 'succesfully!!'
                        else:
                            self.all_staff.append(staff)
                            office_all = random.choice(self.available_room)
                            office_all.append(staff)
                            client = Client(account_sid, auth_token)
                            client.messages.create(
                                to=person_phone,
                                from_='+14026206866',
                                body='Hello' + staff.person_name + ', ' + 'you have been allocated to' + office_all + 'succesfully!!. Amity')
            else:
                return "This Name Combination already exist in Amity. Please use the Edit or Delete Command to Modify Entry."
        if person_role == 'FELLOW':
            fellow = Fellow(person_name, person_role, person_accomodation, person_phone)
            if fellow.person_name not in self.all_fellow:
                    if fellow.person_accomodation == 'N' or '':
                        if fellow.person_phone == '':
                            self.all_fellow.append(fellow)
                            return fellow.person_name + 'has been succesfully added to Amity'
                        else:
                            self.all_fellow.append(fellow)
                            client = Client(account_sid, auth_token)
                            client.messages.create(
                                to=person_phone,
                                from_="+14026206866",
                                body='Hello' + fellow.person_name + ', ' + 'has been succesfully added to Amity')

                    else:
                        if fellow.person_phone == '':
                            self.all_fellow.append(fellow)
                            lv_all = random.choice(self.available_room)
                            lv_all.append(fellow)
                            return fellow.person_name + 'has been allocated to' + lv_all + 'succesfully!!'
                        else:
                            self.all_fellow.append(fellow)
                            lv_all = random.choice(self.available_room)
                            lv_all.append(fellow)
                            client = Client(account_sid, auth_token)
                            client.messages.create(
                                to=person_phone,
                                from_='+14026206866',
                                body='Hello' + fellow.person_name + ', ' + 'you have been allocated to' + lv_all + 'succesfully!!')
            else:
                return 'This Name Combination already exist in Amity. Please use the Edit or Delete Command to Modify Entry.'


    def edit_person_info(self, entry):
        '''this edits a persons name'''
        self.all_people = self.all_staff + self.all__fellow
        if self.all_people:
                if len(entry) > 1:
                    value = ('which' + entry + '? Please Enter their index number')
                    for a_name in entry:
                        if self.all_people.index(a_name) is int(value):
                            person = Person()
                            self.all_people.replace(person)
                else:
                    person = Person()
                    self.all_people.replace(person)

        if not self.all_staff or self.all__fellow:
                return 'This entry cannot be found in Amity'
    def reallocate_person(self, person_name,room_name):
        '''this reallocates a person to the next available room'''
        for person in self.all_people:
            if len(person_name) > 1:
                value = ('which' + person_name + '? Please Enter their index number')
                for a_name in person_name:
                    if self.all_people.index(a_name) is int(value):
                        if person.person_role == "STAFF":
            else:
                    if person.person_name == person_name:
                        if person.person_role == "STAFF":
                            for room in self.available_room:
                                if (room.room_name == room_name) and (room.room_type == "Office"):
                                    self.remove()
                            else:
                                return room_name + 'has no available space'
                        else:
                            for room in self.available_room:
                                if (room.room_name == room_name):
                                    return person_name + 'has been reallocated succesfully to ' + room_name
        else:
            return person_name + 'Is not in Amity'

    def allocate_unallocated_person(self, entry):
        ''' this allocates a student who didnt want accomodation but would like accomodation now, a living space'''
        if self.all_people:

    def Delete_person(self, entry):
        ''' this deletes a person from the system'''
        self.all_people = self.all_staff + self.all__fellow
        if self.all_people:
                if len(entry) > 1:
                    value = ('which' + entry + '? Please Enter their index number')
                    for a_name in entry:
                        if self.all_people.index(a_name) is int(value):
                            self.all_people.remove(a_name)
                            return a_name + 'has been deleted succesfully!!'
                else:
                    self.all_people.remove(entry)
                    return entry + 'has been removed succesfully!!'
        if not self.all_people:
                return 'This entry cannot be found in Amity'

        pass
    def loadpeople(self, filename):
        '''loads people from text file filename.txt'''
        person_details = open(filename, 'r')
        for info in person_details:
            self.all_people.append(info.strip())
            if person_role == "STAFF":
                staff = Staff(person_name, person_role, person_accomodation, person_phone)
                if person_accomodation == "N" or "":
                    self.all_people.append(info.strip())
                else:

                self.all_people.append(info.strip())

    def printallocation(self):
        '''prints office and livingspace  allocation for fellows and staff
            you can also choose to optionally save them to a text file'''

        pass
    def printunallocated(self):
        '''prints fellows and staff who have not been allocated to rooms
            you can also choose to optionally save them to a text file'''
        pass
    def printroom(self, room_name):
        ''' this prints the members of a room once a name is given'''
        pass
    def savestate(self, db_name):
        ''' this saves all the information to an sqlite db '''
        pass
    def loadstate(self, db_name):
        ''' this loads all the data from an sqlite db into the application '''
        pass
    def edit_room_info(self, entry):
        ''' this edits a room type from both db and list'''
        self.all_rooms = self.all_offices + self.all_livingspace
        if self.all_rooms:
            if len(entry) > 1:
                value = ('which' + entry + '? Please Enter their index number')
                for a_room in entry:
                    if self.all_rooms.index(a_room) is int(value):
                        room = Room()
                        self.all_rooms.replace(room)
                        return entry + 'has been edited succesfully!!'
            else:
                room = Room()
                self.all_rooms.replace(room)
                return entry + 'has been edited succesfully'

        if not self.all_rooms:
            return 'This entry cannot be found in Amity'

    def Delete_a_room(self, entry):
        '''this deletes a room from the Amity '''
        self.all_rooms = self.all_offices + self.all_livingspace
        if self.all_rooms:
                if len(entry) > 1:
                    value = ('which' + entry + '? Please Enter their index number')
                    for a_room in entry:
                        if self.all_rooms.index(a_room) is int(value):
                            self.all_people.remove(a_room)
                            return a_room + 'has been deleted succesfully!!'
                else:
                    self.all_people.remove(entry)
                    return entry + 'has been deleted succesfully'

        if not self.all_rooms:
                return 'This entry cannot be found in Amity'

         
   