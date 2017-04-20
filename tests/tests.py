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

import unittest
from Amity import Amity

class TestAmity(unittest.TestCase):

    def setUp(self):
       self.amity = Amity()
    
    def test_create_room(self):
       self.assertEqual(self.amity.createroom("Antonorivo","LivingSpace"),"Room Created Succesfully!")

    def test_create_room_that_already_exist(self):
        self.amity.createroom("LivingSpace", "Madagascar")
        self.assertEqual(self.amity.createroom("LivingSpace","Madagascar"),"Room already Exists")
    
    def test_create_room_multiple_offices(self):
        self.assertEqual(self.amity.createroom("Office","Nairobi", "Mombasa", "Lagos"),"Rooms Created Succesfully!")

    def test_create_room_multiple_livingspaces(self):
        self.assertEqual(self.amity.createroom("LivingSpace","Emerald","Ruby","Diamond","Opal"),"Rooms Created succesfully")

    def test_create_room_without_room_type(self):
        self.assertEqual(self.amity.createroom("Johberg"),"Room type not specified!")
    
    def test_create_room_with_wrong_datatype_name(self):
       self.assertEqual(self.amity.createroom(9192,"LivingSpace"),"Room name cannot be an integer")

    def test_add_person(self):
       ''' this tests succesful creation of Fellow who want accomodation '''
       self.assertEqual(self.amity.addperson("Joan Awinja","Fellow","Y"),"Person added succesfully")
       
       '''this tests succeful creation of Staff who want accomodation '''
       self.assertEqual(self.amity.addperson("Eric Oyondi","Staff","Y"),"Person added succesfully")
      
       ''' this tests succesful creation of Fellow who does not  want accomodation '''
       self.assertEqual(self.amity.addperson("John Liboyi","Fellow","N"),"Person added succesfully")
       
       ''' this tests succesfull creation of Staff who does not want accomodation'''
       self.assertEqual(self.amity.addperson("Mike Katiechi","Staff","N"),"Person added succesfully")
       
       ''' this tests succesfull creation of Fellows with No accomoadation status '''
       self.assertEqual(self.amity.addperson("Tom Ingari","Fellow"),"Person added succesfully")
       
       ''' this tests succesfull creation of staff with No accomodation status '''
       self.assertEqual(self.amity.addperson("Fredrick Omukunda","Staff"),"Person added succesfully")
    
    def test_add_person_with_missing_employement_status(self):
       self.assertEqual(self.amity.addperson("Sharon Kandie", "Y"),"Please Give full deatils of person you are trying to add")

    def test_add_person_when_there_is_no_space(self):
       self.amity.createroom("LivingSpace", "Malasia")
       self.amity.addperson("Dennis Mokandu","Fellow","Y")
       self.amity.addperson("Jeff Kanyari","Fellow","Y")
       self.amity.addperson("Linnet Kanyari","Fellow","Y")
       self.amity.addperson("Vivian Perose","Fellow","Y")
       self.amity.addperson("Angela Mutava","Fellow","Y")
       self.amity.addperson("Cecilia Wahome","Fellow","Y")
       self.assertEqual(self.amity.addperson("Jasmine Khasoa","Fellow","Y"),"Sorry there is no more rooms available for occupation.Please create one")
       
    def test_add_person_existing(self):
       ''' this test add person functionality when the name details already exist'''
       self.amity.addperson("James Nyakenyanya","Fellow","N")
       self.assertEqual(self.amity.addperson("James Nyakenyanya","Fellow","N"),"This name combination already exists would you like to edit it?")
       
    def test_add_person_existing_swapped_details(self):
       ''' this tests add person functionlity-existing combination different status(fellow|staff) '''
       self.amity.addperson("Jeffery Eyama","Staff","N")
       self.assertEqual(self.amity.addperson("Jeffery Eyama","Fellow","Y"),"This name combination already exists would you like to edit it?")
       
    def test_reallocate(self):
       ''' this tests reallocate person functionality '''
       self.amity.addperson("Joan Awinja","Fellow","Y")
       self.amity.createroom("LivingSpace","Ruby","Opal")
       self.assertEqual(self.amity.reallocate("Joan Awinja","Ruby"),"reallocation succesfull")

    def test_reallocate_to_full_room(self):
       self.amity.createroom("LivingSpace", "Mongolia","Jade")
       self.amity.addperson("Jeffery Liboyi","Fellow","Y")
       self.amity.addperson("Jeffery Ingari","Fellow","Y")
       self.amity.addperson("Jeffery Vera","Fellow","Y")
       self.amity.addperson("Jeffery Caroline","Fellow","Y")
       self.amity.addperson("Jeffery Doe","Fellow","Y")
       self.amity.addperson("Jeffery Sabuni","Fellow","Y")
       self.amity.addperson("Emma Kipkech", "Fellow", "Y")
       self.amity.reallocate("Jeffery Liboyi","Mongolia")
       self.amity.reallocate("Jeffery Ingari","Mongolia")
       self.amity.reallocate("Jeffery Vera","Mongolia")
       self.amity.reallocate("Jeffery Caroline","Mongolia")
       self.amity.reallocate("Jeffery Doe","Mongolia")
       self.amity.reallocate("Jeffery Sabuni","Mongolia")
       self.assertEqual(self.amity.reallocate("Emma Kipkech","Mongolia"),"Sorry this room is full")

    def test_reallocate_staff(self):
       ''' this tests reallocate functionality for a staff to livingspace and raises an error''' 
       self.amity.createroom("LivingSpace","Ruby")
       self.amity.createroom("Office","Califonia")
       self.amity.addperson("Karen Kinoti","Staff","Y")
       self.assertEqual(self.amity.reallocate("Karen Kinoti","Ruby"),"You cannot reallocate Staff to Living Space")

    def test_reallocate_to_a_room_that_does_not_exist(self):
       ''' this tests reallocate functionality to a room that does not exist'''
       self.amity.createroom("Office", "Ruby")
       self.amity.addperson("George Oliwa", "Staff", "Y")
       self.assertEqual(self.amity.reallocate("George Oliwa","Accra"),"Sorry this room does not exist. Please create it.")

    def test_reallocate_a_person_that_does_not_exist(self):
       '''this tests application response to trying to reallocate a preson who is not in the syste,m'''
       self.amity.createroom("Office", "Ray","kendrick")
       self.assertEqual(self.amity.reallocate("Shem Ogumbe","Ray"),"This person does not Exist in the system")

    def test_load_people_to_a_room_using_file(self):
       '''this tests loading people succesfully to the application using a text file '''
       self.assertEqual(self.amity.loadpeople("files/people.txt"),"file uploaded succesfully")

    def test_load_people_to_a_room_using_empty_file(self):
       '''this test loading people to the application using a text file that is empty '''
       self.assertEqual(self.amity.loadpeople("files/empty_file.txt"),"This file is empty")

    def test_print_allocation(self):
       ''' this tests print the names of the people and the room they are  allocated to'''
       self.assertEqual(self.amity.printallocation(),"Print sucessfull")

    def test_print_room(self):
       '''this tests print room functionality'''
       self.amity.createroom("Office", "Mombasa")
       self.amity.addperson("Joan Awinja", "fellow","Y")
       self.amity.addperson("Jeff Ingari", "fellow","Y")
       self.amity.addperson("Jeremy Atema", "fellow","Y")
       self.assertEqual(self.amity.printroom("Mombasa"),"Mombasa: Joan Awinja, Jeff Ingari, Jeremy Atema")

    def test_print_room_that_is_not_in_the_system(self):
       '''this tests printint members of a room that is not in the system'''
       self.assertEqual(self.amity.printroom("Valhala"),"This room does not exist in the system")

    def test_print_unallocated(self):
       ''' this tests print unallocated functionality'''
       self.amity.createroom("Office", "Mombasa")
       self.amity.addperson("Joan Awinja", "fellow", "Y")
       self.amity.addperson("flavian Kanaiza", "fellow", "Y")
       self.amity.addperson("Karen Kinoti", "fellow")
       self.assertEqual(self.amity.printunallocated(),"Karen Kinoti")


    def test_save_state(self):
       '''this tests save state functionality where data is loaded from the application to an sqlitedb'''
       self.assertEqual(self.amity.savestate('amitydb'),"saved succesfully")

    def test_load_state(self):
        '''this test load state functionality where data is loaded from db into application'''
        self.assertEqual(self.amity.loadstate("amitydb"),"Information loaded succesfully")


if __name__ == '__main__':

       unittest.main()
