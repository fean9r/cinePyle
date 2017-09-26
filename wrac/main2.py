'''
Created on Sep 13, 2016

@author: fean0r
'''
from best_activities.model import Show
from best_activities.model import TimeInterval
from best_activities.model import overlap
from best_activities.rating_adviser import RatingHelper
from best_activities.rating_adviser import assign_IMDb_ratings
from best_activities.rating_adviser import get_director_map
from best_activities.scheduler import GraphActivitiesDecisor
from best_activities.scheduler import PLActivitiesDecisor
from best_activities.site_scraper import scrape_cinematheque_films
from best_activities.utils import picklIn
from best_activities.utils import picklOut
from best_activities.utils import similar
from best_activities.utils import write_cvs

import time
import datetime
import calendar


def make_busy_days(year, month, day, n_days):
    
    busy_date_start_str = str(year) + '-' + str(month) + '-' + str(day)
    date = datetime.datetime.strptime(busy_date_start_str + ' 01:00:00', '%Y-%m-%d %H:%M:%S')
    busy_date_start_epoch = int(time.mktime(date.timetuple()))
    busy_date_end_epoch = busy_date_start_epoch + n_days * 24 * 3600
    return TimeInterval(busy_date_start_epoch, busy_date_end_epoch)

def make_weeks_of_busy_times(year, month, num_of_weeks):
    calendar_month = calendar.monthcalendar(year, month)
    first_week = calendar_month[0]
    second_week = calendar_month[1]
    if first_week[calendar.MONDAY]:
        first_monday_day = str(first_week[calendar.MONDAY])
    else:
        first_monday_day = str(second_week[calendar.MONDAY])
    first_monday_date_str = str(year) + '-' + str(month) + '-' + first_monday_day
    # print 'First monday is:', first_monday_date_str
    date = datetime.datetime.strptime(first_monday_date_str + ' 01:00:00', '%Y-%m-%d %H:%M:%S')
    month_first_monday = int(time.mktime(date.timetuple()))
    
    busy_list = []
    # Build num_of_weeks busy periods of time
    for i in range(num_of_weeks):
        monday_start = month_first_monday + i * 7 * 24 * 3600
        # Make the day busy times i 0 -> 5
        for j in range(5):
            day_j_week_i_startS = monday_start + 24 * j * 3600
            day_j_week_i_startE = day_j_week_i_startS + 17 * 3600
            busy_list.append(TimeInterval(day_j_week_i_startS, day_j_week_i_startE))        
    return  busy_list 

def scrape_movies_from_url(cinematheque_url, force_scrape):
    month , year = cinematheque_url.split("/")[-1].split(".")[0].split("-")
    cine_pkl_file = 'cinematheque_films' + '_' + month + '_' + year + '.pkl'
    # 1 method that gathers the cinematheque's movies
    print "Scraping Movies", month , year, ":" 
    if force_scrape :
        # compute and store
        cinematheque_films = scrape_cinematheque_films(cinematheque_url)
        picklOut(cinematheque_films, out_file=cine_pkl_file)
    else :
        # print 'Unpickling the cinematheque_films from disk'
        cinematheque_films = picklIn(in_file=cine_pkl_file) 
    return cinematheque_films

