from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from .models import DSCEvent

def index(request):
    dscevent_list = DSCEvent.objects.order_by('-dscevent_date')
    template = loader.get_template('eventCalendar/index.html')
    context = { 
            'dscevent_list': dscevent_list,
            }
    return render(request, 'eventCalendar/index.html', context)


   

