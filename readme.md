## Steps to Get Started 

1. Clone Repo: `git clone https://github.com/aryangupta701/django-monitoring-restro/`

2. Switch to Project Directory: `cd django-monitoring-restro`
 
3. Activate Environment: `source ../bin/activate`

## Pre-requisites 

In data folder add -

Menuhours.csv

storestatus.csv

timezones.csv

## Enable Environment by using the following command - 

`source ./bin/activate`

## Load data

`python manage.py makemigrations`

`python manage.py migrate`

`python manage.py load_data`

## Runserver 

`python manage.py runserver`


## Trigger Report Generation 

METHOD - POST 

`http://127.0.0.1:8000/trigger_report/`

## Get Report

METHOD - GET 

`http://127.0.0.1:8000/get_report/<report-id>`

