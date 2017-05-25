import sqlite3
import os
from os import sys, path
from Amity import Amity
from Room import Room, Office, Livingspace
from Person import Person, Staff, Fellow

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

class DbManager(object):

        def create_all_tables(self, db_name):
            '''Create the tables for storing data'''
            conn = sqlite3.connect(db_name)
            c = conn.cursor()

            c.execute('''CREATE TABLE IF NOT EXISTS all_fellows(
                         person_ID PRIMARY_KEY,
                         person_name,
                         want_accomodation  )
                         ''')
            conn.commit()
            c.execute('''CREATE TABLE IF NOT EXISTS all_staffs(
                         person_ID PRIMARY_KEY,
                         person_name,
                         want_accomodation  )
                         ''')
            conn.commit()
            c.execute('''CREATE TABLE IF NOT EXISTS all_offices(
                         room_ID  PRIMARY KEY,
                         room_name,
                         max_no_occupants
                         )
                         ''')
            conn.commit()
            c.execute('''CREATE TABLE IF NOT EXISTS all_livingspaces(
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
            c.execute('''DROP TABLE IF EXISTS ALL_OFFICES''')

            # Save (commit) the changes
            conn.commit()

            c.execute('''DROP TABLE IF EXISTS ALL_LIVINGSPACES''')

            # Save (commit) the changes
            conn.commit()

            c.execute('''DROP TABLE IF EXISTS ALL_FELLOWS''')

            # Save (commit) the changes
            conn.commit()

            c.execute('''DROP TABLE IF EXISTS ALL_STAFFS''')

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

            for data in Amity().all_fellows:
                c.execute("""INSERT INTO all_fellows (
                                         person_ID, person_name, want_accomodation
                                     ) VALUES (
                                         '%s','%s','%s'
                                     )""" % (data.person_ID, data.person_name, data.want_accomodation))
                # Save (commit) the changes
                conn.commit()

            for data in Amity().all_staffs:
                c.execute("""INSERT INTO all_staff (
                                         person_ID,person_name,want_accomodation
                                     ) VALUES (
                                         '%s','%s','%s'
                                     )""" % (data.person_ID, data.person_name, data.want_accomodation))
                # Save (commit) the changes
                conn.commit()

            for data in Amity().all_offices:
                c.execute("""INSERT INTO all_offices (
                                         room_ID,room_name,
                                         max_no_occupants
                                     ) VALUES (
                                         '%s','%s','%s'
                                     )""" % (
                    data.room_ID, data.room_name, data.max_no_occupants))
                # Save (commit) the changes
                conn.commit()

            for data in Amity().all_livingspaces:
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
            for data in Amity().all_rooms:
                c.execute(""" INSERT INTO all_rooms(
                             room_ID, room_type, room_name, max_no_occupants
                             )VALUES(
                             '%s','%s','%s','%s'
                             )""" % (data.room_ID, data.room_type, data.room_name, data.max_no_occupants
                                     )
                          )
                conn.commit()
            for data in Amity().all_people:
                c.execute("""INSERT INTO all_people(
                             person_ID, person_name, person_role, want_accomodation)
                             VALUES(
                             '%s','%s','%s','%s'
                             )""" % (data.person_ID, data.person_name, data.person_role, data.want_accomodation)
                          )
                conn.commit()

            for data in Amity().awaiting_allocation:
                c.execute(""" INSERT INTO awaiting_allocation(
                     person_ID,person_name, person_role) VALUES(
                     '%s','%s','%s'
                     )""" % (
                    data.person_ID, data.person_name, data.person_role
                ))
                conn.commit()
            for room in Amity().all_rooms:

                for data in room.occupants:
                    c.execute(""" INSERT INTO occupants(
                         room_ID, room_name, room_type, person_ID, person_name,person_role, want_accomodation, max_no_occupants) VALUES(
                         '%s','%s','%s','%s','%s','%s', '%s', '%s')
                     """ % (
                        room.room_ID, room.room_name, room.room_type, data.person_ID, data.person_name, data.person_role,
                        data.want_accomodation, room.max_no_occupants
                    ))
                    conn.commit()

            print('Data successfully saved to database!')
            self.close_conn(db_name)

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
                            """SELECT * FROM all_offices"""
                    ):
                        room_name = str(rows[1])
                        office = Office(room_name)
                        office.room_ID = int(rows[0])
                        office.max_no_occupants = int(rows[2])
                        Amity().all_offices.append(office)
                        Amity().all_rooms.append(office)

                    for rows in c.execute(
                            """SELECT * FROM all_livingspaces"""
                    ):
                        room_name = str(rows[1])
                        living = Livingspace(room_name)
                        living.room_ID = int(rows[0])
                        living.max_no_occupants = int(rows[2])
                        Amity().all_livingspaces.append(living)
                        Amity().all_rooms.append(living)

                    for rows in c.execute(
                            """SELECT * FROM all_fellows"""
                    ):
                        person_name = str(rows[1]).split(",")
                        want_accomodation = str(rows[2])
                        fellow = Fellow(person_name, want_accomodation)
                        fellow.person_ID = int(rows[0])
                        # fellow.want_accomodation = str(rows[2])
                        Amity().all_fellows.append(fellow)
                        Amity().all_people.append(fellow)

                    for rows in c.execute(
                            """SELECT * FROM all_staffs"""
                    ):
                        person_name = str(rows[1]).split(",")
                        staff = Staff(person_name, want_accomodation='n')
                        staff.person_ID = int(rows[0])
                        Amity().all_staffs.append(staff)
                        Amity().all_people.append(staff)

                    for rows in c.execute(
                            """SELECT * FROM all_rooms"""
                    ):
                        room_name = str(rows[2]).split(" ")
                        room = Room(room_name)
                        room.room_ID = int(rows[0])
                        room.room_type = str(rows[1])
                        room.max_no_occupants = int(rows[3])
                        Amity().all_rooms.append(room)

                    for rows in c.execute(
                            """SELECT * FROM all_people"""
                    ):
                        person_name = str(rows[1]).split(" ")
                        want_accomodation = ''
                        person = Person(person_name, want_accomodation)
                        person.person_ID = int(rows[0])
                        person.person_role = str(rows[2])
                        person.want_accomodation = str(rows[3])
                        Amity().all_people.append(person)

                    for rows in c.execute(
                            """SELECT * FROM awaiting_allocation"""
                    ):
                        person_name = str(rows[1]).split(" ")
                        want_accomodation = ''
                        person = Person(person_name, want_accomodation)
                        person.person_ID = int(rows[0])
                        person.person_role = str(rows[2])
                        Amity().awaiting_allocation.append(person)

                    for rows in c.execute(
                            """SELECT * FROM occupants"""
                    ):
                        room_name = str(rows[2])
                        room = Room(room_name)
                        room.room_ID = int(rows[0])
                        room.room_type = str(rows[1])
                        room.max_no_occupants = int(rows[7])
                        if room.room_type == "livingspace":
                            Amity().all_livingspaces.append(room)
                        else:
                            Amity().all_offices.append(room)
                        Amity().all_rooms.append(room)

                        person_name = str(rows[4])
                        want_accomodation = str(rows[6])
                        person = Person(person_name, want_accomodation)
                        person.person_ID = int(rows[3])
                        person.person_role = str(rows[5])

                        room.occupants.append(person)
                        if person.person_role == "fellow":
                            Amity().all_fellows.append(person)
                        else:
                            Amity().all_staffs.append(person)
                        Amity().all_people.append(person)

                self.close_conn(db_name)
                print('Data has been successfully loaded into the app')
                return 'Data has been successfully loaded into the app'
