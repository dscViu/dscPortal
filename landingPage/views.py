
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

##############################################
#Regular django specific imports 
from django.shortcuts import render

from django.http import HttpResponseRedirect #for forms submitted.. 
from .forms import StudentInfo

from django.http import HttpResponse #TODO: Confirm if still needed with the above ...Redirect
from django.template import loader
from .models import DSCEvent



# Create your views here.

''' GCAL API '''
### CREATING CALENDAR INSTANCE ###
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
    #NOTE#: commented out for google cloud platform / app engine lauch (cannot write) ###
     #TODO1#:  Will creds expire???!

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
    
    #TODO#2: find out how to concatenate service and service1 into a single 
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
    #tmfmt = '%d %B, %H:%M %p'             # Gives you date-time in the format '26 December, 10:00 AM'



    #if not events:
    #    print('No upcoming events found.')
    for event in events:


        #get event time 
        start = event['start'].get('dateTime', event['start'].get('date'))
        # using dtparse to read event start time and dt.strftime to format time
     #   stime = dt.strftime(dtparse(start), format=tmfmt)

        #create object instance for each loop 
        #DSCEvent.objects.create(dscevent_title=str(event['summary']), dscevent_date = stime )
        #DSCEvent.objects.create(dscevent_title=str(event['summary']), dscevent_date = start )


        event_title = event['summary']
        event_date = start
        
        event_title_list.append(event_title)
        event_date_list.append(event_date)
        #print(start, event['summary'])
        #item = str(event['summary']) + '  :  ' + str(start)

        #item = str(event['summary']) + '  :  ' + str(stime)
       
    dscevent_list = DSCEvent.objects.order_by('-dscevent_date')
    template = loader.get_template('landingPage/index.html')


    '''
    conditional return of index function, 
    depending on whether form has been filled properly and submitted, or not 
    '''
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        
        #Get post request data 
        print(request.POST)
        #print(request.POST.get('studentName'))
        
        #get student name from post
        sName = request.POST.get('studentName')
        sEmail = request.POST.get('email')
        sMajor = request.POST.get('major')
        sYear = request.POST.get('year')
        #print(sName, sEmail, sMajor, sYear)


        '''     If this is a POST request get info and add it to emailListSheet  '''
        # The ID (and range if required) of spreadsheet.
        emailListSheet = '1XmMCdfkYlmpSK-g64aLQcAaa5JXTnxQDpcJxD22BbyM' #test sheet

        # Call the Sheets API
        range_name = 'emails' #name of the sheet. Appending at bottom of sheet
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
