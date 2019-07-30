from django.contrib import admin

''' import object to be modifiable from admin page '''
from .models import WallPost

# Register your models here.
admin.site.register(WallPost)
