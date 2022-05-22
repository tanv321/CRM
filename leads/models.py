from tkinter import CASCADE
from django.db import models
from django.db.models.signals import post_save #signal that will listen for the event when user is created; post_save= after save is commited to database this is called; pre_save first time save method is called right before data is commited; 
from django.contrib.auth.models import AbstractUser #we can use AbstractUser to make our User model 

""" Instead of relying on django's user model (shown below), its recommended to define our own User
 from django.contrib.auth import get_user_model #built in user model provided by django
 User = get_user_model() #Now we can use User with ForeignKey but since it will be only one relationship we can use OneToOneField
"""

class User(AbstractUser): #custom User
   # pass #we are inheriting from AbstractUser so since we have most user detail defined we don't need to edit anything but if we DO want to edit then we could.
    is_organizer = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self) -> str:
        return self.user.username
#models are a reprensation of the database schemer 
"""example: inside our database we will probably have a table of all the leads that we will have and their information
 name, phone number, etc. we will use django models to represent the strcuture of that models. """

class Lead(models.Model): 
    #we would want to imagine what type of data the leads will have
    #in our sql table the leads probably will have first and last name which is of type string  
    first_name = models.CharField(max_length=20) #we create a data type of charfields()/string b/c name can only be string 
    #data base table will require you to restrict the type of data inside each column: e.g., if we look at first column we can see it contains string
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0) 
    agent = models.ForeignKey("Agent", null=True, blank=True, on_delete=models.SET_NULL) #ForeignKey will create a relationship between the two tables: Agent and Lead 
                                                  #foreignKey always need to pass on_delete b/c it tells django when the related table is deleted...if agent is deleted then lead will be too
    organization =  models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    category = models.ForeignKey("Category", related_name="leads", null= True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length = 20)
    email = models.EmailField()



    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    """   A guide into other datatype that is useful 
    phoned = models.BooleanField(default=False) 
    SOURCE_CHOICES = ( #a tuple of choices 
        ('YouTube','YouTube'), #first value will get store in the database and the second value gets displayed so we could have ("yt", "youtube")..this is convient for shortcut  
        ('Google','Google'),
        ('News','News'),
    )
    source = models.CharField(choices=SOURCE_CHOICES, max_length=100) #the choices don't restrict the value that goes in the database


    profile_picture = models.ImageField(blank = True, null = True) #blank means its a empty string....null means theres no value in database 

    special_files = models.FileField() #store reference into this field. this will reference to the actual file that get saved in your project the file is NOT uploaded to the database
"""

class Agent(models.Model): #we would want to assign a lead with a agent 
    user = models.OneToOneField(User, on_delete=models.CASCADE) #one agent for evey one user we use OneToOneField
    organization =  models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.email
    
    """ 
    we already defined name in the abstract use so we don't need them here
    first_name = models.CharField(max_length=20) 
    last_name = models.CharField(max_length=20)
    """

class Category(models.Model):
    name = models.CharField(max_length=30)
    organization =  models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

def post_user_created_signal(sender, instance, created, **kwargs): #event that is being passed to us from post_save.connect(post_user_created_signal, sender=User) 
    print(instance, created)
    if created: #we want to create userprofile if created equal true
        UserProfile.objects.create(user=instance)

post_save.connect(post_user_created_signal, sender=User) #take the signal (post_save) and use the the signal's method called connect  which takes in two parameter connect( name of the function you want to call, what model is sending the event)
#the above code says, once the user model is save; django will send out post_save signal which we are listening to and connecting to that signal and once we recieve that signal we want to use the "post_user_created_signal" function to handle that event    