import os
import sqlite3
import random
from os import sys, path

from Room import Office, Livingspace
from Person import Staff, Fellow
from db_manager import DbManager

db = DbManager()


sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


class Amity(object):
    """ this application should be able to be installed using a package """
    def __init__(self):
        self.all_staffs = []
        self.all_fellows = []
        self.all_people = []
        self.available_rooms = []
        self.all_offices = []
        self.all_livingspaces = []
        self.all_rooms = []
        self.awaiting_allocation = []

    def get_available_rooms(self, arg):
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
                            office = random.choice(self.get_available_rooms(self.all_offices))
                        except IndexError:
                            self.awaiting_allocation.append(person)
                            print ('Please add more than one room to ease up allocation.')
                            return 'Please add more than one room to ease up allocation.'

                        else:
                            self.all_staffs.append(person)
                            self.all_people.append(person)
                            office.occupants.append(person)
                            self.awaiting_allocation.remove(person)
                            print ("")
                            print('{} has been allocated to {} succesfully!!'
                                  .format(person.person_name, office.room_name))
                    else:
                        if self.all_offices and self.all_livingspaces:

                            try:
                                office = random.choice(self.get_available_rooms(self.all_livingspaces))
                                livingspace = random.choice(self.get_available_rooms(self.all_offices))
                            except IndexError:
                                self.awaiting_allocation.append(person)
                                print ("")
                                print ('{} has succesfully been added to Amity but will be allocated'
                                       ' a room one becomes available'.format(
                                        person.person_name))
                                return '{} has succesfully been added to Amity but will be allocated a room one '\
                                       'becomes available'.format(
                                        person.person_name)

                            else:
                                self.all_fellows.append(person)
                                self.all_people.append(person)
                                livingspace.occupants.append(person)
                                office.occupants.append(person)
                                self.awaiting_allocation.remove(person)
                                print ("")
                                print ('{}  has been allocated to {}  and {} succesfully!!'
                                       .format(person.person_name, office.room_name, livingspace.room_name))

    def create_room(self, room_type, room_names):
        room_type = room_type.lower()
        offices = [room.room_name for room in self.all_offices]
        livingspaces = [room.room_name for room in self.all_livingspaces]
        rooms = offices + livingspaces
        if room_type not in ['office', 'livingspace']:
            print("")
            return 'This room type is invalid!!'
        else:
            for name in room_names:
                if name in rooms:
                    print ("")
                    print '{} already exists in Amity'.format(name)
                    return '{} already exists in Amity'.format(name)
                else:
                    name = name.lower()
                    if room_type == 'office':
                        office = Office(name)
                        self.all_offices.append(office)
                        self.all_rooms.append(office)
                        print ("")
                        print ('Office space {} has been created succesfully!!'.format(name))
                        return 'Office space {} has been created succesfully!!'.format(name)

                    else:
                        livingspace = Livingspace(name)
                        self.all_livingspaces.append(livingspace)
                        self.all_rooms.append(livingspace)
                        print ("")
                        print('Livingspace {} has been created succesfully!!'.format(name))
                        return 'Livingspace {} has been created succesfully!!'.format(name)
        if self.awaiting_allocation:
            self.allocate_room()

    def add_person(self, person_name, person_role, want_accomodation="n"):
        person_name = person_name.lower()
        person_role = person_role.lower()
        want_accomodation = want_accomodation.lower()
        for character in person_name:
            if character.isdigit():
                return 'person name cannot contain a digit!'
        if person_role not in ['staff', 'fellow']:
            print ("")
            return 'This person role is invalid!'

        else:
            if person_role == 'staff':
                if want_accomodation == "y":
                    print("")
                    return 'Sorry accomodation is only for Fellows!'
                else:
                    if self.all_offices:
                        staff = Staff(person_name, want_accomodation == 'n')
                        try:
                            office = random.choice(self.get_available_rooms(self.all_offices))

                        except IndexError:
                            self.awaiting_allocation.append(staff)
                            print ("")
                            return '{} has succesfully been added to Amity. but will be allocated' \
                                   ' a room one becomes available'.format(
                                        staff.person_name)
                        else:
                            self.all_staffs.append(staff)
                            self.all_people.append(staff)
                            office.occupants.append(staff)
                            print ("")
                            return '{} has been added to Amity and has been allocated to {} succesfully!!'.format(
                                staff.person_name, office.room_name)
                    else:
                        staff = Staff(person_name, want_accomodation == 'n')
                        self.awaiting_allocation.append(staff)
                        print ("")
                        return '{} has succesfully been added to Amity but will be allocated' \
                               ' a room one becomes available'.format(staff.person_name)

            if person_role == 'fellow':
                    if want_accomodation == "n":
                        if self.all_offices:
                            fellow = Fellow(person_name, want_accomodation)
                            try:
                                office = random.choice(self.get_available_rooms(self.all_offices))
                            except IndexError:
                                self.awaiting_allocation.append(fellow)
                                print ("")
                                return '{} has succesfully been added to Amity. ' \
                                       'but will be allocated a room one becomes available'.format(
                                        fellow.person_name)
                            else:
                                self.all_fellows.append(fellow)
                                self.all_people.append(fellow)
                                office.occupants.append(fellow)
                                print("")
                                return '{} has been added to Amity and has been allocated to {} succesfully!!'\
                                       .format(fellow.person_name, office.room_name)
                        else:
                            fellow = Fellow(person_name, want_accomodation)
                            self.awaiting_allocation.append(fellow)
                            return '{} has succesfully been added to Amity. ' \
                                   'but will be allocated a room one becomes available'.format(
                                    fellow.person_name)
                    else:
                        if self.all_offices and self.all_livingspaces:
                            fellow = Fellow(person_name, want_accomodation)
                            try:
                                office = random.choice(self.get_available_rooms(self.all_livingspaces))
                                livingspace = random.choice(self.get_available_rooms(self.all_offices))
                            except IndexError:
                                self.awaiting_allocation.append(fellow)
                                print ("")
                                return '{} has succesfully been added to Amity but will be allocated a ' \
                                       'room one becomes available'.format(fellow.person_name)
                            else:
                                self.all_fellows.append(fellow)
                                self.all_people.append(fellow)
                                livingspace.occupants.append(fellow)
                                office.occupants.append(fellow)
                                print ("")
                                return '{} has been allocated to {} and {} succesfully!!'\
                                        .format(fellow.person_name, office.room_name, livingspace.room_name)
                        else:
                            fellow = Fellow(person_name, want_accomodation)
                            self.awaiting_allocation.append(fellow)
                            print ("")
                            return '{} has succesfully been added to Amity but will be allocated' \
                                   ' a room one becomes available'.format(fellow.person_name)

    def found_userid(self, person_name):
        person_name = person_name.lower()

        one = None

        for person in self.all_people:
            if person.person_name == person_name:
                one = person

        if one is None:
            return ('This person does not exist in Amity!')

        return '\n {} {} {} {}'.format(one.person_ID, one.person_name, one.person_role, one.want_accomodation)

    def reallocate_person(self, id, room_name):
        person_moving = None

        for person in self.all_people:
            if person.person_ID == id:
                person_moving = person

        if person_moving is None:
            print ('This person does not exist in Amity!')

        new_room = None

        for room in self.all_rooms:
            if room.room_name == room_name:
                new_room = room

        if new_room is None:
            return 'This room does not exist in Amity'

        if new_room not in self.get_available_rooms(self.all_rooms):
            print('This room has no space to reallocate')
            return'This room has no space to reallocate'

        if person_moving.person_role == 'staff':
            if new_room.room_type == 'livingspace':
                print('Staff cannot be allocated to a livingspace')
                return 'Staff cannot be allocated to a livingspace'
            else:
                vacant_rooms = self.get_available_rooms(self.all_offices)
                for room in vacant_rooms:
                    if person_moving.person_ID in [person.person_ID for person in room.occupants]:
                        if new_room == room:
                            print ('You cannot be reallocated to the same room')
                            return 'You cannot be reallocated to the same room'
                        else:
                            # remove from old room
                            room.occupants.remove(person_moving)
                            # add to new room
                            new_room.occupants.append(person_moving)
                            print('{} has been reallocated to  {} succesfully!!'
                                  .format(person_moving.person_name, new_room))

        else:
            if new_room.room_type == 'livingspace':
                vacant_rooms = self.get_available_rooms(self.all_livingspaces)
                for room in vacant_rooms:
                    if person_moving.person_ID in [person.person_ID for person in room.occupants]:
                        if new_room == room:
                            print('You cannot be reallocated to the same room')

                        else:
                            # remove from old room
                            room.occupants.remove(person_moving)
                            # add to new room
                            new_room.occupants.append(person_moving)
                            print ('{} has been reallocated to  {} succesfully!!'
                                   .format(person_moving.person_name, new_room))

            elif new_room.room_type == 'office':
                vacant_rooms = self.get_available_rooms(self.all_offices)
                for room in vacant_rooms:
                    if person_moving.person_ID in [person.person_ID for person in room.occupants]:
                        if new_room == room:
                            print ('You cannot be reallocated to the same room')

                        else:
                            # remove from old room
                            room.occupants.remove(person_moving)
                            # add to new room
                            new_room.occupants.append(person_moving)
                            print ('{} has been reallocated to  {} succesfully!!'
                                   .format(person_moving.person_name, new_room))

    def load_people(self, filename):
        """loads people from text file filename.txt"""
        try:
            people = open(filename, "r")
            for person in people.readlines():
                person_name = person.split()[0].lower() + " " + person.split()[1].lower()
                person_role = person.split()[2].lower()
                if len(person.split()) == 4:
                    want_accomodation = person.split()[3].lower()
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
        """prints office and livingspace  allocation for fellows and staff
            you can also choose to optionally save them to a text file"""
        if not args['--o']:
            if not self.all_livingspaces:
                print ("There are no livingspaces yet")
            else:
                for room in self.all_livingspaces:
                    if room.occupants:
                        print('----------------------------')
                        print('Livingspace {} is occupied by: '.format(room.room_name) )
                        print('----------------------------')
                        for occupant in room.occupants:
                            members = ''
                            members += ('\n {}'.format(occupant.person_name))
                            print(members)
                            print('----------------------------')

            if not self.all_offices:
                print("There are no offices yet")
            else:
                for room in self.all_offices:
                    if room.occupants:
                        print('----------------------------')
                        print('Offices {} is occupied by: '.format(room.room_name))
                        print('----------------------------')
                        for occupant in room.occupants:
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
                for room in self.all_livingspaces:
                    if room.occupants:
                        textfile.write("\n" + '----------------------------' + "\n")
                        textfile.write('Livingspace ' + room.room_name  + ' is occupied by:' )
                        textfile.write("\n" + '----------------------------' + "\n")
                        for occupant in room.occupants:
                            members = ''
                            members += ('\n {}'.format( occupant.person_name))
                            textfile.write(members)
                            textfile.write("\n" + '----------------------------' + "\n")
                for room in self.all_offices:
                    if room.occupants:
                        textfile.write("\n" + '----------------------------' + "\n")
                        textfile.write('Offices {} is occupied by: '.format(room.room_name))
                        textfile.write("\n" + '----------------------------' + "\n")
                        textfile.write(" \n ")
                        for occupant in room.occupants:
                            members = ''
                            members += ('\n {}'.format(occupant.person_name))
                            textfile.write(members)
                            textfile.write("\n" + '----------------------------' + "\n")
            print ('file printed and saved sucessfully!')

    def print_unallocated(self, args):
        """prints fellows and staff who have not been allocated to rooms
            you can also choose to optionally save them to a text file"""
        if (args['--o']) is None:
            if not self.awaiting_allocation:
                print("Everyone in Amity has been allocated a room")
            else:
                print('----------------------------')
                print('Unallocated People: ')
                print('----------------------------')
                for person in self.awaiting_allocation:
                    print str(person.person_name).strip('[]')

        else:
            filename = str(args['--o'])
            filename = filename.strip()
            if filename.endswith(".txt") is False:
                filename += ".txt"
            with open(filename, "wt") as textfile:
                if self.awaiting_allocation:
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
            print('file printed and saved sucessfully!')

    def print_room(self, room_name):
        """ this prints the members of a room once a name is given"""
        room_name = room_name.lower()
        one = None
        for room in self.all_rooms:
            if room_name == room.room_name:
                one = room

        if one is None:
            return'This room does not exist in the system '

        if one.occupants:
            members = ''
            members += ('\n {}'.format(one.occupants))
            return members

        else:
            return'There are no occupants to display'

    def save_state(self, args):
        """ this saves all the current information to an sqlite db """

        db_name = args['--db']
        if not db_name:
            db_name = 'amity.db'
        else:
            if db_name.endswith(".db") is False:
                db_name += ".db"
        self.save_data(db_name)

    def load_state(self, args):
        """ this loads all the data from an sqlite db into the application """
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
        self.load_data(db_name)

    def save_data(self, db_name):
        """this saves the objects to db"""
        try:
            conn = sqlite3.connect(db_name)
            c = conn.cursor()
        except sqlite3.OperationalError:
            print("Database Couldn't be accessed!")

        db.drop_tables(db_name)
        db.create_all_tables(db_name)

        for data in self.all_fellows:
            c.execute("""INSERT INTO all_fellows (
                                     person_ID, person_name, want_accomodation
                                 ) VALUES (
                                     '%s','%s','%s'
                                 )""" % (data.person_ID, data.person_name, data.want_accomodation))
            # Save (commit) the changes
            conn.commit()

        for data in self.all_staffs:
            c.execute("""INSERT INTO all_staffs (
                                     person_ID,person_name,want_accomodation
                                 ) VALUES (
                                     '%s','%s','%s'
                                 )""" % (data.person_ID, data.person_name, data.want_accomodation))
            # Save (commit) the changes
            conn.commit()

        for data in self.all_offices:
            c.execute("""INSERT INTO all_offices (
                                     room_ID,room_name,
                                     max_no_occupants
                                 ) VALUES (
                                     '%s','%s','%s'
                                 )""" % (
                data.room_ID, data.room_name, data.max_no_occupants))
            # Save (commit) the changes
            conn.commit()

        for data in self.all_livingspaces:
            c.execute("""INSERT INTO all_livingspaces (
                                     room_ID,room_name,
                                     max_no_occupants
                                 ) VALUES (
                                         '%s','%s','%s'
                                 )""" % (
                data.room_ID, data.room_name, data.max_no_occupants
            )
                      )
            # Save (commit) the changes
            conn.commit()

        for data in self.all_rooms:
            c.execute(""" INSERT INTO all_rooms(
                         room_ID, room_type, room_name, max_no_occupants
                         )VALUES(
                         '%s','%s','%s','%s'
                         )""" % (data.room_ID, data.room_type, data.room_name, data.max_no_occupants
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
                 person_ID,person_name, person_role, want_accomodation) VALUES(
                 '%s','%s','%s'
                 )""" % (
                data.person_ID, data.person_name, data.person_role
            ))
            conn.commit()

        for room in self.all_rooms:

            for data in room.occupants:
                c.execute(""" INSERT INTO occupants(
                     room_ID, room_name, room_type, person_ID, person_name,person_role,
                     want_accomodation, max_no_occupants) VALUES(
                     '%s','%s','%s','%s','%s','%s', '%s', '%s')
                 """ % (
                    room.room_ID, room.room_name, room.room_type, data.person_ID, data.person_name, data.person_role,
                    data.want_accomodation, room.max_no_occupants
                ))
                conn.commit()

        print('Data successfully saved to database!')
        db.close_conn(db_name)

    def load_data(self, db_name):
        """ this loads all the data from an sqlite db into the application """
        # db_name = args['--db']
        try:
            conn = sqlite3.connect(db_name)
            c = conn.cursor()
        except sqlite3.OperationalError:
            print("Database Doesn't exist!!")

        for rows in c.execute(
                """SELECT * FROM all_offices"""
        ):
            room_name = str(rows[1])
            office = Office(room_name)
            office.room_ID = int(rows[0])
            office.max_no_occupants = int(rows[2])
            self.all_offices.append(office)
            self.all_rooms.append(office)

        for rows in c.execute(
                """SELECT * FROM all_livingspaces"""
        ):
            room_name = str(rows[1])
            living = Livingspace(room_name)
            living.room_ID = int(rows[0])
            living.max_no_occupants = int(rows[2])
            self.all_livingspaces.append(living)
            self.all_rooms.append(living)

        for rows in c.execute(
                """SELECT * FROM all_fellows"""
        ):
            person_name = str(rows[1]).split(",")
            want_accomodation = str(rows[2])
            fellow = Fellow(person_name, want_accomodation)
            fellow.person_ID = int(rows[0])
            self.all_fellows.append(fellow)
            self.all_people.append(fellow)

        for rows in c.execute(
                """SELECT * FROM all_staffs"""
        ):
            person_name = str(rows[1]).split(",")
            staff = Staff(person_name, want_accomodation='n')
            staff.person_ID = int(rows[0])
            self.all_staffs.append(staff)
            self.all_people.append(staff)

        for rows in c.execute(
                """SELECT * FROM all_rooms"""
        ):
            room_type = str(rows[1])
            if room_type == "livingspace":
                room_name = str(rows[2]).split(" ")
                room = Livingspace(room_name)
                room.room_ID = int(rows[0])
                room.room_type = str(rows[1])
                room.max_no_occupants = int(rows[3])
            else:
                room_name = str(rows[2]).split(" ")
                room = Office(room_name)
                room.room_ID = int(rows[0])
                room.room_type = str(rows[1])
                room.max_no_occupants = int(rows[3])
            self.all_rooms.append(room)

        for rows in c.execute(
                """SELECT * FROM all_people"""
        ):
            person_role = str(rows[2])
            if person_role == "staff":
                person_name = str(rows[1]).split(" ")
                staff = Staff(person_name, want_accomodation='n')
                staff.person_ID = int(rows[0])
                self.all_people.append(staff)

            elif person_role == "fellow":
                person_name = str(rows[1]).split(" ")
                want_accomodation = str(rows[3])
                fellow = Fellow(person_name, want_accomodation)
                fellow.person_ID = int(rows[0])
                self.all_people.append(fellow)

        for rows in c.execute(
                """SELECT * FROM awaiting_allocation"""
        ):

            person_role = str(rows[2])
            if person_role == "staff":
                person_name = str(rows[1]).split(" ")
                staff = Staff(person_name, want_accomodation='n')
                staff.person_ID = int(rows[0])
                self.awaiting_allocation.append(staff)

            elif person_role == "fellow":
                person_name = str(rows[1]).split(" ")
                want_accomodation = str(rows[3])
                fellow = Fellow(person_name, want_accomodation)
                fellow.person_ID = int(rows[0])
                self.awaiting_allocation.append(fellow)

        for rows in c.execute(
                """SELECT * FROM occupants"""
        ):
            room_type = str(rows[1])
            if room_type == "livingspace":
                room_name = str(rows[2])
                room = Livingspace(room_name)
                room.room_ID = int(rows[0])
                room.max_no_occupants = int(rows[7])
                self.all_livingspaces.append(room)
                self.all_rooms.append(room)

                person_name = str(rows[4])
                want_accomodation = str(rows[6])
                fellow = Fellow(person_name, want_accomodation)
                fellow.person_ID = int(rows[3])
                fellow.person_role = str(rows[5])

                room.occupants.append(fellow)
                self.all_fellows.append(fellow)
                self.all_people.append(fellow)
            else:
                room_name = str(rows[2])
                room = Office(room_name)
                room.room_ID = int(rows[0])
                room.max_no_occupants = int(rows[7])
                self.all_offices.append(room)
                self.all_rooms.append(room)

                person_role = str(rows[5])
                if person_role == "staff":
                    person_name = str(rows[4])
                    staff = Staff(person_name, want_accomodation='n')
                    staff.person_ID = int(rows[3])
                    room.occupants.append(staff)
                    self.all_staffs.append(staff)
                    self.all_people.append(staff)
                elif person_role == "fellow":
                    person_name = str(rows[4])
                    want_accomodation = str(rows[6])
                    fellow = Fellow(person_name, want_accomodation)
                    fellow.person_ID = int(rows[3])
                    room.occupants.append(fellow)
                    self.all_fellows.append(fellow)
                    self.all_people.append(fellow)

        db.close_conn(db_name)
        print('Data has been successfully loaded into the app')
        return 'Data has been successfully loaded into the app'
