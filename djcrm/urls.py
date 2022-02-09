"""djcrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include #include will help us redirect our request to another fileline 33 will use it

from leads.views import home_page, random_page, second_page, third_page

urlpatterns = [ #manages the path of our web applications by  telling django which view to handle the path 
    #when request made django will start from top and go all the way down
    path('admin/', admin.site.urls), #when we go to /admin in the browser that urls in admin.site.urls will handle that request
    path('home/', home_page), #when someone goes to root, django will then activate home_page to handle the request
    path('second/', second_page), 
    path("third/", third_page),
    path('random/', random_page),
    #normally inside each apps/folder we use our own urls.py file and direct it from this urls.py file
    #with include we can redirect to another file
    path('leads/', include('leads.urls', namespace="leads")) #include (path of the file, unique way of identifying all the urls inside the file)
]
