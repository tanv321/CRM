#we will work with the form module
from django import forms 
class LeadForm(forms.Form): #inhert from django forms class 
    #give fields to include when capturing inputs from user 
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value = 0)
