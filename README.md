# Olist-Biller 

**DESCRIPTION:** 

This application was designed to provide a REST API and a Frontend report page to render phone bills by specific periods. 
It takes call details through REST API and stores on database to further calculate the value from that period, with partial time charge.
Having in mind the simplicity and very short time, I've wrote a small core calculator intended to split out the periods and charge 
'em by minutes.

A simple frontend was designed to provide the billing report by subscriber number and the desired period by month and year.
Data validation is done while retrieving data information, and calls with inconsistency are being ignored rendered in the report. 
The truncated data can be modified, and properly corrected by the REST API or using third app like POSTMAN.
A lot of improvements can be done, the app was designed mainly supporting plug and play sensitive data information although a 
very few information are being displayed as requested by the initial application contest. 

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

The REST API used is default django rest framework that can be found at https://www.django-rest-framework.org/ and therefore
most of the task was fulfilled by its framework. In a future release I'll provide a report callback by REST API.

When application is opened a login is required. All interfaces requires user be to logged in. There is a link for the REST API on the index,
along with a Django-Form requesting data to fullfill the report. The system is very intuitive


# Environment and Development Resources

This application was done using Pycharm Professional 2018.2.4 under a Linux Mint distro, using a intel i686 64-bits processor and 16gb memory.
Extensively tested on Wintel box, however with some weird Python Datetime behavior which had lead me to find out solutions for workaround
the problems of UNIX POSIX data calculation vs Processor architecture. I ran some performance testes and code coverage using Pycharm 
and VS Code with no clues.

# Enviroment needs

Follows down a generated list by **pip freeze** containing project packages requirements, just removed some inheritance dependencies 
which comes with these frameworks, eg. bpython.

* bpython==0.17.1 
* dj-database-url==0.5.0
* Django==2.1.2
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

# Project standards

I've tried my best to follow up the project requirements as follows:

* Practice the 12 Factor-App concepts;
* Use SOLID design principles;
* Use programming good practices;
* Use git best practices (With clear and straightforward messages)
* Flexible database fields with no locks by datatype
* PEP8 code standard

However, due my lack of time some pieces of code that could be rewritten in a more pythonic and clear way couldn't be done yet. 
Certainly it they will be done in future releases. Pieces that require modification were #commented and #TODOed. 
This app spent about 30 hours of my time working during night shift between my spare time. If you are a more experienced developer 
using Python and Django under web singleton or any MVC, I would appreciate any corrections and comments.

Hit me at: 
aislandiego@gmail.com 