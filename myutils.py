import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta


def normalize(v):
    return (v - v.min()) / (v.max() - v.min())


def get_atttribute(response, attr):
    return response[[attr]].to_numpy()


def get_avg_price(response, is_normalize=True):
    row = get_atttribute(response, "low")
    high = get_atttribute(response, "high")
    if is_normalize:
        return normalize((high+row)/2)
    else:
        return (high+row)/2


def get_volume(response, is_normalize=True):
    if is_normalize:
        return normalize(get_atttribute(response, "volume"))
    else:
        return get_atttribute(response, "volume")


# def get_date(response):
#     return get_atttribute(response, "date")
def get_date(response):
    return get_atttribute(response, "time")


def get_turnover(response, is_normalize=True):
    avg = get_avg_price(response)
    vol = get_volume(response)
    if is_normalize:
        return normalize(np.multiply(avg,vol)), avg
    else:
        return np.multiply(avg,vol), avg


def correlation_test(avg):
    avg =normalize(avg)
    avg = avg.flatten()
    y = np.arange(len(avg))
    return np.absolute(np.cov(avg,y)[0][1])


def date_str_to_datetime(date_str, include="ymdhms"):
    if include == "ymd":
        return datetime.strptime(date_str, '%Y-%m-%d')
    else:
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S+0000')


def date_str_to_timestamp(date_str):
    date = date_str_to_datetime(date_str)
    return datetime.timestamp(date)


def date_str_to_timestamp_str(date_str):
    timestamp = date_str_to_timestamp(date_str)
    return timestamp_to_timestamp_str(timestamp)


def datetime_to_timestamp_str(date):
    timestamp_str = timestamp_to_timestamp_str(datetime.timestamp(date))
    return timestamp_str.split(".")[0]


def timestamp_to_datetime(timestamp):
    return datetime.fromtimestamp(timestamp)


def timestamp_to_timestamp_str(timestamp):
    return str(timestamp).split(".")[0]


def timestamp_to_date_str(timestamp):
    date = datetime.fromtimestamp(timestamp)
    return datetime_to_date_str(date)


def timestamp_str_to_date_str(timestamp):
    date = datetime.fromtimestamp(float(timestamp))
    return datetime_to_date_str(date)


def datetime_to_date_str(date, include="ymdhms"):
    if include == "ymd":
         return date.strftime('%Y-%m-%d')
    else:
        return date.strftime('%Y-%m-%dT%H:%M:%S+0000')


def add_days(sourcedate, days):
    day_rel = relativedelta(days=days)
    return sourcedate+day_rel


def add_hours(sourcedate, hours):
    hrs_rel = relativedelta(hours=hours)
    return sourcedate+hrs_rel


def add_seconds(sourcedate, seconds):
    day_rel = relativedelta(seconds=seconds)
    return sourcedate+day_rel
