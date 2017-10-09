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
    
def compute_months(time_1 , time_2):
    months = []
    months.append('11-2017')
    return months

def make_cinematheque_show(event):
    start = int(time.mktime(time.strptime(event['start'], '%Y-%m-%d %H:%M:%S')))
    end = int(time.mktime(time.strptime(event['end'], '%Y-%m-%d %H:%M:%S'))) 
    title = event['title']#show_title.encode('utf-8')
    director = event['director'] #realisateur.encode('utf-8')
    timezone = event['timezone']
    return Show(title, start, end , 0 ,director )


from .model import Show
from .model import TimeInterval


from functools import wraps
import os, pickle

def with_pickle(func):
    print "ciao"
    @wraps(func)
    def wrap(*args):
        file_name = type(args[0]).__name__ + args[1] +'.pkl'
        if os.path.exists(file_name):
            print 'reading cached file'
            with open(file_name) as f:
                cache = pickle.load(f)
        else:
            print 'Running func'
            cache = func(*args)
            # update the cache file
            with open(file_name, 'wb') as f:
                pickle.dump(cache, f)
        return cache
    return wrap

class CinemathequeCalendarAdapter(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.calendar = CinemathequeCalendar.CinemqthequeCalendar()
    
    @with_pickle
    def retreive(self, month):
        return map(lambda x:make_cinematheque_show(x), self.calendar.getEvents(month))
    
    def retreiveSeances(self, time_1 , time_2):
        all_seances= []
        # depending on the months between time 1 and time 2
        months = compute_months(time_1 , time_2)
        for month in months:
            all_seances += self.retreive(month)
            
        return all_seances