'''
Created on Jun 19, 2017

@author: ibreschi
'''

from imdb import IMDb

from best_activities import RatingAssigner
from best_activities.utils import cached

# @cached('directors_cache.pickle')
def load_directors(films):
        director_films = {}
        directors = set()
        for film in films:
            directors.add(film.director)
        
        
        ia = IMDb()
        pbar = ProgressBar(len(directors))
        for name in directors:
            print '\tAquiring informations from IMDb about :', name
            directors_with_one_name = ia.search_person(name) 
            if len(directors_with_one_name) == 0:
                print '\t', name, ' not found in IMDb'
                continue
            
            # !!!!!! We suppose that the first in the list is allways the one we are looking for.
            
            director = directors_with_one_name[0]
            ia.update(director)
            films = []
            if director.data.has_key('director'):
                films += director[u'director']

            director_films[name] = films
            pbar.progress()
        return director_films


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
        if directorToFilm_map.has_key(cinem_film.director):
            l_films = directorToFilm_map[cinem_film.director]
        
        # Search the films in the director films that have a name similar to the one we retreived from the cinematheque.
        l_result = filter(lambda x: x if (similar(x['title'], cinem_film.name) > 0.7) else None, l_films)
        if len(l_result) > 1:
            # take the most similar one
            l_result = [reduce(lambda a, b: a if (similar(a['title'], cinem_film.name) > similar(b['title'], cinem_film.name)) else b, l_result)]
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



class MoviesRatingAssigner(RatingAssigner):
    """
    Implementation of RatingAssigner.
    """

    def __init__(self, films, force_rating = False, refresh_directors = False):
        self.force_rating = force_rating
        self.films = films
        self.director_films = load_directors(films)
        
    def rate(self):
        ia = IMDb()
        print '## We have', len(self.films), 'films to rate!'
        pbar = ProgressBar(len(self.films))
    
        for film in self.films:
            films = []
            if film.director in self.director_films:
                films = self.director_films[film.director]
        
            # Search the films in the director films that have a name similar to the one we retreived from the cinematheque.
            result = filter(lambda x: x if (similar(x['title'], film.name) > 0.7) else None, films)
            if len(l_result) > 1:
                # take the most similar one
            l_result = [reduce(lambda a, b: a if (similar(a['title'], cinem_film.name) > similar(b['title'], cinem_film.name)) else b, l_result)]
        if len(l_result) == 0:
            # no film found in director's film list continue to next director in director list
            # Try again by looking by movie name and match it with the director
            rating, votes = search_single(cinem_film.name, cinem_film.director)
            if rating == 0:
                print '\t\tNo film named', cinem_film.name , 'directed by', cinem_film.director, 'found on IMDb. Assigning: 6.5'
                rating = 6.5
                votes = 1
            film.setValue(rating)
            film.setVotes(votes)
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

    
