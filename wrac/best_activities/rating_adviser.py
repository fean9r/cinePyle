'''
Created on Sep 13, 2016

@author: fean0r
'''
from imdb import IMDb

from .utils import ProgressBar
from .utils import similar, same_name


class RatingHelper(object):
    def __init__(self, min_for_top):    
        self.min_for_top = min_for_top
        self.num_stored_votes = 0.0
        self.sum_stored_vals = 0.0
        
    def add_rating(self, rating):
        self.num_stored_votes+=1.0
        self.sum_stored_vals+=rating
        
    def get_mean_vote(self):   
        return self.sum_stored_vals / self.num_stored_votes

    def get_true_bayesian_rating(self, film_rating, film_num_votes):
        #(WR) = (v / (v+m)) * R + (m / (v+m)) * C , where:
        # R = average for the movie (mean) = (Rating)
        # v = number of votes for the movie = (votes)
        # m = minimum votes required to be listed in the Top (currently 3000)
        # C = the mean vote across the whole report (currently 6.9)
        R = film_rating
        v = film_num_votes
        m = self.min_for_top
        C = self.get_mean_vote()
        WR = (v / (v+m+0.0)) * R + (m / (v+m+0.0)) * C
        return WR

def get_director_map(l_directorsNames):
    
    ia = IMDb()
    directorToFilm_map = {}
    pbar = ProgressBar(len(l_directorsNames))
    for director_name in l_directorsNames:
        print '\tAquiring informations from IMDb about :', director_name
        l_directorsForOneName = ia.search_person(director_name) 
        if len(l_directorsForOneName) == 0:
            print '\t', director_name, ' not found in IMDb'
            continue
        #!!!!!! We suppose that the first in the list is allways the one we are looking for.
        director = l_directorsForOneName[0]
        ia.update(director)
        l_films = []
        if director.data.has_key('director'):
            l_films += director[u'director']

        directorToFilm_map[director_name] = l_films
        pbar.progress()
    
    return directorToFilm_map


def search_single(film_name, director_name):
    
    if director_name == '':
        return (0, 0)
    
    ia = IMDb()
    film_list = ia.search_movie(film_name)
    print '\tSearching', film_name, 'directed by:', director_name
    for film in film_list:
        ia.update(film)
        if film.data.has_key('director'):
            # take the first director
            director = film['director'][0]
            if same_name(director['name'], director_name) and film.data.has_key('rating'):
                return (film['rating'] , film['votes'])
            else :
                print '\t\tOther director found:', director , 'continuing..'

    return (0, 0)

def assign_IMDb_ratings(films, directorToFilm_map):
    ia = IMDb()
       
    print '## We have', len(films), 'films to rate!'
    pbar = ProgressBar(len(films))
    
    for cinem_film in films:
        l_films = []
        if cinem_film.director in directorToFilm_map:
            l_films = directorToFilm_map[cinem_film.director]
        
        # Search the films in the director films that have a name similar to the one we retreived from the cinematheque.
        l_result = filter(lambda x: x if (similar(x['title'], cinem_film.name) > 0.7) else None, l_films)
        if len(l_result) > 1:
            # take the most similar one
            l_result = [reduce(lambda a,b: a if (similar(a['title'], cinem_film.name) > similar(b['title'], cinem_film.name)) else b, l_result)]
        if len(l_result) == 0:
            # no film found in director's film list continue to next director in director list
            # Try again by looking by movie name and match it with the director
            rating, votes = search_single(cinem_film.name, cinem_film.director)
            if rating == 0:
                print '\t\tNo film named', cinem_film.name , 'directed by', cinem_film.director, 'found on IMDb. Assigning: 6.5'
                rating = 6.5
                votes = 1
            cinem_film.setValue(rating)
            cinem_film.setVotes(votes)
        else :
            # one film found!
            film = l_result[0]
            ia.update(film)
            # print 'Imdb Rating for film:', film , 'is :', film['rating']
            if film.data.has_key('rating'):
                rating = float(film['rating'])
                votes = str(film['votes'])
            else:
                print '\t\tThe film named', cinem_film.name, 'directed by', cinem_film.director, 'not rated in IMDb! Assigning: 6.5'
                rating = 6.5
                votes = 1
            cinem_film.setValue(rating)
            cinem_film.setVotes(votes)

        pbar.progress()
