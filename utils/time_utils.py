import pytz
from datetime import datetime, timedelta

"""
A function to get the epoch time of yesterday and now in the Europe/Amsterdam timezone.
"""

def get_now_and_yesterday_epoch():
    now_utc = datetime.now(pytz.utc)
    amsterdam_tz = pytz.timezone('Europe/Amsterdam')
    now_amsterdam = now_utc.astimezone(amsterdam_tz)
    yesterday_amsterdam = now_amsterdam - timedelta(days=1)
    yesterday_epoch = int(yesterday_amsterdam.timestamp())
    now_epoch = int(now_amsterdam.timestamp())

    return yesterday_epoch, now_epoch

"""
A function to calculate the delay until the next 15th minute.
"""

def delay_until_next_15th_minute():
    now = datetime.now()
    minutes = (now.minute // 15 + 1) * 15
    if minutes < 60:
        future = now.replace(minute=minutes, second=0, microsecond=0)
    else:
        future = now.replace(hour=(now.hour + 1) % 24, minute=0, second=0, microsecond=0)
        if future < now:
            future += timedelta(days=1)
    delta_s = (future - now).total_seconds()
    return round(delta_s)

"""
A function to calculate the delay until the next midnight
"""

def delay_until_next_midnight():
    now = datetime.now()
    next_midnight = datetime.combine(now + timedelta(days=1), datetime.min.time())
    seconds_until = (next_midnight - now).total_seconds()
    return round(seconds_until)