#we are creating urls.py for our leads folder/app from scratch

from django.urls import path
from .views import (
    lead_list, lead_detail, lead_create, lead_update, lead_delete, 
    LeadListView, LeadDetailView, LeadCreateView, LeadUpdateView, LeadDeleteView, AssignAgentView, CategoryListView, CategoryDetailView,
    LeadCategoryUpdateView
)

app_name = "leads"

urlpatterns = [
    #for every path we can also give it a  name to reference our path easisly 
    path('create/', LeadCreateView.as_view(), name ='lead-create'), #we want to put this line above <pk> b/c if we have it below and we go to "/create" in browser django will think create is a pk and cause error....we can have it below pk by specfying the pk with datatype so <int:pk>
    path('', LeadListView.as_view(), name='lead-list'),
    path('<int:pk>/',LeadDetailView.as_view(), name='lead-detail'), #using pk we can direct traffic to the corresponding pk...pk (primary key) can be found inside of out SQlite database (id) 
    path('<int:pk>/update/',LeadUpdateView.as_view(), name='lead-update'), 
    path('<int:pk>/delete/', LeadDeleteView.as_view(), name='lead-delete'),
    path('<int:pk>/assign-agent/', AssignAgentView.as_view(), name='assign-agent'),
    path('<int:pk>/category/', LeadCategoryUpdateView.as_view(), name='lead-category-update'),
    path('categories/', CategoryListView.as_view(), name ='category-list'), 
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name ='category-detail'), 




] 