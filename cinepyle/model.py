'''
Created on Sep 13, 2016

@author: fean0r
'''
import datetime
import sys


reload(sys)
sys.setdefaultencoding('utf-8')

class TimeInterval(object):
    def __init__(self, start, end , timezone='Europe/Paris'):    
        self.start = start
        self.end = end 
        self.duration = self.end - self.start
    
    def start_date(self):
        s_date = datetime.datetime.fromtimestamp(self.start).strftime('%Y-%m-%d')
        return "%s" % (s_date)
    def start_time(self):
        s_time = datetime.datetime.fromtimestamp(self.start).strftime('%H:%M:%S')
        return "%s" % (s_time)

    def end_date(self):
        e_date = datetime.datetime.fromtimestamp(self.end).strftime('%Y-%m-%d')
        return "%s" % (e_date)
    def end_time(self):
        e_time = datetime.datetime.fromtimestamp(self.end).strftime('%H:%M:%S')
        return "%s" % (e_time)
    
    def __str__(self):
        # 19h00  20h30 (88 min) 
        try:
            s = datetime.datetime.fromtimestamp(self.start).strftime('%Y-%m-%d %H:%M:%S')
            e = datetime.datetime.fromtimestamp(self.end).strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            print self.start , self.end
        return "%s -> %s (%s sec)" % (s, e , self.duration)

#     def __str__(self):
#         return self.__repr__().encode(stdout.encoding)    
    __repr__ = __str__
    
    def getEnd(self):
        return self.end
    
def overlap(interval1, interval2):
    overlap = False
    # ends after the beginning of the other and before its end   
    if interval2.start <= interval1.end <= interval2.end :
        overlap = True
    # Start after the beginning of the other and before its end 
    if interval2.start <= interval1.start <= interval2.end :
        overlap = True   
    return overlap
    
def same_day(interval1, interval2):
    same_day = False
    day1 = datetime.datetime.fromtimestamp(interval1.start).strftime('%Y-%m-%d') 
    day2 = datetime.datetime.fromtimestamp(interval2.start).strftime('%Y-%m-%d')
    if day1 == day2:
        same_day = True 
    return same_day
 
def same_week(interval1, interval2):
    same_week = False
    week1 = datetime.datetime.fromtimestamp(interval1.start).isocalendar()[1]
    week2 = datetime.datetime.fromtimestamp(interval2.start).isocalendar()[1]
    if week1 == week2:
        same_week = True 
    return same_week    
    
    
class Activity(object):
    """
      
    """
    
    def __init__(self, name, start, end, value):    
        self.name = name.decode('utf-8')
        self.interval = TimeInterval(start, end)
        self.value = value

    def setValue(self, value):
        self.value = value
    
    def __str__(self):
        # print self.name
        return "name: %s interval: %s value: %s" % (self.name, self.interval , self.value)

#     def __repr__(self):
#         return self.__repr__().encode(stdout.encoding)
    
    __repr__ = __str__


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
