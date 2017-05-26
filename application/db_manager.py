import sqlite3


class DbManager(object):

        def create_all_tables(self, db_name):
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
                                      person_role,
                                      want_accomodation
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

