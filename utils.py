import pytz
from datetime import datetime, timedelta
import os
import requests
from PIL import Image
from io import BytesIO
from colorthief import ColorThief

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
A function to get the most common color in an image. 
Returns a value that can be used as a color in a Discord Embed.
"""

def get_most_common_color(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img.save("temp_image.png")  # save image temporarily
    color_thief = ColorThief("temp_image.png")
    dominant_color = color_thief.get_color(quality=1)
    os.remove("temp_image.png")  # delete the temporary image
    return dominant_color[0] * 256 * 256 + dominant_color[1] * 256 + dominant_color[2]

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