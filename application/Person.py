import random

from abc import ABCMeta, abstractmethod


class Person(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, person_name, want_accomodation):
        self.person_name = person_name
        self.want_accomodation = want_accomodation
        pin = random.randint(999, 9999)
        self.person_ID = pin


class Fellow(Person):
    def __init__(self, person_name, want_accomodation):
        Person.__init__(self, person_name, want_accomodation)
        self.person_role = 'fellow'
        self.room_type = 'livingSpace', 'office'

    def __repr__(self):
        return self.person_name


class Staff(Person):
    def __init__(self, person_name, want_accomodation):
        Person.__init__(self, person_name, want_accomodation)
        self.person_role = 'staff'
        self.room_type = 'office'

    def __repr__(self):
        return self.person_name
