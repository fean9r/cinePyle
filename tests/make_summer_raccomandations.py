'''
Created on Jun 16, 2016

@author: fean0r
'''
from best_activities.decider import DecisionMaker

from cinepylia.rating_assigner import MoviesRatingAssigner
from cinepylia.film_decider import DecisionConstraints
from cinepylia.decision_maker import SchedulerConstraints


def __main__():
    # Fill the Agenda with your events
    my_cal = GoogleCalendar(start="", end="")
    my_cal.retreive()
    # my_agenda.add_busy_hours("Work", start = Hour(8, 30), stop = Hour(17, 30), validiy = [WEEK_DAYS.MONDAY, WEEK_DAYS.TUESDAY, WEEK_DAYS.WEDNESDAY, WEEK_DAYS.THURSDAY, WEEK_DAYS.FRIDAY])
    # my_agenda.add_event(Event("Portugal", start = Date(2017, 6, 23), all_day = True, duration = 5))
    # my_agenda.add_event(Event("Surgery", start = Date(2017, 6, 29), all_day = True, duration = 3))
    # my_agenda.add_event(Event("Loctudy trip", start = Date(2017, 7, 13), all_day = True, duration = 4))
    
    # Retrive the activities 
    # cinematheque_urls = ['http://www.cinematheque.fr/calendrier/06-2017.html', 'http://www.cinematheque.fr/calendrier/07-2017.html']
    cine_cal = CinemathequeCalendar(start="", end="")
    cine_cal.retreive()
    
    #cine_cal.remove_overlapping_events(my_cal.events())
    
    
    #cinematheque_retreiver = CinematequeFilmRetriever(cinematheque_urls)
    #cinematheque_shows = cinematheque_retreiver.retreive()
    
    # Give Rating to activities :
    #MoviesRatingAssigner(cine_cal.events())
    
    # Set the decision constraints 
    constraints = SchedulerConstraints()
    constraints.add_rating_function(MoviesRatingAssigner)
    constraints.add_time_constraints(my_cal)
    constraints.set_max_activity_by_day = 1
    constraints.set_max_activity_by_week = 3
    constraints.add_activity_to_avoid("")
    constraints.add_activity_to_perfom("")
    
    # Get the best cinematheque_shows with my agenda and decision params
    decision_maker = Scheduler(constraints)
    best_shows = decision_maker.make_decision(cine_cal.events())
    # force_scrape=False, load_IMDb_directors=False, assign_ratings=False)    
    print best_shows
    # cine_cal.write_cvs("summer_films.cvs")
    
__main__()
