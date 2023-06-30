## Steps to Get Started 

1. Clone Repo: `git clone https://github.com/aryangupta701/django-monitoring-restro/`

2. Switch to Project Directory: `cd django-monitoring-restro`
 
3. Activate Environment: `source ../bin/activate`

## Pre-requisites 

In data folder add -

- Menuhours.csv

- storestatus.csv

- timezones.csv

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


##  logic for computing the hours overlap and uptime/downtime

1. Every time is converted into UTC before use 

2. To get all the unique store_id the database table store_status is used 

- To Calculate uptime/downtime for each store_id the following logic is being used : 

1. An interpolation curve is being formed with points defined as timestamps (in seconds) of the poll of previous 10 days using scipy using the following code 

`interp_func = interp1d(timestamps, states, kind='nearest', fill_value='extrapolate')` 

- On X-axis - Timestamp 

- On Y-axis - Either 0 (for inactive) or 1 (for active) is stored 

2. Now to calculate last hour uptime used the following logic : 

- Iterated over each second in the last hour and checked if the timestamp of the second is within the range of working hours of that day or not. 

- If it is in the range then append it in the `interpolated_timestamps` array 

- Now pass this function to the interpolation object and we will get the predicted values of each timestamp in `interpolated_states` which consits of either 0 or 1. 

- Now uptime can be calculated by adding the whole `interpolated_states` array 

- To calculate the downtime we can be calculated by subtracting the uptime from the total length of `interpolated_timestamps`

3. The same logic is used for the calculation of last day and last week. 

4. At the the uptime and downtime which was calculated in seconds is converted into the required format (hours or minutes )