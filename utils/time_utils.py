import pytz
from datetime import datetime, timedelta
from config.config import RETROACHIEVEMENTS_INTERVAL, TROPHIES_INTERVAL, PRESENCE_INTERVAL

"""
A function to get the epoch time of yesterday and now in the Europe/Amsterdam timezone.

Returns:
Tuple of two integers representing the epoch time of yesterday and now.
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
A function to calculate the delay to start the task until the next interval.

Args:
- interval_type: Type of interval ('retro', 'trophies', or other).

Returns:
Integer representing the delay in seconds until the next interval.
"""

def delay_until_next_interval(interval_type):
    now = datetime.now()
    if interval_type == 'retro':
        interval = RETROACHIEVEMENTS_INTERVAL
    elif interval_type == 'trophies':
        interval = TROPHIES_INTERVAL
    else:
        interval = PRESENCE_INTERVAL
    minutes = (now.minute // interval + 1) * interval
    if minutes < 60:
        future = now.replace(minute=minutes, second=0, microsecond=0)
    else:
        future = now.replace(hour=(now.hour + 1) % 24, minute=0, second=0, microsecond=0)
        if future < now:
            future += timedelta(days=1)
    delta_s = (future - now).total_seconds()
    return round(delta_s)

"""
A function to calculate the delay until the next midnight.

Returns:
Integer representing the delay in seconds until the next midnight.
"""

def delay_until_next_midnight():
    now = datetime.now()
    next_midnight = datetime.combine(now + timedelta(days=1), datetime.min.time())
    seconds_until = (next_midnight - now).total_seconds()
    return round(seconds_until)

"""
A function to calculate the time difference between two dates.

Args:
- earliest_date_str: String representing the earliest date.
- latest_date_str: String representing the latest date.

Returns:
String representing the time difference in a human-readable format.
"""

def calculate_time_difference(earliest_date_str: str, latest_date_str: str) -> str:
    format_str = '%Y-%m-%d %H:%M:%S'
    earliest_date = datetime.strptime(earliest_date_str, format_str)
    latest_date = datetime.strptime(latest_date_str, format_str)
    
    total_seconds = int((latest_date - earliest_date).total_seconds())
    minutes, _ = divmod(total_seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    months, days = divmod(days, 30)
    years, months = divmod(months, 12)
    
    time_units = format_time_units(years, months, days, hours, minutes)
    
    if len(time_units) > 1:
        last = time_units.pop()
        return ', '.join(time_units) + ' and ' + last
    elif time_units:
        return time_units[0]
    else:
        return '0 minutes'

def format_time_units(years, months, days, hours, minutes):
    time_units = []
    if years > 0:
        time_units.append(f"{years} year{'s' if years > 1 else ''}")
    if months > 0:
        time_units.append(f"{months} month{'s' if months > 1 else ''}")
    if days > 0:
        time_units.append(f"{days} day{'s' if days > 1 else ''}")
    if hours > 0:
        time_units.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes > 0:
        time_units.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    
    return time_units
    
"""
A function to get the ordinal suffix of a number.

Args:
- n: Number for which the ordinal suffix is to be determined.

Returns:
String representing the number with its ordinal suffix.
"""
    
def ordinal(n):
    suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    return str(n) + suffix