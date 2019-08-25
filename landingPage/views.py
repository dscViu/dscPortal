''' 
Google Calendar API imports (must be on top) 
'''
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

'''
imports for the formatting of time and date 
'''
from dateutil.parser import parse as dtparse
from datetime import datetime as dt

import re # for formatting of all day events
''' 
Regular django specific imports 
'''
from django.shortcuts import render

from django.http import HttpResponseRedirect #same as HttpResponse but allows for redirect on other page

from django.http import HttpResponse #TODO: Could be redundant with HttpResponseRedirect
from django.template import loader
from .models import DSCEvent  #NOTE# used for database, currently not used


'''''''''
# Create views below: #

    The python code that supports the web app lives here.
    - The Google API code to read from our Google Calendar 
    - The Google API code to write to our Google Sheets
    - The information gathered from POST request when the HTML form is submitted
'''''''''




'''
## Google Calendar API ##
This section is required for all Google API services. 
    - 'SCOPES' specify the level of access (ie: readonly, readwrite, etc)
    - 'creds' store login credentials
'''
# If modifying these scopes, delete the file token.pickle.
#SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
def index(request):
    SCOPES = ['https://www.googleapis.com/auth/calendar','https://www.googleapis.com/auth/spreadsheets']
    
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    '''
    #NOTE#: 
    The section below was commented out for launch on Google Cloud Platform / Google App Engine,
    as GAE cannot write to file (for creds) 

    ###TODO###: Will creds expire???!
    '''

    '''
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

    '''
    
    '''
    ###TODO###: find out how to concatenate service and service1 into a single 
    '''
    # build methods
    service = build('calendar', 'v3', credentials=creds)
    service1 = build('sheets', 'v4', credentials=creds)

    # Calling the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='n40oh5qth67bge038cmj49gp7g@group.calendar.google.com', timeMin=now,
                                        maxResults=2, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])


    # Declaring empty array to hold event name and dates
    event_title_list = []
    event_date_list = []
    
    tmfmt = '%B %d, %I:%M %p'             # Gives you date-time in the format '26 December, 10:00 AM'



    #if not events:
    #    print('No upcoming events found.')
    for event in events:

        #get event time 
        start = event['start'].get('dateTime', event['start'].get('date'))
        
        
        # using dtparse to read event start time and dt.strftime to format time
        stime = dt.strftime(dtparse(start), format=tmfmt)

        #create object instance for each loop 
        #DSCEvent.objects.create(dscevent_title=str(event['summary']), dscevent_date = stime )
        #DSCEvent.objects.create(dscevent_title=str(event['summary']), dscevent_date = start )

        
        ''' 
        Storing title of the event, date and time of event for display in template. 
        
        All day events display with time of 12:00 AM.
        So if time is 12:00 AM, the time will not be displayed for the event 
        '''
        event_title = event['summary']

        # Grabbing date and time from string using regex
            ## Date Regex: "^\w+ \d\d, "  
            ## Time Regex: "\d\d:\d\d"

        dateOfEvent = re.search("^\w+ \d\d", stime).group()
        timeOfEvent = re.search("\d\d:\d\d \w\w", stime).group()

        if timeOfEvent == "12:00 AM":      #All day events have Google Calendar time 00:00
            event_date = dateOfEvent #+ "All Day"

        else:   #Not an all day event
            event_date = stime


        #event_date = start  #non formatted time string 
        
        event_title_list.append(event_title)
        event_date_list.append(event_date)
        

        #print(start, event['summary'])
        #item = str(event['summary']) + '  :  ' + str(start)
        #item = str(event['summary']) + '  :  ' + str(stime)
       
    dscevent_list = DSCEvent.objects.order_by('-dscevent_date')
    template = loader.get_template('landingPage/index.html')


    '''
    When the html 'register' form is submitted, it creates a POST request 
    This section determines how to handle catching the POST request data. 

    The values for the 'request.POST.get() method are define in the ./templates/landingPage/index.html
        in the appropriate section:
        - for 'studentName', 'email', and 'major', they are defined as 'name' of the 'input' tag
        - for 'year', it is defined as 'value' of the input tag
    '''
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        
        ''' 
        #Get post request data#
        '''
        print(request.POST) #show the data to CLI
        #print(request.POST.get('studentName'))
        
        ''' 
        Get student name from POST request and store in appropriate variable
        '''

        sName = request.POST.get('studentName')
        sEmail = request.POST.get('email')
        sMajor = request.POST.get('major')
        sYear = request.POST.get('year')
        #print(sName, sEmail, sMajor, sYear)


        ''' 
        If this is a POST request get info and add it to emailListSheet on Google Drive
        '''

        # The ID (and range if required) of spreadsheet.
        ''' 
        Sheet/Spreadsheet ID are located in the URL
        ie: https://docs.google.com/spreadsheets/d/spreadsheetId/edit#gid=sheetId
        '''

        #emailListSheet = '1XmMCdfkYlmpSK-g64aLQcAaa5JXTnxQDpcJxD22BbyM' #test sheet
        emailListSheet = '1lBNP9sjGrK7RmI9AdI-GpIE5SFetTy33vUTFJKtm4XQ'
        # Call the Sheets API
        range_name = 'from webpage' #name of the sheet. Appending at bottom of sheet
        valueInputOption = "RAW" #input user data as is #TODO safe?
   
        '''
        An array of array that holds the values to be inserted in the Google Sheeet.
        Insert in 'rows' by default, unless specified otherwise. 
        Each item in the inner-most array represents a cell.
        Each item in the outer array represents a row.
        '''
        values = [
            [
                sEmail, sName, sMajor, sYear
            ],
            # Additional rows ...
        ]

        '''
        A dictionary of the values to be inserted in the Google Sheets
        '''
        body = {
            'values': values   
        }

        '''
        Performing the actual insertion here with the parameters below:
        - service1 calls the spreadsheet created earlier
        - values.append() method adds 'values' at the next empty row
        - range name: refers to the string name of the sheet (or range if other)
        - valueInputOption='RAW' : takes the user input from the form 'as is'
        '''
        result = service1.spreadsheets().values().append(
            spreadsheetId=emailListSheet, range=range_name,
            valueInputOption='RAW', body=body).execute()
   
        #printout number of cells appended (ie: 2 for email and name)
        print('{0} cells appended.'.format(result \
                                               .get('updates') \
                                               .get('updatedCells')))


        context = {
                'event_title_list':event_title_list,
                'event_date_list':event_date_list,
                #'form':form,
                }
        
        return render(request, 'landingPage/index.html', context)
        #return HttpResponseRedirect('/thanks/') #TODO: Redirect to same page??? Or create thanks page

    # if a GET (or any other method) #TODO: This may not be req'd here
    else:
        context = {
                'event_title_list':event_title_list,
                'event_date_list':event_date_list,
                }
    
    return render(request, 'landingPage/index.html', context)
