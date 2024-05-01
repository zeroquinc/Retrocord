from datetime import datetime, timedelta, timezone
from psnawp_api import PSNAWP
from config.config import PSNTOKEN

psnawp = PSNAWP(PSNTOKEN)

def get_client():
    return psnawp.me()

def get_current_time():
    return datetime.now(timezone.utc)

def get_recent_titles(client, days=4):
    now = get_current_time()
    titles = list(client.title_stats())
    return [title.title_id for title in titles if title.last_played_date_time > now - timedelta(days=days)]

def get_earned_trophies(client, title_ids):
    trophies = []
    for trophy_title in client.trophy_titles_for_title(title_ids=title_ids):
        earned_trophies = client.trophies(np_communication_id=trophy_title.np_communication_id, platform='all', trophy_group_id='all', include_metadata=True)
        # Add each trophy and its title to the list
        trophies.extend((trophy, trophy_title) for trophy in earned_trophies)
    return trophies

def print_trophy_info(trophies, days=4):
    now = get_current_time()
    for trophy, trophy_title in trophies:  # Unpack each tuple into a trophy and a title
        if trophy.earned and trophy.earned_date_time > now - timedelta(days=days):
            print("Game Name:", trophy_title.title_name)
            print("Game Icon URL:", trophy_title.title_icon_url)
            print("Trophy Name:", trophy.trophy_name)
            print("Trophy Details:", trophy.trophy_detail)
            print("Trophy Rarity:", trophy.trophy_rarity)
            print("Trophy Type:", trophy.trophy_type.name.lower().capitalize())
            print("Trophy Icon URL:", trophy.trophy_icon_url)
            print("Trophy Earned Date:", trophy.earned_date_time, end="\n\n")

def start_trophy_info():
    client = get_client()
    title_ids = get_recent_titles(client)
    if title_ids:
        trophies = get_earned_trophies(client, title_ids)
        print_trophy_info(trophies)

start_trophy_info()