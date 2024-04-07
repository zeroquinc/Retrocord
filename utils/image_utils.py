import os
import requests
from PIL import Image
from io import BytesIO
from colorthief import ColorThief

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