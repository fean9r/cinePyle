# -*- coding: utf-8 -*-
'''
Created on Jun 16, 2016

@author: fean0r
'''

from cinepyle import calendar
from cinepyle import cinematheque
from cinepyle import rating
from cinepyle import decider

from datetime import datetime

import pytz
import json

def make_raccomandations(config):

    start = datetime.strptime(config['start'], '%Y/%m/%d')
    start = pytz.utc.localize(start)
    end = datetime.strptime(config['end'], '%Y/%m/%d')
    end = pytz.utc.localize(end)

    avoid = config['avoid']
    watch = config['watch']
    per_day = config['max_per_day']
    per_week = config['max_per_week']

    # Fill the Agenda with your events
    personal_calendar = calendar.CalendarManager()
    personal_events = personal_calendar.retreiveEvents(start, end)

    # Retrive the activities
    seances = cinematheque.retreive_seances(start, end)

    # Rate to activities :
    rated_seances = rating.assign_movie_rating(seances)

    # Remove from the seances the overlapping personal_events :
    remaining_seances = calendar.filter_overlapping_events(personal_events, rated_seances)

    best_shows = decider.decide_best_films(remaining_seances, avoid, watch, per_day, per_week)
    print(len(best_shows[0]), best_shows[1], best_shows[1] / len(best_shows[0]))

    # personal_calendar.push_events(best_shows)
    calendar.write_cvs(best_shows[0], "Cinematheque_films.cvs")
    print("Done!")

if __name__ == "__main__" :
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', type=str, help='network name', required=True)
    args = parser.parse_args()

    filename = args.config
    with open(filename) as f:
        config = json.loads(f.read())
        make_raccomandations(config)
