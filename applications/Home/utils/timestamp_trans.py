import datetime


def timestamp_to_date(timestamp):

    dt_object = datetime.datetime.fromtimestamp(timestamp)

    formatted_date = dt_object.strftime('%Y-%m-%d')
    return formatted_date
