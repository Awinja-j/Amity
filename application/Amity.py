from Room import Room, Office, Livingspace
from Person import Person, Staff, Fellow
import random
from pprint import pprint
from twilio.rest import Client

# put your own credentials here
account_sid = 'ACc684e833e5afc573a4cccee306537e95'
auth_token = "8d835935196f549c04527d55adeac603"

class Amity(object):
    ''' this application should be able to be installed using a package '''
    ''' on add person,if person has a phone number, the person will be sent a text message with the room they have been allocated '''
    def __init__(self):
        self.all_staff = []
        self.all_fellow = []
        self.all_people = self.all_staff + self.all_fellow
        self.livingspace_allocations = []
        self.office_allocations = []
        self.all_allocations = self.livingspace_allocations + self.office_allocations
        self.available_room = []
        self.all_offices = []
        self.all_livingspace = []
        self.all_rooms = self.all_offices + self.all_livingspace

    def get_available_room(self, arg):
        room_list = [key for key in arg
                     if len(key.occupants) < key.max_no_occupants]
        return room_list

    def create_room(self, room_type, room_name):
        room_type = room_type.lower()
        room_names = [room.room_name for room in self.all_offices]
        room_names1 = [room.room_name for room in self.all_livingspace]

        for name in room_name:
            name = name.lower()
            if room_type == 'office':
                if name in room_names:
                    print('This office name already exists in Amity')
                else:
                    office = Office(name)
                    self.all_offices.append(office)
                    print('Office space ' + name + ' has been created succesfully!!')

            else:
                    if name in room_names1:
                        print('This livingspace name already exists in Amity')
                    else:
                        lv = Livingspace(name)
                        self.all_livingspace.append(lv)
                        print('Livingspace ' + name + ' has been created succesfully!!')

    def add_person(self, person_name, person_role, want_accomodation, phone_number):
        person_name = person_name.lower()
        person_role = person_role.lower()
        want_accomodation = want_accomodation.lower()
        if person_role == 'staff':
                if want_accomodation == "n":
                    if not phone_number:
                        staff = Staff(person_name, want_accomodation, phone_number)
                        self.all_staff.append(staff)
                        print(staff.person_name + 'has been succesfully added to Amity')
                    else:
                        staff = Staff(person_name, want_accomodation, phone_number)
                        self.all_staff.append(staff)
                        client = Client(account_sid, auth_token)
                        client.messages.create(
                            to=phone_number,
                            from_="+14026206866",
                            body='Hello' + staff.person_name + ', ' + 'you have been succesfully added to Amity')
                        print('Hooray!')
                else:
                    if self.all_offices:
                        if not phone_number:
                            staff = Staff(person_name, want_accomodation, phone_number)
                            self.all_staff.append(staff)
                            room = random.choice(self.get_available_room(self.all_offices))
                            room.occupants.append(staff)
                            print(staff.person_name + 'Has been allocated to' + room.room_name + 'succesfully!!')
                        else:
                            staff = Staff(person_name, want_accomodation, phone_number)
                            self.all_staff.append(staff)
                            room = random.choice(self.get_available_room(self.all_offices))
                            print(room.room_name)
                            room.occupants.append(staff)
                            client = Client(account_sid, auth_token)
                            client.messages.create(
                                to=phone_number,
                                from_='+14026206866',
                                body='Hello' + staff.person_name + ', ' + 'you have been allocated to '+ room.room_name +' succesfully!!. Amity')
                    else:
                        print('There is no rooms available in Amity. Use the createroom command to create one!')
        if person_role == 'fellow':
            if person_name not in self.all_fellow:
                    if want_accomodation == "n":
                        if not phone_number:
                            fellow = Fellow(person_name, want_accomodation, phone_number)
                            self.all_fellow.append(fellow)
                            print(person_name + 'has been succesfully added to Amity')
                        else:
                            fellow = Fellow(person_name, want_accomodation, phone_number)
                            self.all_fellow.append(fellow)
                            client = Client(account_sid, auth_token)
                            client.messages.create(
                                to=phone_number,
                                from_="+14026206866",
                                body='Hello ' + fellow.person_name + ', ' + 'you have been succesfully added to Amity')

                    else:
                        # if self.all_offices and self.all_livingspace:
                        if self.all_rooms:
                            if not phone_number:
                                fellow = Fellow(person_name, want_accomodation, phone_number)
                                self.all_fellow.append(fellow)
                                room = random.choice(self.get_available_room(self.all_livingspace))
                                room.occupants.append(id(fellow))
                                print(fellow.person_name + 'has been allocated to' + room.room_name + 'succesfully!!')
                            else:
                                fellow = Fellow(person_name, want_accomodation, phone_number)
                                self.all_fellow.append(fellow)
                                room = random.choice(self.get_available_room(self.all_livingspace))
                                room.occupants.append(fellow)
                                client = Client(account_sid, auth_token)
                                client.messages.create(
                                    to=phone_number,
                                    from_='+14026206866',
                                    body='Hello ' + fellow.person_name + ', ' + ' you have been allocated to' + room.room_name + 'succesfully!!')
                        else:
                            print('There is no rooms available in Amity. Use the createroom command to create one!')
            else:
                print(person_name + " already exist in Amity. Please use the Edit or Delete Command to Modify Entry.")


    def edit_person_info(self, person_name):
        '''this edits a persons name'''
        if person_name in self.all_staff or self.all_fellow:
            if self.all_people.count(person_name) > 1:
                value = input('which' + person_name + '? Please Enter their ID number')
                for a_name in person_name:
                    if self.all_people.ID(a_name) is int(value):
                        new_details = input('Enter new the new details about ' + a_name)
                        self.all_people.replace(new_details)
        else:
            print('This entry cannot be found in Amity')
    def find_userid(self,person_name):
        if person_name in self.all_staff or self.all_fellow:
            # for person in person_name:
            # print(person_name.ID)
            pprint(vars(person_name))
        else:
            print('This person is not in Amity')
    def reallocate_person(self, person_name,room_name):
        '''this reallocates a person to their room of choice'''
        room_names = [room.room_name for room in self.all_offices if len(room_name.occupants) < room_name.max_no_occupants]
        if person_name in Room.occupants:
            if room_name in room_names:
                Room.occupants.person_name[room_name] = room_name
            else:
                print(room_name + 'is not avalible for reallocation. Please try another room')
        else:
            print(person_name + ' does not exist in Amity')

        # for room in self.available_room:
        #     if room.room_name == room_name and room.room_type == 'Office':
        #         for person in self.all_people:
        #             if self.all_people.count(person_name) > 1:
        #                 value = ('which' + person_name + '? Please Enter their index number')
        #                 for a_name in person_name:
        #                     if self.all_people.index(a_name) is int(value):
        #                         self.all_allocations.remove(a_name)
        #                         room_all = a_name.append(room)
        #                         self.all_allocations.append(room_all)
        #                         return a_name + 'has been relocated to ' + room + 'succesfully!!'
        #                     else:
        #                         return 'That index number does not exist!'
        #             elif self.all_people.count(person_name) == 1:
        #                         self.all_allocations.remove(person)
        #                         room_all = person.append(room)
        #                         self.all_allocations.append(room_all)
        #                         return person.person_name + 'has been relocated to ' + room + 'succesfully!!'
        #         else:
        #             return person_name + 'Is not in Amity'
        #     elif room.room_name == room_name and room.room_type == 'Livingspace':
        #         for person in self.all_fellow:
        #             if self.all_fellow.count(person_name) > 1:
        #                 value = ('which' + person_name + '? Please Enter their index number')
        #                 for a_name in person_name:
        #                     if self.all_fellow.index(a_name) is int(value):
        #                         self.all_allocations.remove(a_name)
        #                         room_all = a_name.append(room)
        #                         self.all_allocations.append(room_all)
        #                         return a_name + 'has been relocated to ' + room + 'succesfully!!'
        #                     else:
        #                         return 'That index number does not exist!'
        #             elif self.all_fellow.count(person_name) == 1:
        #                         self.all_allocations.remove(person)
        #                         room_all = person.append(room)
        #                         self.all_allocations.append(room_all)
        #                         return person.person_name + 'has been relocated to ' + room + 'succesfully!!'
        #         else:
        #             return person_name + 'Is not in Amity'
        #     else:
        #         return room_name + 'is not available for reallocation'

    def allocate_unallocated_person(self, person_name):
        ''' this allocates a student who didnt want accomodation but would like accomodation now, a living space'''
        if person_name in self.all_staff or self.all_fellow:
            if Person.person_role == 'staff' and Person.want_accomodation == 'n':
                if self.get_available_room(self.all_offices) == True:
                        person_accomodation = 'y'
                        room = random.choice(self.get_available_room(self.all_offices))
                        room.occupants.append(person)
                        print(person_name + 'has been allocated succesfully to ' + room)
                else:
                    print('There is no room in Amity to allocate this person!')
            elif Person.person_role == 'fellow' and Person.want_accomodation == 'n':
                if self.get_available_room(self.all_livingspace) == True:
                        Person.want_accomodation = 'y'
                        room = random.choice(self.get_available_room(self.all_livingspace))
                        room.occupants.append(person)
                        print(person_name + 'has been allocated succesfully to ' + room)
                else:
                    print('There is no room in Amity to allocate this person!')

            else:
                print('This person does not exist in Amity')


    def Delete_person(self, person_name):
        ''' this deletes a person from the system'''
        if person_name in self.all_rooms:
                if len(person_name) > 1:
                    value = ('which' + person_name + '? Please Enter their ID number')
                    for a_name in person_name:
                        if self.all_people.ID(a_name) is int(value):
                            self.all_people.remove(a_name)
                            print(a_name + 'has been deleted succesfully!!')
                else:
                    self.all_people.remove(person_name)
                    return person_name + 'has been removed succesfully!!'
        else:
            print('This entry cannot be found in Amity')

    def loadpeople(self, filename):
        '''loads people from text file filename.txt'''
        person_details = open(filename, 'r')
        for info in person_details:
            pass

    def printallocations(self):
        '''prints office and livingspace  allocation for fellows and staff
            you can also choose to optionally save them to a text file'''
        if self.all_rooms:
            print str(Room.occupants).strip('[]')
        else:
            print('There are no rooms in Amity')

    def printunallocated(self):
        '''prints fellows and staff who have not been allocated to rooms
            you can also choose to optionally save them to a text file'''
        if self.all_people:
            for name in self.all_people:
                if name.want_accomodation == 'n':
                    print('name')
        else:
            print('There is are no people entered into Amity')
    def printroom(self, room_name):
        ''' this prints the members of a room once a name is given'''
        if self.all_rooms:
            if room_name in self.all_rooms:
                print str(room_name.occupants).strip('[]')
        else:
            print('This room does not exist in Amity')

    def savestate(self, db_name):
        ''' this saves all the information to an sqlite db '''
        pass
    def loadstate(self, db_name):
        ''' this loads all the data from an sqlite db into the application '''
        pass
    def edit_room_info(self, room_name):
        ''' this edits a room type from both db and list'''
        if room_name in self.all_rooms:
            new_details = input('Enter the New details')
            self.all_rooms.replace(new_details)
            print('This room information has been edited succesfully')

        if not self.all_rooms:
            return 'This entry cannot be found in Amity'

    def Delete_a_room(self, room_name):
        '''this deletes a room from the Amity '''
        if room_name in self.all_rooms:
            if self.all_rooms.count(room_name) > 1:
                value = ('which' + room_name + '? Please Enter their index number')
                for a_room in room_name:
                    if self.all_rooms.index(a_room) is int(value):
                        self.all_people.remove(a_room)
                        print(a_room + 'has been deleted succesfully!!')
                else:
                    self.all_people.remove(room_name)
                    print(room_name + 'has been deleted succesfully')

        else:
            return 'This entry cannot be found in Amity'

         
   