
#Google Calendar API imports
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
##########################################
#for datetime formatting
from dateutil.parser import parse as dtparse
from datetime import datetime as dt

#######################
#Regular django imports 
from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from .models import DSCEvent




# Create your views here.

''' #GCAL API '''
### CREATING CALENDAR INSTANCE ###

# If modifying these scopes, delete the file token.pickle.
#SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def index(request):
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)





    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='n40oh5qth67bge038cmj49gp7g@group.calendar.google.com', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    cal = [] 
    tmfmt = '%d %B, %H:%M %p'             # Gives you date-time in the format '26 December, 10:00 AM'

    #if not events:
    #    print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))

        # using dtparse to read event start time and dt.strftime to format time
        stime = dt.strftime(dtparse(start), format=tmfmt)




        #print(start, event['summary'])
#        item = str(event['summary']) + '  :  ' + str(start)
        item = str(event['summary']) + '  :  ' + str(stime)
        cal.append(item)
        #cal.append(start, event['summary'])
        #cal.append(start)
        #cal.append(event['summary'])
        #cal.append('\n')


#def index(request):
#    dscevent_list = DSCEvent.objects.order_by('-dscevent_date')
    template = loader.get_template('landingPage/index.html')
    context = {
            'cal': cal,
            #'events': events,
            #'dscevent_list': dscevent_list,
            }
    return render(request, 'landingPage/index.html', context)


   

