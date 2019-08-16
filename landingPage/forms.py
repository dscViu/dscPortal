''' this file works similarly to models.
Here we are setting up the form fields for this app
'''

#import django forms class
from django import forms 

#here we inherit from the forms class 
class StudentInfo(forms.Form):
    studentName = forms.CharField(label='Full Name', max_length=100)
    studentMajor = forms.CharField(label='Major', max_length=100)
    studentEmail = forms.EmailField(label='Email address', min_length=5)
    studentYear = forms.IntegerField()

