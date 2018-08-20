'''
Created on Aug 21, 2018

@author: fean9r
'''
from opchoice import scheduler



def decide_best_films(seances, avoid_list, watch_list, max_per_day=1,max_per_week=3 ):
    # Set the decision constraints 
    constraints = scheduler.SchedulerConstraints()
    constraints.max_activity_by_day = max_per_day
    constraints.max_activity_by_week = max_per_week

    for avoid in avoid_list:
        found = 0
        for film in seances:
            if avoid == film.name or avoid == film.cine_title:
                print("\tAvoid", film.name, film.cine_title)
                found = 1
                constraints.addActivityToAvoid(film.name)
        if found == 0:
            print("\tNot found", avoid)
    
    for watch in watch_list :
        found = 0
        for film in seances:
            if watch == film.name or watch == film.cine_title:
                print("\tWatch", film.name, film.cine_title)
                found = 1
                constraints.addActivityToPerform(film.name)
        if found == 0:
            print("\tNot found", watch)
    
    # Get the best cinematheque_shows with my agenda and decision params
    decision_maker = scheduler.Scheduler(constraints)
    return decision_maker.make_decision(seances)
    
