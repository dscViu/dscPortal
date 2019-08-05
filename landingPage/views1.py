from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
#from .models import <className> 

# Create your views here.

def index(request):
    template = loader.get_template('landingPage/index.html')

    return render(request, 'landingPage/index.html')
        

