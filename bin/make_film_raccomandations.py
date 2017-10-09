'''
Created on Jun 16, 2016

@author: fean0r
'''

from cinepyle import CalendarAdapters
# from cinepylia.rating import MoviesRatingAssigner
# import opchoice

import datetime

def __main__():
    
    start = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    end = datetime.datetime.strptime('2017-12-31','%Y-%m-%d').isoformat() + 'Z'
    
    
    # Fill the Agenda with your events
    personal_calendar = CalendarAdapters.GoogleCalendarAdapter()
    events = personal_calendar.retreiveEvents(start, end)
    #for event in events:
    #    print(event)

    
    # Retrive the activities 
    cine_cal = CalendarAdapters.CinemathequeCalendarAdapter()
    seances = cine_cal.retreiveSeances(start, end)
    for seance in seances:
        print(seance)
        
    #cine_cal.remove_overlapping_events(my_cal.events())
    
    
    #cinematheque_retreiver = CinematequeFilmRetriever(cinematheque_urls)
    #cinematheque_shows = cinematheque_retreiver.retreive()
    
    # Give Rating to activities :
    #MoviesRatingAssigner(cine_cal.events())
    
    # Set the decision constraints 
#     constraints = opchoice.SchedulerConstraints()
#     constraints.add_rating_function(MoviesRatingAssigner)
#     constraints.add_time_constraints(personal_calendar)
#     constraints.set_max_activity_by_day = 1
#     constraints.set_max_activity_by_week = 3
#     constraints.add_activity_to_avoid("")
#     constraints.add_activity_to_perfom("")
#     
#     # Get the best cinematheque_shows with my agenda and decision params
#     decision_maker = opchoice.Scheduler(constraints)
#     best_shows = decision_maker.make_decision(cine_cal.events())
#     # force_scrape=False, load_IMDb_directors=False, assign_ratings=False)    
#     print best_shows
#     # cine_cal.write_cvs("summer_films.cvs")
    
__main__()
