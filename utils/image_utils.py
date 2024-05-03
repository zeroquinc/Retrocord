import requests
from PIL import Image
from io import BytesIO
from colorthief import ColorThief
import numpy as np

def get_discord_color(image_url, border_percentage=0.2):
    """
    Get the most common color from an image for Discord usage.

    Args:
        image_url (str): The URL of the image to analyze.
        border_percentage (float): The percentage of border to exclude when cropping the image (default is 0.2).

    Returns:
        int: The most common color in hexadecimal format.

    Raises:
        (Exception): If there is an issue with fetching or processing the image.
    """
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content)).convert('RGB')

    # Crop the image to exclude borders
    width, height = img.size
    img = img.crop((width * border_percentage, height * border_percentage, width * (1 - border_percentage), height * (1 - border_percentage)))

    color_thief = ColorThief(BytesIO(response.content))
    palette = color_thief.get_palette(color_count=4, quality=4)

    img_arr = np.array(img)
    color_counts = {tuple(color): np.sum(np.all(img_arr == color, axis=-1)) for color in palette}

    # Find the most common color
    most_common_color = max(color_counts, key=color_counts.get)

    return int('0x{:02x}{:02x}{:02x}'.format(*most_common_color), 16)