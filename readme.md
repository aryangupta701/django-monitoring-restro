## Pre-requisites 

In data folder add -

Menuhours.csv

storestatus.csv

timezones.csv

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

