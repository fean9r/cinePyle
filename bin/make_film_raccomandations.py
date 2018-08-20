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
    #start = datetime.datetime.now(tz=pytz.utc)
    start = datetime.datetime(2018, 8, 28, tzinfo=pytz.utc)
    end = datetime.datetime(2018, 12, 1, tzinfo=pytz.utc)

    # Fill the Agenda with your events
    personal_calendar = calendar.CalendarManager()
    personal_events = personal_calendar.retreiveEvents(start, end)

    # Retrive the activities 
    seances = cinematheque.retreive_seances(start, end)

    # Rate to activities :
    rated_seances = rating.assign_movie_rating(seances)

    # Remove from the seances the overlapping personal_events :
    remaining_seances = calendar.filter_overlapping_events(personal_events, rated_seances)

#     sceances_berg = [item for item in rated_seances if item.director == "Jean Renoir" ]
#     for i in sceance_mizo:
#         i.setValue(10)
    
    #remaining_seances = [x for x in remaining_seances if x.value > 7]
    avoid_list = ["Vertigo", "Match Point","La Honte","Le Bon, la brute et le truand","Le Magicien d'Oz","Le Septième sceau","Persona","La Règle du jeu"]
    watch_list = ["Orochi","Tsuma yo Bara no yo ni","Bianco, rosse e verdone","Elena et les hommes","Le journal d'une femme de chambre"]
    best_shows = decider.decide_best_films(remaining_seances, avoid_list, watch_list )
    print(len(best_shows[0]), best_shows[1], best_shows[1] / len(best_shows[0]))
    
    # personal_calendar.push_events(best_shows)
    calendar.write_cvs(best_shows[0], "Cinematheque_films.cvs")
    print("Ciao!")
__main__()
