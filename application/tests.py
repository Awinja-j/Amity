'''
This are tests that will be used in the entire amity application.
Amity has both offices and living spaces
offices can have 6 spaces
living spaces can have 4 spaces
person alocated can be either fellow or staff
staff cannot be allocated living space
fellows can select whether they want a living space or offices.
spaces allocated randomly
create test cases for multiple rooms
what change has happened after the function has been run // what do we expect when it fails
check for input[strings/int]
how do the objects in amity relate to each other
'''
import sys, os
import unittest
from Amity2 import Amity

sys.path = [os.path.abspath(os.path.dirname(__file__))] + sys.path

class TestAmity(unittest.TestCase):

    def setUp(self):
       self.amity = Amity()
    
    def test_create_room(self):
       self.assertEqual(self.amity.create_room('office',['Antonorivo']),"Office space antonorivo has been created succesfully!!")

    def test_create_room_that_already_exist(self):
        self.amity.create_room('office', ['Madagascar'])
        self.assertEqual(self.amity.create_room('office', ['Madagascar']),"Office space madagascar has been created succesfully!!")

    def test_add_person(self):
       ''' this tests succesful creation of Fellow who want accomodation '''
       self.assertEqual(self.amity.add_person("Joan Awinja","Fellow", "Y"),"joan awinja has succesfully been added to Amity but will be allocated a room one becomes available")

       '''this tests succeful creation of Staff who want accomodation '''
       self.assertEqual(self.amity.add_person("Eric Oyondi", "Staff", "Y"),"eric oyondi has succesfully been added to Amity but will be allocated a room one becomes available")

       ''' this tests succesful creation of Fellow who does not  want accomodation '''
       self.assertEqual(self.amity.add_person("John Liboyi", "Fellow", "N"),"john liboyi has been succesfully added to Amity")

       ''' this tests succesfull creation of Staff who does not want accomodation'''
       self.assertEqual(self.amity.add_person("Mike Katiechi", "Staff", "N"),"mike katiechi has been succesfully added to Amity")

       ''' this tests succesfull creation of Fellows with No accomoadation status '''
       self.assertEqual(self.amity.add_person("Tom Ingari", "Fellow",''), "tom ingari has succesfully been added to Amity but will be allocated a room one becomes available")

       ''' this tests succesfull creation of staff with No accomodation status '''
       self.assertEqual(self.amity.add_person("Fredrick Omukunda", "Staff", ' '), "fredrick omukunda has succesfully been added to Amity but will be allocated a room one becomes available")

    def test_add_person_more_than_once(self):
       ''' this test add person functionality when the name details already exist'''
       self.amity.add_person("James Nyakenyanya","Fellow","N")
       self.assertEqual(self.amity.add_person("James Nyakenyanya","Fellow","N"),"james nyakenyanya has been succesfully added to Amity")

    def test_add_person_existing_swapped_details(self):
       ''' this tests add person functionlity-existing combination different status(fellow|staff) '''
       self.amity.add_person("Jeffery Eyama","Staff","N")
       self.assertEqual(self.amity.add_person("Jeffery Eyama","Fellow","N"),"jeffery eyama has been succesfully added to Amity")

    def test_reallocate(self):
       ''' this tests reallocate person functionality '''
       self.amity.create_room("office", ['valhala'])
       self.amity.add_person("Joan Awinja", "staff", "y")
       self.amity.create_room("office", ["red"])
       test_ID = [key for key in self.amity.find_userid('Joan Awinja') if key == key.person_ID]
       print(test_ID)
       self.assertEqual(self.amity.reallocate_person(test_ID,"Ruby"),"reallocation succesfull")

    def test_reallocate_to_full_room(self):
        self.amity.create_room('office', ['lagos'])
        self.amity.add_person("Jeffery Eyama", "Staff", "y")
        self.amity.add_person("Jeffery k", "Staff", "y")
        self.amity.add_person("Jeffery p", "Staff", "y")
        self.amity.add_person("Jeffery q", "Staff", "y")
        ID = self.amity.find_userid("Jeffery Eyama")
        new_office = self.amity.create_room('office', ['the den'])
        self.amity.reallocate_person(ID, new_office )
        self.assertTrue(self.amity.new_office.occupants)

    def test_reallocate_staff(self):
        self.amity.create_room('livingspace', ['blue'])
        self.amity.create_room('office', ['yellow'])
        self.amity.add_person('blue ivy', 'staff', 'y')
        ID = self.amity.find_userid("blue ivy")
        print(ID)
        self.assertEqual(self.amity.reallocate_person(ID,'blue'), 'Staff cannot be allocated to a livingspace')

    def test_reallocate_to_a_room_that_does_not_exist(self):
        self.amity.create_room('office', ['yellow'])
        self.amity.add_person('blue ivy', 'staff', 'y')
        ID = self.amity.find_userid("blue ivy")
        print(ID)
        self.assertEqual(self.amity.reallocate_person(ID,'yellow'), 'This room does not exist in Amity')

    def test_reallocate_to_the_same_room(self):
        self.amity.create_room('office', ['yellow'])
        self.amity.add_person('blue ivy', 'staff', 'y')
        ID = self.amity.find_userid("blue ivy")
        print(ID)
        self.assertEqual(self.amity.reallocate_person(ID,'yellow'), 'You cannot be reallocated to the same room')

    def test_reallocate_a_person_that_does_not_exist(self):
       '''this tests application response to trying to reallocate a preson who is not in the syste,m'''
       self.amity.create_room("Office", ['Umoja'])
       self.assertEqual(self.amity.reallocate_person(1234,'umoja'),"This person does not exist in Amity!")

    def test_load_people_to_a_room_using_file(self):
       '''this tests loading people succesfully to the application using a text file '''
       self.assertEqual(self.amity.load_people("loadpeople.txt"),"File content read succesfully!")

    def test_load_people_to_a_room_using_empty_file(self):
       '''this test loading people to the application using a text file that is empty '''
       self.assertEqual(self.amity.load_people("empty_file.txt"),"Error: can't find file or read data.")

    def test_print_allocation(self):
       ''' this tests print the names of the people and the room they are  allocated to'''
       self.amity.create_room("Office", ["Naija"])
       self.amity.add_person("Joan Awinja", "staff", "Y")
       self.amity.print_allocations(args={'--o': "try1.txt"})
       self.assertTrue(os.path.exists('try1.txt'))
       os.remove('try1.txt')


    def test_print_room(self):
       '''this tests print room functionality'''
       self.amity.create_room('Office', ['Mombasa'])
       self.amity.add_person("Joan Awinja", "staff", "Y")
       self.amity.add_person("Jeff Ingari", "staff", "Y")
       self.amity.add_person("Jeremy Atema", "staff", "Y")
       self.amity.print_room('mombasa')
       self.assertTrue('mombasa')
       self.assertTrue('Joan Awinja')

    def test_print_room_that_is_not_in_the_system(self):
       '''this tests printint members of a room that is not in the system'''
       self.assertEqual(self.amity.print_room("Valhala"),"This room does not exist in Amity")

    def test_print_unallocated(self):
       ''' this tests print unallocated functionality'''
       # self.amity.create_room("Office",["Mombasa"])
       self.amity.add_person("Joan Awinja", "staff", "Y")
       self.amity.add_person("flavian Kanaiza", "fellow", "Y")
       self.amity.print_unallocated(args={'--o': "try2.txt"})
       self.assertTrue(os.path.exists('try2.txt'))
       os.remove('try2.txt')



    def test_save_state(self):
       '''this tests save state functionality where data is loaded from the application to an sqlitedb'''
       self.assertEqual(self.amity.save_state(args = {'--db' : "amity.db"}),"Data successfully saved to database!")

    def test_load_state(self):
        '''this test load state functionality where data is loaded from db into application'''
        self.assertEqual(self.amity.load_state(args = {'--db' : "amity.db"}),"Data has been successfully loaded into the app")


if __name__ == '__main__':

       unittest.main()
