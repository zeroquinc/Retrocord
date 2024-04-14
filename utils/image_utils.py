import requests
from PIL import Image
from io import BytesIO
from colorthief import ColorThief
import numpy as np

def get_discord_color(image_url, border_percentage=0.1):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content)).convert('RGB')

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
    palette = color_thief.get_palette(color_count=3, quality=1)

    # Convert image to numpy array and count pixel occurrence for each color
    img_arr = np.array(img)
    color_counts = {tuple(color): np.sum(np.all(img_arr == np.array(color), axis=(0, 1))) for color in palette}

    # find the color with the most pixels
    most_common_color = max(color_counts, key=color_counts.get)

    # Convert the color to hexadecimal format and then to an integer
    hex_color = '#{:02x}{:02x}{:02x}'.format(*most_common_color)
    int_color = int(hex_color[1:], 16)

    return int_color