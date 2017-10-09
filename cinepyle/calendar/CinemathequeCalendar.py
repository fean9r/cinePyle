'''
Created on Oct 4, 2017

@author: fean9r
'''
import locale
from lxml import html
import time
import requests

#from .utils import ProgressBar
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

def scrape_cinematheque_films(url_to_scrape):
    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    shows_activities = []
    
    errorMap = {
            0:'film parsing error',
            1:'realisateur parsing error',
            2:'calendar_box parsing error ',
            3:'original_title parsing error',
            4:'date_start parsing error',
            5:'date_end parsing error',
            6:'timezone parsing error',
            7:'french_title parsing error',
        }
    
    
    page = requests.get(url_to_scrape)
    tree = html.fromstring(page.content)
    
    show_hrefs = map(lambda x: x.get('href'), tree.xpath('//a[@class="show"]'))
    num_scraped_shows = len(show_hrefs)
    print 'Scraped : ', num_scraped_shows, ' show references!'
    pbar = ProgressBar(num_scraped_shows)
    for href in show_hrefs:
        # http://www.cinematheque.fr/seance/25041.html
        url = 'http://www.cinematheque.fr/' + href
        show_page = requests.get(url)
        show_tree = html.fromstring(show_page.content)
        
        show_map = {}
        
        realisateur = ''
        show_title = ''
        date_start = ''
        date_end = ''
        try:
            # Global Parsing stage
            i = 0
            film = show_tree.xpath('//div[@class="film"]')[0]
            
            # Realisateur Parsing stage
            ++i
            l_realisateur = film.xpath('span[@class="realisateur"]/text()')
            if len(l_realisateur) >= 1:
                realisateur = l_realisateur[0]
            
            # Calendar_box Parsing stage
            ++i
            calendar_box = show_tree.xpath('//var[@class="atc_event"]')[0]
            
            # original_title Parsing stage
            ++i
            l_original_title = show_tree.xpath('//span[@class="sub custom-text-color-light"]/text()')
            french_title = calendar_box.xpath('var[@class="atc_title"]/text()')[0]
            
            ++i
            if len(l_original_title) >= 1:
                show_title = l_original_title[0]
            else:
                show_title = french_title
            
            date_start = calendar_box.xpath('var[@class="atc_date_start"]/text()')[0]
            ++i
            date_end = calendar_box.xpath('var[@class="atc_date_end"]/text()')[0]
            ++i
            timezone = calendar_box.xpath('var[@class="atc_timezone"]/text()')[0]

            show_map['title'] = show_title.encode('utf-8')
            show_map['start'] = date_start
            show_map['end'] = date_end
            show_map['timezone'] = timezone
            show_map['director'] = realisateur.encode('utf-8')
            
            shows_activities.append(show_map)
        except IndexError:
            print errorMap[i] , ' ' , url , realisateur , show_title , date_start , date_end
            # ++numer_of_error
            # Past shows dont have calendar_box.
            pbar.progress()
            continue
              
        pbar.progress()
         
    return shows_activities


class CinemqthequeCalendar(object):
    '''
    classdocs
    '''
 
    def __init__(self):
        '''
        Constructor
        '''
        self.cine_calendar_base_url = 'http://www.cinematheque.fr/calendrier/'

    def getEvents(self, month):
        print("Getting the upcoming events for period: %s " % month)
        # this is the format of the cine month calendar url
        # http://www.cinematheque.fr/calendrier/11-2017.html
        seances = scrape_cinematheque_films(self.cine_calendar_base_url + month + '.html')
        return seances
