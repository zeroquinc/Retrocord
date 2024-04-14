import requests
from PIL import Image
from io import BytesIO
from colorthief import ColorThief
import math

def get_discord_color(image_url, border_percentage=0.1):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    # Crop the image to exclude borders
    width, height = img.size
    left = width * border_percentage
    top = height * border_percentage
    right = width * (1 - border_percentage)
    bottom = height * (1 - border_percentage)
    img = img.crop((left, top, right, bottom))

    # Convert image object to bytes and get color palette
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    color_thief = ColorThief(BytesIO(img_byte_arr))
    palette = color_thief.get_palette(color_count=6, quality=5)

    # find most distinct color
    most_distinct_color = None
    max_min_distance = -1
    for color in palette:
        min_distance = min([math.sqrt((color[0]-other_color[0])**2 + (color[1]-other_color[1])**2 + (color[2]-other_color[2])**2) for other_color in palette if color != other_color])
        if min_distance > max_min_distance:
            max_min_distance = min_distance
            most_distinct_color = color

    return most_distinct_color[0] * 256 * 256 + most_distinct_color[1] * 256 + most_distinct_color[2]