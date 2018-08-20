# -*- coding: utf-8 -*-
'''
Created on Jun 16, 2016

@author: fean0r
'''

from cinepyle import calendar
from cinepyle import cinematheque
from cinepyle import rating
from cinepyle import decider

import datetime
import pytz

def __main__():
    start = datetime.datetime.now(tz=pytz.utc)
    end = datetime.datetime(2018, 1, 28, tzinfo=pytz.utc)

    # Fill the Agenda with your events
    personal_calendar = calendar.CalendarManager()
    events = personal_calendar.retreiveEvents(start, end)
    print (events)
    # Retrive the activities 
    seances = cinematheque.retreive_seances(start, end)

    # Remove from the seances the overlapping events :    
    remaining_seances = calendar.filter_overlapping_events(events, seances)

    #sceances_berg = [item for item in rated_seances if item.director == "Ingmar Bergman" ]
#     for i in sceance_mizo:
#         i.setValue(10)
    
    remaining_seances = [x for x in remaining_seances if x.value > 7]
    avoid_list = []
    watch_list = []

    best_shows = decider.decide_best_films(remaining_seances, avoid_list, watch_list )

    print(len(best_shows[0]), best_shows[1], best_shows[1] / len(best_shows[0]))
    
    # personal_calendar.push_events(best_shows)
    calendar.write_cvs(best_shows[0], "Cinematheque_films.cvs")
    
__main__()
