from django.shortcuts import render

from django.http import HttpResponse
from django.template import loader
from .models import WallPost

# Create your views here.

""" testing Hello World """
def index(request):
    wallpost_list = WallPost.objects.order_by('-pub_date')
    template = loader.get_template('announcementWall/index.html')
    context = {
        'wallpost_list': wallpost_list,
    }
    return render(request, 'announcementWall/index.html', context)
    #return HttpResponse(template.render(context, request))
    #return HttpResponse("Hello to the World of CS. We're here!")

def detail(request, wallpost_id):
    wallpost = WallPost.objects.get(pk=wallpost_id)
    return render(request, 'announcementWall/detail.html',{'wallpost': wallpost })
