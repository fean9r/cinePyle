'''
Created on Oct 11, 2017

@author: fean9r
'''
from difflib import SequenceMatcher
def similar(a, b):   
    return SequenceMatcher(None, a, b).ratio()

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