'''
Created on Sep 13, 2016

@author: fean0r
'''

from difflib import SequenceMatcher
import os
import re
import pickle
import timeit

def write_cvs(header, lines, file_name ='calendar.cvs' ):
    cv_out = header
    for line in lines:
        cv_out += line
    with open(file_name, 'w') as cvs_file:
        cvs_file.write(cv_out)

def pickl_out(data, file_name ='data.pkl' ):
    pkls_dir_path = os.getcwd() +'/pkl/'
    with open(pkls_dir_path + file_name , 'wb') as pkl_file:
        pickle.dump(data, pkl_file)
    
def pickl_in(file_name ='data.pkl' ):
    pkls_dir_path = os.getcwd() +'/pkl/'
    with open(pkls_dir_path + file_name , 'rb') as pkl_file:
        loaded_objects = pickle.load( pkl_file)
        return loaded_objects

def similar(a, b):   
    return SequenceMatcher(None, a, b).ratio()
   
def same_name(name1, name2):
    times_same = 0
    parts_name1 = re.compile("\.*\s*").split(name1)
    parts_name2 = re.compile("\.*\s*").split(name2)
    for part_i in parts_name1:
        for part_j in parts_name2:
            if similar(part_i,part_j) > 0.75:
                times_same+=1
                parts_name2.remove(part_j)
    if times_same == len(parts_name1):
        return True
    else:
        return False

class ProgressBar():
    def __init__(self, tot):   
        self.RedrawFrequency = 10.0
        self.elem_for_redraw = tot / self.RedrawFrequency
        self.i_progress = 0
        self.perc_bar = self.elem_for_redraw
        self.tot= tot/100.0
        self.times = [0,0]
          
    def clear(self):
        self.i_progress = 0
        self.perc_bar = self.RedrawFrequency
    
    def __getPercProgress(self):
        return self.i_progress/self.tot
    
    def progress(self):
        
        if self.i_progress == 0 :
            self.times[0] = timeit.default_timer()
        
        self.i_progress += 1
        
        if self.i_progress >= self.perc_bar:
            self.perc_bar += self.elem_for_redraw
            self.times[1] = timeit.default_timer()
            duration = self.times[1] - self.times[0]
            perc_progress = self.__getPercProgress()
            estimate_final_duration = duration/perc_progress *100
            remaining = estimate_final_duration-duration
            print perc_progress, '% done in', duration, 'sec.',remaining,'remaining.'   

    def getTime(self):
        return self.times[1] - self.times[0]


def cached(cachefile):
    """
    A function that creates a decorator which will use "cachefile" for caching the results of the decorated function "fn".
    """
    def decorator(fn):  # define a decorator for a function "fn"
        def wrapped(*args, **kwargs):   # define a wrapper that will finally call "fn" with all arguments            
            # if cache exists -> load it and return its content
            if os.path.exists(cachefile):
                    with open(cachefile, 'rb') as cachehandle:
                        print("using cached result from '%s'" % cachefile)
                        return pickle.load(cachehandle)

            # execute the function with all arguments passed
            res = fn(*args, **kwargs)

            # write to cache file
            with open(cachefile, 'wb') as cachehandle:
                print("saving result to cache '%s'" % cachefile)
                pickle.dump(res, cachehandle)

            return res

        return wrapped

    return decorator   # return this "customized" decorator that uses "cachefile"

