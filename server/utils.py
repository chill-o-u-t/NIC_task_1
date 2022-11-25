import datetime


def time_now():
    return str(datetime.now().strftime("%Y%m%dT%H%M%S.%f")[:-3])