def best_cine_moviesPL(cinematheque_urls, busy_days, avoid_list, force_scrape=False, load_IMDb_directors=False, assign_ratings=False, write_cvs=False):
 
    month_s , year_s = cinematheque_urls[0].split("/")[-1].split(".")[0].split("-")
    month_e , year_e = cinematheque_urls[-1].split("/")[-1].split(".")[0].split("-")
    how_many_weeks = (int(month_e) - int(month_s) + 1) * 5 
    
    # Scrape as many times as urls
    cinematheque_films = []
    for url_i in cinematheque_urls:
        cinematheque_films = cinematheque_films + scrape_movies_from_url(url_i, force_scrape)
    print 'Scraped', len(cinematheque_films), 'activities from cinematheque site.'
    # Make busy list
    busy_list = make_weeks_of_busy_times(int(year_s), int(month_s), how_many_weeks)

    # Filter events without director 
    cinematheque_films = filter(lambda x: x if (x.director != '') else None, cinematheque_films)

    # Filter based on busy list
    for interval in busy_list:
        cinematheque_films = filter(lambda x: None if ( overlap(x.interval, interval)) else x, cinematheque_films)
    print 'Remaining', len(cinematheque_films), 'activities after busy periods filtering.'

    # 2 method to load from imdb the list of directors of the cinematheque films
    directors_pkl_file = 'directorToFilm_map' + '_' + month_s + '_' + year_s + '_' + month_e + '_' + year_e + '.pkl'
    print "Loading IMDB directors:"
    if (load_IMDb_directors):
        director_names_uniq = set()
        for film in cinematheque_films:
            director_names_uniq.add(film.director)
        # clean a little the directors set
        if '' in director_names_uniq:
            director_names_uniq.remove('')
        if 'Anonyme' in director_names_uniq:
            director_names_uniq.remove('Anonyme')
        # print director_names_uniq
        
        directorToFilm_map = get_director_map(director_names_uniq)
        # print 'Pickling on disk the directorToFilm_map'
        picklOut(directorToFilm_map, out_file=directors_pkl_file)
    else:
        # print 'Unpickling the directorToFilm_map from disk \n'
        directorToFilm_map = picklIn(in_file=directors_pkl_file)

    # 3 method to assign ratings to the movies take them from imdb
    cine_pkl_file = 'cinematheque_filmsWithRate' + '_' + month_s + '_' + year_s + '_' + month_e + '_' + year_e + '.pkl'
    print "Assigning ratings to Movies:"
    if (assign_ratings):
        assign_IMDb_ratings(cinematheque_films, directorToFilm_map)
        # print 'Pickling on disk the Rated cinematheque_films'
        picklOut(cinematheque_films, out_file=cine_pkl_file)
    else:
        # print 'Unpickling the Rated cinematheque_films from disk \n'
        cinematheque_films = picklIn(in_file=cine_pkl_file) 
  
    # print "".join(str(interval)+'\n' for interval in busy_list)
    
    # Change the rating to weight it by number of votes
    rating_help = RatingHelper(750)
    [rating_help.add_rating(film.value) for film in cinematheque_films]
    [film.setValue( rating_help.get_true_bayesian_rating(film.value, int(film.votes))) for film in cinematheque_films]
    print [(film.name, film.value) for film in cinematheque_films]
    # 4 Filter from the activities list the activities that overlap with the busy periods
    # or have a rating inferior to the minimum or you have already seen it
    # TBD
    # seen_list = [0] * len(self.cinematheque_films)
    minRating = 7.0
    for interval in busy_list:
        cinematheque_films = filter(lambda x: None if (x.value < minRating) else x, cinematheque_films)
    print 'Remained:', len(cinematheque_films), 'film after rating filtering.'
    
    # Filter based on avoid film list
    for film_name in avoid_list:
        cinematheque_films = filter(lambda x: None if (similar(x.name, film_name) > 0.7) else x, cinematheque_films)
    print 'Remaining', len(cinematheque_films), 'activities after avoid film filtering.'
      
    for interval in busy_days:
        cinematheque_films = filter(lambda x: None if (overlap(x.interval, interval)) else x, cinematheque_films)
    print 'Remaining', len(cinematheque_films), 'activities afterbusy periods filtering.'
    
    # 5 method to assign ratings to the movies take them from imdb
    print "----# Decide films #----"
    pl_decisor = PLActivitiesDecisor(cinematheque_films, max_film_for_day=1)
    pl_decision = pl_decisor.decideActivities()   
    print len(pl_decision[0]), 'movies with', pl_decision[1], ' AVG rating of:', pl_decision[1] / len(pl_decision[0])
    
    tot_film_duration = 0
    for act in pl_decision[0]:
        tot_film_duration += act.interval.duration
    print "Tot hours:", tot_film_duration / 60.0 / 60.0
    
    cal_head = 'Subject,Start Date,Start Time,End Date,End Time,Description,Location\n'
    cal_events = []    
    for act in pl_decision[0]:
        subject = '"' + act.name + '"'
        start_date = act.interval.start_date()
        start_time = act.interval.start_time()
        end_date = act.interval.end_date()
        end_time = act.interval.end_time()
        description = '"' + act.director + ' IMDb Rating ' + str("%.2f" % act.value) + ' '+ str(act.votes)+' votes"'
        location = 'Cinematheque\n'
        cal_events.append(subject + ',' + start_date + ',' + start_time + ',' + end_date + ',' + end_time + ',' + description + ',' + location)
    

    if write_cvs:
        write_cvs(cal_head, cal_events, file_name ='cine_calendar.cvs')


def __main__():
    cinematheque_urls = ['http://www.cinematheque.fr/calendrier/03-2017.html', 'http://www.cinematheque.fr/calendrier/04-2017.html', 'http://www.cinematheque.fr/calendrier/05-2017.html']
    avoid_list = ['Mr Smith Goes to Washington', 'It\'s a Wonderful Life','Seven']

    normandie_busy_days = make_busy_days(2017, 04, 7, 3)
    roma_busy_days = make_busy_days(2017, 04, 13, 6)
    genLisa_busy_days = make_busy_days(2017, 05, 19, 3)
    malta_busy_days = make_busy_days(2017, 06, 1, 6)
    busy_days = [normandie_busy_days, roma_busy_days, genLisa_busy_days,malta_busy_days]
    
    force_scrape = False
    load_IMDb_directors = False
    assign_ratings = False
    write_cvs = False
    best_cine_moviesPL(cinematheque_urls, busy_days, avoid_list, force_scrape, load_IMDb_directors, assign_ratings, write_cvs)    
    
# import cProfile
# cProfile.run('__main__()', sort='tottime')
    
__main__()
