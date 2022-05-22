from django.contrib import admin

# Register your models here.
#to display our models in the www.local\admin page we import our models 
from .models import User, Lead, Agent, UserProfile, Category

admin.site.register(Category)
admin.site.register(User)
admin.site.register(Lead)
admin.site.register(Agent)
admin.site.register(UserProfile)