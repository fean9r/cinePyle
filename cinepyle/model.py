'''
Created on Sep 13, 2016

@author: fean0r
'''
from opchoice.model import Activity

class Show(Activity):
    """
      
    """
    
    def __init__(self, orig_title, cine_title, start, end, value, director):
        Activity.__init__(self, orig_title, start, end, value)
        self.director = director.replace(',', ' &')
        self.cine_title = cine_title

    def setVotes(self, votes):
        self.votes= votes
    
    def setDescription(self, desc):
        self.description = desc
    
    def __str__(self):
        return "%s cine title: %s director: %s" % (super(Show, self).__str__(), self.cine_title, self.director)
    
    __repr__ = __str__
