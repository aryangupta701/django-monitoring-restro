from .models import Report, StoreStatus, StoreTimezone, StoreBusinessHours
from datetime import time, datetime, timedelta
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
from django.db.models import Max
import pytz
import io

def loadCurrentDate():
    max_timestamp_utc = StoreStatus.objects.aggregate(max_timestamp_utc=Max('timestamp_utc'))['max_timestamp_utc']
    return max_timestamp_utc
    
def getStoreIds():
    distinct_store_ids = StoreStatus.objects.values('store_id').distinct()
    return distinct_store_ids

def get_store_timezone(store_id):
    try:
        store_timezone = StoreTimezone.objects.get(store_id=store_id)
        return pytz.timezone(store_timezone.timezone_str)
    except Exception as e:
        return pytz.timezone("America/Chicago")

def convertTimeToUTC(time_local, timezone):
    current_date = datetime.now(timezone).date()
    datetime_local = datetime.combine(current_date, time_local)
    localized_datetime = timezone.localize(datetime_local)
    utc_datetime = localized_datetime.astimezone(pytz.UTC)
    time_utc = utc_datetime.time()
    return time_utc


def get_working_hours(store_id, timezone):
    res = []
    for i in range(7):
        try:
            store_data_row = StoreBusinessHours.objects.filter(store_id=store_id, day=i).first()
            start_time_utc = convertTimeToUTC(store_data_row.start_time_local, timezone)
            end_time_utc = convertTimeToUTC(store_data_row.end_time_local, timezone)
        except Exception as e:
            start_time_utc = time(0, 0, 0)
            end_time_utc = time(23, 59, 59)
        
        data = [start_time_utc, end_time_utc]
        res.append(data)
    return res

def calculate_timestamps(start_time, end_time,interval, working_hours_utc ):
    interpolated_timestamps = []
    for timestamp in np.arange(start_time, end_time + interval, interval):
        dt_time = datetime.utcfromtimestamp(timestamp).time()
        flag = False
        for openTime, closeTime in working_hours_utc:
            if(openTime > closeTime):
                if not (dt_time >= closeTime and dt_time<=openTime):
                    flag = True
                    break 
            elif (dt_time >= openTime and dt_time<=closeTime):
                flag = True
                break

        if(flag):
            interpolated_timestamps.append(timestamp)
    return np.array(interpolated_timestamps)

def getDurations(interp_func, working_hours_utc, start_time, end_time):
    interval = 1 
    interpolated_timestamps = calculate_timestamps(start_time, end_time,interval, working_hours_utc)
    interpolated_states = interp_func(interpolated_timestamps)

    active_duration = np.sum(interpolated_states) * interval
    inactive_duration = len(interpolated_timestamps) * interval - active_duration
    return [active_duration, inactive_duration]

def getDurationsForHour(interp_func, working_hours_utc, max_timestamp_utc):
    end_time = max_timestamp_utc.timestamp()
    start_time =  end_time - 60*60 

    return getDurations(interp_func, working_hours_utc,start_time, end_time)

def getDurationsForDay(interp_func, working_hours_utc, max_timestamp_utc):
    end_time = max_timestamp_utc.timestamp()
    start_time =  end_time - 60*60*24

    return getDurations(interp_func, working_hours_utc,start_time, end_time)

def getDurationsForWeek(interp_func, working_hours_utc, max_timestamp_utc):
    end_time = max_timestamp_utc.timestamp()
    start_time =  end_time - 60*60*24*7

    return getDurations(interp_func, working_hours_utc,start_time, end_time)

def getInterpolationFunction(store_id, max_timestamp_utc):
    min_timestamp_utc = max_timestamp_utc - timedelta(days=10)
    filtered_records = StoreStatus.objects.filter(store_id=store_id, timestamp_utc__range=(min_timestamp_utc, max_timestamp_utc)).order_by('timestamp_utc')
    timestamps = []
    states = []
    for record in filtered_records:
        # print(record)
        timestamps.append(record.timestamp_utc.timestamp())
        states.append(1 if record.status == 'active' else 0)

    interp_func = interp1d(timestamps, states, kind='nearest', fill_value='extrapolate')
    return interp_func

def processStore(store_id, max_timestamp_utc):
    timezone = get_store_timezone(store_id)
    interp_func = getInterpolationFunction(store_id, max_timestamp_utc)
    working_hours_utc = get_working_hours(store_id, timezone)
    last_hour = getDurationsForHour(interp_func, working_hours_utc, max_timestamp_utc)
    last_day = getDurationsForDay(interp_func, working_hours_utc, max_timestamp_utc)
    last_week = getDurationsForWeek(interp_func, working_hours_utc, max_timestamp_utc)
    data = {
        "store_id": store_id,
        "uptime_last_hour" : last_hour[0]/60,
        "uptime_last_day" : last_day[0]/(60*60),
        "uptime_last_week" : last_week[0]/(60*60),
        "downtime_last_hour" : last_hour[1]/60,
        "downtime_last_day" : last_day[1]/(60*60),
        "downtime_last_week" : last_week[1]/(60*60),
    }
    temp_df = pd.DataFrame(data, index=[1])
    return temp_df


def startReportGeneration(distinct_store_ids, max_timestamp_utc):
    frames = []
    # i=100
    for store_id in distinct_store_ids:
        print(store_id['store_id'])
        # if(i>100):
        #     break 
        # i+=1
        try:
            data = processStore(store_id['store_id'], max_timestamp_utc)
            # data = processStore('2367299134091594697', max_timestamp_utc)
            frames.append(data); 
        except Exception as e:
            print(e)
        
        
    return pd.concat(frames, ignore_index=True)
    
    
def generate_report(report_id):
    try:
        report = Report.objects.get(report_id=report_id)
        max_timestamp_utc = loadCurrentDate()
        print("Maximum Time in Status Data", max_timestamp_utc)
        print(report)
        dataframe = startReportGeneration(getStoreIds(), max_timestamp_utc)
        print(dataframe)
        csv_data = dataframe.to_csv(index=False)
        csv_file = io.BytesIO(csv_data.encode())
        report.csv_file.save(f"reports/{report_id}.csv", csv_file, save=True)
        report.isProcessing = False
        report.isGenerated = True
        report.save()
    except Exception as e:
        print(e)
