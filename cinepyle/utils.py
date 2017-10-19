'''
Created on Oct 11, 2017

@author: fean9r
'''
import hashlib
from functools import wraps
import os, pickle

def with_pickle(func):
    @wraps(func)
    def wrap(*args):
        
        if len(args) > 1 :
            file_name = type(args[0]).__name__ +"_"+ func.__name__ +"_"+ hashlib.md5(str(args[1])).hexdigest() +'.pkl'
        else :
            file_name = func.__name__ +"_"+ hashlib.md5(str(args[0])).hexdigest() +'.pkl'
        if os.path.exists(file_name):
            print "Reading cached", func.__name__,"function output.."
            with open(file_name) as f:
                cache = pickle.load(f)
        else:
            print 'Running', func.__name__,"and dumping the output to file.."
            cache = func(*args)
            # update the cache file
            with open(file_name, 'wb') as f:
                pickle.dump(cache, f)
        return cache
    return wrap


from difflib import SequenceMatcher
def similar(a, b):   
    return SequenceMatcher(None, a, b).ratio()

import re

def same_name(name1, name2):
    times_same = 0
    parts_name1 = re.compile("\.*\s*").split(name1)
    parts_name2 = re.compile("\.*\s*").split(name2)
    for part_i in parts_name1:
        for part_j in parts_name2:
            if similar(part_i,part_j) > 0.66:
                times_same+=1
                parts_name2.remove(part_j)
    if times_same == len(parts_name1):
        return True
    else:
        return False

import timeit
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
            estimate_final_duration = duration/(perc_progress + 0.0) * 100
            remaining = estimate_final_duration-duration            
            print ("\tExecution at %4.1f%% done. Elapsed: %6.2fs. Remaining: %6.2fs." % (perc_progress, duration, remaining))   

    def getTime(self):
        return self.times[1] - self.times[0]