# Olist-Biller 

**DESCRIPTION:** 

This application was designed to provide a REST API and a Frontend report page to render phone bills. 
It process call details through a REST API interface storing in DB for further calculations, within or without partial 
time charge. 

A simple frontend was designed to provide the billing report by subscriber number and the desired period by month and 
year. Data validation is done while retrieving data information excluding calls with inconsistency which are ignored. 
The truncated data can be modified lately and properly corrected thought REST API or using third app like POSTMAN.
Improvements need to be done the app was designed mainly supporting plug and play sensitive data information although a 
very few are being displayed as requested by the initial application contest. 


# Installing and testing instructions
a) Make sure to create a file named **.env** containing the following lines:

* SECRET_KEY=
* DEBUG=

b) run python manage.py migrate 
this command will create a new sqlite3 db locally for you.

c) run python manage.py createsuperuser
to create a superuser so you can login the system

d) pip install -r requirements.txt
This will make sure to install all the project requirements 

# REST API Interface
The rest API was placed at https://olist-biller.herokuapp.com/rest/ separated by callstart and callend pages. The callstart is intended 
to input initial call information using the following formats:

A. callstart way

```
{
  "id":  // Record unique identificator;
  "type":  // Indicate if it's a call "start" or "end" record;
  "timestamp":  // The timestamp of when the event occured;
  "call_id":  // Unique for each call record pair;
  "source":  // The subscriber phone number that originated the call;
  "destination":  // The phone number receiving the call.
}
```

The callend has the following fields

B. callend way

```
{
   "id":  // Record unique identificator;
   "type":  // Indicate if it's a call "start" or "end" record;
   "timestamp":  // The timestamp of when the event occured;
   "call_id":  // Unique for each call record pair.
}
```

The REST API used is default django rest framework that can be found at https://www.django-rest-framework.org/ 
and therefore most of the task was fulfilled by its framework. In a future release I'll provide a report callback 
by REST API.

The Django REST API provides many methods for manipulating the data, lets suppose you have inserted an invalid value
for a specific register with number 10 on callstart. You can navigate to update this item manually or you can replace
all fields by the REST JSON format, with the following arguments available: 

Allow: 
    * GET, 
    * PUT,
    * PATCH, 
    * DELETE, 
    * HEAD, 
    * OPTIONS

For full REST documentation please visit this link: https://www.django-rest-framework.org/#quickstart


Once application is opened a login is required. All interfaces requires user be to logged in. There is a link for the REST API on the index,
along with a Django-Form requesting data to fulfill the report. The system is very intuitive


# Environment and Development Resources

This application was designed using the following resources:
* Pycharm Professional 2018.2.4 
* Linux Mint 4.15.0-38-generic distro,
* Hardware Intel i686 64-bits processor with 16 GB memory and 2tb SSD disk.
* bpython / ptpython / ipython were used for debug purposes and calculate POSIX datetime objects

Extensively tested on Wintel box with no major issues, however with some weird Python Datetime behavior. 
It ran some performance testes and code coverage using Pycharm and VS Code with no clues.
The testing was done by Internal Django tests collection of tools.

# Enviroment needs

Here a generated list by **pip freeze** containing project packages requirements, just removed some inheritance dependencies 
which comes with these frameworks, eg. bpython.

* bpython==0.17.1 
* dj-database-url==0.5.0
* Django==2.0.1 
* django-bootstrap-form==3.4
* djangorestframework==3.8.2
* gunicorn==19.9.0
* psycopg2-binary==2.7.5
* python-dateutil==2.7.3
* python-decouple==3.1
* pytz==2018.5
* whitenoise==4.1
* django-heroku==0.3.1

**For full list of project needs check requirements.txt** 

**WARNING:**  
(Make sure to avoid DJANGO v2.1.3 in this specific app. It doesn't work with Heroku and Google Chrome)

# Project standards

* Practice the 12 Factor-App concepts; 
* Use SOLID design principles;
* Use programming good practices;
* Use git best practices (With clear and straightforward messages)
* Flexible database fields with no locks by datatype
* PEP8 code standard

**NOTE:**  

Pieces that require modification were **#commented** and **#TODOed.**
 
This app spent about 30 hours of development during night shift between my spare time. 

Any comments, let me know
aislandiego@gmail.com 