from django.db import models

# Create your models here. 
'''   This is essentially, your database layout  '''

#creating wall post model
class WallPost(models.Model):
    wallpost_title = models.CharField(max_length=1000)
    wallpost_text = models.TextField(max_length=5000)
    pub_date = models.DateTimeField('Date Posted')
    

    #will represent posts as string instead of primary key
    def __str__(self):
        return self.wallpost_title
