from django.db import models

# Create your models here.
class DSCEvent(models.Model):
    dscevent_title = models.CharField(max_length=500)

    dscevent_date = models.DateTimeField('Event Date')


#represent event as string instead of primary key
def __str__(self):
    return self.dscevent_title


