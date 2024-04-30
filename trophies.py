from datetime import datetime, timedelta, timezone
from psnawp_api import PSNAWP

from config.config import PSNTOKEN

psnawp = PSNAWP(PSNTOKEN)

# This is you
client = psnawp.me()
print(client.online_id)
print(client.account_id)

# Retrieve an overall summary of your trophies
#print(client.trophy_summary())

# Get the current time
now = datetime.now(timezone.utc)

titles = list(client.title_stats())
title_ids = [title.title_id for title in titles if title.last_played_date_time > now - timedelta(days=4)]

for trophy_title in client.trophy_titles_for_title(title_ids=title_ids):
    # Print the icon URL of the trophy title
    print("Trophy Title Icon URL:", trophy_title.title_icon_url)

    # Get all trophies for the title
    all_trophies = client.trophies(np_communication_id=trophy_title.np_communication_id, platform='PS4_game', trophy_group_id='all', include_metadata=True)

    # Print the icon URLs of all earned trophies
    for trophy in all_trophies:
        if trophy.earned and trophy.earned_date_time > now - timedelta(days=4):
            print("Achievement Name:", trophy.trophy_detail)
            print("Trophy Type:", trophy.trophy_type.name.lower().capitalize())
            print("Trophy Icon URL:", trophy.trophy_icon_url)