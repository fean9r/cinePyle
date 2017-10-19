'''
Created on Jun 16, 2016

@author: fean0r
'''

from cinepyle import calendar
from cinepyle import cinematheque
from cinepyle import rating
from opchoice import scheduler

import datetime

def __main__():
    
    start = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    end = datetime.datetime.strptime('2017-12-31','%Y-%m-%d').isoformat() + 'Z'
    
    # Fill the Agenda with your events
    personal_calendar = calendar.CalendarManager()
    events = personal_calendar.retreiveEvents(start, end)

    # Retrive the activities 
    seances = cinematheque.retreive_seances(start, end)
    print seances
    
    # Remove from the seances the overlapping events :    
    #personal_calendar.removeOverlappingEvents(seances)
        
    # Rate to activities :
    rated_seances = rating.assign_movie_rating(seances)
    print rated_seances
    
    # Set the decision constraints 
    constraints = scheduler.SchedulerConstraints()
#    constraints.add_rating_function(rating_assigner.rate_one)
#    constraints.add_time_constraints(events)
    constraints.set_max_activity_by_day = 1
    constraints.set_max_activity_by_week = 3
    constraints.add_activity_to_avoid("")
    constraints.add_activity_to_perfom("")
     
    # Get the best cinematheque_shows with my agenda and decision params
    decision_maker = scheduler.Scheduler(constraints)
    best_shows = decision_maker.make_decision(rated_seances)
    print best_shows
    
    # personal_calendar.push_events(best_shows)
    # personal_calendar.writeCVS("Cinematheque_films.cvs")
    
__main__()
