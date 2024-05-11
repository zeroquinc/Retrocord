import discord
from datetime import datetime, timedelta, timezone
from psnawp_api import PSNAWP

from utils.image_utils import get_discord_color
from utils.trophy_utils import format_title
from utils.date_utils import format_date
from config.config import PSNTOKEN, DISCORD_IMAGE, TROPHIES_INTERVAL

from utils.custom_logger import logger

psnawp = PSNAWP(PSNTOKEN)

def get_client():
    logger.debug("Calling Sony API for profile information.")
    client = psnawp.me()
    profile_legacy = client.get_profile_legacy()
    profile_picture_url = profile_legacy['profile']['personalDetail']['profilePictureUrls'][0]['profilePictureUrl']
    client.profile_picture_url = profile_picture_url
    return client

def get_current_time():
    return datetime.now(timezone.utc)

def get_recent_titles(client, hours=24): # Use 24 hours because Sony's API is not updating the last_played_date_time very often
    logger.info("Calling Sony API to get recently played games")
    now = get_current_time()
    titles = list(client.title_stats())
    title_ids = [(title.title_id, 'PS5' if 'ps5' in title.category.value else 'PS4') for title in titles if title.last_played_date_time > now - timedelta(hours=hours)]
    logger.debug(f"API response: {titles}")
    for title in titles:
        if title.title_id in [id_ for id_, platform in title_ids]:
            logger.debug(f"Found a recently played game: {title.name}")
    return title_ids

def get_earned_trophies(client, title_ids):
    logger.debug("Calling Sony API to get earned trophies.")
    trophies = []
    for title_id, platform in title_ids:
        for trophy_title in client.trophy_titles_for_title(title_ids=[title_id]):
            try:
                earned_trophies = client.trophies(np_communication_id=trophy_title.np_communication_id, platform=platform, trophy_group_id='all', include_metadata=True)
                # Add each trophy and its title to the list
                trophies.extend((trophy, {'trophy_title': trophy_title, 'platform': platform}) for trophy in earned_trophies)
            except Exception as e:
                logger.error(f"Failed to get trophies for platform {platform}: {e}")
    return trophies

def create_trophy_embed(trophy, trophy_title_info, client, current, total_trophies):
    trophy_title = trophy_title_info['trophy_title']
    game_url = format_title(trophy_title.title_name)  # format the title name into a URL
    platform = trophy_title_info['platform']
    most_common_color = get_discord_color(trophy.trophy_icon_url)
    completion = current
    percentage = (completion / total_trophies) * 100
    embed = discord.Embed(description=f"**[{trophy_title.title_name}]({game_url}) ({platform})** \n\n {trophy.trophy_detail} \n\n Unlocked by {trophy.trophy_earn_rate}% of players", color=most_common_color)
    embed.add_field(name="Trophy", value=f"[{trophy.trophy_name}]({trophy.trophy_icon_url})", inline=True)
    embed.add_field(name="Rarity", value=f"{trophy.trophy_type.name.lower().capitalize()}")
    embed.add_field(name="Completion", value=f"{completion}/{total_trophies} ({percentage:.2f}%)", inline=True)
    embed.set_image(url=DISCORD_IMAGE)
    embed.set_thumbnail(url=trophy.trophy_icon_url)
    embed.set_footer(text=f"{client.online_id} • Earned on {format_date(trophy.earned_date_time)}", icon_url=client.profile_picture_url)
    embed.set_author(name="A Trophy Unlocked", icon_url=trophy_title.title_icon_url)
    return embed

async def process_trophies_embeds(client, title_ids, TROPHIES_INTERVAL):
    trophy_embeds = []
    for title_id, platform in title_ids:
        # Get all trophies for the current title_id
        all_trophies = get_earned_trophies(client, [(title_id, platform)])
        # Filter out trophies with None earned date
        earned_trophies = [t for t in all_trophies if t[0].earned_date_time is not None]
        # Get the game name from the first trophy_title object
        game_name = all_trophies[0][1]['trophy_title'].title_name if all_trophies else "Unknown"
        logger.debug(f"Found {len(earned_trophies)} earned trophies for game {game_name}")
        # Sort earned trophies by earned date
        earned_trophies.sort(key=lambda x: x[0].earned_date_time)
        # Calculate total trophies of the game (before filtering for earned_date_time)
        total_trophies = len(all_trophies)
        # Get current time and calculate cutoff time
        now = get_current_time()
        logger.debug(f"Current time: {now}")
        cutoff = now - timedelta(minutes=TROPHIES_INTERVAL)
        logger.debug(f"Cutoff time: {cutoff}")
        recent_trophies = [t for t in earned_trophies if t[0].earned_date_time >= cutoff]
        logger.debug(f"Recent trophies after filtering: {recent_trophies}")
        # Calculate total trophies earned (after filtering)
        total_trophies_earned = len(earned_trophies)
        # Calculate the starting count
        starting_count = total_trophies_earned - len(recent_trophies)
        for i, (trophy, trophy_title) in enumerate(recent_trophies):
            # Pass total_trophies to create_trophy_embed function
            embed = create_trophy_embed(trophy, trophy_title, client, starting_count + i + 1, total_trophies)
            trophy_embeds.append((trophy.earned_date_time, embed))
    return trophy_embeds, len(recent_trophies)

async def process_trophies(trophies_channel):
    client = get_client()
    if title_ids := get_recent_titles(client):
        trophy_embeds, _ = await process_trophies_embeds(client, title_ids, TROPHIES_INTERVAL)
        # Filter out trophy embeds with None earned date before sorting
        trophy_embeds = [te for te in trophy_embeds if te[0] is not None]
        trophy_embeds.sort(key=lambda x: x[0])  # Sort embeds by trophy earned date
        if trophy_embeds:
            logger.info(f"Sending {len(trophy_embeds)} trophy embeds to {trophies_channel}")
            for i in range(0, len(trophy_embeds), 10):
                await trophies_channel.send(embeds=[embed[1] for embed in trophy_embeds[i:i+10]])