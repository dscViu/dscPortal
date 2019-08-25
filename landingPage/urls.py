from django.urls import path 
from . import views

app_name = 'landingPage'

urlpatterns = [
        path('ajax/bro', views.index, name = 'index'),
        path('', views.index, name = 'index'),
]
