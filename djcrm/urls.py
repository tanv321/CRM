from django.conf import settings
from django.conf.urls.static import static 
from django.contrib import admin
from django.urls import path, include #include will help us redirect our request to another fileline 33 will use it
from leads.views import home_page, random_page, second_page, third_page, landing_page, LandingPageView, SignupView, LeadCreateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView




urlpatterns = [ #manages the path of our web applications by  telling django which view to handle the path 
    #when request made django will start from top and go all the way down
    path('admin/', admin.site.urls), #when we go to /admin in the browser that urls in admin.site.urls will handle that request
    path('home/', home_page), #when someone goes to root, django will then activate home_page to handle the request
    path('second/', second_page), 
    path("third/", third_page),
    path('random/', random_page),
    path('', LandingPageView.as_view(), name = 'landing-page'),
    #normally inside each apps/folder we use our own urls.py file and direct it from this urls.py file
    #with include we can redirect to another file
    path('leads/', include('leads.urls', namespace="leads")), #include (path of the file, unique way of identifying all the urls inside the file)
    path('agents/', include('agents.urls', namespace="agents")),
    path('signup/', SignupView.as_view(), name = 'signup'),
    path('reset-password/', PasswordResetView.as_view(), name='reset-password'),
    path('password-reset-done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('create/', LeadCreateView.as_view(), name='lead-create'),
    path('login/', LoginView.as_view(), name = 'login'),
    path('logout/', LogoutView.as_view(), name= "logout"),
]
if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) #typically this path should not be inside the urlpatterns...in production we will use services like digitial ocean to manage the static files  to reference that web server instead of refercing your own web server 


