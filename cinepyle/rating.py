'''
Created on Jun 19, 2017

@author: ibreschi
'''
from . import utils
from imdb import IMDb

class MovieRatingAssigner(object):
    """
    Implementation of RatingAssigner.
    """

    def __init__(self):
        self.ia = IMDb()
        self.director_to_films = {}
    
    def fetch_movie_by_name(self, film_name, director_name):
        if director_name == '' or film_name == '':
            return None
        print '\tSearching', film_name, 'directed by:', director_name

        fetched_films = self.ia.search_movie(film_name)
    
        for film in fetched_films:
            self.ia.update(film)
            if film.data.has_key('director'):
                # take the first director
                director = film['director'][0]
                if utils.same_name(director['name'], director_name) and film.data.has_key('rating'):
                    return film
                else :
                    print '\t\tOther director found:', director , 'continuing..'
        return None
    
    @utils.with_pickle
    def fetch_directors(self, directors):
        director_to_films = {}
        directors = set(directors)       
        pbar = utils.ProgressBar(len(directors))
        for name in directors:
            print '\tAquiring informations about:', name
            directors_with_one_name = self.ia.search_person(name) 
            if len(directors_with_one_name) == 0:
                print '\t', name, ' not found in IMDb'
                continue
            
            director = max(directors_with_one_name, key=lambda x: utils.similar(x['name'], name) )
            self.ia.update(director)
            films = []
            if director.data.has_key('director'):
                films += director[u'director']

            director_to_films[name] = films
            pbar.progress()
        return director_to_films
    
    def rate_one(self, film):    
        imdb_film = None
        rating = 6.5
        votes = 1
        print "\tRating:", film.name,"by:", film.director,"..."
        #1) try to find if the we have already fetched the director
        if film.director in self.director_to_films:
            director_films = self.director_to_films[film.director]
            if len(director_films) > 0: 
                imdb_film = max(director_films, key=lambda x: utils.similar(x['title'], film.name) )
        
        #2) If nothing acceptable has been found try to fetch the single movie
        if imdb_film is None or utils.similar(imdb_film['title'], film.name) <= 0.7:
            # Try again by looking by movie name and match it with the director        
            imdb_film = self.fetch_movie_by_name(film.name, film.director)
            if imdb_film is None:
                print '\t\tNo film named', film.name , 'directed by', film.director, 'found on IMDb. Assigning: 6.5'
        else:
            self.ia.update(imdb_film)
            # print 'Imdb Rating for film:', film , 'is :', film['rating']
            if imdb_film.data.has_key('rating'):
                rating = float(imdb_film['rating']) 
                votes = str(imdb_film['votes'])
            else:
                print '\t\tThe film named', film.name, 'directed by', film.director, 'not rated in IMDb! Assigning: 6.5'
        film.setValue(rating)
        film.setVotes(votes)  

@utils.with_pickle
def assign_movie_rating(seances):
    assigner = MovieRatingAssigner() 
    assigner.fetch_directors([show.director for show in seances])
    rated_films = []
    print '## We have', len(seances), 'films to rate!'
    pbar = utils.ProgressBar(len(seances))
    for film in seances:
        assigner.rate_one(film)
        rated_films.append(film)
        pbar.progress()
    return rated_films