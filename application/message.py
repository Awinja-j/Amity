# from Person import Person
# from Room import Room
#
# # put your own credentials here
# account_sid = "ACc684e833e5afc573a4cccee306537e95"
# auth_token = "8d835935196f549c04527d55adeac603"
#
# class Message(object):
#     def __init__(self, person_name, person_phone, ):
#         self.person_name = person_name
#         self.person_phone = person_phone
#
#     def text(self, name, messages):
#         """ send message to person with room allocated and saves texts into db"""
#         client = TwilioRestClient(account_sid, auth_token)
#         confirm = session.query(Contact).filter(
#              Contact.full_name.contains(name.lower())).all()
#         if len(confirm) > 1:
#             for i in confirm:
#                 print('[' + str(i.id) + ']' + i.full_name +
#                     ' ' + str(i.phone_number) + '\n')
#             print(type(name), name)
#             g = raw_input('Which ' + name + ': ')
#             for i in confirm:
#                 if i.id is int(g):
#                     client.messages.create(
#                         to=("+" + str(i.phone_number)),
#                         from_='+14026206866',
#                         body=messages)
#                     msg = Message(full_name=name, phone_messages=messages)
#                     session.add(msg)
#                     session.commit()
#             return ('Message saved  and sent succesfully!!!')
#         elif len(confirm) == 1:
#             client.messages.create(
#                 to=("+" + str(confirm[0].phone_number)),
#                 from_='+14026206866',
#                 body=messages)
#             msg = Message(full_name=name, phone_messages=messages)
#             session.add(msg)
#             session.commit()
#             return ('Message saved  and sent succesfully!!!')
#         else:
#             return ('Person not found!!!')

from twilio.rest import Client
from Person import Staff, Fellow
from Room import Room, Livingspace, Office
new_staff = []
new_fellow = []
# put your own credentials here
account_sid = 'ACc684e833e5afc573a4cccee306537e95'
auth_token = "8d835935196f549c04527d55adeac603"
class Amity(object):
    def checkavailablerooms(self):
        if not Room.offices and Room.Livingspace_room:
            print ("There are no rooms available, Please use the create command to make Rooms")

        else:
            (Room.available_room).append(Room.Livingspace_room)
            (Room.available_room).append(Room.offices)
            for x in Room.available_room:
                if x == "Office" and len(x) < 4:
                    print ("The following Office space" + x + "has spaces available for occupation" )
                elif x == "Livingspace" and len(x) < 6:
                    print ("The following Livingspace" + x + "has spaces available for occupation")

    def createroom(self, room_type, room_name):
            if room_type == 'Office':
                if Room.offices:
                    office = Office(room_type, room_name)
                    for item in Room.offices:
                        if item == room_name:
                            return (office.room_name + 'already exists in Amity')
                        else:
                            print(room_name)
                            return ((Room.offices).append(office))
            if room_type == 'Livingspace':
                if Room.Livingspace_room:
                    lv = Livingspace(room_type, room_name)
                    for item in Room.Livingspace_room:
                        if item == room_name:
                            return (lv.room_name + 'already exists in Amity')
                        else:
                            print(room_name)
                            return ((Room.Livingspace_room).append(lv))


    def addperson(self, person_name, person_role, person_accomodation, person_phone):
        if person_role == 'STAFF':
            staff = Staff(person_name, person_role, person_accomodation, person_phone)
            if staff.person_phone == '':
                new_staff.append(staff)
                return (staff.person_name + 'Has been allocated succesfully!!')
            else:
                new_staff.append(staff)
                client = Client(account_sid, auth_token)
                client.messages.create(
                    to=person_phone,
                    from_="+14026206866",
                    body='Hello' + staff.person_name + ', ' + 'you have been allocated to Andela. Amity')
        if person_role == 'FELLOW':
            fellow = Fellow(person_name, person_role, person_accomodation, person_phone)
            if fellow.person_phone == '':
                new_fellow.append(fellow)
                return (fellow.person_name + 'Has been allocated succesfully!!')
            else:
                new_fellow.append(fellow)
                client = Client(account_sid, auth_token)
                client.messages.create(
                    to=person_phone,
                    from_="+14026206866",
                    body='Hello' + fellow.person_name + ', ' + 'you have been allocated to Andela. Amity')


amity = Amity()
amity.addperson("Joan Awinja", "STAFF","N", "+254725792909")
amity.addperson("Joan Awinja", "STAFF","N", "")
amity.createroom("Office", "Narnia")
amity.createroom("Livingspace", "Ruby")
