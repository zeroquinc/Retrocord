from PIL import Image
import requests
from io import BytesIO
import numpy as np
import os
import json
from sklearn.cluster import KMeans

def cache_color(image_url, cache_file='image_cache.json', num_clusters=3):
    """
    Cache the most vibrant and colorful area of the image to avoid recalculating it.

    Args:
        image_url (str): The URL of the image to cache.
        cache_file (str): Path to the JSON file used to store the cached color.
        num_clusters (int): Number of color clusters to detect.

    Returns:
        int: The most vibrant and colorful color in hexadecimal format.
    """
    # Check if the cache file exists
    if os.path.exists(cache_file):
        with open(cache_file, 'r') as f:
            cached_data = json.load(f)
            if image_url in cached_data:
                # If the color is already cached, return it
                return cached_data[image_url]

    # If color not cached, fetch and calculate it
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    img = img.convert("RGB")  # Ensure the image is in RGB format

    # Resize the image for faster processing
    img = img.resize((img.width // 2, img.height // 2))

    # Convert the image to a NumPy array
    img_data = np.array(img)

    # Reshape the image data into a 2D array of pixels for clustering
    pixels = img_data.reshape((-1, 3))

    # Remove colors that are too close to black/gray/white
    mask = np.linalg.norm(pixels, axis=1) > 50  # A simple threshold to remove very dark colors
    filtered_pixels = pixels[mask]

    # Perform KMeans clustering to find color clusters
    kmeans = KMeans(n_clusters=num_clusters, random_state=0)
    kmeans.fit(filtered_pixels)

    # Get the centers of the clusters (the most common colors)
    cluster_centers = kmeans.cluster_centers_

    # Calculate the distance from each cluster center to the black/white axis (i.e., evaluate vibrancy)
    distances = np.linalg.norm(cluster_centers - np.array([0, 0, 0]), axis=1)

    # Get the most vibrant cluster (the one that is farthest from black)
    most_vibrant_cluster_idx = np.argmax(distances)
    vibrant_color = cluster_centers[most_vibrant_cluster_idx]

    # Convert the RGB color to hexadecimal format
    vibrant_color_hex = int('0x{:02x}{:02x}{:02x}'.format(*vibrant_color.astype(int)), 16)

    # Cache the color
    if not os.path.exists(cache_file):
        cached_data = {}

    cached_data[image_url] = vibrant_color_hex

    # Save the color to the cache file
    with open(cache_file, 'w') as f:
        json.dump(cached_data, f)

    return vibrant_color_hex

def get_discord_color(image_url, cache_file='image_cache.json', num_clusters=3):
    """
    Get the most vibrant and colorful color (Discord color) from the image for caching.

    Args:
        image_url (str): The URL of the image to analyze.
        cache_file (str): Path to the JSON file used to store cached color.
        num_clusters (int): Number of color clusters to detect.

    Returns:
        int: The most vibrant and colorful color in hexadecimal format.
    """
    return cache_color(image_url, cache_file, num_clusters)