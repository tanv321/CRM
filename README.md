# CRM
Django based CRM. <br />
To keep track of the relations between different entities and their role within the buisness. <br />

To get the server running:<br />
-Create a virtual env <br />
-Install all required packages via command: pip install -r requirements.txt<br />
-create a .env file inside the root directory<br />
-The .env file should contain a SECRET_KEY and DEBUG as shown below:<br />
SECRET_KEY = 0000<br />
DEBUG = True<br />
-use the following command: python manage.py migrate<br />
-start your program via command: python manage.py runserver<br />

