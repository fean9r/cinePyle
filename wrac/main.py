'''
Created on Sep 13, 2016

@author: fean0r
'''
from best_activities.model import Show
from best_activities.model import TimeInterval
from best_activities.rating_adviser import assign_IMDb_ratings
from best_activities.rating_adviser import get_director_map
from best_activities.scheduler import GraphActivitiesDecisor
from best_activities.scheduler import PLActivitiesDecisor
from best_activities.site_scraper import scrape_cinematheque_films
from best_activities.utils import picklIn
from best_activities.utils import picklOut


def best_cine_movies(scrape_movies=False, load_IMDb_directors=False, assign_ratings=False, make_decision_Graph=False, make_decision_PL=False):

    # 1 method that gathers the cinematheque's movies
    if (scrape_movies):
        cinematheque_films = scrape_cinematheque_films('http://www.cinematheque.fr/calendrier/10-2016.html')
        print 'Pickling on disk the cinematheque_films'
        picklOut(cinematheque_films, out_file='cinematheque_films.pkl')
    else:
        print 'Unpickling the cinematheque_films from disk \n'
        cinematheque_films = picklIn(in_file='cinematheque_films.pkl') 
    
    # 2 method to load from imdb the list of directors of the cinematheque films
    if (load_IMDb_directors):
        director_names_uniq = set()
        for film in cinematheque_films:
            director_names_uniq.add(film.director)
        
        if '' in director_names_uniq:
            director_names_uniq.remove('')
        if 'Anonyme' in director_names_uniq:
            director_names_uniq.remove('Anonyme')
        print director_names_uniq
        directorToFilm_map = get_director_map(director_names_uniq)
        print 'Pickling on disk the directorToFilm_map'
        picklOut(directorToFilm_map, out_file='directorToFilm_map.pkl')
    else:
        print 'Unpickling the directorToFilm_map from disk \n'
        directorToFilm_map = picklIn(in_file='directorToFilm_map.pkl')
     
    # 3 method to assign ratings to the movies take them from imdb
    if (assign_ratings):
        assign_IMDb_ratings(cinematheque_films, directorToFilm_map)
        print 'Pickling on disk the Rated cinematheque_films'
        picklOut(cinematheque_films, out_file='cinematheque_filmsWithRate.pkl')
    else:
        print 'Unpickling the Rated cinematheque_films from disk \n'
        cinematheque_films = picklIn(in_file='cinematheque_filmsWithRate.pkl') 
     
    print 'The month has:', len(cinematheque_films), 'activities.'
     
     
    def make_week_busy_times(monday_start):
        # i 0 -> 5
        busy_list = []
        for i in range(5):   
            day_week_i_startS = monday_start + 24 * i * 3600
            day_week_i_startE = day_week_i_startS + 17 * 3600
         
    #         day_week_i_endS = day_week_i_startE + 5 *3600
    #         day_week_i_endE = day_week_i_endS+ + 1 *3600
         
            busy_list.append(TimeInterval(day_week_i_startS, day_week_i_startE))
    #         busy_list.append(TimeInterval(day_week_i_endS,day_week_i_endE ))
        return busy_list
         

    month_first_monday = 1472425200
    
    import time
    import datetime
    #str_date = datetime.datetime.fromtimestamp(month_first_monday).strftime('%Y-%m-%d %H:%M:%S')
    date= datetime.datetime.strptime('2016-10-3 01:00:00','%Y-%m-%d %H:%M:%S')
    month_first_monday = int( time.mktime(date.timetuple()))
    
    
    busy_list = []
    for i in range(5):
        busy_list_week_i = make_week_busy_times(month_first_monday + i * 7 * 24 * 3600)  
        busy_list = busy_list + busy_list_week_i
    # print "".join(str(interval)+'\n' for interval in busy_list)
     
    # 4 Filter from the activities list the activities that overlap with the busy periods
    # or have a rating inferior to the minimum or you have already seen it
    #TBD
    #seen_list = [0] * len(self.cinematheque_films)
    minRating = 6.6
    for interval in busy_list:
        cinematheque_films = filter(lambda x: None if (x.interval.overlap(interval) or x.value < minRating) else x, cinematheque_films)
    print 'Remained:', len(cinematheque_films), 'activities after filtering.'
     
     
    #cinematheque_films = cinematheque_films[0:50]   
    # 5 method to assign ratings to the movies take them from imdb
    if (make_decision_Graph):
        graph_decisor = GraphActivitiesDecisor(cinematheque_films)
        graph_decision = graph_decisor.decideActivities()
        print 'Pickling on disk the result'
        picklOut(graph_decision, out_file='cinematheque_filmsResult.pkl')
    else:
        print 'Graph Unpickling the result from disk \n'
        graph_decision = picklIn(in_file='cinematheque_filmsResult.pkl') 
    print len(graph_decision[0]), 'movies with', graph_decision[1], ' AVG rating of:', graph_decision[1] / len(graph_decision[0])
    
    if (make_decision_PL):
        pl_decisor = PLActivitiesDecisor(cinematheque_films, max_film_for_day=1)
        pl_decision = pl_decisor.decideActivities()
        print 'Pickling on disk the result'
        picklOut(pl_decision, out_file='cinematheque_filmsResultPL.pkl')
    else:
        print 'PL Unpickling the result from disk \n'
        pl_decision = picklIn(in_file='cinematheque_filmsResultPL.pkl') 
    
    print len(pl_decision[0]), 'movies with', pl_decision[1], ' AVG rating of:', pl_decision[1] / len(pl_decision[0])
    
    
    names = {}
    for i in graph_decision[0]:
        if names.has_key(i.name):
            names[i.name].append(i)
        else:
            names[i.name] = [i]
    d_map = names 
    for l_elem in d_map.values():
        if len(l_elem) >1:
            print True
    
#     for act in graph_decision[0]:
#         print act.name , act.interval
#         
#     print '___'
    tot_film_duration=0
    for act in pl_decision[0]:
        print act.name ,  act.interval
        tot_film_duration += act.interval.duration
    print tot_film_duration/60.0/60.0



def __main__():
    scrape_movies = False
    load_IMDb_directors = False
    assign_ratings = False
    make_decision_Graph = False
    make_decision_PL = True
    best_cine_movies(scrape_movies, load_IMDb_directors, assign_ratings, make_decision_Graph, make_decision_PL)    
    
# import cProfile
# cProfile.run('__main__()', sort='tottime')
    
__main__()




