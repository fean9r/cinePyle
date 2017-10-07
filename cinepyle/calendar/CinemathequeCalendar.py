'''
Created on Oct 4, 2017

@author: fean9r
'''
import locale
from lxml import html
import time

import requests

from .model import Show
from .model import TimeInterval
from .utils import ProgressBar


def scrape_cinematheque_films(url_to_scrape):
    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    shows_activities = []
    
    errorMap = {0:'film parsing error',
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
    
    show_hrefs = map(lambda x: x.get('href'),tree.xpath('//a[@class="show"]'))
    num_scraped_shows= len(show_hrefs)
    print 'Scraped : ', num_scraped_shows, ' show references!'
    pbar = ProgressBar(num_scraped_shows)
    for href in show_hrefs:
        #http://www.cinematheque.fr/seance/25041.html
        url = 'http://www.cinematheque.fr/'+href
        show_page = requests.get(url)
        show_tree = html.fromstring(show_page.content)
        
        realisateur= ''
        show_title= ''
        date_start= ''
        date_end = ''
        try:
            i=0
            film = show_tree.xpath('//div[@class="film"]')[0]
            i=1
            l_realisateur = film.xpath('span[@class="realisateur"]/text()')
            if len(l_realisateur)>=1:
                realisateur = l_realisateur[0]
            else :
                realisateur = ''
            i=2
            calendar_box = show_tree.xpath('//var[@class="atc_event"]')[0]
            i=3
            l_original_title = show_tree.xpath('//span[@class="sub custom-text-color-light"]/text()')
            french_title = calendar_box.xpath('var[@class="atc_title"]/text()')[0]
            i=4
            if len(l_original_title)>=1:
                show_title = l_original_title[0]
            else:
                show_title = french_title
            
            date_start = calendar_box.xpath('var[@class="atc_date_start"]/text()')[0]
            i=5
            date_end = calendar_box.xpath('var[@class="atc_date_end"]/text()')[0]
            i=6
            timezone = calendar_box.xpath('var[@class="atc_timezone"]/text()')[0]

            ts_date_start = int(time.mktime(time.strptime(date_start, '%Y-%m-%d %H:%M:%S')))
            ts_date_end = int(time.mktime(time.strptime(date_end, '%Y-%m-%d %H:%M:%S'))) 
            shows_activities.append(Show( show_title.encode('utf-8'), TimeInterval(ts_date_start, ts_date_end , str(timezone)), 0 , realisateur.encode('utf-8')))
        except IndexError:
            print errorMap[i] , ' ' ,url , realisateur , show_title ,date_start , date_end
            #++numer_of_error
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

    def getEvents(self, time_1 , time_2):
        print('Getting the upcoming events, ', time_1 , time_2)
        
        return []