'''
Created on Sep 18, 2017

@author: fean9r
'''
class Decision(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''

class DecisionConstraints(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
class SchedulerConstraints(DecisionConstraints):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
class TSPConstraints(DecisionConstraints):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''        

class DecisionMaker(object):
    '''
    classdocs
    '''


    def __init__(self, constraint):
        '''
        Constructor
        '''
        self._constraint = constraint
    
    @abc.abstractmethod
    def make_decision(self):
        pass

class Scheduler(DecisionMaker):
    '''
    classdocs
    '''


    def __init__(self, constraint):
        '''
        Constructor
        '''
        DecisionMaker.__init__(self, constraint) 
    
    @abc.abstractmethod
    def make_decision(self):
        pass
    
class TSP(DecisionMaker):
    '''
    classdocs
    '''


    def __init__(self, constraint):
        '''
        Constructor
        '''
        DecisionMaker.__init__(self, constraint) 
    
    @abc.abstractmethod
    def make_decision(self):
        pass