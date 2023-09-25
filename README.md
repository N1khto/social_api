# social_api

API for social network 
With our service users can create and manage their profile and posts, follow other users and like their posts.
Modern authentication via JWT.
Logout functionality implemented via blacklisting refresh tokens combined with super short access token lifespan.
Creation of their own profile available for all registered users.
Searching users by names and\or their bio.
Searching posts by content.
API has convenient documentation provided by drf_spectacular and Swagger.
Optimised database queries.

Setup
Create and activate a virtual environment (Python3) using your preferred method. 
This functionality is built into Python, if you do not have a preference.

From the command line, type:

 - git clone https://github.com/N1khto/social_api
 - pip install -r requirements.txt
 - get your own DJANGO_SECRET_KEY (form https://djecrety.ir/) 
and put it into your own .env file or directly into settings
 - python manage.py migrate
 - python manage.py createsuperuser 
 - python manage.py runserver
