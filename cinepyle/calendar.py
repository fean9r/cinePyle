'''
Created on Oct 20, 2017

@author: fean9r
'''

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage


class GoogleCalendar(object):
    '''
    classdocs
    '''
    """Shows basic usage of the Google Calendar API.

    Creates a Google Calendar API service object and outputs a list of the next
    10 events on the user's calendar.
    """
    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/calendar-python-quickstart.json
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
    CLIENT_SECRET_FILE = 'credential/client_secret.json'
    APPLICATION_NAME = 'Google Calendar API Python Quickstart'
    
    def __init__(self, calendars_to_ids):
        '''
        Constructor
        '''
        credentials = self.getCredentials()
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=http)
        self.calendars_to_ids = calendars_to_ids
    
    def getCredentials(self):
        """Gets valid user credentials from storage.
    
        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.
    
        Returns:
            Credentials, the obtained credential.
        """
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')
    
        store = Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            try:
                import argparse
                flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
            except ImportError:
                flags = None
            flow = client.flow_from_clientsecrets(GoogleCalendar.CLIENT_SECRET_FILE, GoogleCalendar.SCOPES)
            flow.user_agent = GoogleCalendar.APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else:  # Needed only for compatibility with Python 2.6
                credentials = tools.run(flow, store)
            print ('Storing credentials to ' + credential_path)
        return credentials
    
    def printCalendars(self):
        my_calendars = self.service.calendarList().list().execute()
        for cal in my_calendars['items']:
            print (cal['summary'] , cal['id'])
    
    def getEvents(self, start, end):
        print ("Getting the upcoming events from: %s to %s." % (start , end))
        events_result = []
        for cal_id in self.calendars_to_ids.values():
            events_result += self.service.events().list(
                calendarId=cal_id, timeMin=start.isoformat(), timeMax=end.isoformat(), singleEvents=True,
                orderBy='startTime').execute().get('items', [])
        return events_result

from opchoice import model
from .model import Activity
import dateutil.parser
import time

def make_internal_time(g_time):
    date = dateutil.parser.parse(g_time)
    return int(time.mktime(date.timetuple()))

class CalendarManager(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        calendars_to_ids= {
                            'Iacopo Breschi G' :'primary',
                            'Lapo & Lisa'      :'prpbnbms11adra74lhi7q9mee4@group.calendar.google.com',
                            'Work'             :'07q9ft47r02q56sid2fub34dtc@group.calendar.google.com'
                        }
        self.calendar = GoogleCalendar(calendars_to_ids)
        
    def retreiveEvents(self, retrive_start , retrive_end):
        activities = []
        events = self.calendar.getEvents(retrive_start , retrive_end)
        if not events:
            print ('No upcoming events found.')
        for event_i in events:
            title = event_i['summary']
            start = make_internal_time(event_i['start']['dateTime'] if 'dateTime' in event_i['start'] else event_i['start']['date'])
            end   = make_internal_time(event_i['end']['dateTime'] if 'dateTime' in event_i['end'] else event_i['end']['date'])  
            activities.append(Activity(title, start, end, 0))            
        return activities
    
def write_cvs(events, file_name ='calendar.cvs' ):
    header = 'Subject,Start Date,Start Time,End Date,End Time,Description,Location\n'
    cv_out = header
    for event in events:
        cv_out += event.name +','+event.interval.start_date() +','+event.interval.start_time()+','+event.interval.end_date() +','+event.interval.end_time()+','+event.director+' IMDb Rating:'+str(event.value)+','+'Cinematheque' '\n'
        #+','+event.interval.start_date()+','+event.interval.start_time()+','+event.interval.end_date()+','+event.interval.end_time()+','+event.director+' IMDb Rating',event.value,','+'Cinematheque'
    print (cv_out)
    #with open(file_name, 'w') as cvs_file:
    #    cvs_file.write(cv_out)
            
def filter_overlapping_events(confirmed_events, unconfirmed_events):
    print ('Starting with', len(unconfirmed_events), 'activities before busy periods filtering.') 
    for event in confirmed_events:
        unconfirmed_events = list(filter(lambda x: None if (model.overlap(x.interval, event.interval)) else x, unconfirmed_events))
    print ('Remaining', len(unconfirmed_events), 'activities after busy periods filtering.')
    return unconfirmed_events
