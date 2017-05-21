from Room import Room, Office, Livingspace
from Person import Person, Staff, Fellow
import random
import sqlite3
from os import sys, path
import os

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class Amity(object):
    ''' this application should be able to be installed using a package '''
    def __init__(self):
        self.all_staff = []
        self.all_fellow = []
        self.all_people = []
        self.available_room = []
        self.all_offices = []
        self.all_livingspace = []
        self.all_rooms = []
        self.awaiting_allocation = []

    def get_available_room(self, arg):
        room_list = [key for key in arg
                     if len(key.occupants) < key.max_no_occupants]
        return room_list
    def allocate_room(self):
        if self.awaiting_allocation:
            for person in self.awaiting_allocation:
                if person.person_role not in ['staff', 'fellow']:
                    print ("")
                    print ('This person role is invalid!')
                    return 'This person role is invalid!'

                else:
                    if person.person_role == 'staff':

                        try:
                            room = random.choice(self.get_available_room(self.all_offices))
                        except IndexError:
                            self.awaiting_allocation.append(person)
                            print ('Please add more than one room to ease up allocation.')

                        else:
                            self.all_staff.append(person)
                            self.all_people.append(person)
                            room.occupants.append(person)
                            self.awaiting_allocation.remove(person)
                            print ("")
                            print('{} has been allocated to {} succesfully!!'.format(person.person_name,room.room_name))


                    else:
                        if self.all_offices and self.all_livingspace:

                            try:
                                room = random.choice(self.get_available_room(self.all_livingspace))
                                room1 = random.choice(self.get_available_room(self.all_offices))
                            except IndexError:
                                self.awaiting_allocation.append(person)
                                print ("")
                                print ('{} has succesfully been added to Amity but will be allocated a room one becomes available'.format(
                                    person.person_name))

                            else:
                                self.all_fellow.append(person)
                                self.all_people.append(person)
                                room1.occupants.append(person)
                                room.occupants.append(person)
                                self.awaiting_allocation.remove(person)
                                print ("")
                                print ('{}  has been allocated to {}  and {} succesfully!!'.format(person.person_name, room.room_name, room1.room_name))



    def create_room(self, room_type, room_name):
        room_type = room_type.lower()
        offices = [room.room_name for room in self.all_offices]
        livingspaces = [room.room_name for room in self.all_livingspace]
        rooms = offices + livingspaces
        if room_type not in ['office','livingspace']:
            print ("")
            return 'This room type is invalid!!'
        else:
            for name in room_name:
                if name in rooms:
                    print ("")
                    print '{} already exists in Amity'.format(name)
                else:
                    name = name.lower()
                    if room_type == 'office':
                        office = Office(name)
                        self.all_offices.append(office)
                        self.all_rooms.append(office)
                        print ("")
                        print ('Office space {} has been created succesfully!!'.format(name))


                    else:
                        lv = Livingspace(name)
                        self.all_livingspace.append(lv)
                        self.all_rooms.append(lv)
                        print ("")
                        print('Livingspace {} has been created succesfully!!'.format(name))


        if len(self.awaiting_allocation) > 0:
            self.allocate_room()


    def add_person(self, person_name, person_role, want_accomodation):
        person_name = person_name.lower()
        person_role = person_role.lower()
        want_accomodation = want_accomodation.lower()
        if person_role not in ['staff', 'fellow']:
            print ("")
            return ('This person role is invalid!')

        else:
            if person_role == 'staff':
                if want_accomodation == "y":
                    print("")
                    return ('Sorry accomodation is only for Fellows!')
                else:
                    if self.all_offices:
                        staff = Staff(person_name, want_accomodation == 'n')
                        try:
                            room = random.choice(self.get_available_room(self.all_offices))

                        except IndexError:
                            self.awaiting_allocation.append(staff)
                            print ("")
                            return '{} has succesfully been added to Amity. but will be allocated a room one becomes available'.format(
                                staff.person_name)
                        else:
                            self.all_staff.append(staff)
                            self.all_people.append(staff)
                            room.occupants.append(staff)
                            print ("")
                            return '{} has been added to Amity and has been allocated to {} succesfully!!'.format(
                                staff.person_name, room.room_name)
                    else:
                        staff = Staff(person_name, want_accomodation == 'n')
                        self.awaiting_allocation.append(staff)
                        print ("")
                        return '{} has succesfully been added to Amity but will be allocated a room one becomes available'.format(staff.person_name)


            if person_role == 'fellow':
                    if want_accomodation == "n":
                        if self.all_offices:
                            fellow = Fellow(person_name, want_accomodation)
                            try:
                                room = random.choice(self.get_available_room(self.all_offices))
                            except IndexError:
                                self.awaiting_allocation.append(fellow)
                                print ("")
                                return '{} has succesfully been added to Amity. but will be allocated a room one becomes available'.format(
                                    fellow.person_name)
                            else:
                                self.all_fellow.append(fellow)
                                self.all_people.append(fellow)
                                room.occupants.append(fellow)
                                print("")
                                return '{} has been added to Amity and has been allocated to {} succesfully!!'.format(fellow.person_name, room.room_name)
                        else:
                            fellow = Fellow(person_name, want_accomodation)
                            self.awaiting_allocation.append(fellow)
                            return '{} has succesfully been added to Amity. but will be allocated a room one becomes available'.format(
                                fellow.person_name)
                    else:
                        if (self.all_offices) and (self.all_livingspace):
                            fellow = Fellow(person_name, want_accomodation)
                            try:
                                room = random.choice(self.get_available_room(self.all_livingspace))
                                room1 = random.choice(self.get_available_room(self.all_offices))
                            except IndexError:
                                self.awaiting_allocation.append(fellow)
                                print ("")
                                return '{} has succesfully been added to Amity but will be allocated a room one becomes available'.format(
                                    fellow.person_name)
                            else:
                                self.all_fellow.append(fellow)
                                self.all_people.append(fellow)
                                room1.occupants.append(fellow)
                                room.occupants.append(fellow)
                                print ("")
                                return '{} has been allocated to {} and {} succesfully!!'.format(fellow.person_name, room.room_name, room1.room_name)
                        else:
                            fellow = Fellow(person_name, want_accomodation)
                            self.awaiting_allocation.append(fellow)
                            print ("")
                            return '{} has succesfully been added to Amity but will be allocated a room one becomes available'.format(fellow.person_name)


    def find_userid(self, person_name):
        Person_name = person_name.lower()

        one = None

        for person in self.all_people:
            if person.person_name == Person_name:
                one = person

        if one is None:
            return ('This person does not exist in Amity!')

        return ('\n {} {} {} {}'.format(one.person_ID, one.person_name, one.person_role, one.want_accomodation))



    def reallocate_person(self, ID, room_name):
        person_moving = None

        for person in self.all_people:
            if person.person_ID == ID:
                person_moving = person

        if person_moving is None:
            print ('This person does not exist in Amity!')

        new_room = None

        for room in self.all_rooms:
            if room.room_name == room_name:
                new_room = room

        if new_room is None:
            return ('This room does not exist in Amity')

        if new_room not in self.get_available_room(self.all_rooms):
            print('This room has no space to reallocate')
            return('This room has no space to reallocate')

        if person_moving.person_role == 'staff':
            if new_room.room_type == 'livingspace':
                print('Staff cannot be allocated to a livingspace')
                return('Staff cannot be allocated to a livingspace')
            else:
                vacant_rooms = self.get_available_room(self.all_offices)
                for room in vacant_rooms:
                    if person_moving.person_ID in [person.person_ID for person in room.occupants]:
                        if new_room == room:
                            print ('You cannot be reallocated to the same room')
                            return('You cannot be reallocated to the same room')
                        else:
                            #remove from old room
                            room.occupants.remove(person_moving)
                            #add to new room
                            new_room.occupants.append(person_moving)
                            print(
                            '{} has been reallocated to  {} succesfully!!'.format(person_moving.person_name, new_room))


        else:
            if new_room.room_type == 'livingspace':
                vacant_rooms = self.get_available_room(self.all_livingspace)
                for room in vacant_rooms:
                    if person_moving.person_ID in [person.person_ID for person in room.occupants]:
                        if new_room == room:
                            print('You cannot be reallocated to the same room')

                        else:
                            # remove from old room
                            room.occupants.remove(person_moving)
                            # add to new room
                            new_room.occupants.append(person_moving)
                            print ('{} has been reallocated to  {} succesfully!!'.format(person_moving.person_name, new_room))

            elif new_room.room_type == 'office':
                vacant_rooms = self.get_available_room(self.all_offices)
                for room in vacant_rooms:
                    if person_moving.person_ID in [person.person_ID for person in room.occupants]:
                        if new_room == room:
                            print ('You cannot be reallocated to the same room')

                        else:
                            # remove from old room
                            room.occupants.remove(person_moving)
                            # add to new room
                            new_room.occupants.append(person_moving)
                            print (
                            '{} has been reallocated to  {} succesfully!!'.format(person_moving.person_name, new_room))



    def load_people(self, filename):
        '''loads people from text file filename.txt'''
        try:
            person = open(filename, "r")
            for a_name in person.readlines():
                person_name = a_name.split()[0].lower() + " " + a_name.split()[1].lower()
                person_role = a_name.split()[2].lower()
                if len(a_name.split()) == 4:
                    want_accomodation = a_name.split()[3].lower()
                else:
                    want_accomodation = "n"

                self.add_person(person_name, person_role, want_accomodation)

        except IOError:
            print("")
            return "Error: can\'t find file or read data."
        else:
            print("")
            return "File content read succesfully!"

    def print_allocations(self, args):
        '''prints office and livingspace  allocation for fellows and staff
            you can also choose to optionally save them to a text file'''
        if not args['--o']:
            if len(self.all_livingspace) < 1:
                print ("There are no livingspaces yet")
            else:
                for rooms in self.all_livingspace:
                    if len(rooms.occupants) > 0:
                        print('----------------------------')
                        print('Livingspace {} is occupied by: '.format(rooms.room_name) )
                        print('----------------------------')
                        for occupant in rooms.occupants:
                            members = ''
                            members += ('\n {}'.format(occupant.person_name))
                            print(members)
                            print('----------------------------')

            if len(self.all_offices) < 1:
                print("There are no offices yet")
            else:
                for rooms in self.all_offices:
                    if len(rooms.occupants) > 0:
                        print('----------------------------')
                        print('Offices {} is occupied by: '.format(rooms.room_name))
                        print('----------------------------')
                        for occupant in rooms.occupants:
                            members = ''
                            members += ('\n {}'.format(occupant.person_name))
                            print(members)
                            print('----------------------------')

        else:
            filename = str(args['--o'])
            filename = filename.strip()
            if filename.endswith(".txt") is False:
                filename += ".txt"
            with open(filename, "wt") as textfile:
                for rooms in self.all_livingspace:
                    if len(rooms.occupants) > 0:
                        textfile.write("\n" + '----------------------------' + "\n")
                        textfile.write('Livingspace ' + rooms.room_name  + ' is occupied by:' )
                        textfile.write("\n" + '----------------------------' + "\n")
                        for occupant in rooms.occupants:
                            members = ''
                            members += ('\n {}'.format( occupant.person_name))
                            textfile.write(members)
                            textfile.write("\n" + '----------------------------' + "\n")
                for rooms in self.all_offices:
                    if len(rooms.occupants) > 0:
                        textfile.write("\n" + '----------------------------' + "\n")
                        textfile.write('Offices {} is occupied by: '.format(rooms.room_name))
                        textfile.write("\n" + '----------------------------' + "\n")
                        textfile.write(" \n ")
                        for occupant in rooms.occupants:
                            members = ''
                            members += ('\n {}'.format(occupant.person_name))
                            textfile.write(members)
                            textfile.write("\n" + '----------------------------' + "\n")
            print ('file printed and saved sucessfully!')

    def print_unallocated(self, args):
        '''prints fellows and staff who have not been allocated to rooms
            you can also choose to optionally save them to a text file'''
        if (args['--o']) is None:
            if len(self.awaiting_allocation) < 1:
                print("Everyone in Amity has been allocated a room")
            else:
                print('----------------------------')
                print('Unallocated People: ')
                print('----------------------------')
                for person in self.awaiting_allocation:
                    return str(person.person_name).strip('[]')


            print('----------------------------')
            print('Unallocated Rooms')
            print('----------------------------')
            for room in self.all_rooms:
                if len(room.occupants) < 1:
                    return str(room.occupants).strip('[]')

                else:
                    print("")
                    return ("All rooms in Amity have been allocated")



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
                            textfile.write("\n" + '----------------------------' + "\n")
                            members = ''
                            members += ('\n {} '.format(person.person_name))
                            textfile.write(members)
                        else:
                            textfile.write('Unallocated Fellows: ')
                            textfile.write("\n" + '----------------------------' + "\n")
                            members = ''
                            members += ('\n {}'.format(person.person_name))
                            textfile.write(members)
                else:
                    print("Everyone in Amity has been allocated a room")
                for room in self.all_rooms:
                    if len(room.occupants) == 0:
                        textfile.write('This room has not been allocated ')
                        textfile.write("\n" + '----------------------------' + "\n")
                        members = ''
                        members += ('\n {}'.format(room.room_name))
                        textfile.write(members)
                        textfile.write("\n" + '----------------------------' + "\n")
                    else:
                        textfile.write("")
                        textfile.write("All rooms in Amity have been allocated")
                        textfile.write("")
            print('file printed and saved sucessfully!')


    def print_room(self, room_name):
        ''' this prints the members of a room once a name is given'''
        room_name = room_name.lower()
        one = None
        for rooms in self.all_rooms:
            if room_name == rooms.room_name:
                one = rooms

        if one is None:
            return('This room does not exist in the system ')


        if len(one.occupants) > 0:
            members = ''
            members += ('\n {}'.format(one.occupants))
            return (members)

        else:
            return('There are no occupants to display')


    def create_all_tables(self, db_name):
        conn = sqlite3.connect(db_name)
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS all_fellow(
                    person_ID PRIMARY_KEY,
                    person_name,
                    want_accomodation  )
                    ''')
        conn.commit()
        c.execute('''CREATE TABLE IF NOT EXISTS all_staff(
                    person_ID PRIMARY_KEY,
                    person_name,
                    want_accomodation  )
                    ''')
        conn.commit()
        c.execute('''CREATE TABLE IF NOT EXISTS all_office(
                    room_ID  PRIMARY KEY,
                    room_name,
                    max_no_occupants
                    )
                    ''')
        conn.commit()
        c.execute('''CREATE TABLE IF NOT EXISTS all_livingspace(
                    room_ID  PRIMARY KEY,
                    room_name,
                    max_no_occupants
                    )
                    ''')
        conn.commit()
        c.execute('''CREATE TABLE IF NOT EXISTS all_rooms(
                    room_ID  PRIMARY KEY, 
                    room_type, 
                    room_name, 
                    max_no_occupants
                     )
                     ''')
        conn.commit()
        c.execute('''CREATE TABLE IF NOT EXISTS all_people(
                    person_ID PRIMARY KEY, 
                    person_name, 
                    person_role, 
                    want_accomodation
                    )
                    ''')
        conn.commit()
        c.execute('''CREATE TABLE IF NOT EXISTS awaiting_allocation(
                            person_ID PRIMARY_KEY,
                            person_name,
                            person_role
                            )
                            ''')
        conn.commit()
        c.execute('''CREATE TABLE IF NOT EXISTS occupants(
                                    room_ID PRIMARY_KEY,
                                    room_type,
                                    room_name,
                                    person_ID,
                                    person_name,
                                    person_role,
                                    want_accomodation,
                                    max_no_occupants
                                    )
                                    ''')
        conn.commit()

        print('Tables created succesfully!')

    def drop_tables(self, db_name):
        """Delete all the existing tables in the database."""
        conn = sqlite3.connect(db_name)
        c = conn.cursor()
        c.execute('''DROP TABLE IF EXISTS ALL_OFFICE''')

        # Save (commit) the changes
        conn.commit()

        c.execute('''DROP TABLE IF EXISTS ALL_LIVINGSPACE''')

        # Save (commit) the changes
        conn.commit()

        c.execute('''DROP TABLE IF EXISTS ALL_FELLOW''')

        # Save (commit) the changes
        conn.commit()

        c.execute('''DROP TABLE IF EXISTS ALL_STAFF''')

        # Save (commit) the changes
        conn.commit()
        c.execute('''DROP TABLE IF EXISTS ALL_ROOMS''')

        # Save (commit) the changes
        conn.commit()
        c.execute('''DROP TABLE IF EXISTS ALL_PEOPLE''')

        # Save (commit) the changes
        conn.commit()

        c.execute('''DROP TABLE IF EXISTS AWAITING_ALLOCATION''')

        # Save (commit) the changes
        conn.commit()
        c.execute('''DROP TABLE IF EXISTS OCCUPANTS''')

        # Save (commit) the changes
        conn.commit()

    def close_conn(self, db_name):
        conn = sqlite3.connect(db_name)
        conn.close()

    def save_state(self, args):
        ''' this saves all the current information to an sqlite db '''

        db_name = args['--db']
        if not db_name:
            db_name = 'amity.db'
        else:
            if db_name.endswith(".db") is False:
                db_name += ".db"
        self.save_data(db_name)


    def save_data(self, db_name):
        """this saves the objects to db"""
        try:
            conn = sqlite3.connect(db_name)
            c = conn.cursor()
        except sqlite3.OperationalError:
            print("Database Couldn't be accessed!")

        self.drop_tables(db_name)
        self.create_all_tables(db_name)


        for data in self.all_fellow:
            c.execute("""INSERT INTO all_fellow (
                                    person_ID, person_name, want_accomodation
                                ) VALUES (
                                    '%s','%s','%s'
                                )""" % (data.person_ID, data.person_name, data.want_accomodation))
            # Save (commit) the changes
            conn.commit()


        for data in self.all_staff:
            c.execute("""INSERT INTO all_staff (
                                    person_ID,person_name,want_accomodation
                                ) VALUES (
                                    '%s','%s','%s'
                                )""" % (data.person_ID, data.person_name, data.want_accomodation))
            # Save (commit) the changes
            conn.commit()

        for data in self.all_offices:
            c.execute("""INSERT INTO all_office (
                                    room_ID,room_name,
                                    max_no_occupants
                                ) VALUES (
                                    '%s','%s','%s'
                                )""" % (
                data.room_ID, data.room_name, data.max_no_occupants))
            # Save (commit) the changes
            conn.commit()

        for data in self.all_livingspace:
            c.execute("""INSERT INTO all_livingspace (
                                    room_ID,room_name,
                                    max_no_occupants
                                ) VALUES (
                                        '%s','%s','%s'
                                )""" % (
                data.room_ID,data.room_name, data.max_no_occupants
            )
                      )
            # Save (commit) the changes
            conn.commit()
        for data in self.all_rooms:
            c.execute(""" INSERT INTO all_rooms(
                        room_ID, room_type, room_name, max_no_occupants
                        )VALUES(
                        '%s','%s','%s','%s'
                        )""" %(data.room_ID, data.room_type, data.room_name, data.max_no_occupants
                               )
                      )
            conn.commit()
        for data in self.all_people:
            c.execute("""INSERT INTO all_people(
                        person_ID, person_name, person_role, want_accomodation)
                        VALUES(
                        '%s','%s','%s','%s'
                        )""" % (data.person_ID, data.person_name, data.person_role, data.want_accomodation)
                      )
            conn.commit()

        for data in self.awaiting_allocation:
            c.execute(""" INSERT INTO awaiting_allocation(
                person_ID,person_name, person_role) VALUES(
                '%s','%s','%s'
                )""" % (
                data.person_ID, data.person_name, data.person_role
            ))
            conn.commit()
        for room in self.all_rooms:

            for data in room.occupants:
                c.execute(""" INSERT INTO occupants(
                    room_ID, room_name, room_type, person_ID, person_name,person_role, want_accomodation, max_no_occupants) VALUES(
                    '%s','%s','%s','%s','%s','%s', '%s', '%s')
                """ %(
                    room.room_ID, room.room_name, room.room_type,data.person_ID, data.person_name, data.person_role,
                    data.want_accomodation, room.max_no_occupants
                ))
                conn.commit()

        print('Data successfully saved to database!')


    def load_state(self, args):
        ''' this loads all the data from an sqlite db into the application '''
        # db_name = args['--db']
        if not args['--db']:
            print ('no db selected')
            return ('no db selected')
        else:
            db_name = args['--db']
            if db_name.endswith(".db") is False:
                return 'This is not a Database'

            elif not os.path.isfile(db_name):
                print("Database Couldn't be accessed!")
                return "Database Couldn't be accessed!"

            else:
                try:
                     conn = sqlite3.connect(db_name)
                     c = conn.cursor()
                except sqlite3.OperationalError:
                        print("Database Doesn't exist!!")

                for rows in c.execute(
                     """SELECT * FROM all_office"""
                     ):
                     room_name = str(rows[1])
                     office = Office(room_name)
                     office.room_ID = int(rows[0])
                     office.max_no_occupants = int(rows[2])
                     self.all_offices.append(office)
                     self.all_rooms.append(office)

                for rows in c.execute(
                     """SELECT * FROM all_livingspace"""
                    ):

                     room_name = str(rows[1])
                     living = Livingspace(room_name)
                     living.room_ID = int(rows[0])
                     living.max_no_occupants = int(rows[2])
                     self.all_livingspace.append(living)
                     self.all_rooms.append(living)

                for rows in c.execute(
                     """SELECT * FROM all_fellow"""
                ):
                     person_name = str(rows[1]).split(",")
                     want_accomodation = str(rows[2])
                     fellow = Fellow(person_name, want_accomodation)
                     fellow.person_ID = int(rows[0])
                     # fellow.want_accomodation = str(rows[2])
                     self.all_fellow.append(fellow)
                     self.all_people.append(fellow)


                for rows in c.execute(
                     """SELECT * FROM all_staff"""
                    ):
                     person_name = str(rows[1]).split(",")
                     staff = Staff(person_name, want_accomodation='n')
                     staff.person_ID = int(rows[0])
                     self.all_staff.append(staff)
                     self.all_people.append(staff)

                for rows in c.execute(
                    """SELECT * FROM all_rooms"""
                ):
                    room_name = str(rows[2]).split(" ")
                    room = Room(room_name)
                    room.room_ID = int(rows[0])
                    room.room_type = str(rows[1])
                    room.max_no_occupants = int(rows[3])
                    self.all_rooms.append(room)

                for rows in c.execute(
                    """SELECT * FROM all_people"""
                ):
                    person_name = str(rows[1]).split(" ")
                    want_accomodation = ''
                    person = Person(person_name, want_accomodation)
                    person.person_ID = int(rows[0])
                    person.person_role = str(rows[2])
                    person.want_accomodation = str(rows[3])
                    self.all_people.append(person)

                for rows in c.execute(
                     """SELECT * FROM awaiting_allocation"""
                ):

                     person_name = str(rows[1]).split(" ")
                     want_accomodation = ''
                     person = Person(person_name, want_accomodation)
                     person.person_ID = int(rows[0])
                     person.person_role = str(rows[2])
                     self.awaiting_allocation.append(person)


                for rows in c.execute(
                     """SELECT * FROM occupants"""
                ):
                     room_name = str(rows[2])
                     room = Room(room_name)
                     room.room_ID = int(rows[0])
                     room.room_type = str(rows[1])
                     room.max_no_occupants = int(rows[7])
                     if room.room_type == "livingspace":
                        self.all_livingspace.append(room)
                     else:
                        self.all_offices.append(room)
                     self.all_rooms.append(room)

                     person_name = str(rows[4])
                     want_accomodation = str(rows[6])
                     person = Person(person_name, want_accomodation)
                     person.person_ID = int(rows[3])
                     person.person_role = str(rows[5])

                     room.occupants.append(person)
                     if person.person_role ==  "fellow":
                         self.all_fellow.append(person)
                     else:
                         self.all_staff.append(person)
                     self.all_people.append(person)


            self.close_conn(db_name)
            print('Data has been successfully loaded into the app')
            return 'Data has been successfully loaded into the app'
