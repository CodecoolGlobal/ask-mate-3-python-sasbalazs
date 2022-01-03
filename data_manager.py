import connection
from datetime import datetime


def convert_to_date(timestamp):
    ts = int(timestamp)
    data = datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return data


def sorting_by_time(data):
    pass