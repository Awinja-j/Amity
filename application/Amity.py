class Amity(object):
    ''' this application should be able to be installed using a package '''
    ''' this applicaation should be linked to firebase '''
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
        ''' this prints the members of a room once a name is given'''
        pass
    def savestate(self, db_name):
        ''' this saves all the information to an sqlite db '''
        pass
    def loadstate(self, db_name):
        ''' this loads all the data from an sqlite db into the application '''
        pass