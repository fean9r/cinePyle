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

    # Remove from the seances the overlapping events :    
    remaining_seances = calendar.filter_overlapping_events(events, seances)

    # Rate to activities :
    rated_seances = rating.assign_movie_rating(remaining_seances)
    
    # Set the decision constraints 
    constraints = scheduler.SchedulerConstraints()
#    constraints.add_rating_function(rating_assigner.rate_one)
#    constraints.add_time_constraints(events)
    constraints.max_activity_by_day = 1
    constraints.max_activity_by_week = 3
    #TODO: DO NOT WORK
    constraints.add_activity_to_avoid("The Pianist")
    constraints.add_activity_to_perfom("")
     
    # Get the best cinematheque_shows with my agenda and decision params
    decision_maker = scheduler.Scheduler(constraints)
    best_shows = decision_maker.make_decision(rated_seances)
    print len(best_shows[0]),best_shows[1],  best_shows[1]/len(best_shows[0])
    
    # personal_calendar.push_events(best_shows)
    calendar.write_cvs(best_shows[0], "Cinematheque_films.cvs")
    
__main__()
