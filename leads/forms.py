#we will work with the form module
from dataclasses import field
from django import forms 
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import Lead, Agent


User = get_user_model()

class LeadModelForm(forms.ModelForm): #simpler way to create forms...take existing model and reuse it
    class Meta: #where we specify info about form
        model = Lead #we will name the model are we working with?
        fields = ( #displat this fields into the form 
            'first_name',
            'last_name',
            'age',
            'agent',
            'description',
            'phone_number',
            'email',
        )


class LeadForm(forms.Form): #harder way to create form.... first inhert from django forms class 
    #give fields to include when capturing inputs from user 
    first_name = forms.CharField()
    last_name = forms.CharField()
    age = forms.IntegerField(min_value = 0)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': UsernameField}

class AssignAgentForm(forms.Form):
    agent = forms.ModelChoiceField(queryset= Agent.objects.none())
    
    
    def __init__(self, *args, **kwargs):
        request = kwargs.pop("request") 
        agents = Agent.objects.filter(organization=request.user.userprofile)
        super(AssignAgentForm,self).__init__(*args, **kwargs)
        self.fields["agent"].queryset = agents

class LeadCategoryUpdateForm(forms.ModelForm):
    class Meta: #where we specify info about form
        model = Lead #we will name the model are we working with?
        fields = ( #displat this fields into the form 
            'category',
        )