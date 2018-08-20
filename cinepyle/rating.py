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

    def __init__(self, directors):
        self.ia = IMDb()
        self.director_to_films = self.fetch_directors(directors)
    
    def fetch_movie_by_title_and_director(self, title, director_name):
        if title == '' or director_name == '':
            return None

        max_update = 5
        for film_i in self.ia.search_movie(title):
            max_update=max_update-1
            self.ia.update(film_i)
            if 'director' in film_i.data:
                # take the first director
                director = film_i['director'][0]
                if utils.same_name(director['name'], director_name):
                    return film_i
            if max_update== 0:
                break
        return None
            
    @utils.with_pickle
    def fetch_directors(self, directors):
        director_to_films = {}
        directors = set(directors)       
        pbar = utils.ProgressBar(len(directors))
        for name in directors:
            print ('\tAquiring informations about:', name)
            directors_with_one_name = self.ia.search_person(name) 
            if len(directors_with_one_name) == 0:
                print ('\t', name, ' not found in IMDb')
                continue
            
            director = max(directors_with_one_name, key=lambda x: utils.similar(x['name'], name) )
            self.ia.update(director)
            films = []
            if 'director' in director.data:
                films += director[u'director']

            director_to_films[name] = films
            pbar.progress()
        return director_to_films

    def retrive_regional_title(self, film, country):
        self.ia.update(film,'akas')
        if 'akas from release info' in film.data:
            various_title = film.data['akas from release info']
            for t in various_title:
                nation = t.split('::')[0]
                name   = t.split('::')[1]
                if nation == country :
                    return name
        return None

    def retrive_cached_film(self, film):
        
        if film.director in self.director_to_films:
            for film_i in self.director_to_films[film.director]: 
                if utils.similar(film_i['title'], film.name) >= 0.6:
                    return film_i
                if utils.similar(film_i['title'], film.cine_title) >= 0.6:
                    return film_i
        # Nothing found..
        return None

    def rate_one(self, film):
        rating = 6.5
        votes = 1
        print ("\tRating:", film.name, "by:", film.director)    
        
        imdb_film = self.retrive_cached_film(film)
                
        if imdb_film is None:
            imdb_film = self.fetch_movie_by_title_and_director(film.cine_title, film.director)
            if imdb_film is None:
                imdb_film = self.fetch_movie_by_title_and_director(film.name, film.director)
            
        if imdb_film is None:
            print ('\t\tThe film named', film.name, 'directed by', film.director, 'not rated in IMDb! Assigning:', rating)
        else:
            self.ia.update(imdb_film, 'vote details')
            if 'demographics' in imdb_film.data:
                rating = float(imdb_film['demographics']['imdb users']['rating'])
                votes = str(imdb_film['demographics']['imdb users']['votes'])
        film.setValue(rating)
        film.setVotes(votes)  

@utils.with_pickle
def assign_rating_to_month_seances(month_i_seances):
    assigner = MovieRatingAssigner([show.director for show in month_i_seances]) 
    num_seances = len(month_i_seances)
    print ('## We have', num_seances, 'films to rate in month!')
    rated_films = []
    pbar = utils.ProgressBar(num_seances)
    for film in month_i_seances:
        assigner.rate_one(film)
        rated_films.append(film)
        pbar.progress()
    return rated_films

def assign_movie_rating(months_seances):
    rated_films = []
    for month_i_seances in months_seances:
        rated_films += assign_rating_to_month_seances(month_i_seances)
    return rated_films
