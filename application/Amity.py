from Room import Room, Office, Livingspace
from Person import Person, Staff, Fellow
import random
from twilio.rest import client
# from twilio.rest import Client
from twilio.rest.lookups import TwilioLookupsClient
from twilio.rest.exceptions import TwilioRestException

# put your own credentials here
account_sid = 'ACc684e833e5afc573a4cccee306537e95'
auth_token = "8d835935196f549c04527d55adeac603"


class Amity(object):
    ''' this application should be able to be installed using a package '''
    ''' on add person,if person has a phone number, the person will be sent a text message with the room they have been allocated '''
    def __init__(self):
        self.all_staff = []
        self.all_fellow = []
        self.all_people = []
        self.available_room = []
        self.all_offices = []
        self.all_livingspace = []
        self.all_rooms = []
        self.office_allocations = []
        self.livingspace_allocations = []
        self.awaiting_allocation = []

    def check_if_number_is_verified(self,phone_number):
        client = TwilioLookupsClient(account_sid, auth_token)
        try:
            response = client.phone_numbers.get(phone_number)
            response.phone_number  # If invalid, throws an exception.
            return phone_number
        except TwilioRestException as e:
            if e.code == 20404:
                print('The number you have provided is invalid!!')

    def get_available_room(self, arg):
        room_list = [key for key in arg
                     if len(key.occupants) < key.max_no_occupants]
        return room_list
    def allocate_room(self):
        if self.awaiting_allocation:
            for person in self.awaiting_allocation:
                if person.person_role not in ['staff', 'fellow']:
                    print ("")
                    print('This person role is invalid!')
                    print ("")
                else:
                    if person.person_role == 'staff':
                        if not person.phone_number:
                            self.all_staff.append(person)
                            self.all_people.append(person)
                            room = random.choice(self.get_available_room(self.all_offices))
                            room.occupants.append(person)
                            self.awaiting_allocation.remove(person)
                            print ("")
                            print(person.person_name + ' has been allocated to '  + room.room_name + ' succesfully!!')
                            print ("")
                        else:
                            self.all_staff.append(person)
                            self.all_people.append(person)
                            room = random.choice(self.get_available_room(self.all_offices))
                            room.occupants.append(person)
                            self.awaiting_allocation.remove(person)
                            number = self.check_if_number_is_verified(person.phone_number)
                            Client = client(account_sid, auth_token)
                            Client.messages.create(
                                to=number,
                                from_='+14026206866',
                                body='Hello ' + person.person_name + ', ' + ' you have been allocated to '  + room.room_name + ' succesfully!!. Amity')
                    else:
                        if self.all_offices and self.all_livingspace:
                            if not person.phone_number:
                                self.all_fellow.append(person)
                                self.all_people.append(person)
                                room = random.choice(self.get_available_room(self.all_livingspace))
                                room1 = random.choice(self.get_available_room(self.all_offices))
                                room1.occupants.append(person)
                                room.occupants.append(person)
                                self.awaiting_allocation.remove(person)
                                print ("")
                                print(person.person_name + ' has been allocated to '+ room.room_name + ' and ' + room1.room_name +  ' succesfully!!')
                                print ("")
                            else:
                                self.all_fellow.append(person)
                                self.all_people.append(person)
                                room = random.choice(self.get_available_room(self.all_livingspace))
                                room1 = random.choice(self.get_available_room(self.all_offices))
                                room1.occupants.append(person)
                                room.occupants.append(person)
                                self.awaiting_allocation.remove(person)
                                number = self.check_if_number_is_verified(person.phone_number)
                                client = Client(account_sid, auth_token)
                                client.messages.create(
                                    to=number,
                                    from_='+14026206866',
                                    body='Hello ' + person.person_name + ', ' + ' you have been allocated to ' + room.room_name + ' and ' + room1.room_name + ' succesfully!!')


    def create_room(self, room_type, room_name):
        room_type = room_type.lower()
        offices = [room.room_name for room in self.all_offices]
        livingspaces = [room.room_name for room in self.all_livingspace]
        rooms = offices + livingspaces
        if room_type not in ['office','livingspace']:
            print ("")
            print('This room type is invalid!!')
            print ("")
        else:
            for name in room_name:
                if name in rooms:
                    print ("")
                    print(name + ' already exists in Amity')
                    print ("")
                else:
                    name = name.lower()
                    if room_type == 'office':
                        office = Office(name)
                        self.all_offices.append(office)
                        self.all_rooms.append(office)
                        print ("")
                        print('Office space ' + name + ' has been created succesfully!!')
                        print ("")

                    else:
                        lv = Livingspace(name)
                        self.all_livingspace.append(lv)
                        self.all_rooms.append(lv)
                        print ("")
                        print('Livingspace ' + name + ' has been created succesfully!!')
                        print ("")
        if len(self.awaiting_allocation) > 0:
            self.allocate_room()


    def add_person(self, person_name, person_role, phone_number, want_accomodation):
        person_name = person_name.lower()
        person_role = person_role.lower()
        want_accomodation = want_accomodation.lower()
        if person_role not in ['staff', 'fellow']:
            print ("")
            print('This person role is invalid!')
            print ("")
        else:
            if person_role == 'staff':
                    if want_accomodation == "n":
                        if not phone_number:
                            staff = Staff(person_name, phone_number, want_accomodation)
                            self.all_staff.append(staff)
                            self.all_people.append(staff)
                            print ("")
                            print(staff.person_name + ' has been succesfully added to Amity')
                            print ("")
                        else:
                            staff = Staff(person_name, want_accomodation, phone_number)
                            self.all_staff.append(staff)
                            self.all_people.append(staff)
                            number = self.check_if_number_is_verified(phone_number)
                            client = Client(account_sid, auth_token)
                            client.messages.create(
                                to=number,
                                from_="+14026206866",
                                body='Hello ' + staff.person_name + ', ' + ' you have been succesfully added to Amity')
                            print('Hooray!')
                    else:
                        if self.all_offices:
                            if not phone_number:
                                staff = Staff(person_name, phone_number, want_accomodation)
                                self.all_staff.append(staff)
                                self.all_people.append(staff)
                                room = random.choice(self.get_available_room(self.all_offices))
                                room.occupants.append(staff)
                                print ("")
                                print(staff.person_name + ' has been added to Amity and has allocated to ' + room.room_name + ' succesfully!!')
                                print ("")
                            else:
                                staff = Staff(person_name, phone_number, want_accomodation)
                                self.all_staff.append(staff)
                                self.all_people.append(staff)
                                room = random.choice(self.get_available_room(self.all_offices))
                                room.occupants.append(staff)
                                number = self.check_if_number_is_verified(phone_number)
                                client = Client(account_sid, auth_token)
                                client.messages.create(
                                    to=number,
                                    from_='+14026206866',
                                    body='Hello ' + staff.person_name + ', ' + ' you have been allocated to '+ room.room_name +' succesfully!!. Amity')
                        else:
                            if not phone_number:
                                staff = Staff(person_name, phone_number, want_accomodation)
                                self.awaiting_allocation.append(staff)
                                print ("")
                                print(staff.person_name + ' has succesfully been allocated to Amity but will be alocated a room when room has been created')
                                print ("")
                            else:
                                staff = Staff(person_name, phone_number, want_accomodation)
                                self.awaiting_allocation.append(staff)
                                number = self.check_if_number_is_verified(phone_number)
                                client = Client(account_sid, auth_token)
                                client.messages.create(
                                    to=number,
                                    from_='+14026206866',
                                    body='Hello ' + staff.person_name + ', ' + ' succesfully been allocated to Amity but will be alocated a room when room has been created')
            if person_role == 'fellow':
                if person_name not in self.all_fellow:
                        if want_accomodation == "n":
                            if not phone_number:
                                fellow = Fellow(person_name, phone_number, want_accomodation)
                                self.all_fellow.append(fellow)
                                self.all_people.append(fellow)
                                print ("")
                                print(person_name + ' has been succesfully added to Amity')
                                print ("")
                            else:
                                fellow = Fellow(person_name, phone_number, want_accomodation)
                                self.all_fellow.append(fellow)
                                self.all_people.append(fellow)
                                number = self.check_if_number_is_verified(phone_number)
                                client = Client(account_sid, auth_token)
                                client.messages.create(
                                    to=number,
                                    from_="+14026206866",
                                    body='Hello ' + fellow.person_name + ', ' + ' you have been succesfully added to Amity')

                        else:
                            if (self.all_offices) and (self.all_livingspace):
                                if not phone_number:
                                    fellow = Fellow(person_name, phone_number, want_accomodation)
                                    self.all_fellow.append(fellow)
                                    self.all_people.append(fellow)
                                    room = random.choice(self.get_available_room(self.all_livingspace))
                                    room1 = random.choice(self.get_available_room(self.all_offices))
                                    room1.occupants.append(fellow)
                                    room.occupants.append(fellow)
                                    print ("")
                                    print(fellow.person_name + ' has been allocated to '  + room.room_name + ' and ' + room1.room_name + ' succesfully!!')
                                    print ("")
                                else:
                                    fellow = Fellow(person_name, phone_number, want_accomodation)
                                    self.all_fellow.append(fellow)
                                    self.all_people.append(fellow)
                                    room = random.choice(self.get_available_room(self.all_livingspace))
                                    room1 = random.choice(self.get_available_room(self.all_offices))
                                    room1.occupants.append(fellow)
                                    room.occupants.append(fellow)
                                    number = self.check_if_number_is_verified(phone_number)
                                    client = Client(account_sid, auth_token)
                                    client.messages.create(
                                        to=number,
                                        from_='+14026206866',
                                        body='Hello ' + fellow.person_name + ', ' + ' you have been allocated to '  + room.room_name + ' and ' + room1.room_name + ' succesfully!!')
                            else:
                                if not phone_number:
                                    fellow = Fellow(person_name, phone_number, want_accomodation)
                                    self.awaiting_allocation.append(fellow)
                                    print ("")
                                    print(fellow.person_name + ' has succesfully been allocated to Amity but will be alocated a room when room has been created')
                                    print ("")
                                else:
                                    fellow = Fellow(person_name, phone_number, want_accomodation)
                                    self.awaiting_allocation.append(fellow)
                                    number = self.check_if_number_is_verified(phone_number)
                                    client = Client(account_sid, auth_token)
                                    client.messages.create(
                                        to=number,
                                        from_='+14026206866',
                                        body='Hello ' + fellow.person_name + ', ' + ' succesfully been allocated to Amity but will be alocated a room when room has been created')
                else:
                    print ("")
                    print(person_name + " already exist in Amity. Please use the Edit or Delete Command to Modify Entry.")
                    print ("")

    def find_userid(self, person_name):
        person_name = person_name.lower()
        for person in self.all_people:
            if person.person_name == person_name:
                print(person.person_ID ,person.person_name, person.person_role, person.want_accomodation,
                    person.phone_number)
            else:
                print ("")
                print('This person does not exist in Amity!')
                print ("")



    def reallocate_person(self, person_ID, room_name):
        ''' 
        this reallocates a person to their room of choice
        check if person exists in  Amity
        check the person type and reallocate accordingly
        check if the room exists in Amity
        find the room the person_Id was perviously in
        check if the new room and the old room are the same
        check if the new room has space
        if it has space remove person_id from old room
        append person_id in new_room
        '''
        for person in self.all_people:
            # print(person.person_ID, person.person_name)
            if person.person_ID == person_ID:
                if person.person_role == 'staff':
                    for room in self.all_rooms:
                        if room.room_name not in self.all_offices:
                            print("")
                            print ('This room is not in Amity!')
                            print("")
                        else:
                            old_room = person.room.occupants
                            if old_room == room_name:
                                print("")
                                print('You cannot be reallocated to the same room')
                                print("")
                            else:
                                if self.get_available_room(room_name) == True:
                                    new_room = room_name
                                    old_room.remove(person)
                                    new_room.append(person)
                                    print("")
                                    print(person_ID + 'has been reallocated to ' + new_room + 'succesfully!!')
                                    print("")
                                else:
                                    print("")
                                    print('This room has no space to reallocate')
                                    print("")

                else:
                    for room in self.all_rooms:
                        if room.room_name not in self.all_rooms:
                            print("")
                            print ('This room is not in Amity!')
                            print("")
                        else:
                            old_room = person.room.occupants
                            if old_room == room_name:
                                print("")
                                print('You cannot be reallocated to the same room')
                                print("")
                            else:
                                if self.get_available_room(room_name) == True:
                                    new_room = room_name
                                    old_room.remove(person)
                                    new_room.append(person)
                                    print("")
                                    print(person_ID + 'has been reallocated to ' + new_room + 'succesfully!!')
                                    print("")
                                else:
                                    print("")
                                    print('This room has no space to reallocate')
                                    print("")
            else:
                print("")
                print(person.person_ID)
                print('This person does not exist in Amity!')
                print("")


    def load_people(self, filename):
        '''loads people from text file filename.txt'''
        try:
            person = open(filename, "r")
            for a_name in person.readlines():
                person_name = a_name.split()[0].lower() + " " + a_name.split()[1].lower()
                person_role = a_name.split()[2].lower()
                if len(a_name.split()) == 4:
                    phone_number = None
                    want_accomodation = a_name.split()[3].lower()
                else:
                    phone_number = None
                    want_accomodation = "n"

                self.add_person(person_name, person_role, phone_number, want_accomodation)

        except IOError:
            print("")
            print("Error: can\'t find file or read data.")
            print("")
        else:
            print("")
            print("File content read succesfully!")
            print("")

    def print_allocations(self, args):
        '''prints office and livingspace  allocation for fellows and staff
            you can also choose to optionally save them to a text file'''
        people = ""
        filename = str(args['--o'])
        if not args['--o']:
            if len(self.all_livingspace) < 1:
                print("There are no livingspaces yet")
            else:
                for rooms in self.all_livingspace:
                    if len(rooms.occupants) > 0:
                        print('----------------------------')
                        print('Livingspace Name: ' + rooms.room_name)
                        print('----------------------------')
                        for occupant in rooms.occupants:
                            print(", ".join(occupant.person_ID))
                            print(", ".join(occupant.person_name))
                            print(", ".join(occupant.phone_number))
                            print("")
                            print("")
                            print('----------------------------')
                    else:
                        print('Livingspace' + rooms.room_name + ' is empty')

            if len(self.all_offices) < 1:
                print("There are no offices yet")
            else:
                for rooms in self.all_offices:
                    if len(rooms.occupants) > 0:
                        print('----------------------------')
                        print('Offices: ' + rooms.room_name)
                        print('----------------------------')
                        for occupant in rooms.occupants:
                            # people += "\n".join(map(rooms.room_name, occupant))
                            print(occupant.person_ID, occupant.person_name, occupant.phone_number)
                            # print(people)
                            print("")
                            print("")
                            print('----------------------------')
                    else:
                        print('Office' + rooms.room_name + ' is empty')

        else:
            # filename = str(args['-o=filename'])
            filename = filename.strip()
            if filename.endswith(".txt") is False:
                filename += ".txt"
                with open(filename, "wt") as textfile:
                    for rooms in self.all_livingspace:
                        if len(rooms.occupants) > 0:
                            textfile.write('----------------------------')
                            textfile.write('Livingspaces: ' + rooms.room_name)
                            textfile.write('----------------------------')
                            textfile.write(" \n ")
                            for occupant in rooms.occupants:
                                # people += "\n".join(map(rooms.room_name, occupant))
                                # textfile.write(people + '\n')
                                textfile.write(occupant)
                                print("")
                                print("")
                                print('----------------------------')
                                print ("Allocations writen and saved to " + args["<filename>"])
                    for rooms in self.all_offices:
                        if len(rooms.occupants) > 0:
                            textfile.write('----------------------------')
                            textfile.write('Offices: ' + rooms.room_name)
                            textfile.write('----------------------------')
                            textfile.write(" \n ")
                            for occupant in rooms.occupants:
                                # people += "\n".join(map(rooms.room_name, occupant))
                                # textfile.write(people + '\n')
                                textfile.write(occupant)
                                print("")
                                print("")
                                print('----------------------------')
                                print ("Allocations writen and saved to " + args["<filename>"])

    def print_unallocated(self, args):
        '''prints fellows and staff who have not been allocated to rooms
            you can also choose to optionally save them to a text file'''
        people = ""
        if (args['--o']) is None:
            if len(self.awaiting_allocation) > 0:
                for person in self.awaiting_allocation:
                    if person.person_role == 'staff':
                        print('----------------------------')
                        print('Unallocated Staff: ')
                        print('----------------------------')
                        print('\n')
                        print(person.person_ID, person.person_name, person.phone_number, person.want_accomodation)
                        print("")
                        print("")
                        print('----------------------------')
                    else:
                        print('----------------------------')
                        print('Unallocated Fellows: ')
                        print('----------------------------')
                        print('\n')
                        print(person.person_ID, person.person_name, person.phone_number, person.want_accomodation)
                        print("")
                        print("")
                        print('----------------------------')
            else:
                print("Everyone in Amity has been allocated a room")
            for room in self.all_rooms:
                if len(room.occupants) == 0:
                    print('----------------------------')
                    print('This rooms have not been allocated')
                    print('----------------------------')
                    print('\n')
                    print(room.room_name, room.room_type)
                    print("")
                    print("")
                    print('----------------------------')
                else:
                    print("")
                    print("All rooms in Amity have been allocated")
                    print("")


        else:
            filename = str(args['--o'])
            filename = filename.strip()
            if filename.endswith(".txt") is False:
                filename += ".txt"
            with open(filename, "wt") as textfile:
                if len(self.awaiting_allocation) > 0:
                    for person in self.awaiting_allocation:
                        if person.person_role == 'staff':
                            textfile.write('Unallocated Staff: ')
                            textfile.write('----------------------------')
                            textfile.write('\n')
                            textfile.write(person.person_ID, person.person_name, person.phone_number, person.want_accomodation)
                        else:
                            textfile.write('Unallocated Fellows: ')
                            textfile.write('----------------------------')
                            textfile.write('\n')
                            textfile.write(person.person_ID, person.person_name, person.phone_number, person.want_accomodation)
                else:
                    print("Everyone in Amity has been allocated a room")
                for room in self.all_rooms:
                    if len(room.occupants) == 0:
                        textfile.write('This rooms have not been allocated')
                        textfile.write('----------------------------')
                        textfile.write('\n')
                        textfile.write(room)
                    else:
                        textfile.write("")
                        textfile.write("All rooms in Amity have been allocated")
                        textfile.write("")


    def print_room(self, room_name):
            ''' this prints the members of a room once a name is given'''

            for rooms in self.all_rooms:
                if room_name == rooms.room_name:
                    if len(rooms.occupants) > 0:
                        print("")
                        print(rooms.occupants)
                        print("")
                        continue
                    else:
                        print('There are no occupants to display')
    def reset(self):
        pass



         
   