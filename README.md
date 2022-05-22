# CRM
Django based CRM.
To keep track of the relations between different entities and their role within the buisness. 

To get the server running:
-Create a virtual env 
-Install all required packages via command: pip install -r requirements.txt
-create a .env file inside the root directory
-The .env file should contain a SECRET_KEY and DEBUG as shown below:
SECRET_KEY = 0000
DEBUG = True
-use the following command: python manage.py migrate
-start your program via command: python manage.py runserver

