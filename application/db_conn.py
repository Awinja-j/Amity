from os import sys, path
import sqlite3
from Room import Room, Office, Livingspace
from Person import Person, Fellow, Staff
from Amity import Amity

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

class DbManager(object):

    def create_all_tables(self):
        conn = sqlite3.connect('amity.db')
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS fellow(
                    person_ID PRIMARY_KEY,
                    person_name,
                    person_role,
                    phone_number,
                    want_accomodation  )
                    ''')
        conn.commit()
        c.execute('''CREATE TABLE IF NOT EXISTS staff(
                    person_ID PRIMARY_KEY,
                    person_name,
                    person_role,
                    phone_number,
                    want_accomodation  )
                    ''')
        conn.commit()
        c.execute('''CREATE TABLE IF NOT EXISTS office(
                    room_ID  PRIMARY KEY,
                    room_type,
                    room_name,
                    max_no_occupants, 
                    occupants,
                    user_id ForeignKey)
                    ''')
        conn.commit()
        c.execute('''CREATE TABLE IF NOT EXISTS livingspace(
                    room_ID  PRIMARY KEY,
                    room_type,
                    room_name,
                    max_no_occupants, 
                    occupants,
                    user_id ForeignKey)
                    ''')
        conn.commit()

        print('Tables created succesfully!')

    def drop_tables(self):
        """Delete all the existing tables in the database."""
        conn = sqlite3.connect('amity.db')
        c = conn.cursor()
        c.execute('''DROP TABLE IF EXISTS OFFICE''')

        # Save (commit) the changes
        conn.commit()

        c.execute('''DROP TABLE IF EXISTS LIVINGSPACE''')

        # Save (commit) the changes
        conn.commit()

        c.execute('''DROP TABLE IF EXISTS FELLOW''')

        # Save (commit) the changes
        conn.commit()

        c.execute('''DROP TABLE IF EXISTS STAFF''')

        # Save (commit) the changes
        conn.commit()

    def close_conn(self):
        conn = sqlite3.connect('amity.db')
        conn.close()

    def save_state(self, args):
        ''' this saves all the current information to an sqlite db '''

        db_name = args['--db']
        if not db_name:
            db_name = 'amity.db'
        else:
            if db_name.endswith(".db") is False:
                db_name += ".db"
        if not path.isfile('application/' + db_name):
            self.save_data()
        else:
            print('Database already exists. Would you like to overwrite it?')
            answer = input("Enter \'Yes\' to Proceed or \'No\' to cancel\n")
            if answer.lower() == 'yes':
                self.save_data()
            else:
                print("Operation Canceled")

    def save_data(self):
        """this saves the objects to db"""
        # db_name = 'amity.db'
        try:
            conn = sqlite3.connect(
                "application/" + self.save_state().db_name)
            c = conn.cursor()
        except sqlite3.OperationalError:
            print("Database Couldn't be accessed!")

        self.drop_tables()
        self.create_all_tables()

        for data in Amity().all_fellow:
            c.execute("""INSERT INTO fellow (
                            person_ID, person_name,phone_number,want_accomodation,
                        ) VALUES (
                            '%s','%s','%s','%s'
                        )""" % (
                data.person_ID, data.person_name,
                data.phone_number, data.want_accomodation)
                                )
            # Save (commit) the changes
            conn.commit()

        for data in Amity().all_staff:
            c.execute("""INSERT INTO staff (
                            person_ID,person_name,phone_number,want_accomodation,
                        ) VALUES (
                            '%s','%s','%s','%s'
                        )""" % (data.person_ID, data.person_name,
                data.phone_number, data.want_accomodation)
                                )
            # Save (commit) the changes
            conn.commit()

        for data in Amity().all_offices:
            occupant = data.occupants
            current_number = len(occupant)

            c.execute("""INSERT INTO office (
                            room_type,room_name,
                            max_no_occupants,occupant,current_number
                        ) VALUES (
                            '%s','%s','%s','%s','%s'
                        )""" % (
                data.room_type, data.room_name, data.max_no_occupants, data.occupant, data.current_number
                                )
                                )
            # Save (commit) the changes
            conn.commit()

        for data in Amity().all_livingspace:
            occupant = data.occupants
            current_number = len(occupant)

            c.execute("""INSERT INTO livingspace (
                            room_type,room_name,
                            max_no_occupants,occupant,current_number
                        ) VALUES (
                                '%s','%s','%s','%s','%s'
                        )""" % (
                data.room_type, data.room_name, data.max_no_occupants, data.occupant, data.current_number
                                )
                                )
            # Save (commit) the changes
            conn.commit()

        print('Data successfully saved to database!')

        DbManager().close_conn()

    def load_state(self, args):
        print(args)
        ''' this loads all the data from an sqlite db into the application '''
        db_name = str(args['--db'])
        if db_name.endswith(".db") is False:
            db_name += ".db"
        if path.isfile('application/' + db_name):
            print(
                "This operation will reset your current working data. "
                "Are you sure you want to proceed?')"
            )
            answer = input(
                "Enter \'Yes\' to Proceed or \'No\' to cancel\n")

            if answer.lower() == 'yes':
                Amity().reset()

                try:
                    db_conn = sqlite3.connect(
                        "application/" + db_name)
                    self.cursor = db_conn.cursor()
                except sqlite3.OperationalError:
                    print("Database Doesn't exist!!")

                for rows in self.cursor.execute(
                        """SELECT * FROM office"""
                ):
                    room_name = str(rows[0])
                    room_type = str(rows[1])
                    room = Office(room_name)
                    occupants = str(rows[2]).split(" ") + str(rows[3])
                    room.occupants = occupants
                    room.current_number = int(rows[4])
                    room.max_no_occupants = int(rows[5])
                    Amity().all_offices[room_name] = room

                for rows in self.cursor.execute(
                        """SELECT * FROM livingspace"""
                ):
                    room_name = rows[0]
                    room_type = str(rows[1])
                    room = Livingspace(room_name)
                    occupants = str(rows[2]).split(" ") + str(rows[3])
                    room.occupants = occupants
                    room.current_number = int(rows[4])
                    room.max_no_occupants = int(rows[5])
                    Amity().all_livingspace[room_name] = room

                for rows in self.cursor.execute(
                        """SELECT * FROM fellow"""
                ):
                    person_name = str((rows[1]).split(" ") + (rows[2]))
                    phone_number = int(rows[2])
                    want_accomodation = str(rows[3])
                    fellow = Fellow(person_name,phone_number,want_accomodation)
                    fellow.person_ID = int(rows[1])
                    if rows[4] == 'True':
                        fellow.office_allocated = True
                    else:
                        fellow.office_allocated = False
                    fellow.office = rows[4]
                    if rows[5] == 'True':
                        fellow.livingspace_allocated = True
                    else:
                        fellow.livingspace_allocated = False
                    fellow.livingspace = rows[5]
                    Amity().all_fellow[rows[0]] = fellow

                for rows in self.cursor.execute(
                        """SELECT * FROM staff"""
                ):
                    person_name = str((rows[1]).split(" ") + (rows[2]))
                    phone_number = int(rows[2])
                    want_accomodation = str(rows[3])
                    staff = Staff(person_name,phone_number,want_accomodation)
                    staff.person_ID = int(rows[1])
                    if rows[4] == 'True':
                        staff.office_allocated = True
                    else:
                        staff.office_allocated = False
                    staff.office = rows[4]
                    Amity().all_staff[rows[0]] = staff

                self.close_conn()
                print('Data has been successfully loaded into the app')
            else:
                print('Operation Canceled!')
        else:
            print("Database doesn't exist!")
