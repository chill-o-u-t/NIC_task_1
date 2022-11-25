def time_now():
    import datetime
    return str(datetime.now().strftime("%Y%m%dT%H%M%S.%f")[:-3])
