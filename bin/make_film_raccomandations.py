# -*- coding: utf-8 -*-
'''
Created on Jun 16, 2016

@author: fean0r
'''

from cinepyle import calendar
from cinepyle import cinematheque
from cinepyle import rating
from opchoice import scheduler

import datetime
import pytz

def __main__():
    start = datetime.datetime.now(tz=pytz.utc)
    end = datetime.datetime(2017, 12, 31, tzinfo=pytz.utc)

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
    constraints.max_activity_by_day = 1
    constraints.max_activity_by_week = 3
    
    avoid_list = ["The Pianist", "My Darling Clementine"]
    
    for avoid in avoid_list:
        constraints.addActivityToAvoid(avoid)

    watch_list = ["L'Assassin habite au 21","Brasil / Le Corbeau", "Les Diaboliques",
                  "Manon","Miquette et sa mère","Le Mystère Picasso",
                  "Quai des Orfèvres","Le Salaire de la peur","Le 41e",
                  "Aerograd","Alexandre Nevski","Le Chemin de la vie",
                  "L'Enfance de Gorki","La Fièvre des échecs","La Grève",
                  "Ivan le Terrible","La Jeunesse de Maxime","Kino-Nedelia",
                  "Kino-Pravda n° 21 : un cinépoème sur Lénine","La Nouvelle Babylone","La Symphonie du Donbass",
                  "Tarass l'indompté","Trois chants sur Lénine","Zvenigora"]
    
    for watch in watch_list :
        found = 0
        for film in seances:
            if watch == film.name or  watch == film.original_title:
                print "\tWatch",film.name, film.original_title
                found = 1
                constraints.addActivityToPerform(film.name)
        if found == 0:
            print "\tNot found", watch

    # Get the best cinematheque_shows with my agenda and decision params
    decision_maker = scheduler.Scheduler(constraints)
    best_shows = decision_maker.make_decision(rated_seances)
    print len(best_shows[0]),best_shows[1],  best_shows[1]/len(best_shows[0])
    
    # personal_calendar.push_events(best_shows)
    calendar.write_cvs(best_shows[0], "Cinematheque_films.cvs")
    
__main__()
