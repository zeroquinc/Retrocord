import re

def format_title(title):
    title = title.lower()  # convert to lowercase
    title = re.sub(r"[^\w\s]", '', title)  # remove special characters except whitespace and underscores
    title = title.replace(' ', '-')  # replace spaces with hyphens
    return f"https://www.playstation.com/games/{title}/"  # prepend base URL

def calculate_total_time(td):
    minutes, _ = divmod(td.seconds + td.days * 86400, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    weeks, days = divmod(days, 7)
    years, weeks = divmod(weeks, 52)

    result = []
    if years:
        result.append(f"{years} year{'s' if years > 1 else ''}")
    if weeks:
        result.append(f"{weeks} week{'s' if weeks > 1 else ''}")
    if days:
        result.append(f"{days} day{'s' if days > 1 else ''}")
    if hours:
        result.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes:
        result.append(f"{minutes} minute{'s' if minutes > 1 else ''}")

    if len(result) > 1:
        last = result.pop()
        return ', '.join(result) + ' and ' + last
    elif result:
        return result[0]
    else:
        return ''