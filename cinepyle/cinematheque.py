'''
Created on Oct 19, 2017

@author: fean9r
'''
import locale
from lxml import html
import requests

from .utils import ProgressBar

def extract_director(l_directors):
    if len(l_directors) > 1:
        raise Exception("bau")
    name = l_directors[0]
    
    if ', ' in name:
        name = name.split(', ',1)[0]
    if  ' et ' in name:
        name = name.split(' et ',1)[0]
    #print l_directors, ' ==> ', name
    return  name

def scrape_cinematheque_films(url_to_scrape):
    locale.setlocale(locale.LC_ALL, 'fr_FR.UTF-8')
    shows_activities = []
    
    errorMap = {
            0:'film parsing error',
            1:'realisateur parsing error',
            2:'calendar_box parsing error',
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
            i=i+1
            l_realisateur = film.xpath('span[@class="realisateur"]/text()')
            if len(l_realisateur) >= 1:
                realisateur = extract_director(l_realisateur)
            
            # Calendar_box Parsing stage
            i=i+1
            calendar_box = show_tree.xpath('//var[@class="atc_event"]')[0]
            
            # original_title Parsing stage
            i=i+1
            l_original_title = show_tree.xpath('//span[@class="sub custom-text-color-light"]/text()')
            french_title = calendar_box.xpath('var[@class="atc_title"]/text()')[0]
            
            i=i+1
            if len(l_original_title) >= 1:
                show_title = l_original_title[0]
            else:
                show_title = french_title
            
            date_start = calendar_box.xpath('var[@class="atc_date_start"]/text()')[0]
            i=i+1
            date_end = calendar_box.xpath('var[@class="atc_date_end"]/text()')[0]
            i=i+1
            timezone = calendar_box.xpath('var[@class="atc_timezone"]/text()')[0]

            show_map['title'] = show_title.encode('utf-8')
            show_map['start'] = date_start
            show_map['end'] = date_end
            show_map['timezone'] = timezone
            show_map['director'] = realisateur.encode('utf-8')
            
            shows_activities.append(show_map)
        except IndexError:
            print errorMap[i], url, realisateur, show_title, date_start, date_end
            # ++numer_of_error
            # Past shows dont have calendar_box.
            pbar.progress()
            continue
              
        pbar.progress()
         
    return shows_activities

class GeneralCalendar(object):
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
        seances = scrape_cinematheque_films(self.cine_calendar_base_url + month + '.html')
        return seances

from .model import Show
from .utils import with_pickle
import time

from dateutil.rrule import rrule, MONTHLY

def compute_months(strt_dt , end_dt):
    dates = [str(dt.month)+"-"+str(dt.year) for dt in rrule(MONTHLY, dtstart=strt_dt, until=end_dt)]
    return dates

def make_show(event):
    start = int(time.mktime(time.strptime(event['start'], '%Y-%m-%d %H:%M:%S')))
    end = int(time.mktime(time.strptime(event['end'], '%Y-%m-%d %H:%M:%S'))) 
    title = event['title']#show_title.encode('utf-8')
    director = event['director'] #realisateur.encode('utf-8')
    timezone = event['timezone']
    return Show(title, start, end , 0 ,director )

@with_pickle
def retreive_seances(start, end):
    calendar = GeneralCalendar()
    all_seances= []
    # depending on the months between start and end
    months = compute_months(start, end)
    for m_i in months:
        all_seances += map(lambda x:make_show(x), calendar.getEvents(m_i))
    return all_seances