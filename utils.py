import datetime

IP = '127.0.0.1'
PORT = 8000

VARINT_32 = 32


def time_now():
    return str(datetime.datetime.now().isoformat())

