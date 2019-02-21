import sys
import os
import unittest
from Amity import Amity
from db_manager import DbManager

sys.path = [os.path.abspath(os.path.dirname(__file__))] + sys.path

class TestAmity(unittest.TestCase):

    def setUp(self):
       self.amity = Amity()
       self.db = DbManager()

    def test_create_room_office(self):
        self.amity.create_room('office', ['Antonorivo'])
        self.assertTrue(len(self.amity.all_offices),1)
        self.assertTrue('Office space {} has been created succesfully!!'.format('Antonorivo'))
        self.assertEqual(self.amity.create_room('office', ['Antonorivo']),
                         'Office space {} has been created succesfully!!'.format('antonorivo'))

    def test_create_room_livingspace(self):
        self.amity.create_room('livingspace', ['Brampton'])
        self.assertTrue(len(self.amity.all_livingspaces), 1)
        self.assertTrue('Livingspace {} has been created succesfully!!'.format('Brampton'))
        self.assertEqual(self.amity.create_room('livingspace', ['Brampton']),
                         'Livingspace {} has been created succesfully!!'.format('brampton') )

    def test_create_room_name_that_already_exist(self):
        self.amity.create_room('office', ['Madagascar'])
        self.amity.create_room('livingspace', ['Madagascar'])
        self.assertTrue(len(self.amity.all_offices), 1)
        self.assertEqual(self.amity.create_room('office', ['Madagascar']),
                         '{} already exists in Amity'.format('Madagascar'))

    def test_create_room_wrong_room_type(self):
        self.amity.create_room('mango', ['Madagascar'])
        self.assertTrue('this room type is invalid!!')
        self.assertEqual(self.amity.create_room('mango', ['Madagascar']), 'This room type is invalid!!')
    def test_add_person(self):
       """ this tests succesful creation of Fellow who want accomodation """
       self.assertEqual(self.amity.add_person("Joan Awinja", "Fellow", "Y"),
                        "joan awinja has succesfully been added to Amity but "
                        "will be allocated a room one becomes available")

       """this tests succeful creation of Staff who wants accomodation """
       self.assertEqual(self.amity.add_person("Eric Oyondi", "Staff", "Y"), "Sorry accomodation is only for Fellows!")

       """ this tests succesful creation of Fellow who does not  want accomodation """
       self.assertEqual(self.amity.add_person("John Liboyi", "Fellow", "N"),
                        "john liboyi has succesfully been added to Amity. but will be "
                        "allocated a room one becomes available")

       """ this tests succesfull creation of Staff who does not want accomodation"""
       self.assertEqual(self.amity.add_person("Mike Katiechi", "Staff", "N"),
                        "mike katiechi has succesfully been added to Amity but will be "
                        "allocated a room one becomes available")

       """ this tests succesfull creation of Fellows with No accomoadation status """
       self.assertEqual(self.amity.add_person("Tom Ingari", "Fellow",''),
                        "tom ingari has succesfully been added to Amity but will be "
                        "allocated a room one becomes available")

       """ this tests succesfull creation of staff with No accomodation status """
       self.assertEqual(self.amity.add_person("Fredrick Omukunda", "Staff", ' '),
                        "fredrick omukunda has succesfully been added to Amity but will be "
                        "allocated a room one becomes available")
       """this tests adding a digit as person name"""
       self.assertEqual(self.amity.add_person('1 2', 'staff', ''), "person name cannot contain a digit!")

    def test_allocate_room(self):
        self.amity.add_person('Jones Marion', 'staff', ' ')
        if self.amity.awaiting_allocation:
            self.amity.create_room('office', 'deli')
            self.amity.allocate_room()
            out = sys.stdout
            output = out.getvalue().strip().split("\n")[-1]
            self.assertTrue(output, '{} has been allocated to {} succesfully!!'.format('jones marion', 'deli'))

    def test_add_person_wrong_role_type(self):
        self.amity.add_person("James Nyakenyanya", "jelly", "N")
        self.assertTrue('This person role is invalid!')
        self.assertEqual(self.amity.add_person("James Nyakenyanya", "jelly", "N"), 'This person role is invalid!')

    def test_add_person_more_than_once(self):
       """ this test add person functionality when the name details already exist"""
       self.amity.add_person("James Nyakenyanya", "Fellow", "N")
       self.assertEqual(self.amity.add_person("James Nyakenyanya", "Fellow", "N"),
                        "james nyakenyanya has succesfully been added to Amity. "
                        "but will be allocated a room one becomes available")

    def test_add_person_existing_swapped_details(self):
       """ this tests add person functionlity-existing combination different status(fellow|staff) """
       self.amity.add_person("Jeffery Eyama", "Staff", "N")
       self.assertEqual(self.amity.add_person("Jeffery Eyama", "Fellow", "N"),
                        "jeffery eyama has succesfully been added to Amity. "
                        "but will be allocated a room one becomes available")

    def test_find_userid(self):
        self.amity.create_room('office', ['lade'])
        self.amity.add_person("Jeffery Eyama", "Staff", "N")
        one = None
        for person in self.amity.all_people:
            one = person.person_ID
        self.assertTrue(one)
        self.assertTrue('jeffery eyama')
        self.assertEqual(self.amity.found_userid('Jeffery Eyama'), '\n {} {} {} {}'
                         .format(one, 'jeffery eyama', 'staff', 'True'))

    def test_reallocate(self):
        """ this tests reallocate person functionality """
        self.amity.create_room("office", ['valhala'])
        self.amity.add_person("Joan Awinja", "staff", 'n')
        one = None
        for person in self.amity.all_people:
            one = person.person_ID
        for room in self.amity.all_offices:
                if room.room_name == 'valhala':
                    if room.occupants:
                        self.amity.create_room('office', ['Penny'])
                        self.amity.reallocate_person(one, 'penny')
                        output = sys.stdout.getvalue().strip().split("\n")[-1]
                        self.assertTrue(output, '{} has been reallocated to {} succesfully!!'.format('joan awinja', 'penny'))
                    else:
                        print('nothing inside')

    def test_reallocate_staff_to_livingspace(self):
        self.amity.create_room('office', ['yellow'])
        self.amity.add_person('blue ivy', 'staff', 'n')
        one = None
        for person in self.amity.all_people:
            one = person.person_ID
        self.amity.create_room('livingspace', ['blue'])
        self.assertEqual(self.amity.reallocate_person(one, 'blue'), 'Staff cannot be allocated to a livingspace')

    def test_reallocate_to_a_room_that_does_not_exist(self):
        self.amity.create_room('office', ['yellow'])
        self.amity.add_person('blue ivy', 'staff', 'n')
        one = None
        for person in self.amity.all_people:
            one = person.person_ID
        self.assertEqual(self.amity.reallocate_person(one, 'red'), 'This room does not exist in Amity')

    def test_reallocate_to_the_same_room(self):
        self.amity.create_room('office', ['yellow'])
        self.amity.add_person('blue ivy', 'staff', 'n')
        one = None
        for person in self.amity.all_people:
            one = person.person_ID
        self.assertEqual(self.amity.reallocate_person(one, 'yellow'), 'You cannot be reallocated to the same room')

    def test_reallocate_a_person_that_does_not_exist(self):
        """this tests application response to trying to \
         a person who is not in the system"""
        self.amity.create_room("Office", ['Umoja'])
        try:
            self.amity.reallocate_person(1234, 'umoja')
        except AttributeError:
            self.assertTrue("This person does not exist in Amity!")

    def test_load_people_to_a_room_using_file(self):
        """this tests loading people succesfully to the application using a text file """
        self.assertEqual(self.amity.load_people("loadpeople.txt"), "File content read succesfully!")

    def test_load_people_to_a_room_using_empty_file(self):
        """this test loading people to the application using a text file that is empty """
        self.assertEqual(self.amity.load_people("empty_file.txt"), "Error: can't find file or read data.")

    def test_print_allocation(self):
        """ this tests print the names of the people
        and the room they are  allocated to"""
        self.amity.create_room("Office", ["Naija"])
        self.amity.add_person("Joan Awinja", "staff", "Y")
        self.amity.print_allocations(args={'--o': "try1.txt"})
        self.assertTrue(os.path.exists('try1.txt'))
        os.remove('try1.txt')

    def test_print_allocations_display(self):
        self.amity.create_room("Office", ["Naija"])
        self.amity.add_person("Joan Awinja", "staff", "Y")
        self.amity.print_allocations(args={'--o': " "})
        output = sys.stdout.getvalue().strip().split("\n")[-1]
        self.assertTrue(output, 'Offices {} is occupied by: '.format('naija'))


    def test_print_room(self):
        """this tests print room functionality"""
        self.amity.create_room('Office', ['Mombasa'])
        self.amity.add_person("Joan Awinja", "staff", "n")
        self.amity.add_person("Jeff Ingari", "staff", "n")
        self.amity.add_person("Jeremy Atema", "staff", "n")
        self.amity.print_room('mombasa')
        output = sys.stdout.getvalue().strip().split("\n")[-1]
        self.assertTrue(output, 'mombasa')
        self.assertTrue(output, 'Joan Awinja')

    def test_print_room_that_is_not_in_the_system(self):
        """this tests print if members of a room that is not in the system"""
        self.assertEqual(self.amity.print_room("Valhala"), "This room does not exist in the system ")

    def test_print_unallocated_display(self):
        """this tests print if members of a room that is not in the system"""
        self.amity.add_person("Joan Awinja", "staff", "Y")
        self.amity.add_person("flavian Kanaiza", "fellow", "Y")
        self.amity.print_unallocated(args={'--o': " "})
        output = sys.stdout.getvalue().strip().split("\n")[-1]
        self.assertTrue(output, 'Joan Awinja')

    def test_print_unallocated(self):
        """ this tests print unallocated functionality"""
        self.amity.add_person("Joan Awinja", "staff", "Y")
        self.amity.add_person("flavian Kanaiza", "fellow", "Y")
        self.amity.print_unallocated(args={'--o': "try2.txt"})
        self.assertTrue(os.path.exists('try2.txt'))
        os.remove('try2.txt')

    def test_save_state(self):
        """this tests save state functionality where data is loaded from the application to an sqlitedb"""
        self.amity.create_room('Office', ['Mombasa'])
        self.amity.add_person("Joan Awinja", "staff", "Y")
        self.amity.save_state(args = {'--db':'try1.db'})
        self.assertTrue(os.path.exists('try1.db'))
        output = sys.stdout.getvalue().strip().split("\n")[-1]
        self.assertTrue(output, "Data successfully saved to database!")
        os.remove('try1.db')

    def test_save_state_empty_param(self):
        """this tests save state functionality when no db name is provided"""
        self.amity.create_room('Office', ['Mombasa'])
        self.amity.add_person("Joan Awinja", "staff", "Y")
        self.amity.save_state(args={'--db': ' '})
        self.assertTrue(os.path.exists('amity.db'))
        output = sys.stdout.getvalue().strip().split("\n")[-1]
        self.assertTrue(output, "Data successfully saved to database!")
        os.remove('amity.db')

    def test_load_state_no_params(self):
        self.amity.load_state(args={'--db': ''})
        self.assertTrue('no db selected')
        self.assertEqual(self.amity.load_state(args={'--db': ''}), 'no db selected')

    def test_load_state_not_a_db(self):
        self.amity.load_state(args={'--db': "amity"})
        self.assertTrue('This is not a Database')
        self.assertEqual(self.amity.load_state(args={'--db': "amity"}), 'This is not a Database')

    def test_load_state_db_doesnt_exist(self):
        self.amity.load_state(args={'--db': "mango.db"})
        self.assertTrue('Database Couldn\'t be accessed!')
        self.assertEqual(self.amity.load_state(args={'--db': "mango.db"}), 'Database Couldn\'t be accessed!')

    def test_load_state(self):
        """this test load state functionality where data is loaded from db into application"""
        self.amity.save_state(args={'--db': "amity.db"})
        self.amity.load_state(args={'--db': "amity.db"})
        output = sys.stdout.getvalue().strip().split("\n")[-1]
        self.assertTrue(output, "Data has been successfully loaded into the app")


if __name__ == '__main__':

       unittest.main()
