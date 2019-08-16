
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

'''
def getStudentInfo(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = getStudentInfo(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/') #TODO: Redirect to same page??? Or create thanks page

    # if a GET (or any other method) we'll create a blank form
    else:
        form = getStudentInfo()

#    return render(request, 'name.html', {'form': form}) #FIXME
'''    


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


    # Calling the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='n40oh5qth67bge038cmj49gp7g@group.calendar.google.com', timeMin=now,
                                        maxResults=2, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])


    #declaring empty array to hold events
    #cal = [] 
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
#        DSCEvent.objects.create(dscevent_title=str(event['summary']), dscevent_date = stime )
#        DSCEvent.objects.create(dscevent_title=str(event['summary']), dscevent_date = start )


        event_title = event['summary']
        event_date = start
        
        event_title_list.append(event_title)
        event_date_list.append(event_date)
        #print(start, event['summary'])
#        item = str(event['summary']) + '  :  ' + str(start)

        #item = str(event['summary']) + '  :  ' + str(stime)
        #cal.append(item)
       

       #cal.append(start, event['summary'])
        #cal.append(start)
        #cal.append(event['summary'])
        #cal.append('\n')


    dscevent_list = DSCEvent.objects.order_by('-dscevent_date')
    template = loader.get_template('landingPage/index.html')


    '''
    conditional return of index function, 
    depending on whether form has been filled properly and submitted, or not 
    '''
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        
        #form = StudentInfo(request.POST)
        
        print(request.POST)
        print(request.POST.get('id',))
        
        
        context = {
                'event_title_list':event_title_list,
                'event_date_list':event_date_list,
                #'form':form,
                }
    
        # check whether it's valid:
        #if form.is_valid():
            # process the data in form.cleaned_data as required
            # ... #FIXME: append to proper google sheet using google api
            # redirect to a new URL:
        return HttpResponseRedirect('/thanks/') #TODO: Redirect to same page??? Or create thanks page

    # if a GET (or any other method) we'll create a blank form
    else:
        #form = StudentInfo()

        
        context = {
                'event_title_list':event_title_list,
                'event_date_list':event_date_list,
                #'form':form,
                }
    
    return render(request, 'landingPage/index.html', context)


   

