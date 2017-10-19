'''
Created on Oct 7, 2017

@author: fean9r
'''
# class Event(object):
#     '''
#     classdocs
#     '''
# 
# 
#     def __init__(self, params):
#         '''
#         Constructor
#         '''
# 
# class Calendar(object):
#     '''
#     classdocs
#     '''
# 
# 
#     def __init__(self, strategy, params):
#         '''
#         Constructor
#         '''
#         self._retreiving_strategy = strategy
# 
#     def retreive(self):
#         print "retreive" 
#         self._retreiving_strategy.algorithm_interface()
#     
#     def remove_overlapping_events(self, events):
#         print "remove other over"  ,events 
#         
#     def export(self):
#         print"ciao"
#
         
from calendar import GoogleCalendar
from calendar import CinemathequeCalendar

from model import Activity
import dateutil.parser
import time


def make_internal_time(g_time):

    date = dateutil.parser.parse(g_time)
    return int(time.mktime(date.timetuple()))
    
    
class GoogleCalendarAdapter(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.calendar = GoogleCalendar.GoogleCalendar()
        
    def retreiveEvents(self, time_1 , time_2):
        activities = []
        
        events = self.calendar.getEvents(time_1 , time_2)
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = make_internal_time(event['start'].values()[0])
            end = make_internal_time(event['end'].values()[0])
            act = Activity(event['summary'],start, end,0)
            activities.append(act)            
        return activities
    