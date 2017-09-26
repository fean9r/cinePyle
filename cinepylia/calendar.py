'''
Created on Sep 17, 2017

@author: fean9r
'''

class Event(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''

class Calendar(object):
    '''
    classdocs
    '''


    def __init__(self, strategy, params):
        '''
        Constructor
        '''
        self._retreiving_strategy = strategy

    def retreive(self):
        print "retreive" 
        self._retreiving_strategy.algorithm_interface()
    
    def remove_overlapping_events(self, events):
        print "remove other over"  ,events 
        
    def export(self):
        print"ciao"
        
class GoogleCalendar(Calendar):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        Calendar.__init__(self, GoogleRetrivingStrategy()) 

class CinemqthequeCalendar(Calendar):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        Calendar.__init__(self, CinemqthequeRetrivingStrategy())     