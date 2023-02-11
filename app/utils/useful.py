import random
import time
import datetime


def random_string(length):
    tim = time.localtime()
    current_time = time.strftime("%d%m%Y%H%M%S", tim)
    random_str = ''.join(random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ') for i in range(length))
    return random_str + current_time


def acticode(length):
    # random_str = ''.join(random.choice('0123456789A') for i in range(length))
    # Only numbers
    random_str = ''.join(random.choice('0123456789') for i in range(length))
    return random_str


def dayday(day):
    t = datetime.datetime.now() + datetime.timedelta(days=day)
    d = f"{t.year}-{t.month}-{t.day} {t.hour}:{t.minute}:{t.second}"
    return d


def current_datetime():
    tim = time.localtime()
    current_time = time.strftime("%Y-%d-%m %H:%M:%S", tim)
    return current_time
