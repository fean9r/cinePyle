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
    
    def __init__(self):
        '''
        Constructor
        '''
        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('calendar', 'v3', http=http)
    
    def get_credentials(self):
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
            print('Storing credentials to ' + credential_path)
        return credentials
    
    def getEvents(self, time_1 , time_2):
        print("Getting the upcoming events from: %s to %s."% (time_1 , time_2))
        eventsResult = self.service.events().list(
        calendarId='primary', timeMin=time_1, timeMax=time_2, singleEvents=True,
        orderBy='startTime').execute()
        return eventsResult.get('items', [])



from model import Activity
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
        self.calendar = GoogleCalendar()
        
    def retreiveEvents(self, time_1 , time_2):
        activities = []
        
        events = self.calendar.getEvents(time_1 , time_2)
        if not events:
            print('No upcoming events found.')
        for event in events:
            start = make_internal_time(event['start'].values()[0])
            end = make_internal_time(event['end'].values()[0])
            act = Activity(event['summary'],start, end,0)
            activities.append(act)            
        return activities
    
    def write_cvs(self, header, lines, file_name ='calendar.cvs' ):
        cv_out = header
        for line in lines:
            cv_out += line
        with open(file_name, 'w') as cvs_file:
            cvs_file.write(cv_out)