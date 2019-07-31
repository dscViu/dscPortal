from django.urls import path 
from . import views

app_name = 'eventCalendar'

urlpatterns = [
        path('', views.index, name = 'index'),
        #path('<int:wallpost_id>/', views.detail, name='detail'),

]
