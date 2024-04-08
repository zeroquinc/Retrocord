import requests
from PIL import Image
from io import BytesIO
from colorthief import ColorThief
from collections import Counter
"""
A function to get the most common color in an image. 
Returns a value that can be used as a color in a Discord Embed.
"""

def get_most_common_color(image_url, border_percentage=0.1):
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

    # count pixels of each color
    pixels = list(img.getdata())
    color_counts = Counter(pixels)

    # find most common and colorful color
    most_colorful_color = None
    max_saturation = -1
    max_count = -1
    for color in palette:
        saturation = max(color) - min(color)  # calculate saturation
        count = color_counts[color]
        if saturation > 30 and count > max_count:  # lower saturation threshold to include more colors
            max_saturation = saturation
            max_count = count
            most_colorful_color = color

    return most_colorful_color[0] * 256 * 256 + most_colorful_color[1] * 256 + most_colorful_color[2]