class Amity(object):
    roomname = []
    def createroom(self, *args):
        '''this creates a room'''
        pass
    def addperson(self, *args):
        """this adds a person"""
        pass
    def reallocate(self,name, room):
        """this reallocates a person"""
        pass
    def loadpeople(self, filename):
        """loads people from text file filename.txt"""
        pass
    def printallocation(self):
        """prints office and livingspace  allocation for fellows and staff
        you can also choose to optionally save them to a text file"""
        pass
    def printunallocated(self):
        """prints fellows and staff who have not been allocated to rooms
        you can also choose to optionally save them to a text file"""
        pass
    def printroom(self, room_name):
        pass
    def savestate(self, db_name):
        pass
    def loadstate(self, db_name):
        pass