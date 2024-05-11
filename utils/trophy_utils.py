import re

def format_title(title):
    title = title.lower()  # convert to lowercase
    title = re.sub(r"[^\w\s]", '', title)  # remove special characters except whitespace and underscores
    title = title.replace(' ', '-')  # replace spaces with hyphens
    return f"https://www.playstation.com/games/{title}/"  # prepend base URL