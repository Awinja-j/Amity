class Person(object):
    def __init__(self, person_name, person_role, person_accomodation, person_phone):
       self.person_name = person_name
       self.person_role = person_role
       self.person_accomodation = person_accomodation
       self.person_phone = person_phone
       
class Fellow(Person):
    def __init__(self, person_name, person_role, person_accomodation, person_phone):
        Person.__init__(self, person_name, person_role, person_accomodation, person_phone)
        self.room_type = "LivingSpace"

   
class Staff(Person):
    def __init__(self, person_name, person_role,person_accomodation, person_phone):
        Person.__init__(self, person_name, person_role,person_accomodation, person_phone)
        self.room_type = "office"