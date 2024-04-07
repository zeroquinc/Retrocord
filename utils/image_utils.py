import os
import requests
from PIL import Image
from io import BytesIO
from colorthief import ColorThief
from collections import Counter

"""
A function to get the most common color in an image. 
Returns a value that can be used as a color in a Discord Embed.
"""

def get_most_common_color(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img.save("temp_image.png")  # save image temporarily
    color_thief = ColorThief("temp_image.png")

    # get color palette
    palette = color_thief.get_palette(color_count=6)

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
        if saturation > 50 and count > max_count:  # exclude colors close to black, white, or grey
            max_saturation = saturation
            max_count = count
            most_colorful_color = color

    os.remove("temp_image.png")  # delete the temporary image
    return most_colorful_color[0] * 256 * 256 + most_colorful_color[1] * 256 + most_colorful_color[2]