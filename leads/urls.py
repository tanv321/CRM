#we are creating urls.py for our leads folder/app from scratch

from django.urls import path
from .views import lead_list, lead_detail, lead_create

app_name = "leads"

urlpatterns = [
    path('', lead_list),
    path('<int:pk>/',lead_detail), #using pk we can direct traffic to the corresponding pk...pk (primary key) can be found inside of out SQlite database (id) 
    path('create/', lead_create) #we want to put this line above <pk> b/c if we have it below and we go to "/create" in browser django will think create is a pk and cause error....we can have it below pk by specfying the pk with datatype so <int:pk>
    

]