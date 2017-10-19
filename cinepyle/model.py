'''
Created on Sep 13, 2016

@author: fean0r
'''
from opchoice.model import Activity

class Show(Activity):
    """
      
    """
    
    def __init__(self, name, start, end, value, director):   
        Activity.__init__(self, name, start, end, value) 
        self.director = director.replace(',', ' &').decode('utf-8') 
#     def __repr__(self):
#         return "%s director: %s" % (super(Show, self).__str__(), self.director)
    
    def setVotes(self, votes):
        self.votes= votes
    
    def setDescription(self, desc):
        self.description = desc
    
    def __str__(self):
        return "%s director: %s" % (super(Show, self).__str__(), self.director)
    
    __repr__ = __str__
