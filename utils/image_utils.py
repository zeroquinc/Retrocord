from PIL import Image
import requests
from io import BytesIO
import numpy as np
from sklearn.cluster import KMeans

def get_discord_color(image_url, num_colors=5, crop_percentage=0.5):
    """
    Get the most distinct color from the center of an image for Discord usage.

    Args:
        image_url (str): The URL of the image to analyze.
        num_colors (int): Number of dominant colors to extract (default is 5).
        crop_percentage (float): Percentage of the image to keep in the center (default is 0.5).

    Returns:
        int: The most distinct color in hexadecimal format.

    Raises:
        (Exception): If there is an issue with fetching or processing the image.
    """
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    
    # Calculate the crop dimensions
    width, height = img.size
    crop_width = int(width * crop_percentage)
    crop_height = int(height * crop_percentage)
    left = (width - crop_width) // 2
    top = (height - crop_height) // 2
    right = left + crop_width
    bottom = top + crop_height
    
    img = img.crop((left, top, right, bottom))

    img = img.resize((img.width // 2, img.height // 2))  # Resize for faster processing

    img_array = np.array(img)
    img_flattened = img_array.reshape(-1, 3)

    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(img_flattened)

    dominant_color = kmeans.cluster_centers_[np.argmax(np.bincount(kmeans.labels_))]

    return int('0x{:02x}{:02x}{:02x}'.format(*dominant_color.astype(int)), 16)